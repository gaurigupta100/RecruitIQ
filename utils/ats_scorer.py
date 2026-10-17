import re

EDUCATION_KEYWORDS = [
    "bachelor", "master", "phd", "doctorate", "degree", "university", "college",
    "education", "diploma", "btech", "mtech", "bsc", "msc", "mba", "bca", "mca",
    "graduation", "postgraduate", "undergraduate", "school", "institute", "academy",
    "certification course", "honors", "honours",
]

EXPERIENCE_KEYWORDS = [
    "experience", "worked", "employment", "employer", "intern", "internship",
    "senior", "junior", "lead", "manager", "director", "consultant", "analyst",
    "engineer", "developer", "associate", "specialist", "coordinator", "supervisor",
    "years", "months", "responsibilities", "achievements", "professional",
]

PROJECT_KEYWORDS = [
    "project", "projects", "developed", "built", "implemented", "created",
    "designed", "deployed", "launched", "portfolio", "github", "repository",
    "prototype", "application", "solution", "case study",
]

CERTIFICATION_KEYWORDS = [
    "certified", "certification", "certificate", "credential", "licensed",
    "aws certified", "azure certified", "google certified", "pmp", "scrum master",
    "cissp", "comptia", "oracle certified", "cisco certified", "professional certificate",
]


def _count_keyword_matches(text, keywords):
    text_lower = text.lower()
    return sum(1 for keyword in keywords if keyword in text_lower)
def calculate_ats_score(raw_text, detected_skills):
    """Generate an ATS compatibility score out of 100."""
    if not raw_text:
        return 0, "Needs Improvement", []

    from utils.skills import get_job_recommendations
    recs = get_job_recommendations(detected_skills)
    highest_match = recs[0]["match_percentage"] if recs else 0.0

    word_count = len(raw_text.split())

    # 1. Length & Formatting Score (Max 15)
    length_score = 0
    if 300 <= word_count <= 800:
        length_score = 15
    elif 200 <= word_count < 300 or 800 < word_count <= 1000:
        length_score = 10
    elif 100 <= word_count < 200 or 1000 < word_count <= 1200:
        length_score = 5
    else:
        length_score = 2

    # 2. Role Alignment Score (Max 30)
    role_match_score = round(highest_match * 0.3, 1)

    # 3. Section Completeness Scores (Max 55)
    education_matches = _count_keyword_matches(raw_text, EDUCATION_KEYWORDS)
    education_score = min(education_matches * 3, 15)

    project_matches = _count_keyword_matches(raw_text, PROJECT_KEYWORDS)
    project_score = min(project_matches * 3, 15)

    experience_matches = _count_keyword_matches(raw_text, EXPERIENCE_KEYWORDS)
    experience_score = min(experience_matches * 2, 15)

    certification_matches = _count_keyword_matches(raw_text, CERTIFICATION_KEYWORDS)
    certification_score = min(certification_matches * 3, 10)

    total_score = round(
        length_score + role_match_score + education_score + project_score +
        experience_score + certification_score,
        1,
    )
    total_score = min(total_score, 100)

    if total_score >= 80:
        rating = "Excellent"
    elif total_score >= 65:
        rating = "Good"
    elif total_score >= 45:
        rating = "Average"
    else:
        rating = "Needs Improvement"

    tips = _generate_improvement_tips(
        word_count=word_count,
        highest_match=highest_match,
        education_matches=education_matches,
        project_matches=project_matches,
        experience_matches=experience_matches,
        certification_matches=certification_matches,
        total_score=total_score,
    )

    return total_score, rating, tips


def _generate_improvement_tips(
    word_count,
    highest_match,
    education_matches,
    project_matches,
    experience_matches,
    certification_matches,
    total_score,
):
    tips = []

    if word_count < 250:
        tips.append("Expand your resume to at least 300 words with relevant achievements and responsibilities.")
    elif word_count > 900:
        tips.append("Trim lengthy sections and keep the resume concise for better ATS readability.")

    if highest_match < 40:
        tips.append("Your skills do not closely match any core job roles (below 40%). Target specific roles by listing their mandatory technologies.")
    elif highest_match < 65:
        tips.append("Improve your role alignment score by adding more skills relevant to your target role.")

    if education_matches == 0:
        tips.append("Include a dedicated education section with degree, institution, and graduation details.")

    if project_matches < 2:
        tips.append("Highlight 2-3 projects with technologies used, outcomes, and measurable impact.")

    if experience_matches < 3:
        tips.append("Add clear work experience entries with job titles, duration, and key accomplishments.")

    if certification_matches == 0:
        tips.append("List relevant certifications to improve credibility and ATS keyword coverage.")

    if not tips and total_score < 90:
        tips.append("Use strong action verbs and quantify achievements to push your ATS score even higher.")

    if not tips:
        tips.append("Your resume is well optimized. Keep updating it with recent skills and accomplishments.")

    return tips[:5]
