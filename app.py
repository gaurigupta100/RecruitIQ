import os
import uuid
from datetime import datetime
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash

from flask import (
    Flask,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    session,
    url_for,
)
from werkzeug.exceptions import RequestEntityTooLarge
from werkzeug.utils import secure_filename

import config
from utils.ats_scorer import calculate_ats_score
from utils.database import (
    delete_history_record,
    get_all_history,
    get_dashboard_stats,
    get_history_by_id,
    init_db,
    save_screening_result,
    create_user,
    get_user_by_username,
    get_user_by_id,
)
from utils.ml_predictor import get_predictor
from utils.pdf_report import generate_pdf_report
from utils.resume_parser import extract_resume_text
from utils.skills import extract_skills, get_job_recommendations, get_missing_skills, get_potential_career_paths
from utils.text_cleaner import clean_text, get_resume_stats



def create_app():
    app = Flask(__name__)
    app.config.from_object(config)

    os.makedirs(config.UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(os.path.dirname(config.DATABASE_PATH), exist_ok=True)
    init_db()

    def allowed_file(filename):
        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower() in config.ALLOWED_EXTENSIONS
        )

    def login_required(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "user_id" not in session:
                flash("Please log in to access this page.", "warning")
                return redirect(url_for("login"))
            return f(*args, **kwargs)
        return decorated_function

    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if "user_id" in session:
            return redirect(url_for("dashboard"))
            
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            email = request.form.get("email", "").strip()
            password = request.form.get("password", "")
            role = request.form.get("role", "candidate").strip()
            
            if not all([username, email, password, role]):
                flash("Please fill in all fields.", "danger")
                return render_template("register.html")
                
            if role not in ["candidate", "recruiter"]:
                flash("Invalid role choice.", "danger")
                return render_template("register.html")
                
            existing_user = get_user_by_username(username)
            if existing_user:
                flash("Username already exists. Please choose another one.", "danger")
                return render_template("register.html")
                
            hashed_pw = generate_password_hash(password)
            user_id = create_user(username, email, hashed_pw, role)
            if user_id:
                flash("Registration successful! Please log in.", "success")
                return redirect(url_for("login"))
            else:
                flash("Registration failed. Please try again.", "danger")
                
        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if "user_id" in session:
            return redirect(url_for("dashboard"))
            
        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "")
            
            if not username or not password:
                flash("Please enter both username and password.", "danger")
                return render_template("login.html")
                
            user = get_user_by_username(username)
            if user and check_password_hash(user["password_hash"], password):
                session["user_id"] = user["id"]
                session["username"] = user["username"]
                session["role"] = user["role"]
                flash(f"Welcome back, {user['username']}!", "success")
                return redirect(url_for("dashboard"))
            else:
                flash("Invalid username or password.", "danger")
                
        return render_template("login.html")

    @app.route("/logout")
    def logout():
        session.clear()
        flash("You have been logged out successfully.", "success")
        return redirect(url_for("login"))

    @app.route("/upload", methods=["GET", "POST"])
    @login_required
    def upload():
        if request.method == "GET":
            return render_template("upload.html")

        if "resume" not in request.files:
            flash("No file selected. Please choose a PDF or DOCX resume.", "danger")
            return redirect(url_for("upload"))

        file = request.files["resume"]
        if not file or file.filename == "":
            flash("No file selected. Please choose a PDF or DOCX resume.", "danger")
            return redirect(url_for("upload"))

        if not allowed_file(file.filename):
            flash("Invalid file type. Only PDF and DOCX files are allowed.", "danger")
            return redirect(url_for("upload"))

        original_filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{original_filename}"
        file_path = os.path.join(config.UPLOAD_FOLDER, unique_filename)

        try:
            file.save(file_path)
            raw_text = extract_resume_text(file_path)

            if not raw_text or len(raw_text.strip()) < 50:
                if os.path.exists(file_path):
                    os.remove(file_path)
                flash("Could not extract enough text from the resume. Please upload a readable file.", "danger")
                return redirect(url_for("upload"))

            cleaned_text = clean_text(raw_text)
            if not cleaned_text:
                if os.path.exists(file_path):
                    os.remove(file_path)
                flash("Resume text could not be processed after cleaning. Please try another file.", "danger")
                return redirect(url_for("upload"))

            predictor = get_predictor()
            prediction, confidence = predictor.predict(cleaned_text)

            detected_skills = extract_skills(raw_text)
            missing_skills = get_missing_skills(prediction, detected_skills)
            job_recommendations = get_job_recommendations(detected_skills)
            potential_career_paths = get_potential_career_paths(detected_skills)
            stats = get_resume_stats(raw_text)
            ats_score, ats_rating, improvement_tips = calculate_ats_score(raw_text, detected_skills)
            upload_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            result_data = {
                "filename": original_filename,
                "stored_filename": unique_filename,
                "prediction": prediction,
                "confidence": confidence,
                "detected_skills": detected_skills,
                "missing_skills": missing_skills,
                "job_recommendations": job_recommendations,
                "potential_career_paths": potential_career_paths,
                "word_count": stats["word_count"],
                "char_count": stats["char_count"],
                "resume_length": stats["resume_length"],
                "ats_score": ats_score,
                "ats_rating": ats_rating,
                "improvement_tips": improvement_tips,
                "upload_time": upload_time,
            }

            record_id = save_screening_result({
                "filename": original_filename,
                "prediction": prediction,
                "confidence": confidence,
                "ats_score": ats_score,
                "skills": ", ".join(detected_skills),
                "missing_skills": ", ".join(missing_skills),
                "word_count": stats["word_count"],
                "char_count": stats["char_count"],
                "resume_length": stats["resume_length"],
                "ats_rating": ats_rating,
                "improvement_tips": "||".join(improvement_tips),
            }, user_id=session["user_id"])

            session["last_result"] = {**result_data, "record_id": record_id}
            return redirect(url_for("result", record_id=record_id))

        except ValueError as exc:
            if os.path.exists(file_path):
                os.remove(file_path)
            flash(str(exc), "danger")
            return redirect(url_for("upload"))
        except Exception:
            if os.path.exists(file_path):
                os.remove(file_path)
            flash("An error occurred while processing the resume. Please try again.", "danger")
            return redirect(url_for("upload"))

    @app.route("/result")
    @app.route("/result/<int:record_id>")
    @login_required
    def result(record_id=None):
        if record_id:
            record = get_history_by_id(record_id)
            if not record:
                flash("Result not found.", "warning")
                return redirect(url_for("history"))

            if session["role"] == "candidate" and record["user_id"] != session["user_id"]:
                flash("Access denied.", "danger")
                return redirect(url_for("history"))

            detected_skills = [s.strip() for s in record["skills"].split(",") if s.strip()]
            missing_skills = [s.strip() for s in record["missing_skills"].split(",") if s.strip()]
            ats_score = record["ats_score"]
            ats_rating = record["ats_rating"] or "Average"
            stored_tips = record["improvement_tips"] or ""
            improvement_tips = [tip for tip in stored_tips.split("||") if tip.strip()]

            result_data = {
                "record_id": record["id"],
                "filename": record["filename"],
                "prediction": record["prediction"],
                "confidence": record["confidence"],
                "detected_skills": detected_skills,
                "missing_skills": missing_skills,
                "job_recommendations": get_job_recommendations(detected_skills),
                "potential_career_paths": get_potential_career_paths(detected_skills),
                "word_count": record["word_count"],
                "char_count": record["char_count"],
                "resume_length": record["resume_length"],
                "ats_score": ats_score,
                "ats_rating": ats_rating,
                "improvement_tips": improvement_tips,
                "upload_time": record["created_at"],
            }
        else:
            result_data = session.get("last_result")
            if not result_data:
                flash("No screening result available. Please upload a resume first.", "warning")
                return redirect(url_for("upload"))

            if result_data.get("record_id"):
                rec = get_history_by_id(result_data["record_id"])
                if rec and session["role"] == "candidate" and rec["user_id"] != session["user_id"]:
                    flash("Access denied.", "danger")
                    return redirect(url_for("history"))

        return render_template("result.html", result=result_data)

    @app.route("/download-report/<int:record_id>")
    @login_required
    def download_report(record_id):
        record = get_history_by_id(record_id)
        if not record:
            flash("Report not found.", "warning")
            return redirect(url_for("history"))

        if session["role"] == "candidate" and record["user_id"] != session["user_id"]:
            flash("Access denied.", "danger")
            return redirect(url_for("history"))

        detected_skills = [s.strip() for s in record["skills"].split(",") if s.strip()]
        missing_skills = [s.strip() for s in record["missing_skills"].split(",") if s.strip()]
        ats_score = record["ats_score"]
        ats_rating = record["ats_rating"] or "Average"
        stored_tips = record["improvement_tips"] or ""
        improvement_tips = [tip for tip in stored_tips.split("||") if tip.strip()]

        pdf_buffer = generate_pdf_report({
            "filename": record["filename"],
            "prediction": record["prediction"],
            "confidence": record["confidence"],
            "ats_score": ats_score,
            "ats_rating": ats_rating,
            "detected_skills": detected_skills,
            "missing_skills": missing_skills,
            "job_recommendations": get_job_recommendations(detected_skills),
            "potential_career_paths": get_potential_career_paths(detected_skills),
            "word_count": record["word_count"],
            "char_count": record["char_count"],
            "resume_length": record["resume_length"],
            "upload_time": record["created_at"],
            "improvement_tips": improvement_tips,
        })

        report_name = f"resume_report_{record_id}.pdf"
        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name=report_name,
            mimetype="application/pdf",
        )

    @app.route("/dashboard")
    @login_required
    def dashboard():
        stats = get_dashboard_stats(user_id=session["user_id"], role=session["role"])
        return render_template("dashboard.html", stats=stats)

    @app.route("/history")
    @login_required
    def history():
        records = get_all_history(user_id=session["user_id"], role=session["role"])
        return render_template("history.html", records=records)

    @app.route("/history/delete/<int:record_id>", methods=["POST"])
    @login_required
    def delete_history(record_id):
        record = get_history_by_id(record_id)
        if not record:
            flash("Record not found.", "warning")
            return redirect(url_for("history"))

        if session["role"] == "candidate" and record["user_id"] != session["user_id"]:
            flash("Access denied.", "danger")
            return redirect(url_for("history"))

        deleted = delete_history_record(record_id)
        if deleted:
            flash("History record deleted successfully.", "success")
        else:
            flash("Record not found.", "warning")
        return redirect(url_for("history"))

    @app.route("/about")
    def about():
        return render_template("about.html")

    @app.route("/contact", methods=["GET", "POST"])
    def contact():
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            email = request.form.get("email", "").strip()
            subject = request.form.get("subject", "").strip()
            message = request.form.get("message", "").strip()

            if not all([name, email, subject, message]):
                flash("Please fill in all contact form fields.", "danger")
            else:
                flash("Thank you for reaching out! We will get back to you shortly.", "success")
                return redirect(url_for("contact"))

        return render_template("contact.html")

    @app.errorhandler(404)
    def not_found(error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        return render_template("500.html"), 500

    @app.errorhandler(RequestEntityTooLarge)
    def file_too_large(error):
        flash("File is too large. Maximum allowed size is 5 MB.", "danger")
        return redirect(url_for("upload"))

    return app

app = create_app()


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
