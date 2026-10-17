import re

TECHNICAL_SKILLS = [
    "Python", "Java", "C++", "C#", "C", "JavaScript", "TypeScript", "Go", "Golang",
    "Rust", "Kotlin", "Swift", "Ruby", "PHP", "Scala", "R", "MATLAB", "Perl", "Dart",
    "React", "React Native", "Angular", "Vue.js", "Vue", "Next.js", "Nuxt.js", "Svelte",
    "Node.js", "Node", "Express.js", "Express", "Django", "Flask", "FastAPI", "Spring Boot",
    "Spring", "ASP.NET", ".NET", "Laravel", "Ruby on Rails", "Rails", "Bootstrap", "Tailwind CSS",
    "HTML", "HTML5", "CSS", "CSS3", "SASS", "SCSS", "jQuery", "Redux", "GraphQL", "REST API",
    "REST", "WebSocket", "Microservices", "MongoDB", "MySQL", "PostgreSQL", "SQL", "SQLite",
    "Oracle", "SQL Server", "Redis", "Cassandra", "DynamoDB", "Firebase", "Elasticsearch",
    "Neo4j", "MariaDB", "NoSQL", "TensorFlow", "PyTorch", "Keras", "Scikit-learn", "Scikit Learn",
    "Machine Learning", "Deep Learning", "Natural Language Processing", "NLP", "Computer Vision",
    "OpenCV", "Pandas", "NumPy", "SciPy", "Matplotlib", "Seaborn", "Plotly", "XGBoost",
    "LightGBM", "Random Forest", "Neural Networks", "CNN", "RNN", "LSTM", "Transformers",
    "BERT", "GPT", "LLM", "Large Language Models", "Generative AI", "MLOps", "Data Analysis",
    "Data Visualization", "Statistical Analysis", "A/B Testing", "Feature Engineering",
    "Model Deployment", "Docker", "Kubernetes", "AWS", "Azure", "Google Cloud", "GCP",
    "Heroku", "DigitalOcean", "Linux", "Unix", "Windows Server", "Git", "GitHub", "GitLab",
    "Bitbucket", "CI/CD", "Jenkins", "GitHub Actions", "Terraform", "Ansible", "Puppet",
    "Chef", "Nginx", "Apache", "Load Balancing", "Networking", "TCP/IP", "DNS", "VPN",
    "Firewall", "Cybersecurity", "Penetration Testing", "Ethical Hacking", "OWASP",
    "SIEM", "Splunk", "Wireshark", "Network Security", "Information Security", "SOC",
    "Incident Response", "Risk Assessment", "Compliance", "GDPR", "HIPAA", "ISO 27001",
    "Hadoop", "Spark", "Apache Spark", "Kafka", "Apache Kafka", "Airflow", "Apache Airflow",
    "ETL", "Data Pipeline", "Data Warehouse", "Data Lake", "Snowflake", "BigQuery", "Redshift",
    "Databricks", "Hive", "Pig", "HBase", "Tableau", "Power BI", "Looker", "QlikView",
    "Excel", "Google Sheets", "VBA", "SAP", "SAP HANA", "SAP Fiori", "ABAP", "Salesforce",
    "CRM", "ERP", "Oracle ERP", "ServiceNow", "Jira", "Confluence", "Agile", "Scrum",
    "Kanban", "Project Management", "Stakeholder Management", "Business Analysis",
    "Requirements Gathering", "Process Improvement", "Six Sigma", "Lean", "UML",
    "System Design", "Object Oriented Programming", "OOP", "Design Patterns", "SOLID",
    "Data Structures", "Algorithms", "API Development", "API Integration", "Selenium",
    "Cypress", "Playwright", "JUnit", "TestNG", "PyTest", "Unit Testing", "Integration Testing",
    "Automation Testing", "Manual Testing", "QA", "Quality Assurance", "Performance Testing",
    "Load Testing", "JMeter", "Postman", "Swagger", "OpenAPI", "Blockchain", "Ethereum",
    "Solidity", "Smart Contracts", "Web3", "Cryptocurrency", "Hyperledger", "DevOps",
    "Site Reliability Engineering", "SRE", "Monitoring", "Prometheus", "Grafana", "ELK Stack",
    "Logstash", "Kibana", "CloudFormation", "ARM Templates", "Serverless", "Lambda",
    "Azure Functions", "Cloud Functions", "Figma", "Adobe XD", "UI/UX", "UX Design",
    "UI Design", "Responsive Design", "Wireframing", "Prototyping", "Photoshop",
    "Illustrator", "AutoCAD", "SolidWorks", "CATIA", "ANSYS", "MATLAB Simulink",
    "PLC", "SCADA", "IoT", "Embedded Systems", "Arduino", "Raspberry Pi", "RTOS",
    "ARM", "FPGA", "VHDL", "Verilog", "PCB Design", "Circuit Design", "Power Systems",
    "Control Systems", "Structural Analysis", "Revit", "STAAD Pro", "ETABS", "Primavera",
    "MS Project", "Construction Management", "Surveying", "Geotechnical", "Hydraulics",
    "Thermodynamics", "Fluid Mechanics", "Mechanical Design", "Manufacturing", "Lean Manufacturing",
    "Quality Control", "Supply Chain", "Inventory Management", "Procurement", "Logistics",
    "Operations Management", "Business Intelligence", "Financial Analysis", "Budgeting",
    "Forecasting", "Market Research", "Digital Marketing", "SEO", "SEM", "Google Analytics",
    "Content Marketing", "Social Media Marketing", "Email Marketing", "Copywriting",
    "Public Speaking", "Negotiation", "Leadership", "Team Management", "HR Management",
    "Talent Acquisition", "Recruitment", "Onboarding", "Employee Relations", "Payroll",
    "Compensation", "Benefits Administration", "Performance Management", "Training and Development",
    "Labor Law", "Workday", "BambooHR", "Legal Research", "Contract Law", "Litigation",
    "Corporate Law", "Intellectual Property", "Compliance Management", "Due Diligence",
    "Case Management", "Court Proceedings", "Legal Writing", "Mediation", "Arbitration",
    "Nutrition", "Fitness Training", "Personal Training", "Yoga", "Physiotherapy",
    "Sports Science", "Wellness Coaching", "Health Coaching", "Anatomy", "Kinesiology",
    "Rehabilitation", "Pilates", "CrossFit", "Strength Training", "Cardio Training",
    "Weight Management", "Mental Health", "Mindfulness", "Meditation", "Holistic Health",
    "Public Health", "Epidemiology", "Clinical Research", "Biostatistics", "Healthcare Management",
    "Medical Coding", "ICD-10", "HIPAA Compliance", "Patient Care", "First Aid", "CPR",
    "BLS", "ACLS", "Pharmacy", "Pharmacology", "Nursing", "Radiology", "Laboratory Techniques",
    "Microbiology", "Biochemistry", "Genetics", "Molecular Biology", "Cell Culture",
    "PCR", "Western Blot", "ELISA", "Flow Cytometry", "Mass Spectrometry", "Chromatography",
    "Spectroscopy", "Titration", "Organic Chemistry", "Inorganic Chemistry", "Analytical Chemistry",
    "Physical Chemistry", "Polymer Chemistry", "Electrochemistry", "Catalysis", "Nanotechnology",
    "Materials Science", "Metallurgy", "Welding", "CNC", "CAM", "CAD", "3D Printing",
    "Additive Manufacturing", "Robotics", "Automation", "PLC Programming", "HMI",
    "Industrial IoT", "Predictive Maintenance", "Digital Twin", "Augmented Reality", "AR",
    "Virtual Reality", "VR", "Mixed Reality", "MR", "Unity", "Unreal Engine", "Game Development",
    "Blender", "Maya", "3D Modeling", "Animation", "Video Editing", "Premiere Pro",
    "After Effects", "DaVinci Resolve", "Final Cut Pro", "Sound Design", "Music Production",
    "Graphic Design", "Typography", "Branding", "Print Design", "Packaging Design",
    "Interior Design", "Fashion Design", "Textile Design", "Fine Arts", "Drawing",
    "Painting", "Sculpture", "Ceramics", "Printmaking", "Photography", "Videography",
    "Storytelling", "Creative Writing", "Screenwriting", "Journalism", "Editing",
    "Proofreading", "Translation", "Interpretation",
    "Wireshark", "Nmap", "Burp Suite", "Metasploit", "Kali Linux", "Snort",
    "OpenShift", "Rancher", "Istio", "Envoy", "Consul", "Vault", "Packer",
    "Vagrant", "CircleCI", "Travis CI", "GitLab CI", "Azure DevOps", "Bamboo",
    "SonarQube", "Code Review", "Pair Programming", "TDD", "BDD", "DDD",
    "Event Driven Architecture", "Message Queues", "RabbitMQ", "ActiveMQ",
    "ZeroMQ", "gRPC", "Protocol Buffers", "Thrift", "SOAP", "XML", "JSON",
    "YAML", "TOML", "Markdown", "LaTeX", "Technical Writing", "Documentation",
    "Swagger UI", "MkDocs", "Sphinx", "Webpack", "Vite", "Rollup", "esbuild",
    "Babel", "ESLint", "Prettier", "npm", "yarn", "pnpm", "Shell Scripting",
    "PowerShell", "Robot Framework", "Appium", "Espresso", "BrowserStack",
    "Sauce Labs", "TestRail", "Bugzilla", "Trello", "Asana", "Notion", "Slack",
    "Microsoft Teams", "Zoom", "Google Meet", "Webex", "Discord", "Celery",
    "Hibernate", "Maven", "Gradle", "LINQ", "Entity Framework", "Visual Studio",
    "WordPress", "Accessibility", "Informatica", "SSIS", "Talend", "MapReduce",
    "HDFS", "YARN", "Sqoop", "Flume", "Oozie", "Zookeeper", "Scala", "ABAP",
    "SAP UI5", "OData", "SAP BTP", "Truffle", "Hardhat", "Ganache", "IPFS",
    "DeFi", "NFT", "Rest Assured", "Cucumber", "Page Object Model", "Jupyter",
    "Statistics", "Simulink", "Concrete Technology", "Steel Design", "BIM",
    "Quantity Surveying", "Site Supervision", "Building Codes", "Heat Transfer",
    "Machine Design", "Renewable Energy", "Electrical Safety", "Instrumentation",
    "Signal Processing", "Microcontrollers", "Client Counseling", "Regulatory Compliance",
    "Legal Drafting", "Evidence Law", "Criminal Law", "Civil Law", "Constitutional Law",
    "Digital Art", "Color Theory", "Composition", "Group Fitness", "Diversity and Inclusion",
    "HR Analytics", "ATS", "Interviewing", "Conflict Resolution", "Organizational Development",
    "B2B Sales", "B2C Sales", "Pipeline Management", "Closing Techniques", "Territory Management",
    "Resource Planning", "Governance", "Change Management", "PMP", "KPI Management",
    "Vendor Management", "Highway Engineering", "Environmental Engineering",
]

CATEGORY_SKILLS = {
    "Data Science": [
        "Python", "R", "SQL", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch",
        "Pandas", "NumPy", "Scikit-learn", "Statistics", "Data Analysis", "Data Visualization",
        "Tableau", "Power BI", "NLP", "Computer Vision", "Feature Engineering", "MLOps",
        "Jupyter", "Matplotlib", "Seaborn", "XGBoost", "A/B Testing", "BigQuery", "Spark",
        "Hadoop", "AWS", "Azure", "Docker", "Kubernetes", "Git", "Excel",
    ],
    "Python Developer": [
        "Python", "Django", "Flask", "FastAPI", "REST API", "SQL", "PostgreSQL", "MongoDB",
        "Git", "Docker", "AWS", "Azure", "Linux", "Redis", "Celery", "PyTest", "Unit Testing",
        "API Development", "Microservices", "CI/CD", "Kubernetes", "Pandas", "NumPy",
    ],
    "Java Developer": [
        "Java", "Spring Boot", "Spring", "Hibernate", "Maven", "Gradle", "SQL", "MySQL",
        "PostgreSQL", "Oracle", "REST API", "Microservices", "Git", "Docker", "Kubernetes",
        "JUnit", "Agile", "Scrum", "AWS", "Azure", "Linux", "Redis", "Kafka", "JUnit",
    ],
    "DotNet Developer": [
        "C#", ".NET", "ASP.NET", "Entity Framework", "SQL Server", "REST API", "Azure",
        "Git", "Visual Studio", "LINQ", "MVC", "Web API", "Microservices", "Docker",
        "Unit Testing", "Agile", "Scrum", "JavaScript", "HTML", "CSS", "Bootstrap",
    ],
    "Web Designing": [
        "HTML5", "CSS3", "JavaScript", "React", "Bootstrap", "Tailwind CSS", "Responsive Design",
        "UI/UX", "Figma", "Adobe XD", "Photoshop", "Illustrator", "jQuery", "SASS", "SCSS",
        "Vue.js", "Angular", "WordPress", "SEO", "Accessibility", "Wireframing", "Prototyping",
    ],
    "DevOps Engineer": [
        "Docker", "Kubernetes", "AWS", "Azure", "GCP", "CI/CD", "Jenkins", "GitHub Actions",
        "Terraform", "Ansible", "Linux", "Bash", "Python", "Monitoring", "Prometheus",
        "Grafana", "Nginx", "Load Balancing", "Networking", "Git", "Infrastructure as Code",
        "CloudFormation", "Helm", "ArgoCD",
    ],
    "Database": [
        "SQL", "MySQL", "PostgreSQL", "Oracle", "SQL Server", "MongoDB", "Redis",
        "Database Design", "Normalization", "Indexing", "Query Optimization", "ETL",
        "Data Modeling", "PL/SQL", "T-SQL", "Backup and Recovery", "Replication",
        "High Availability", "Performance Tuning", "NoSQL", "Cassandra", "DynamoDB",
    ],
    "Testing": [
        "Manual Testing", "Automation Testing", "Selenium", "Cypress", "Playwright",
        "JUnit", "TestNG", "PyTest", "Postman", "API Testing", "Performance Testing",
        "JMeter", "Load Testing", "QA", "Bug Tracking", "Jira", "Test Cases", "Agile",
        "Scrum", "Regression Testing", "Integration Testing", "Unit Testing",
    ],
    "Automation Testing": [
        "Selenium", "Cypress", "Playwright", "TestNG", "JUnit", "PyTest", "Cucumber",
        "BDD", "API Testing", "Postman", "Rest Assured", "CI/CD", "Jenkins", "Git",
        "Java", "Python", "JavaScript", "Page Object Model", "Framework Design",
        "Performance Testing", "JMeter", "Agile", "Scrum",
    ],
    "Blockchain": [
        "Blockchain", "Ethereum", "Solidity", "Smart Contracts", "Web3", "Cryptocurrency",
        "Hyperledger", "Truffle", "Hardhat", "Ganache", "IPFS", "DeFi", "NFT",
        "Rust", "Go", "JavaScript", "Node.js", "Python", "Cryptography", "Consensus Algorithms",
        "Distributed Systems", "Git",
    ],
    "Hadoop": [
        "Hadoop", "Spark", "Apache Spark", "Hive", "Pig", "HBase", "Kafka", "Apache Kafka",
        "MapReduce", "HDFS", "YARN", "Sqoop", "Flume", "Oozie", "Zookeeper", "Scala",
        "Java", "Python", "SQL", "ETL", "Data Pipeline", "Big Data", "NoSQL",
    ],
    "ETL Developer": [
        "ETL", "SQL", "Python", "Informatica", "SSIS", "Talend", "Apache Airflow",
        "Data Pipeline", "Data Warehouse", "Snowflake", "Redshift", "BigQuery",
        "Oracle", "SQL Server", "MySQL", "PostgreSQL", "Data Modeling", "Data Quality",
        "Shell Scripting", "Linux", "Git", "Spark", "Kafka",
    ],
    "Network Security Engineer": [
        "Network Security", "Cybersecurity", "Firewall", "VPN", "SIEM", "Splunk",
        "Penetration Testing", "Ethical Hacking", "OWASP", "TCP/IP", "DNS", "Wireshark",
        "Incident Response", "Risk Assessment", "Compliance", "ISO 27001", "GDPR",
        "Linux", "Python", "Bash", "Cloud Security", "AWS", "Azure",
    ],
    "SAP Developer": [
        "SAP", "ABAP", "SAP HANA", "SAP Fiori", "SAP UI5", "OData", "SAP BTP",
        "SAP Cloud", "ERP", "SAP MM", "SAP SD", "SAP FI", "SAP CO", "SAP HR",
        "SAP Basis", "SQL", "JavaScript", "REST API", "Git", "Agile",
    ],
    "Business Analyst": [
        "Business Analysis", "Requirements Gathering", "SQL", "Excel", "Power BI",
        "Tableau", "UML", "Process Improvement", "Stakeholder Management", "Agile",
        "Scrum", "Jira", "Confluence", "Data Analysis", "Documentation", "User Stories",
        "Wireframing", "BPMN", "SWOT Analysis", "Gap Analysis", "Project Management",
    ],
    "HR": [
        "Recruitment", "Talent Acquisition", "Onboarding", "Employee Relations",
        "Performance Management", "HR Management", "Payroll", "Compensation",
        "Benefits Administration", "Training and Development", "Labor Law", "Workday",
        "BambooHR", "ATS", "Interviewing", "Conflict Resolution", "Organizational Development",
        "Diversity and Inclusion", "HR Analytics", "Compliance",
    ],
    "Sales": [
        "Sales", "CRM", "Salesforce", "Lead Generation", "Negotiation", "Cold Calling",
        "Account Management", "B2B Sales", "B2C Sales", "Pipeline Management",
        "Forecasting", "Market Research", "Customer Relationship", "Presentation Skills",
        "Closing Techniques", "Territory Management", "Digital Marketing", "SEO",
        "Social Media Marketing", "Email Marketing",
    ],
    "PMO": [
        "Project Management", "Agile", "Scrum", "Kanban", "MS Project", "Primavera",
        "Jira", "Confluence", "Risk Management", "Stakeholder Management", "Budgeting",
        "Resource Planning", "PMO", "Governance", "Reporting", "Process Improvement",
        "Change Management", "Six Sigma", "Lean", "PMP",
    ],
    "Operations Manager": [
        "Operations Management", "Supply Chain", "Inventory Management", "Logistics",
        "Procurement", "Process Improvement", "Lean", "Six Sigma", "Quality Control",
        "Team Management", "Budgeting", "Forecasting", "KPI Management", "Vendor Management",
        "ERP", "SAP", "Excel", "Power BI", "Project Management", "Leadership",
    ],
    "Civil Engineer": [
        "AutoCAD", "Revit", "STAAD Pro", "ETABS", "Structural Analysis", "Surveying",
        "Construction Management", "Geotechnical", "Hydraulics", "Primavera", "MS Project",
        "Concrete Technology", "Steel Design", "Highway Engineering", "Environmental Engineering",
        "BIM", "Quantity Surveying", "Site Supervision", "Building Codes", "Project Management",
    ],
    "Mechanical Engineer": [
        "AutoCAD", "SolidWorks", "CATIA", "ANSYS", "MATLAB", "Thermodynamics",
        "Fluid Mechanics", "Mechanical Design", "Manufacturing", "CNC", "CAD", "CAM",
        "Quality Control", "Lean Manufacturing", "Project Management", "Materials Science",
        "Heat Transfer", "Machine Design", "Robotics", "Automation", "3D Printing",
    ],
    "Electrical Engineering": [
        "Circuit Design", "Power Systems", "Control Systems", "MATLAB", "Simulink",
        "PLC", "SCADA", "AutoCAD", "Embedded Systems", "PCB Design", "VHDL", "Verilog",
        "FPGA", "IoT", "Renewable Energy", "Electrical Safety", "Instrumentation",
        "Signal Processing", "Microcontrollers", "Arduino", "Project Management",
    ],
    "Advocate": [
        "Legal Research", "Contract Law", "Litigation", "Corporate Law", "Intellectual Property",
        "Compliance Management", "Due Diligence", "Case Management", "Court Proceedings",
        "Legal Writing", "Mediation", "Arbitration", "Negotiation", "Client Counseling",
        "Regulatory Compliance", "Legal Drafting", "Evidence Law", "Criminal Law",
        "Civil Law", "Constitutional Law",
    ],
    "Arts": [
        "Graphic Design", "Photoshop", "Illustrator", "Drawing", "Painting", "Typography",
        "Branding", "Creative Writing", "Photography", "Videography", "Adobe XD", "Figma",
        "UI Design", "Print Design", "Animation", "Video Editing", "Storytelling",
        "Fine Arts", "Sculpture", "Digital Art", "Color Theory", "Composition",
    ],
    "Health and fitness": [
        "Fitness Training", "Personal Training", "Nutrition", "Yoga", "Strength Training",
        "Cardio Training", "Weight Management", "Anatomy", "Kinesiology", "Sports Science",
        "Wellness Coaching", "CPR", "First Aid", "Pilates", "CrossFit", "Rehabilitation",
        "Mindfulness", "Mental Health", "Holistic Health", "Group Fitness",
    ],
}

JOB_RECOMMENDATIONS = {
    "Data Science": [
        "Data Scientist", "ML Engineer", "AI Engineer", "Data Analyst", "Research Scientist",
    ],
    "Python Developer": [
        "Python Developer", "Backend Developer", "Full Stack Developer", "Software Engineer", "API Developer",
    ],
    "Java Developer": [
        "Java Developer", "Backend Developer", "Software Engineer", "Spring Developer", "Enterprise Developer",
    ],
    "DotNet Developer": [
        ".NET Developer", "C# Developer", "Full Stack .NET Developer", "Software Engineer", "Azure Developer",
    ],
    "Web Designing": [
        "Web Designer", "UI Designer", "UX Designer", "Front-End Developer", "Creative Designer",
    ],
    "DevOps Engineer": [
        "DevOps Engineer", "Site Reliability Engineer", "Cloud Engineer", "Platform Engineer", "Infrastructure Engineer",
    ],
    "Database": [
        "Database Administrator", "Database Developer", "SQL Developer", "Data Engineer", "DBA Specialist",
    ],
    "Testing": [
        "QA Engineer", "Software Tester", "Quality Analyst", "Test Engineer", "QA Lead",
    ],
    "Automation Testing": [
        "Automation Test Engineer", "SDET", "QA Automation Engineer", "Test Automation Lead", "Performance Test Engineer",
    ],
    "Blockchain": [
        "Blockchain Developer", "Smart Contract Developer", "Web3 Developer", "Cryptocurrency Analyst", "DeFi Engineer",
    ],
    "Hadoop": [
        "Big Data Engineer", "Hadoop Developer", "Data Engineer", "Spark Developer", "ETL Developer",
    ],
    "ETL Developer": [
        "ETL Developer", "Data Integration Engineer", "BI Developer", "Data Warehouse Developer", "Informatica Developer",
    ],
    "Network Security Engineer": [
        "Security Engineer", "Cybersecurity Analyst", "Network Security Specialist", "SOC Analyst", "Penetration Tester",
    ],
    "SAP Developer": [
        "SAP ABAP Developer", "SAP Consultant", "SAP Technical Consultant", "SAP Fiori Developer", "SAP Integration Specialist",
    ],
    "Business Analyst": [
        "Business Analyst", "Product Analyst", "Systems Analyst", "Process Analyst", "IT Business Analyst",
    ],
    "HR": [
        "HR Manager", "Talent Acquisition Specialist", "HR Business Partner", "Recruitment Consultant", "People Operations Manager",
    ],
    "Sales": [
        "Sales Executive", "Account Manager", "Business Development Manager", "Sales Representative", "Inside Sales Specialist",
    ],
    "PMO": [
        "Project Manager", "Program Manager", "PMO Analyst", "Project Coordinator", "Portfolio Manager",
    ],
    "Operations Manager": [
        "Operations Manager", "Supply Chain Manager", "Logistics Manager", "Plant Manager", "General Manager",
    ],
    "Civil Engineer": [
        "Civil Engineer", "Structural Engineer", "Site Engineer", "Project Engineer", "Construction Manager",
    ],
    "Mechanical Engineer": [
        "Mechanical Engineer", "Design Engineer", "Production Engineer", "Maintenance Engineer", "R&D Engineer",
    ],
    "Electrical Engineering": [
        "Electrical Engineer", "Power Systems Engineer", "Control Systems Engineer", "Electronics Engineer", "Instrumentation Engineer",
    ],
    "Advocate": [
        "Legal Associate", "Corporate Lawyer", "Litigation Lawyer", "Legal Consultant", "Compliance Officer",
    ],
    "Arts": [
        "Graphic Designer", "Creative Director", "Visual Artist", "Art Director", "Multimedia Designer",
    ],
    "Health and fitness": [
        "Fitness Trainer", "Personal Trainer", "Wellness Coach", "Gym Instructor", "Nutrition Coach",
    ],
}


def _build_skill_pattern(skill):
    escaped = re.escape(skill)
    if " " in skill or "+" in skill or "#" in skill or "." in skill:
        return re.compile(rf"(?<![a-zA-Z0-9]){escaped}(?![a-zA-Z0-9])", re.IGNORECASE)
    return re.compile(rf"\b{escaped}\b", re.IGNORECASE)


SKILL_PATTERNS = {skill: _build_skill_pattern(skill) for skill in TECHNICAL_SKILLS}


def extract_skills(text):
    """Detect technical skills present in resume text."""
    if not text:
        return []

    detected = []
    for skill, pattern in SKILL_PATTERNS.items():
        if pattern.search(text):
            detected.append(skill)
    return sorted(detected, key=str.lower)


def get_missing_skills(category, detected_skills):
    """Return skills recommended for the category but missing from the resume."""
    expected = CATEGORY_SKILLS.get(category, [])
    detected_lower = {skill.lower() for skill in detected_skills}
    missing = [skill for skill in expected if skill.lower() not in detected_lower]
    return missing[:12]


ROLE_SKILLS_DB = {
    # Software & Backend
    "Python Developer": {
        "mandatory": ["Python"],
        "important": ["Django", "Flask", "REST API", "SQL"],
        "optional": ["Docker", "Git", "PostgreSQL", "Unit Testing"]
    },
    "Java Developer": {
        "mandatory": ["Java"],
        "important": ["Spring Boot", "Spring", "SQL", "Hibernate"],
        "optional": ["Docker", "Git", "Maven", "JUnit"]
    },
    "Backend Developer": {
        "mandatory": ["REST API"],
        "important": ["Python", "Node.js", "SQL", "PostgreSQL", "MongoDB"],
        "optional": ["Docker", "Kubernetes", "Redis", "Git", "Microservices"]
    },
    "Frontend Developer": {
        "mandatory": ["JavaScript", "HTML", "CSS"],
        "important": ["React", "Angular", "Vue.js", "Bootstrap", "Tailwind CSS"],
        "optional": ["Figma", "SASS", "TypeScript", "Vite", "Webpack"]
    },
    "Full Stack Developer": {
        "mandatory": ["Python", "JavaScript", "HTML", "CSS"],
        "important": ["React", "Node.js", "Django", "Flask", "SQL"],
        "optional": ["Docker", "Git", "AWS", "REST API", "Bootstrap"]
    },
    "Software Engineer": {
        "mandatory": ["Data Structures", "Algorithms"],
        "important": ["Python", "Java", "C++", "C#", "OOP"],
        "optional": ["Design Patterns", "SOLID", "Git", "Unit Testing"]
    },
    # Data Science & AI/ML
    "Data Scientist": {
        "mandatory": ["Python", "Statistics"],
        "important": ["Machine Learning", "SQL", "Pandas", "NumPy", "Scikit-learn"],
        "optional": ["Data Analysis", "Data Visualization", "Tableau", "R"]
    },
    "ML Engineer": {
        "mandatory": ["Python", "Machine Learning"],
        "important": ["Deep Learning", "TensorFlow", "PyTorch", "Scikit-learn"],
        "optional": ["Docker", "Kubernetes", "Git", "MLOps", "Linux"]
    },
    "AI Engineer": {
        "mandatory": ["Deep Learning", "NLP"],
        "important": ["Python", "Transformers", "BERT", "GPT", "LLM", "Generative AI"],
        "optional": ["PyTorch", "TensorFlow", "Computer Vision", "Git"]
    },
    "Data Analyst": {
        "mandatory": ["SQL", "Excel"],
        "important": ["Data Analysis", "Data Visualization", "Tableau", "Power BI"],
        "optional": ["Python", "Statistics", "Google Sheets", "R"]
    },
    "Data Engineer": {
        "mandatory": ["SQL", "ETL"],
        "important": ["Python", "Spark", "Kafka", "Hadoop", "Data Pipeline"],
        "optional": ["Snowflake", "Redshift", "BigQuery", "Data Warehouse", "NoSQL"]
    },
    # DevOps & Cloud
    "DevOps Engineer": {
        "mandatory": ["Docker", "CI/CD"],
        "important": ["Kubernetes", "AWS", "Jenkins", "GitHub Actions", "Terraform"],
        "optional": ["Ansible", "Linux", "Bash", "Nginx", "Git"]
    },
    "Cloud Engineer": {
        "mandatory": ["AWS"],
        "important": ["Azure", "GCP", "Docker", "Terraform", "CloudFormation"],
        "optional": ["Networking", "Linux", "Kubernetes", "Security"]
    },
    "Site Reliability Engineer": {
        "mandatory": ["Linux", "Kubernetes"],
        "important": ["Python", "Docker", "AWS", "Monitoring", "Prometheus", "Grafana"],
        "optional": ["Bash", "SRE", "Nginx", "Networking"]
    },
    # Operations & Supply Chain
    "Operations Manager": {
        "mandatory": ["Operations Management"],
        "important": ["Process Improvement", "Team Management", "Budgeting", "KPI Management"],
        "optional": ["Lean", "Six Sigma", "Excel", "Project Management"]
    },
    "Supply Chain Manager": {
        "mandatory": ["Supply Chain"],
        "important": ["Logistics", "Procurement", "Inventory Management", "Vendor Management"],
        "optional": ["Negotiation", "ERP", "SAP", "Excel"]
    },
    "Logistics Manager": {
        "mandatory": ["Logistics"],
        "important": ["Supply Chain", "Warehouse Management", "Transportation", "Inventory Management"],
        "optional": ["Distribution", "Procurement", "Excel", "Budgeting"]
    },
    # HR & Management
    "HR Manager": {
        "mandatory": ["HR Management"],
        "important": ["Employee Relations", "Performance Management", "Talent Acquisition", "Conflict Resolution"],
        "optional": ["Labor Law", "Onboarding", "Workday", "BambooHR"]
    },
    "Talent Acquisition Specialist": {
        "mandatory": ["Recruitment"],
        "important": ["Talent Acquisition", "Interviewing", "ATS", "Onboarding"],
        "optional": ["Sourcing", "Negotiation", "Social Media Marketing"]
    },
    "Project Manager": {
        "mandatory": ["Project Management"],
        "important": ["Agile", "Scrum", "Risk Management", "Stakeholder Management", "Budgeting"],
        "optional": ["Kanban", "MS Project", "Jira", "Confluence", "PMP"]
    },
    # Finance & Marketing
    "Financial Analyst": {
        "mandatory": ["Financial Analysis"],
        "important": ["Excel", "Budgeting", "Forecasting", "Data Analysis"],
        "optional": ["Accounting", "SQL", "Tableau", "Market Research"]
    },
    "Digital Marketing Specialist": {
        "mandatory": ["Digital Marketing"],
        "important": ["SEO", "SEM", "Google Analytics", "Content Marketing"],
        "optional": ["Social Media Marketing", "Email Marketing", "Copywriting"]
    },
    "SEO Specialist": {
        "mandatory": ["SEO"],
        "important": ["Google Analytics", "SEM", "Content Marketing", "Copywriting"],
        "optional": ["HTML", "CSS", "Market Research", "Excel"]
    },
    # UI/UX & Design
    "UI/UX Designer": {
        "mandatory": ["UI/UX"],
        "important": ["Figma", "Adobe XD", "Wireframing", "Prototyping", "UX Design"],
        "optional": ["HTML5", "CSS3", "JavaScript", "User Research", "Responsive Design"]
    },
    "Graphic Designer": {
        "mandatory": ["Graphic Design"],
        "important": ["Photoshop", "Illustrator", "Typography", "Branding"],
        "optional": ["Figma", "Adobe XD", "Creative Writing", "Print Design"]
    },
    # Databases & Systems
    "Database Administrator": {
        "mandatory": ["SQL"],
        "important": ["MySQL", "PostgreSQL", "Oracle", "SQL Server", "Performance Tuning"],
        "optional": ["Backup and Recovery", "Replication", "Database Design", "NoSQL"]
    },
    # Legal & Compliance
    "Legal Associate": {
        "mandatory": ["Legal Research"],
        "important": ["Legal Writing", "Case Management", "Contract Law", "Due Diligence"],
        "optional": ["Compliance Management", "Mediation", "Arbitration"]
    },
    "Corporate Lawyer": {
        "mandatory": ["Corporate Law"],
        "important": ["Contract Law", "Due Diligence", "Compliance Management", "Negotiation"],
        "optional": ["Mergers and Acquisitions", "Intellectual Property", "Legal Writing"]
    },
    # Arts & Arts Management
    "Visual Artist": {
        "mandatory": ["Fine Arts"],
        "important": ["Drawing", "Painting", "Digital Art", "Color Theory"],
        "optional": ["Composition", "Sculpture", "Graphic Design"]
    },
    # Health & Fitness
    "Fitness Trainer": {
        "mandatory": ["Fitness Training"],
        "important": ["Personal Training", "Strength Training", "Cardio Training", "Group Fitness"],
        "optional": ["First Aid", "CPR", "Nutrition", "Anatomy"]
    },
    "Nutrition Coach": {
        "mandatory": ["Nutrition"],
        "important": ["Weight Management", "Meal Planning", "Wellness Coaching", "Health Coaching"],
        "optional": ["Anatomy", "Kinesiology", "First Aid"]
    }
}


def get_detailed_job_recommendations(detected_skills):
    """
    Separate role-matching engine.
    - Compares detected_skills against ROLE_SKILLS_DB.
    - If all mandatory skills are present, role is Eligible.
    - If any mandatory skills are missing, role is Ineligible (Potential Career Path).
    - Returns (recommended_roles, potential_career_paths).
    """
    detected_set = {s.lower() for s in detected_skills}
    
    eligible = []
    ineligible = []
    
    for role, skill_groups in ROLE_SKILLS_DB.items():
        mand_skills = skill_groups["mandatory"]
        imp_skills = skill_groups["important"]
        opt_skills = skill_groups["optional"]
        
        mand_set = {s.lower() for s in mand_skills}
        imp_set = {s.lower() for s in imp_skills}
        opt_set = {s.lower() for s in opt_skills}
        
        # Check if all mandatory skills are present
        missing_mand = [s for s in mand_skills if s.lower() not in detected_set]
        
        total_skills_list = mand_skills + imp_skills + opt_skills
        total_skills_set = mand_set.union(imp_set).union(opt_set)
        
        matched_set = total_skills_set.intersection(detected_set)
        matched_skills = [s for s in total_skills_list if s.lower() in matched_set]
        missing_skills = [s for s in total_skills_list if s.lower() not in matched_set]
        
        match_count = len(matched_set)
        total_count = len(total_skills_set)
        
        if total_count > 0:
            match_percentage = round((match_count / total_count) * 100, 1)
        else:
            match_percentage = 0.0
            
        if len(missing_mand) == 0:
            # Eligible role
            # Generate explanation
            if match_percentage >= 80.0:
                reason = f"Excellent match! You satisfy all core requirements and have strong familiarity with important tools like {', '.join(matched_skills[:2])}."
            elif match_percentage >= 60.0:
                reason = f"Strong candidate. You have all mandatory skills. Improving important skills like {', '.join(missing_skills[:2])} will make you highly competitive."
            else:
                reason = f"Foundational match. You have the mandatory core skills. Acquire experience in {', '.join(missing_skills[:2])} to advance in this role."
                
            eligible.append({
                "role": role,
                "match_percentage": match_percentage,
                "matched_skills": matched_skills,
                "missing_skills": missing_skills,
                "explanation": reason
            })
        else:
            # Ineligible role (Potential Career Path)
            ineligible.append({
                "role": role,
                "match_percentage": match_percentage,
                "missing_mandatory": missing_mand,
                "missing_skills": missing_skills,
                "matched_skills": matched_skills
            })
            
    # Rank eligible roles by match percentage (descending)
    eligible.sort(key=lambda x: x["match_percentage"], reverse=True)
    recommended_roles = eligible[:3]
    
    # Rank ineligible roles by number of missing mandatory skills (ascending), then match percentage (descending)
    ineligible.sort(key=lambda x: (len(x["missing_mandatory"]), -x["match_percentage"]))
    potential_paths = ineligible[:3]
    
    return recommended_roles, potential_paths


def get_job_recommendations(detected_skills):
    """Return top 3 eligible recommended job roles."""
    # Convert input back from potential list-like parameters if needed
    if isinstance(detected_skills, str):
        detected_skills = [detected_skills]
    elif not isinstance(detected_skills, (list, set, tuple)):
        detected_skills = []
    recommended, _ = get_detailed_job_recommendations(detected_skills)
    return recommended


def get_potential_career_paths(detected_skills):
    """Return top 3 ineligible job roles with missing mandatory skills."""
    if isinstance(detected_skills, str):
        detected_skills = [detected_skills]
    elif not isinstance(detected_skills, (list, set, tuple)):
        detected_skills = []
    _, potential = get_detailed_job_recommendations(detected_skills)
    return potential

