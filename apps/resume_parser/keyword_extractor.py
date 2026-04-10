import re
import spacy

# spaCy model load karo
try:
    nlp = spacy.load("en_core_web_sm")
except:
    nlp = None
    print("⚠️ spaCy model not found. Run: python -m spacy download en_core_web_sm")

# =============================================
# EXPANDED SKILLS DATABASE
# =============================================
SKILLS_DATABASE = [
    # Programming Languages
    'Python', 'Java', 'JavaScript', 'C++', 'C#', 'Ruby', 'PHP', 'Swift', 'Kotlin', 'Go',
    'TypeScript', 'Scala', 'R', 'Perl', 'Rust', 'Dart', 'Objective-C', 'Bash', 'Shell',
    'MATLAB', 'Groovy', 'Lua', 'Haskell', 'Elixir', 'Clojure', 'VBA', 'COBOL',

    # Web Technologies
    'React', 'Angular', 'Vue.js', 'Node.js', 'Express.js', 'Django', 'Flask', 'FastAPI',
    'Spring Boot', 'ASP.NET', 'Laravel', 'Ruby on Rails', 'Next.js', 'Nuxt.js',
    'HTML', 'CSS', 'Bootstrap', 'Tailwind CSS', 'SASS', 'SCSS', 'Webpack', 'Vite',
    'jQuery', 'Redux', 'GraphQL', 'REST API', 'API Development', 'Web Development',
    'Frontend Development', 'Backend Development', 'Full Stack', 'Fullstack',
    'Responsive Design', 'Responsive UI', 'WebSocket', 'OAuth', 'JWT',

    # Databases
    'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'SQLite', 'Oracle', 'SQL Server',
    'Cassandra', 'DynamoDB', 'Firebase', 'Elasticsearch', 'SQL', 'NoSQL',
    'Database Design', 'Database Management', 'Database Interactions',

    # Cloud & DevOps
    'AWS', 'Azure', 'GCP', 'Google Cloud', 'Docker', 'Kubernetes', 'Jenkins', 'Git',
    'GitLab', 'GitHub', 'CI/CD', 'Terraform', 'Ansible', 'Linux', 'Unix',
    'AWS Cloud Services', 'AWS Bedrock', 'Cloud Integration', 'DevOps',
    'Containerization', 'Microservices', 'Serverless', 'Nginx', 'Apache',

    # Data Science & ML
    'Machine Learning', 'Deep Learning', 'TensorFlow', 'PyTorch', 'Scikit-learn',
    'Pandas', 'NumPy', 'Matplotlib', 'Keras', 'NLP', 'Computer Vision', 'OpenCV',
    'Data Analysis', 'Data Science', 'Data Engineering', 'Big Data',
    'Tableau', 'Power BI', 'Excel', 'Spark', 'Hadoop', 'Streamlit',
    'Generative AI', 'LLM', 'OpenAI', 'LangChain',

    # Mobile
    'Android', 'iOS', 'React Native', 'Flutter', 'Xamarin',

    # Tools & Productivity
    'JIRA', 'Confluence', 'Slack', 'Trello', 'Notion', 'Asana',
    'Email Management', 'Google Workspace', 'Microsoft Office',
    'GitHub Management', 'Project Management', 'CRM',

    # Soft/Work Skills
    'Agile', 'Scrum', 'Team Collaboration', 'Remote Collaboration',
    'Communication', 'Problem Solving', 'Technical Writing', 'Leadership',
    'English', 'Time Management', 'Critical Thinking',

    # Testing & QA
    'Selenium', 'Jest', 'Pytest', 'Unit Testing', 'Integration Testing', 'QA', 'Testing',
]

# Lowercase lookup dict for fast matching
SKILLS_LOWER = {skill.lower(): skill for skill in SKILLS_DATABASE}

# Context patterns — sentence mein se skills nikalne ke liye
SKILL_CONTEXT_PATTERNS = [
    r'manage\s+([A-Za-z][A-Za-z0-9\s\.\+\#\-]{1,30}?)(?:\s*,|\s*\.|$|\s+and)',
    r'experience\s+(?:with|in|of)\s+([A-Za-z][A-Za-z0-9\s\.\+\#]{1,30}?)(?:\s*,|\s*\.|$|\s+and)',
    r'proficiency\s+(?:in|with)\s+([A-Za-z][A-Za-z0-9\s\.\+\#]{1,30}?)(?:\s*,|\s*\.|$|\s+and)',
    r'knowledge\s+(?:of|in|with)\s+([A-Za-z][A-Za-z0-9\s\.\+\#]{1,30}?)(?:\s*,|\s*\.|$|\s+and)',
    r'skilled\s+(?:in|with)\s+([A-Za-z][A-Za-z0-9\s\.\+\#]{1,30}?)(?:\s*,|\s*\.|$|\s+and)',
    r'using\s+([A-Za-z][A-Za-z0-9\s\.\+\#]{1,30}?)(?:\s*,|\s*\.|$|\s+and|\s+to)',
    r'work(?:ing)?\s+with\s+([A-Za-z][A-Za-z0-9\s\.\+\#]{1,30}?)(?:\s*,|\s*\.|$|\s+and)',
    r'build(?:ing)?\s+(?:with|using|in)\s+([A-Za-z][A-Za-z0-9\s\.\+\#]{1,30}?)(?:\s*,|\s*\.|$|\s+and)',
    r'develop(?:ing)?\s+(?:in|with|using)\s+([A-Za-z][A-Za-z0-9\s\.\+\#]{1,30}?)(?:\s*,|\s*\.|$|\s+and)',
    r'tools?\s+(?:like|such as|including)\s+([A-Za-z][A-Za-z0-9\s\.\+\#\,]{1,60}?)(?:\.|$)',
]

# Section headers jo skills/requirements indicate karte hain
SKILL_SECTION_HEADERS = [
    "what we're looking for", "requirements", "qualifications", "skills required",
    "must have", "must-have", "required skills", "technical skills", "tech stack",
    "you should have", "we need", "looking for", "what you need", "you will need",
    "nice to have", "nice-to-have", "bonus", "preferred qualifications",
    "responsibilities", "what you'll do", "your role", "key responsibilities",
    "tools and technologies", "technologies", "tech requirements",
]

# In headers pe section band karo
STOP_SECTION_HEADERS = [
    'how we', 'benefits', 'about us', 'apply now',
    'what we offer', 'why join', 'perks', 'compensation',
    'life at', 'our culture', 'equal opportunity',
]


# =============================================
# MAIN FUNCTION
# =============================================

def extract_skills(text):
    """
    4 methods se skills extract karo:
    1. Direct keyword match
    2. Section-based (Requirements, Skills sections)
    3. spaCy NLP sentence analysis
    4. Context patterns ("manage github", "using pandas")
    """
    if not text:
        return []

    found_skills = set()
    found_skills.update(_direct_keyword_match(text))
    found_skills.update(_extract_from_sections(text))
    if nlp:
        found_skills.update(_spacy_extract(text))
    found_skills.update(_context_pattern_match(text))

    return sorted(list(found_skills))


# =============================================
# METHOD 1: Direct Keyword Match
# =============================================

def _direct_keyword_match(text):
    found = set()
    text_lower = text.lower()
    for skill_lower, skill_original in SKILLS_LOWER.items():
        pattern = r'\b' + re.escape(skill_lower) + r'\b'
        if re.search(pattern, text_lower):
            found.add(skill_original)
    return found


# =============================================
# METHOD 2: Section-Based Extraction
# =============================================

def _extract_from_sections(text):
    found = set()
    lines = text.split('\n')
    in_skill_section = False

    for line in lines:
        line_stripped = line.strip()
        line_lower = line_stripped.lower()

        if any(header in line_lower for header in SKILL_SECTION_HEADERS):
            in_skill_section = True
            continue

        if any(h in line_lower for h in STOP_SECTION_HEADERS):
            in_skill_section = False
            continue

        if in_skill_section and line_stripped:
            if line_stripped.startswith(('-', '*', '•', '·', '>')):
                clean = line_stripped.lstrip('-*•·> ').strip()
                found.update(_parse_skills_from_sentence(clean))
            else:
                found.update(_parse_skills_from_sentence(line_stripped))

    return found


# =============================================
# METHOD 3: spaCy NLP Extraction
# =============================================

def _spacy_extract(text):
    """
    Sentence level NLP:
    "backend developer to manage github and email management"
    → GitHub, Email Management
    """
    found = set()
    doc = nlp(text[:100000])  # spaCy limit

    for sent in doc.sents:
        sent_lower = sent.text.lower()

        # Har sentence mein skills dhundo
        for skill_lower, skill_original in SKILLS_LOWER.items():
            pattern = r'\b' + re.escape(skill_lower) + r'\b'
            if re.search(pattern, sent_lower):
                found.add(skill_original)

        # Named entities se (ORG, PRODUCT)
        for ent in sent.ents:
            ent_lower = ent.text.lower().strip()
            if ent_lower in SKILLS_LOWER:
                found.add(SKILLS_LOWER[ent_lower])

        # Noun chunks se
        for chunk in sent.noun_chunks:
            chunk_lower = chunk.text.lower().strip()
            if chunk_lower in SKILLS_LOWER:
                found.add(SKILLS_LOWER[chunk_lower])
            # Multi-word skills bhi check karo
            for skill_lower, skill_original in SKILLS_LOWER.items():
                if skill_lower in chunk_lower and len(skill_lower) > 3:
                    found.add(skill_original)

    return found


# =============================================
# METHOD 4: Context Pattern Matching
# =============================================

def _context_pattern_match(text):
    """
    "we need backend developer to manage github, email management, pandas"
    → GitHub, Email Management, Pandas
    """
    found = set()
    text_lower = text.lower()

    for pattern in SKILL_CONTEXT_PATTERNS:
        matches = re.findall(pattern, text_lower, re.IGNORECASE | re.MULTILINE)
        for match in matches:
            found.update(_parse_skills_from_sentence(match))
            if match.strip() in SKILLS_LOWER:
                found.add(SKILLS_LOWER[match.strip()])

    return found


# =============================================
# HELPER: Sentence se skills parse karo
# =============================================

def _parse_skills_from_sentence(sentence):
    """
    Ek sentence/phrase se saari skills nikalo.
    Handles:
    - "Python and Django" → [Python, Django]
    - "HTML/CSS/JavaScript" → [HTML, CSS, JavaScript]
    - "manage github, email management" → [GitHub, Email Management]
    - "3+ years of experience with Pandas" → [Pandas]
    """
    found = set()
    sentence_lower = sentence.lower()

    # Direct match
    for skill_lower, skill_original in SKILLS_LOWER.items():
        pattern = r'\b' + re.escape(skill_lower) + r'\b'
        if re.search(pattern, sentence_lower):
            found.add(skill_original)

    # Slash separated: HTML/CSS/JavaScript
    slash_matches = re.findall(
        r'([A-Za-z][A-Za-z0-9\+\#\.]+(?:/[A-Za-z][A-Za-z0-9\+\#\.]+)+)', sentence
    )
    for slash_match in slash_matches:
        for part in slash_match.split('/'):
            part_lower = part.lower().strip()
            if part_lower in SKILLS_LOWER:
                found.add(SKILLS_LOWER[part_lower])

    # Comma/and separated parts
    parts = re.split(r'[,/&]|\s+and\s+', sentence_lower)
    for part in parts:
        part = re.sub(
            r'^(strong|good|excellent|proficient|expert|basic|advanced|'
            r'experience\s+(?:with|in)|knowledge\s+of|proficiency\s+in|'
            r'\d+\+?\s*years?\s*(?:of)?\s*(?:experience\s*(?:with|in)?)?)\s*',
            '', part.strip(), flags=re.IGNORECASE
        ).strip()
        if part in SKILLS_LOWER:
            found.add(SKILLS_LOWER[part])

    return found


# =============================================
# OTHER EXTRACTORS
# =============================================

def extract_experience(text):
    patterns = [
        r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of)?\s*(?:experience|exp)',
        r'experience[:\s]+(\d+)\+?\s*(?:years?|yrs?)',
        r'(\d+)\+?\s*(?:years?|yrs?)',
    ]
    for pattern in patterns:
        matches = re.findall(pattern, text.lower())
        if matches:
            return int(matches[0])
    return 0


def extract_email(text):
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    matches = re.findall(pattern, text)
    return matches[0] if matches else ""


def extract_phone(text):
    pattern = r'[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}'
    matches = re.findall(pattern, text)
    return matches[0] if matches else ""


def extract_location(text):
    cities = [
        'Mumbai', 'Delhi', 'Bangalore', 'Hyderabad', 'Chennai', 'Kolkata',
        'Pune', 'Ahmedabad', 'Jaipur', 'Surat', 'Lucknow', 'Kanpur',
        'Nagpur', 'Indore', 'Thane', 'Bhopal', 'Visakhapatnam', 'Patna',
        'Noida', 'Gurgaon', 'Gurugram', 'Chandigarh', 'Coimbatore',
        'Kochi', 'Vadodara', 'Agra', 'Nashik', 'Ranchi', 'Mysore',
    ]
    text_lower = text.lower()
    for city in cities:
        if city.lower() in text_lower:
            return city
    return "Not Specified"