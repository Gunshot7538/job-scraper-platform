import re
import os
import sys

APPS_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if APPS_DIR not in sys.path:
    sys.path.insert(0, APPS_DIR)

from resume_parser.keyword_extractor import extract_skills


# SKILL CATEGORIES


UNIVERSAL_SKILLS = {
    'git', 'github', 'gitlab', 'english', 'communication', 'problem solving',
    'team collaboration', 'agile', 'scrum', 'jira', 'confluence', 'slack',
    'time management', 'debugging', 'code review', 'documentation',
    'linux', 'command line', 'vs code', 'postman', 'google workspace',
    'ms office', 'microsoft office', 'critical thinking', 'remote collaboration',
}


SKILL_GROUPS = [
    # ── Version Control ──────────────────────────────────────────
    ('git', 'github', 'gitlab', 'version control', 'source control',
     'vcs', 'bitbucket'),

    # ── JavaScript ───────────────────────────────────────────────
    ('javascript', 'js', 'java script', 'ecmascript', 'es6',
     'frontend', 'front end', 'front-end',           
     'programming', 'scripting'),                    

    # ── TypeScript ───────────────────────────────────────────────
    ('typescript', 'ts'),

    # ── React ────────────────────────────────────────────────────
    ('react', 'react.js', 'reactjs', 'react js',
     'ui development', 'ui library'),

    # ── Redux / State Management ─────────────────────────────────
    ('redux', 'redux toolkit', 'state management', 'flux'),

    # ── React Query / TanStack ───────────────────────────────────
    ('react query', 'tanstack', 'tanstack query', 'react-query'),

    # ── Next.js / SSR ────────────────────────────────────────────
    ('next.js', 'next', 'nextjs', 'ssr', 'ssg',
     'server side rendering', 'server-side rendering'),

    # ── Node.js ──────────────────────────────────────────────────
    ('node.js', 'node', 'nodejs', 'backend', 'back end', 'back-end'),

    # ── Express ──────────────────────────────────────────────────
    ('express.js', 'express', 'expressjs'),

    # ── CSS ──────────────────────────────────────────────────────
    ('css3', 'css', 'styling', 'responsive design', 'responsive',
     'ui/ux', 'web design'),

    # ── HTML ─────────────────────────────────────────────────────
    ('html5', 'html', 'markup', 'web markup'),

    # ── Tailwind CSS ─────────────────────────────────────────────
    ('tailwind css', 'tailwind', 'tailwindcss'),

    # ── Bootstrap ────────────────────────────────────────────────
    ('bootstrap', 'bootstrap css'),

    # ── MUI / Material UI ────────────────────────────────────────
    ('mui', 'material ui', 'material-ui', '@mui'),

    # ── AntDesign ────────────────────────────────────────────────
    ('antdesign', 'ant design', 'ant-design', 'antd'),

    # ── Shadcn ───────────────────────────────────────────────────
    ('shadcn', 'shadcn/ui', 'shadcn ui'),

    # ── REST API ─────────────────────────────────────────────────
    ('rest api', 'rest', 'restful', 'rest apis', 'api', 'apis',
     'api integration', 'web services', 'http'),

    # ── GraphQL ──────────────────────────────────────────────────
    ('graphql', 'graph ql', 'gql'),

    # ── PostgreSQL ───────────────────────────────────────────────
    ('postgresql', 'postgres', 'pg'),

    # ── MySQL ────────────────────────────────────────────────────
    ('mysql', 'my sql'),

    # ── SQL (generic) ────────────────────────────────────────────
    ('sql', 'database', 'databases', 'db', 'relational database',
     'rdbms'),

    # ── MongoDB ──────────────────────────────────────────────────
    ('mongodb', 'mongo', 'nosql', 'document database'),

    # ── Testing / Jest ───────────────────────────────────────────
    ('jest', 'unit testing', 'testing', 'test', 'jasmine'),

    # ── Performance ──────────────────────────────────────────────
    ('performance optimization', 'performance', 'web performance',
     'optimization', 'core web vitals', 'lighthouse'),

    # ── Architecture / Scalability ───────────────────────────────
    ('architecture', 'arcitecture',                  # common typo
     'system design', 'scalability', 'architectural',
     'software design', 'design patterns', 'oop',
     'object oriented', 'object oriented programming'),

    # ── Debugging ────────────────────────────────────────────────
    ('debugging', 'troubleshooting', 'bug fixing', 'root cause analysis'),

    # ── CI/CD ────────────────────────────────────────────────────
    ('ci/cd', 'ci cd', 'continuous integration', 'continuous deployment',
     'ci/cd pipelines', 'devops pipelines', 'github actions', 'jenkins'),

    # ── Docker / Containers ──────────────────────────────────────
    ('docker', 'containers', 'containerization'),

    # ── Kubernetes ───────────────────────────────────────────────
    ('kubernetes', 'k8s', 'container orchestration'),

    # ── AWS / Cloud ──────────────────────────────────────────────
    ('aws', 'amazon web services', 'cloud', 'cloud computing',
     'azure', 'gcp', 'google cloud'),

    # ── Python ───────────────────────────────────────────────────
    ('python', 'py'),

    # ── Java ─────────────────────────────────────────────────────
    ('java', 'core java'),

    # ── Kotlin ───────────────────────────────────────────────────
    ('kotlin',),

    # ── Android ──────────────────────────────────────────────────
    ('android', 'android development', 'android sdk'),

    # ── Flutter ──────────────────────────────────────────────────
    ('flutter', 'dart'),

    # ── React Native ─────────────────────────────────────────────
    ('react native', 'rn'),

    # ── Machine Learning ─────────────────────────────────────────
    ('machine learning', 'ml'),

    # ── Deep Learning ────────────────────────────────────────────
    ('deep learning', 'dl', 'neural networks', 'neural network'),

    # ── Data Science ─────────────────────────────────────────────
    ('data science', 'data analysis', 'data analytics'),

    # ── Algorithms / DSA ─────────────────────────────────────────
    ('algorithms', 'data structures', 'dsa', 'data structures and algorithms'),

    # ── Problem Solving ──────────────────────────────────────────
    ('problem solving', 'analytical skills', 'analytical',
     'analytical thinking', 'logical thinking', 'critical thinking'),

    # ── Communication ────────────────────────────────────────────
    ('communication', 'verbal communication', 'written communication',
     'interpersonal skills'),

    # ── Agile / Scrum ────────────────────────────────────────────
    ('agile', 'scrum', 'kanban', 'agile methodology', 'sprint'),

    # ── Linux ────────────────────────────────────────────────────
    ('linux', 'unix', 'bash', 'shell scripting', 'command line',
     'terminal', 'cli'),
]

# ── Auto-build the alias map from SKILL_GROUPS ──────────────────
# canonical = first term in each group (the "main" name)
SKILL_ALIASES: dict[str, str] = {}
for group in SKILL_GROUPS:
    canonical = group[0]
    for term in group:
        SKILL_ALIASES[term.lower()] = canonical


FORCE_CORE_SKILLS = {
    'react', 'angular', 'vue.js', 'javascript', 'typescript',
    'node.js', 'python', 'java', 'django', 'flask', 'fastapi',
    'spring boot', 'next.js', 'flutter', 'android', 'css3', 'html5',
    'css', 'html', 'express.js', 'redux', 'graphql', 'rest api',
    'postgresql', 'mysql', 'mongodb', 'machine learning', 'deep learning',
    'data science', 'devops', 'kubernetes', 'docker', 'aws',
    'performance optimization', 'architecture', 'algorithms',
    'react query', 'tailwind css', 'jest',
}

IMPLIED_SKILLS = {
    'python':           ['git', 'github', 'linux', 'debugging', 'postman'],
    'java':             ['git', 'github', 'linux', 'debugging', 'maven'],
    'javascript':       ['git', 'github', 'html5', 'css3', 'npm'],
    'typescript':       ['javascript', 'git', 'html5', 'css3', 'npm'],
    'react':            ['javascript', 'typescript', 'html5', 'css3', 'git', 'npm', 'architecture'],
    'angular':          ['typescript', 'javascript', 'html5', 'css3', 'git'],
    'vue.js':           ['javascript', 'html5', 'css3', 'git'],
    'node.js':          ['javascript', 'git', 'rest api', 'npm', 'express.js'],
    'next.js':          ['react', 'javascript', 'typescript', 'css3', 'html5'],
    'django':           ['python', 'sql', 'git', 'rest api', 'postman'],
    'flask':            ['python', 'git', 'rest api', 'postman'],
    'fastapi':          ['python', 'git', 'rest api', 'postman'],
    'spring boot':      ['java', 'git', 'rest api', 'maven'],
    'aws':              ['linux', 'git', 'ci/cd', 'command line'],
    'docker':           ['linux', 'git', 'command line', 'ci/cd'],
    'kubernetes':       ['docker', 'linux', 'git', 'ci/cd'],
    'machine learning': ['python', 'numpy', 'pandas', 'git'],
    'deep learning':    ['python', 'numpy', 'tensorflow', 'git'],
    'data science':     ['python', 'numpy', 'pandas', 'sql', 'excel', 'git'],
    'android':          ['java', 'kotlin', 'git'],
    'flutter':          ['dart', 'git'],
    'react native':     ['javascript', 'git'],
    'devops':           ['linux', 'git', 'docker', 'ci/cd'],
    'mysql':            ['sql', 'database design'],
    'postgresql':       ['sql', 'database design'],
    'mongodb':          ['nosql', 'database design'],
    'pandas':           ['python', 'numpy', 'excel'],
    'tensorflow':       ['python', 'numpy', 'machine learning'],
    'pytorch':          ['python', 'numpy', 'machine learning'],
    # Frontend-specific implies
    'redux':            ['react', 'javascript'],
    'react query':      ['react', 'javascript', 'rest api'],
    'tailwind css':     ['css3', 'html5'],
    'jest':             ['javascript', 'debugging'],
    'express.js':       ['node.js', 'javascript', 'rest api'],
}

TOOLS_AND_LIBS = {
    'pandas', 'numpy', 'matplotlib', 'scikit-learn', 'keras', 'tensorflow',
    'pytorch', 'opencv', 'streamlit', 'fastapi', 'flask', 'django', 'react',
    'angular', 'vue.js', 'bootstrap', 'tailwind css', 'jquery', 'redux',
    'docker', 'kubernetes', 'jenkins', 'terraform', 'ansible', 'nginx',
    'apache', 'redis', 'elasticsearch', 'firebase', 'mongodb', 'mysql',
    'postgresql', 'sqlite', 'celery', 'rabbitmq', 'graphql', 'postman',
    'jest', 'pytest', 'selenium', 'webpack', 'vite', 'npm', 'maven',
    'gradle', 'git', 'github', 'gitlab', 'jira', 'confluence', 'slack',
    'vs code', 'jupyter', 'langchain', 'openai',
}



# HIGH-ACCURACY WEIGHTED MATCHER CLASS


class SmartJobMatcher:
    """
    Weighted scoring:
      Core Tech Skills  → 70%
      Tools & Libraries → 20%
      Universal/Soft    → 10%

    Key fix — SKILL_GROUPS based normalization:
      Both resume skills AND job skills are normalized to canonical
      group names BEFORE any comparison.

      This means "version control" (scraped) == "git" (resume),
      "unit testing" == "jest", "analytical skills" == "problem solving",
      etc. — score never drops just because of naming differences.

      To extend: add new tuples to SKILL_GROUPS at the top of this file.
    """

    def normalize_skills(self, skills_set):
        """
        Convert every skill to its canonical group name using SKILL_ALIASES.
        Also handles:
          - compound skills like "JavaScript/TypeScript" → split on /
          - extra whitespace, casing
        """
        normalized = set()
        for skill in skills_set:
            s = skill.lower().strip()
            # Handle compound: "javascript/typescript", "css/html"
            parts = [p.strip() for p in s.split('/')] if '/' in s else [s]
            for part in parts:
                canonical = SKILL_ALIASES.get(part, part)
                normalized.add(canonical)
        return normalized

    def expand_skills(self, skills_set):
        expanded = set(skills_set)
        expanded.update(UNIVERSAL_SKILLS)
        for skill in list(expanded):
            for implied in IMPLIED_SKILLS.get(skill.lower(), []):
                expanded.add(implied.lower())
        return expanded

    def categorize(self, skills_set):
        # FORCE_CORE takes priority — these are always core regardless of TOOLS_AND_LIBS
        core  = {s for s in skills_set if s.lower() in FORCE_CORE_SKILLS}
        remaining = skills_set - core
        tools = {s for s in remaining if s.lower() in TOOLS_AND_LIBS}
        univ  = {s for s in remaining if s.lower() in UNIVERSAL_SKILLS}
        # Anything not categorized yet → also core (benefit of doubt)
        leftover = remaining - tools - univ
        core.update(leftover)
        return core, tools, univ

    def calculate_smart_score(self, resume_skills_raw, job_skills_raw):
        # Normalize BOTH sides before any comparison
        resume_skills = self.normalize_skills(
            {s.lower().strip() for s in resume_skills_raw if s.strip()}
        )
        job_skills = self.normalize_skills(
            {s.lower().strip() for s in job_skills_raw if s.strip()}
        )

        if not job_skills:
            return 50.0, {'note': 'No job skills found — neutral score'}

        expanded_resume = self.expand_skills(resume_skills)
        core_req, tools_req, univ_req = self.categorize(job_skills)

        def match_pct(required, available):
            if not required:
                return 100.0
            return (len(required & available) / len(required)) * 100

        raw_score = (
            match_pct(core_req,  expanded_resume) * 0.70 +
            match_pct(tools_req, expanded_resume) * 0.20 +
            match_pct(univ_req,  expanded_resume) * 0.10
        )
        final = min(round(raw_score, 1), 100)

        matched = job_skills & expanded_resume
        missing = job_skills - expanded_resume

        return final, {
            'resume_skills'  : sorted(resume_skills),
            'job_skills'     : sorted(job_skills),
            'matched_skills' : sorted(matched),
            'missing_skills' : sorted(missing),
            'match_count'    : f"{len(matched)}/{len(job_skills)}",
        }


# DJANGO INTEGRATION

_matcher = SmartJobMatcher()


def extract_years_from_string(exp_string):
    if not exp_string:
        return 0
    matches = re.findall(r'(\d+)', str(exp_string))
    return int(matches[0]) if matches else 0


def calculate_job_match(resume_data, job):
    resume_skills  = list(resume_data.get('skills', []))
    job_skills_str = job.get('skills', '') or ''
    job_desc       = (job.get('description', '') or '') + ' ' + (job.get('requirements', '') or '')

    if len(job_skills_str.strip()) > 5:
        job_skills = [s.strip() for s in job_skills_str.split(',') if s.strip()]
    else:
        job_skills = extract_skills(job_desc.strip()) if job_desc.strip() else []

    return _matcher.calculate_smart_score(resume_skills, job_skills)

# PEHLE (sirf whole stars):
def get_star_rating(score):
    if score >= 80: return 5
    elif score >= 60: return 4
    elif score >= 40: return 3
    elif score >= 20: return 2
    else: return 1

# AB (exact decimal):
def get_star_rating(score):
    return round((score / 100) * 5, 1)

def match_all_jobs(resume_data, jobs_list):
    for job in jobs_list:
        result = calculate_job_match(resume_data, job)
        if isinstance(result, tuple):
            job['match_score'], job['match_breakdown'] = result
        else:
            job['match_score'] = result
        job['star_rating'] = get_star_rating(job['match_score'])
        job['star_fill_pct'] = round(job['star_rating'] / 5 * 100, 1)
    jobs_list.sort(key=lambda x: x['match_score'], reverse=True)
    return jobs_list
