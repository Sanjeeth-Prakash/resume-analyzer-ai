import os
import re
from flask import Flask, request, render_template
import pdfplumber
import pytesseract
from PIL import Image

# --- Configuration and Setup ---
app = Flask(__name__)
try:
    # Ensure this path is correct for your system or that Tesseract is in your system's PATH.
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
except Exception as e:
    print(f"Warning: Tesseract command not found. OCR may not work. Error: {e}")

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- KNOWLEDGE BASE (MASSIVELY EXPANDED) ---
SKILL_GRAPH = {
    # Software Development
    'python': ['python'], 'c/c++': ['c++', 'c'], 'java': ['java'], 'c#': ['c#', '.net'], 'go': ['go', 'golang'],
    'backend': ['backend', 'django', 'spring', 'springboot', 'nodejs', 'express', 'php', 'api', 'microservices', 'rest'],
    'frontend': ['frontend', 'react', 'angular', 'vue', 'javascript', 'css', 'html', 'typescript'],
    'mobile': ['mobile', 'android', 'ios', 'kotlin', 'swift', 'react native', 'flutter', 'xamarin'],
    'database': ['sql', 'mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'nosql'],
    'devops': ['devops', 'ci/cd', 'jenkins', 'docker', 'kubernetes', 'ansible', 'terraform'],
    'cloud': ['aws', 'azure', 'gcp', 'google cloud'],
    'testing': ['testing', 'qa', 'selenium', 'junit', 'pytest', 'quality assurance'],
    'cybersecurity': ['cybersecurity', 'penetration testing', 'infosec', 'siem', 'firewall'],

    # Data & AI
    'data analysis': ['data analysis', 'pandas', 'numpy', 'matplotlib', 'tableau', 'power bi'],
    'machine learning': ['machine learning', 'tensorflow', 'pytorch', 'scikit-learn', 'keras', 'nlp'],
    'data engineering': ['data engineering', 'hadoop', 'spark', 'kafka', 'etl'],

    # Embedded & Systems
    'os fundamentals': ['operating systems', 'os fundamentals', 'linux', 'unix'],
    'kernel programming': ['kernel programming', 'system programming'],
    'device drivers': ['device drivers', 'bsp', 'board support package'],
    'embedded debugging': ['embedded debugging', 'debugging tools', 'jtag', 'gdb'],
    'system-level troubleshooting': ['system-level troubleshooting', 'troubleshooting'],
    'performance optimization': ['performance optimization', 'low-level programming'],

    # Core Engineering Degrees & Related Skills
    'cad': ['cad', 'autocad', 'solidworks', 'catia', 'revit'], 'matlab': ['matlab', 'simulink'],
    'mechanical engineering': ['mechanical engineering', 'thermodynamics', 'fluid mechanics', 'fea', 'ansys'],
    'electrical engineering': ['electrical engineering', 'electronics eng', 'circuit design', 'pcb', 'vlsi', 'verilog', 'vhdl', 'plc'],
    'civil engineering': ['civil engineering', 'structural analysis', 'staad pro', 'etabs'],
    'chemical engineering': ['chemical engineering', 'process simulation', 'aspen hysys'],
    'information technology': ['information technology', 'it', 'information tech'],
    'computer science': ['computer science', 'cs', 'software engineering'],
    'mathematical sciences': ['mathematical sciences', 'mathematics'],

    # Foundational & Business
    'data structures': ['data structures', 'algorithms'], 'system design': ['system design'],
    'project management': ['project management', 'agile', 'scrum', 'jira'],
    'finance': ['finance', 'financial modeling', 'valuation', 'excel', 'vba'],
    'marketing': ['marketing', 'seo', 'sem', 'google analytics', 'social media marketing'],
    'sales': ['sales', 'crm', 'salesforce'],
    'ui/ux': ['ui/ux', 'figma', 'sketch', 'adobe xd', 'user interface', 'user experience'],
    'graphic design': ['graphic design', 'photoshop', 'illustrator', 'indesign'],
    'documentation': ['documentation', 'readme']
}

# --- RESOURCE DATABASE (For the Actionable Preparation Plan) ---
# NOTE: Only actionable, learnable skills are included here. Degree programs are excluded.
RESOURCE_DATABASE = {
    'c/c++': {
        'preparation': "C/C++ is essential for low-level systems and performance-critical applications. Focus on memory management (pointers, malloc/free, new/delete), object-oriented principles in C++, and the Standard Template Library (STL).",
        'projects': ["Implement a custom memory allocator.", "Write a simple shell or command-line interpreter.", "Build a multi-threaded application to understand concurrency."],
        'resources': {"LearnCpp.com": "https://www.learncpp.com/", "GeeksforGeeks C++ Tutorial": "https://www.geeksforgeeks.org/c-plus-plus/"}
    },
    'kernel programming': {
        'preparation': "This is an advanced topic. Start by understanding the difference between user space and kernel space. Learn about system calls, kernel modules, and process scheduling. The Linux kernel is the most common place to start.",
        'projects': ["Write a simple 'Hello World' Linux kernel module.", "Create a basic character device driver.", "Modify a simple scheduler to implement a different scheduling policy."],
        'resources': {"The Linux Kernel Documentation": "https://www.kernel.org/doc/html/latest/", "Linux Device Drivers, 3rd Edition (Online Book)": "https://lwn.net/Kernel/LDD3/"}
    },
    'device drivers': {
        'preparation': "Device drivers are the software that allows the OS to communicate with hardware. Understanding this requires knowledge of both your OS (like Linux) and the hardware you're targeting. Start with simple virtual devices before moving to real hardware.",
        'projects': ["Write a basic keyboard driver for a virtual machine.", "Create a simple driver for a USB device.", "Work with Board Support Packages (BSPs) for a development board like a Raspberry Pi."],
        'resources': {"Linux Device Drivers, 3rd Edition (Online Book)": "https://lwn.net/Kernel/LDD3/", "Writing a Simple Linux Kernel Module (Tutorial)": "https://www.tldp.org/LDP/lkmpg/2.6/html/"}
    },
    'go': {
        'preparation': "Go (Golang) is known for simplicity and high performance, especially in backend systems. Start with the official 'A Tour of Go' to understand its syntax and powerful concurrency model (goroutines).",
        'projects': ["A simple REST API for a to-do list.", "A concurrent web scraper.", "A command-line tool that interacts with a third-party API."],
        'resources': {"Official Go Tour": "https://go.dev/tour/", "Go by Example": "https://gobyexample.com/"}
    },
    'testing': {
        'preparation': "Testing ensures your code works as expected. Learn the three main types: Unit tests (testing one small function), Integration tests (testing how parts work together), and End-to-end tests. Pick a framework like PyTest (Python) or JUnit (Java).",
        'projects': ["Go back to an old project and write unit tests for its core functions.", "Add integration tests for a project that calls an external API."],
        'resources': {"FreeCodeCamp - Software Testing Tutorial": "https://www.freecodecamp.org/news/software-testing-tutorial-beginners-guide/", "Atlassian - Types of Software Testing": "https://www.atlassian.com/continuous-delivery/software-testing/types-of-software-testing"}
    },
    'data structures': {
        'preparation': "This is a fundamental topic for any software role. You MUST understand Arrays, Linked Lists, Stacks, Queues, Trees, Graphs, and Hash Tables. Focus not just on what they are, but WHEN to use each one (time and space complexity).",
        'projects': ["Implement each major data structure from scratch in a language you know.", "Solve problems on LeetCode or HackerRank, specifically focusing on categories like 'Arrays' or 'Trees'."],
        'resources': {"LeetCode": "https://leetcode.com/", "GeeksforGeeks - Data Structures": "https://www.geeksforgeeks.org/data-structures/", "VisuAlgo (Visualizing data structures)": "https://visualgo.net/en"}
    },
    'python': {
        'preparation': "Master core data types, control flow, functions, and object-oriented programming. For internships, strong knowledge of libraries like Pandas and NumPy is a huge advantage.",
        'projects': ["A data analysis project using Pandas on a Kaggle dataset.", "A web scraper using BeautifulSoup or Scrapy.", "A simple web app using Flask or Django."],
        'resources': {"Official Python Tutorial": "https://docs.python.org/3/tutorial/", "Kaggle (for datasets)": "https://www.kaggle.com/datasets"}
    },
    'java': {
        'preparation': "Focus on core Java concepts (OOP, Collections Framework, Exception Handling, Multithreading). For backend roles, learning a framework like Spring Boot is essential.",
        'projects': ["A command-line banking application.", "A simple library management system.", "A REST API using Spring Boot."],
        'resources': {"Baeldung - Spring Boot": "https://www.baeldung.com/spring-boot", "GeeksforGeeks Java Tutorial": "https://www.geeksforgeeks.org/java/"}
    },
    'backend': {
        'preparation': "Backend engineering is about what happens on the server. Focus on APIs (especially REST), databases (SQL vs NoSQL), and authentication. Understand the request/response lifecycle.",
        'projects': ["Build a complete user login system (registration, login, logout) using a framework like Spring Boot or Django.", "Create an e-commerce backend with APIs for products and orders."],
        'resources': {"Roadmap.sh - Backend Developer": "https://roadmap.sh/backend", "FreeCodeCamp - APIs for Beginners": "https://www.freecodecamp.org/news/what-is-an-api-in-english-please/"}
    },
    'cad': {
        'preparation': "For Mechanical/Civil/Aero roles, CAD proficiency is non-negotiable. Master 2D sketching, 3D part modeling, assembly design, and generating engineering drawings. Pick one software (like AutoCAD or SolidWorks) and become an expert.",
        'projects': ["Design a complex mechanical assembly, like a gearbox or a bicycle frame.", "Create a full set of manufacturing drawings for a simple part.", "Model and render a consumer product."],
        'resources': {"SolidWorks Tutorials (Official)": "https://www.solidworks.com/support/solidworks-tutorials", "AutoCAD LinkedIn Learning": "https://www.linkedin.com/learning/topics/autocad"}
    }
}

# --- Core Functions ---
def read_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text(x_tolerance=2) or ""
    return text

def read_image(file_path):
    try:
        return pytesseract.image_to_string(Image.open(file_path))
    except Exception as e:
        return f"Could not read text from image: {e}"

def extract_name(text):
    match = re.search(r'^([A-Z][a-z]+ [A-Z][a-z]+)', text.strip())
    if match: return match.group(1)
    return "Candidate"

def parse_requirements(jd_text):
    return [req.strip() for req in re.split(r'\n|\*|\•|-', jd_text) if len(req.strip()) > 5]

def analyze_requirement_final(requirement, resume_text, skill_graph):
    """The definitive analysis function that understands AND/OR conditions."""
    req_lower = requirement.lower()
    resume_lower = resume_text.lower()
    
    required_skills_on_line = set()
    for canonical_skill, aliases in skill_graph.items():
        for alias in [canonical_skill] + aliases:
            if re.search(r'\b' + re.escape(alias) + r'\b', req_lower):
                required_skills_on_line.add(canonical_skill)

    if not required_skills_on_line:
        return None

    met_skills = set()
    for skill in required_skills_on_line:
        for alias in [skill] + skill_graph.get(skill, []):
             if re.search(r'\b' + re.escape(alias) + r'\b', resume_lower):
                met_skills.add(skill)
                break
    
    is_and_condition = ' and ' in req_lower or '&' in req_lower
    is_or_condition = any(x in req_lower for x in [',', '/', ' or ']) or len(required_skills_on_line) > 2
    
    is_met = False
    if is_and_condition and not is_or_condition:
        is_met = required_skills_on_line.issubset(met_skills)
    else:
        if met_skills:
            is_met = True

    return {"requirement": requirement, "required": sorted(list(required_skills_on_line)), "met": sorted(list(met_skills)), "is_met": is_met}

def generate_feedback_message(score, name):
    score = float(score)
    first_name = name.split(' ')[0]
    if score >= 75:
        return {"message": f"Excellent work, {first_name}! Your profile is a strong match for this role's requirements. Focus on the few unmet areas to become an ideal candidate.", "status": "great"}
    elif score >= 50:
        return {"message": f"Solid foundation, {first_name}. You meet a good number of the requirements. Addressing the key unmet skills will significantly boost your profile.", "status": "good"}
    elif score >= 25:
        return {"message": f"Good start, {first_name}. You meet some requirements, but there are several key areas to focus on. Use this detailed breakdown to bridge the gaps.", "status": "ok"}
    else:
        return {"message": f"Hey {first_name}, this analysis has identified some foundational gaps. The list below is your roadmap to becoming a much stronger candidate for this type of role.", "status": "improvement"}

# --- Flask Routes ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    resume_file = request.files.get('resume_pdf')
    if not resume_file: return "Error: No resume file uploaded."
    resume_filepath = os.path.join(UPLOAD_FOLDER, resume_file.filename)
    resume_file.save(resume_filepath)
    resume_text = read_pdf(resume_filepath)
    os.remove(resume_filepath)

    jd_text = ""
    input_method = request.form.get('jd_input_method')
    if input_method == 'text': jd_text = request.form.get('job_description_text', '')
    elif input_method == 'pdf':
        jd_file = request.files.get('job_description_pdf')
        if jd_file:
            jd_filepath = os.path.join(UPLOAD_FOLDER, jd_file.filename)
            jd_file.save(jd_filepath)
            jd_text = read_pdf(jd_filepath)
            os.remove(jd_filepath)
    elif input_method == 'image':
        jd_file = request.files.get('job_description_image')
        if jd_file:
            jd_filepath = os.path.join(UPLOAD_FOLDER, jd_file.filename)
            jd_file.save(jd_filepath)
            jd_text = read_image(jd_filepath)
            os.remove(jd_filepath)
    if not jd_text.strip(): return "Error: Job description was empty."

    jd_requirements_raw = parse_requirements(jd_text)
    analysis_results = []
    unmet_skills = set()
    for req in jd_requirements_raw:
        result = analyze_requirement_final(req, resume_text, SKILL_GRAPH)
        if result:
            analysis_results.append(result)
            if not result['is_met']:
                for skill in result['required']:
                    if skill not in result['met']:
                        unmet_skills.add(skill)

    met_count = sum(1 for r in analysis_results if r['is_met'])
    total_reqs = len(analysis_results)
    match_score = (met_count / total_reqs) * 100 if total_reqs > 0 else 100

    user_name = extract_name(resume_text)
    feedback = generate_feedback_message(match_score, user_name)
    
    suggestions = {}
    actionable_unmet_skills = {skill for skill in unmet_skills if skill in RESOURCE_DATABASE}
    for skill in sorted(list(actionable_unmet_skills)):
        suggestions[skill] = RESOURCE_DATABASE[skill]
    
    return render_template('index.html',
                           submitted=True,
                           match_score=f"{match_score:.2f}",
                           analysis_results=analysis_results,
                           feedback=feedback,
                           suggestions=suggestions,
                           raw_resume_text=resume_text,
                           raw_jd_text=jd_text)


if __name__ == '__main__':
    app.run(debug=True)