"""
Script to generate the complete 23IT723 DevOps Laboratory Final Project Report (.docx)
Matching the exact Coimbatore Institute of Technology (CIT) format and evaluation guidelines.
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def create_report():
    doc = docx.Document()

    # Set page margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Style definitions
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(12)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)

    # ==========================================
    # COVER PAGE
    # ==========================================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r1 = p_inst.add_run("COIMBATORE INSTITUTE OF TECHNOLOGY\n")
    r1.bold = True
    r1.font.size = Pt(16)
    r2 = p_inst.add_run("(Government Aided Autonomous Institution Affiliated to Anna University)\n\n")
    r2.font.size = Pt(12)
    r2.italic = True

    p_course = doc.add_paragraph()
    p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_c = p_course.add_run("23IT723 – DEVOPS LABORATORY\n")
    r_c.bold = True
    r_c.font.size = Pt(14)
    r_p = p_course.add_run("FINAL MINI PROJECT REPORT\n\n\n")
    r_p.bold = True
    r_p.font.size = Pt(15)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t = p_title.add_run("FLYORA – CLOUD-NATIVE FLIGHT BOOKING SYSTEM\nWITH DEVOPS CI/CD PIPELINE\n\n\n\n")
    r_t.bold = True
    r_t.font.size = Pt(18)
    r_t.font.color.rgb = RGBColor(16, 44, 87)

    p_date = doc.add_paragraph()
    p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_d = p_date.add_run("OCTOBER 2026\n\n\n\n")
    r_d.bold = True
    r_d.font.size = Pt(13)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_sub1 = p_sub.add_run("Submitted by:\n")
    r_sub1.bold = True
    r_sub1.font.size = Pt(12)
    r_sub2 = p_sub.add_run("GOKUL R\n(2303717620521015)\nDEPARTMENT OF INFORMATION TECHNOLOGY\n")
    r_sub2.font.size = Pt(12)

    doc.add_page_break()

    # ==========================================
    # BONAFIDE CERTIFICATE
    # ==========================================
    p_cert_head = doc.add_paragraph()
    p_cert_head.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_c1 = p_cert_head.add_run("COIMBATORE INSTITUTE OF TECHNOLOGY\n")
    r_c1.bold = True
    r_c1.font.size = Pt(15)
    r_c2 = p_cert_head.add_run("(Government Aided Autonomous Institution Affiliated to Anna University)\n\n")
    r_c2.italic = True
    r_c2.font.size = Pt(11)

    r_c3 = p_cert_head.add_run("BONAFIDE CERTIFICATE\n\n")
    r_c3.bold = True
    r_c3.font.size = Pt(14)

    p_cert_body = doc.add_paragraph()
    p_cert_body.paragraph_format.line_spacing = 1.5
    p_cert_body.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_cert_body.add_run(
        "Certified that this project report titled “FLYORA – CLOUD-NATIVE FLIGHT BOOKING SYSTEM WITH DEVOPS CI/CD” "
        "is the bonafide work of GOKUL R (2303717620521015) completed during the academic year 2025-2026 – Semester VII "
        "for the project presentation and laboratory evaluation of 23IT723 – DEVOPS LABORATORY under our supervision.\n\n"
        "Certified that the candidate was examined during the final project laboratory examination.\n\n\n"
    )

    p_rev = doc.add_paragraph()
    p_rev.add_run("Review Members & Faculty In-Charge:\n\n").bold = True
    p_rev.add_run("1. Dr. M. Sangeetha\n   Associate Professor / IT\n\n")
    p_rev.add_run("2. Dr. E. Arul\n   Assistant Professor / IT\n\n\n\n")

    p_sig = doc.add_paragraph()
    p_sig.add_run("Faculty Evaluator I (Signature)                               Faculty Evaluator II (Signature)")
    p_sig.runs[0].bold = True

    doc.add_page_break()

    # ==========================================
    # EVALUATION SCHEME
    # ==========================================
    h_eval = doc.add_heading("23IT723 – DEVOPS LABORATORY\nFINAL MINI PROJECT – EVALUATION SCHEME", level=2)
    h_eval.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in h_eval.runs:
        r.font.size = Pt(13)
        r.font.color.rgb = RGBColor(0, 0, 0)

    p_eval_intro = doc.add_paragraph(
        "The final mini project requires students to integrate major DevOps practices covered in the laboratory. "
        "The project demonstrates practical implementation of version control, collaborative development, Continuous Integration, "
        "containerization, automated configuration/provisioning, and persistent storage with proper execution evidence."
    )
    p_eval_intro.paragraph_format.line_spacing = 1.15

    # Evaluation Scheme Table
    table_eval = doc.add_table(rows=1, cols=4)
    table_eval.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_eval.autofit = False

    hdr_cells = table_eval.rows[0].cells
    hdr_titles = ['S.No.', 'Evaluation Component', 'Key Verification Points', 'Marks']
    col_widths = [Inches(0.6), Inches(2.2), Inches(3.0), Inches(0.7)]

    for idx, title in enumerate(hdr_titles):
        hdr_cells[idx].text = title
        hdr_cells[idx].paragraphs[0].runs[0].bold = True
        set_cell_background(hdr_cells[idx], "2B4C7E")
        hdr_cells[idx].paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
        hdr_cells[idx].width = col_widths[idx]

    eval_data = [
        ('1', 'Problem Definition & Project Planning', 'Problem statement, objectives, requirements, scope, module identification, technology selection and workflow planning.', '10'),
        ('2', 'Git Repository & Version Control', 'Repository creation, meaningful commits, README, .gitignore, remote repository, push/pull/fetch operations and commit history.', '15'),
        ('3', 'Branching, Merging & Collaboration', 'Feature branches, parallel development, merging, conflict handling, branch organization and collaborative workflow.', '10'),
        ('4', 'Application Development & Build', 'Working application/source code, project structure, dependency management, build configuration and successful execution.', '15'),
        ('5', 'Jenkins Continuous Integration', 'Jenkins configuration, source-code integration, automated checkout, build job/pipeline, build execution and console verification.', '15'),
        ('6', 'Docker / Containerization', 'Dockerfile, image creation, container execution, port/configuration handling, application deployment and container verification.', '10'),
        ('7', 'Automation / Configuration Management', 'Ansible playbook/inventory, repeatable container provisioning and successful execution.', '5'),
        ('8', 'Testing & Verification', 'Automated Pytest testing, build verification, error identification, test evidence and corrective action.', '5'),
        ('9', 'Documentation & Technical Presentation', 'Architecture/workflow diagram, commands/configuration, screenshots, results, troubleshooting, conclusion and repository details.', '5'),
        ('10', 'Final Demonstration & Viva-Voce', 'Live demonstration, explanation of implementation, troubleshooting responses and technical understanding.', '10'),
        ('TOTAL', '', '', '100')
    ]

    for row_idx, data in enumerate(eval_data):
        row = table_eval.add_row()
        for c_idx, val in enumerate(data):
            cell = row.cells[c_idx]
            cell.text = val
            cell.width = col_widths[c_idx]
            if data[0] == 'TOTAL':
                if len(cell.paragraphs[0].runs) > 0:
                    cell.paragraphs[0].runs[0].bold = True
                set_cell_background(cell, "EAEAEA")
            elif row_idx % 2 == 1:
                set_cell_background(cell, "F8F9FA")

    doc.add_paragraph("\n")

    # Minimum Evidence Section
    p_ev = doc.add_paragraph()
    p_ev.add_run("Minimum Evidence Submitted:\n").bold = True
    evidence_points = [
        "Project repository URL and comprehensive project README.",
        "Git commit history and branch/merge evidence.",
        "Jenkins job/pipeline configuration (Jenkinsfile) and successful build evidence.",
        "Dockerfile, image build, and running container verification.",
        "Ansible deployment playbook (docker-deploy.yml) and inventory automation.",
        "Pytest automated test suite (test_app.py) passing all functional tests.",
        "Persistent Docker volume (flyora_data) SQLite database verification.",
        "Live demonstration of the complete DevOps automated workflow."
    ]
    for pt in evidence_points:
        doc.add_paragraph(f"• {pt}", style='List Bullet')

    doc.add_page_break()

    # ==========================================
    # TABLE OF CONTENTS
    # ==========================================
    h_toc = doc.add_heading("TABLE OF CONTENTS", level=1)
    h_toc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    for r in h_toc.runs:
        r.font.size = Pt(14)
        r.bold = True
        r.font.color.rgb = RGBColor(0, 0, 0)

    toc_table = doc.add_table(rows=1, cols=3)
    toc_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    toc_table.autofit = False

    t_hdr = toc_table.rows[0].cells
    t_hdr[0].text = 'S.NO.'
    t_hdr[1].text = 'CONTENT'
    t_hdr[2].text = 'PAGE NO.'
    toc_widths = [Inches(0.8), Inches(4.8), Inches(1.0)]

    for idx, c in enumerate(t_hdr):
        c.paragraphs[0].runs[0].bold = True
        c.width = toc_widths[idx]
        set_cell_background(c, "2B4C7E")
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

    toc_items = [
        ('1', 'INTRODUCTION', '05'),
        ('2', 'OBJECTIVES', '05'),
        ('3', 'ABSTRACT', '06'),
        ('4', 'TECHNOLOGY STACK', '06'),
        ('5', 'SYSTEM ARCHITECTURE', '07'),
        ('6', 'MODULE 1 — USER INTERFACE & FLIGHT BOOKING', '08'),
        ('7', 'MODULE 2 — FLASK BACKEND & REST API MANAGEMENT', '09'),
        ('8', 'MODULE 3 — SQLITE DATABASE MANAGEMENT', '10'),
        ('9', 'MODULE 4 — GIT & GITHUB SOURCE CONTROL', '11'),
        ('10', 'MODULE 5 — DOCKER CONTAINERIZATION', '12'),
        ('11', 'MODULE 6 — JENKINS CI/CD PIPELINE', '14'),
        ('12', 'MODULE 7 — AUTOMATED TESTING WITH PYTEST', '15'),
        ('13', 'MODULE 8 — ANSIBLE DEPLOYMENT AUTOMATION', '17'),
        ('14', 'MODULE 9 — PERSISTENT STORAGE (DOCKER VOLUME)', '18'),
        ('15', 'MODULE 10 — ADMIN & PASSENGER MANIFEST MANAGEMENT', '19'),
        ('16', 'MODULE 11 — CI/CD INTEGRATION WORKFLOW', '20'),
        ('17', 'MODULE 12 — APPLICATION & DEPLOYMENT VERIFICATION', '21'),
        ('18', 'RESULTS AND OUTPUT', '23'),
        ('19', 'COMMANDS USED', '23'),
        ('20', 'ADVANTAGES', '27'),
        ('21', 'LIMITATIONS', '27'),
        ('22', 'FUTURE ENHANCEMENTS', '28'),
        ('23', 'CONCLUSION', '28')
    ]

    for item in toc_items:
        row = toc_table.add_row()
        for idx, text in enumerate(item):
            cell = row.cells[idx]
            cell.text = text
            cell.width = toc_widths[idx]

    doc.add_page_break()

    # ==========================================
    # 1. INTRODUCTION & 2. OBJECTIVES
    # ==========================================
    doc.add_heading("1. INTRODUCTION", level=1)
    p_intro = doc.add_paragraph(
        "Flyora is a cloud-native flight booking and aviation management system developed to simplify the process of searching, "
        "booking, and managing domestic and international flights. Designed specifically for the Indian aviation landscape, "
        "the application features an exhaustive database of operational airports across all 28 states and 8 union territories, "
        "transparent Indian Rupee (INR - ₹) fares, realistic airline schedules (IndiGo, Air India, Vistara, Akasa Air, SpiceJet), "
        "interactive seat selection, UPI/RuPay payment authorization, and DigiYatra digital boarding passes.\n\n"
        "The application is engineered using HTML5, CSS3, JavaScript (ES6+), Python, Flask, and SQLite, with Flask serving RESTful "
        "endpoints and SQLite maintaining passenger booking records. To ensure seamless software delivery, the project integrates "
        "industry-standard DevOps practices: Git and GitHub for version control, Jenkins for Continuous Integration and Continuous Deployment (CI/CD), "
        "Docker for containerized packaging, Pytest for automated functional testing, Ansible for configuration management and deployment automation, "
        "and a Docker Volume (flyora_data) for persistent database storage across container lifecycles."
    )
    p_intro.paragraph_format.line_spacing = 1.5
    p_intro.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    doc.add_heading("2. OBJECTIVES", level=1)
    obj_list = [
        "To develop a modern, cloud-native flight booking platform enabling users to search, filter, select seats, and book flights with instant INR fare calculations.",
        "To implement an interactive administrative portal for flight manifests, passenger management, and SQLite database telemetry.",
        "To enforce disciplined version control and collaborative Git workflow with remote tracking on GitHub.",
        "To automate the CI/CD lifecycle using a declarative Jenkins pipeline integrating build, test, and deployment phases.",
        "To containerize the application using Docker, providing a lightweight, portable, and isolated runtime environment.",
        "To implement Pytest automated test suites inside the container to prevent flawed builds from proceeding to production.",
        "To automate application deployment and container configuration using Ansible playbooks (community.docker).",
        "To implement Docker Volume persistent storage ensuring database records remain intact during container recreation."
    ]
    for obj in obj_list:
        p = doc.add_paragraph(f"• {obj}")
        p.paragraph_format.line_spacing = 1.3

    # ==========================================
    # 3. ABSTRACT & 4. TECH STACK
    # ==========================================
    doc.add_heading("3. ABSTRACT", level=1)
    p_abs = doc.add_paragraph(
        "Traditional flight booking architectures often suffer from manual deployment bottlenecks, configuration drifts, and data persistence challenges during container restarts. "
        "The proposed Flyora system addresses these challenges through a unified cloud-native architecture combining an intuitive flight booking frontend with a robust Flask backend and an automated DevOps pipeline. "
        "The application provides rich flight search across all Indian commercial airports, real-time fare computation, DigiYatra-ready boarding passes, and an administrative dashboard for booking oversight. "
        "DevOps automation orchestrates the entire workflow: GitHub acts as the centralized source code repository, Jenkins triggers automated CI/CD builds upon commits, Docker encapsulates the runtime environment, Pytest validates functional API endpoints, Ansible automates container deployment on host port 5001, and a dedicated Docker volume preserves SQLite records. "
        "The complete automated pipeline executes GitHub → Jenkins → Docker Build → Pytest → Ansible → Docker Container → Flask → SQLite, ensuring zero downtime and reliable software release cycles."
    )
    p_abs.paragraph_format.line_spacing = 1.5
    p_abs.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    doc.add_heading("4. TECHNOLOGY STACK", level=1)
    table_tech = doc.add_table(rows=1, cols=3)
    table_tech.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_tech.autofit = False

    t_tech_hdr = table_tech.rows[0].cells
    t_tech_hdr[0].text = 'Technology'
    t_tech_hdr[1].text = 'Version'
    t_tech_hdr[2].text = 'Purpose'
    tech_widths = [Inches(2.0), Inches(1.5), Inches(3.1)]

    for idx, c in enumerate(t_tech_hdr):
        c.paragraphs[0].runs[0].bold = True
        c.width = tech_widths[idx]
        set_cell_background(c, "2B4C7E")
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

    tech_data = [
        ('HTML5', '5.0', 'Web page structure and semantic layout'),
        ('CSS3 / Glassmorphism', '3.0', 'Modern responsive styling, dark theme, animations'),
        ('JavaScript', 'ES6+', 'Dynamic UI controller, live autocomplete, flight radar'),
        ('Python', '3.11 / 3.14', 'Backend programming and API engine'),
        ('Flask', '3.1.3', 'RESTful backend web framework'),
        ('SQLite', '3.x', 'Embedded relational database for booking records'),
        ('Git', '2.54.0', 'Distributed version control system'),
        ('GitHub', 'Cloud', 'Centralized remote code repository and trigger'),
        ('Jenkins', '2.x', 'CI/CD automation server and declarative pipeline'),
        ('Docker', '29.x', 'Application containerization and isolation'),
        ('Pytest', '9.1.1', 'Automated unit and integration testing framework'),
        ('Ansible', '2.10+', 'Automated container provisioning and configuration'),
        ('community.docker', '1.2+', 'Ansible Docker module for container lifecycle')
    ]

    for item in tech_data:
        row = table_tech.add_row()
        for idx, text in enumerate(item):
            cell = row.cells[idx]
            cell.text = text
            cell.width = tech_widths[idx]

    doc.add_page_break()

    # ==========================================
    # 5. SYSTEM ARCHITECTURE
    # ==========================================
    doc.add_heading("5. SYSTEM ARCHITECTURE", level=1)
    p_arch = doc.add_paragraph(
        "The system architecture incorporates an automated DevOps lifecycle from code creation to containerized deployment:\n"
    )
    p_arch.paragraph_format.line_spacing = 1.3

    arch_steps = [
        ("Development: ", "Developers create and test the Flyora flight booking application and DevOps scripts locally."),
        ("Source Code Management: ", "All source code, Dockerfile, Jenkinsfile, test files, and Ansible playbooks are versioned with Git."),
        ("GitHub Repository: ", "The source code is committed and pushed to the centralized GitHub repository (Gokul7176/prepare)."),
        ("Jenkins Trigger: ", "Jenkins fetches the latest codebase from GitHub and initializes the declarative CI/CD pipeline."),
        ("Docker Build Stage: ", "Jenkins constructs the Docker image 'flyora-flight-booking-ci' packaging Flask, Python dependencies, and frontend assets."),
        ("Automated Testing Stage: ", "Jenkins executes Pytest test suites inside the Docker container to validate endpoints and health status."),
        ("Ansible Deployment Stage: ", "Upon test success, Jenkins invokes the Ansible playbook 'docker-deploy.yml' to deploy the container."),
        ("Container Configuration: ", "Ansible configures port mapping (5001:5000), restart policy (always), and persistent volume mounting (flyora_data:/app/data)."),
        ("Application Execution: ", "The Docker container executes Flask backend serving HTTP requests on port 5001."),
        ("Persistent Storage: ", "SQLite database transactions are persisted in the Docker volume, preventing data loss during rebuilds."),
        ("User & Admin Interaction: ", "Passengers search and book flights via the web UI; administrators monitor passenger manifests at /admin.")
    ]

    for title, desc in arch_steps:
        p = doc.add_paragraph()
        r1 = p.add_run(f"• {title}")
        r1.bold = True
        p.add_run(desc)
        p.paragraph_format.line_spacing = 1.3

    # ==========================================
    # MODULES 1 TO 12
    # ==========================================
    modules = [
        ("MODULE 1 — USER INTERFACE & FLIGHT BOOKING", 
         "This module provides the responsive frontend of Flyora. Features include real-time Indian airport autocomplete (DEL, BOM, BLR, MAA, CCU, HYD, AYJ, GOI, GOX, SXR, etc.), date pickers, class selection, live price calculations in INR (₹), interactive seat maps, and DigiYatra boarding passes.",
         "Technologies: HTML5, CSS3, JavaScript (ES6+)"),

        ("MODULE 2 — FLASK BACKEND & REST API MANAGEMENT",
         "Handles business logic, routing, and database communication. Exposes endpoints: GET / (serves UI), GET /health (health check for CI/CD probes), POST /api/book (creates booking and persists to SQLite), GET /api/bookings (retrieves all booking records), and GET /admin (admin dashboard).",
         "Technology: Python 3.11 with Flask 3.1.3"),

        ("MODULE 3 — SQLITE DATABASE MANAGEMENT",
         "Provides lightweight relational data persistence. Stores passenger details, PNR, flight numbers, airline, route, departure timestamp, seat allocation, fare amount, and payment status in data/flights.db. Automatically creates tables upon application startup.",
         "Technology: SQLite 3 (Location: /app/data/flights.db)"),

        ("MODULE 4 — GIT & GITHUB SOURCE CONTROL",
         "Manages version history and collaborative workflows. Tracks changes across commits with descriptive messages. Connects local workspace to remote GitHub repository (https://github.com/Gokul7176/prepare.git), enabling automated Jenkins pipeline checkout.",
         "Technologies: Git 2.54 and GitHub Cloud"),

        ("MODULE 5 — DOCKER CONTAINERIZATION",
         "Packages the application into an isolated container using a multi-layer Dockerfile. Sets up working directory /app, installs dependencies from requirements.txt, configures persistent volume /app/data, exposes port 5000, and executes python app.py.",
         "Docker Image: flyora-flight-booking-ci | Container: flyora-app-ansible | Port: 5001:5000"),

        ("MODULE 6 — JENKINS CI/CD PIPELINE",
         "Automates the continuous integration and delivery pipeline using a declarative Jenkinsfile. Coordinates sequential stages: SCM Checkout → Docker Build → Pytest Test Execution → Ansible Deployment → Health Verification.",
         "Technology: Jenkins 2.x (Accessed on http://localhost:9091)"),

        ("MODULE 7 — AUTOMATED TESTING WITH PYTEST",
         "Executes automated unit tests via test_app.py before deployment. Tests verify home route status (200), health check endpoint (/health), booking creation with authentic 6-character PNR generation, booking retrieval, and admin dashboard rendering.",
         "Test Command: docker run --rm flyora-flight-booking-ci python -m pytest test_app.py -v (Result: 5 passed)"),

        ("MODULE 8 — ANSIBLE DEPLOYMENT AUTOMATION",
         "Automates container deployment using Ansible playbook docker-deploy.yml. Configures container name (flyora-app-ansible), image (flyora-flight-booking-ci), published ports (5001:5000), restart policy (always), and volume mounts (flyora_data:/app/data).",
         "Technology: Ansible with community.docker module"),

        ("MODULE 9 — PERSISTENT STORAGE (DOCKER VOLUME)",
         "Decouples data persistence from the container lifecycle using Docker Volume 'flyora_data' mounted to '/app/data'. Ensures that passenger booking records and SQLite databases remain intact even when application containers are upgraded or recreated.",
         "Volume Configuration: flyora_data:/app/data"),

        ("MODULE 10 — ADMIN & PASSENGER MANIFEST MANAGEMENT",
         "Provides an intuitive administrative dashboard at http://localhost:5001/admin. Allows airline administrators to view real-time booking statistics, total revenue generated in INR (₹), passenger manifests, seat assignments, and database storage telemetry.",
         "Endpoint: http://localhost:5001/admin"),

        ("MODULE 11 — CI/CD INTEGRATION WORKFLOW",
         "Integrates all DevOps tools into a single automated pipeline. Every Git push to GitHub triggers Jenkins to build the Docker image, run Pytest validation, invoke Ansible container deployment, and perform health check verification with zero manual intervention.",
         "Workflow: GitHub → Jenkins → Docker Build → Pytest → Ansible → Docker Volume → Live System"),

        ("MODULE 12 — APPLICATION & DEPLOYMENT VERIFICATION",
         "Verifies system integrity post-deployment across container status (docker ps), port reachability (curl http://localhost:5001/health), database inspection (docker exec sqlite3 query), volume inspection (docker volume inspect), and browser-based flight bookings.",
         "Verification Result: Docker Build SUCCESS | Pytest 5 PASSED | Ansible failed=0 | Pipeline SUCCESS")
    ]

    for title, desc, tech in modules:
        doc.add_heading(title, level=2)
        p = doc.add_paragraph(desc)
        p.paragraph_format.line_spacing = 1.3
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_tech = doc.add_paragraph()
        r_t = p_tech.add_run(f"Configuration: {tech}")
        r_t.italic = True
        r_t.bold = True

    doc.add_page_break()

    # ==========================================
    # RESULTS AND OUTPUT
    # ==========================================
    doc.add_heading("18. RESULTS AND OUTPUT", level=1)
    p_res = doc.add_paragraph(
        "The implemented Flyora Cloud-Native Flight Booking System was successfully built, tested, and deployed using automated DevOps practices. The system achieves:\n"
    )
    p_res.paragraph_format.line_spacing = 1.3
    res_items = [
        "Interactive flight search across 70+ commercial and regional Indian airports.",
        "Accurate fare calculations in Indian Rupees (INR - ₹) with authentic airline schedules.",
        "Interactive seat maps with real-time seat assignment and instant UPI QR payment simulation.",
        "DigiYatra-compliant digital boarding pass generation with 2D barcode formatting.",
        "Robust Flask REST API with SQLite database persistence under data/flights.db.",
        "Multi-layer Docker containerization resulting in a lightweight, self-contained application image.",
        "Automated Pytest testing verifying 100% test pass rate across 5 test suites.",
        "Declarative Jenkins CI/CD pipeline achieving automated build, test, and deployment.",
        "Ansible playbook execution providing idempotent, repeatable container provisioning.",
        "Persistent Docker Volume (flyora_data) ensuring data retention across container lifecycles."
    ]
    for r in res_items:
        doc.add_paragraph(f"✓ {r}", style='List Bullet')

    # ==========================================
    # COMMANDS USED
    # ==========================================
    doc.add_heading("19. COMMANDS USED", level=1)

    cmds = [
        ("1. Docker Environment Commands", [
            ("Check running containers", "docker ps"),
            ("Check all containers", "docker ps -a"),
            ("Start Ansible container lab", "docker start ansible-docker-lab"),
            ("Start Jenkins automation server", "docker start jenkins")
        ]),
        ("2. Docker Image Build & Container Execution", [
            ("Build application Docker image", "docker build -t flyora-flight-booking-ci ."),
            ("Create persistent Docker volume", "docker volume create flyora_data"),
            ("Run container with volume and port mapping", "docker run -d --name flyora-app-ansible -p 5001:5000 -v flyora_data:/app/data --restart always flyora-flight-booking-ci")
        ]),
        ("3. Automated Testing (Pytest)", [
            ("Run tests inside Docker container", "docker run --rm flyora-flight-booking-ci python -m pytest test_app.py -v"),
            ("Run tests locally in development environment", "python -m pytest test_app.py -v")
        ]),
        ("4. Ansible Deployment Playbook Commands", [
            ("Execute Ansible playbook from lab container", "docker exec ansible-docker-lab ansible-playbook -i /inventory.ini /docker-deploy.yml"),
            ("Execute Ansible playbook locally", "ansible-playbook -i inventory.ini docker-deploy.yml"),
            ("View deployed playbook configuration", "cat docker-deploy.yml")
        ]),
        ("5. Persistent Volume & SQLite Database Verification", [
            ("List Docker volumes", "docker volume ls"),
            ("Inspect persistent volume", "docker volume inspect flyora_data"),
            ("Query SQLite booking records inside container", "docker exec flyora-app-ansible python -c \"import sqlite3; c=sqlite3.connect('data/flights.db'); print(c.execute('SELECT * FROM bookings').fetchall()); c.close()\""),
            ("Verify SQLite database tables", "docker exec flyora-app-ansible python -c \"import sqlite3; c=sqlite3.connect('data/flights.db'); print(c.execute(\\\"SELECT name FROM sqlite_master WHERE type='table'\\\").fetchall()); c.close()\"")
        ]),
        ("6. Git & GitHub Source Code Commands", [
            ("Initialize Git repository", "git init"),
            ("Check repository status", "git status"),
            ("Stage all files", "git add ."),
            ("Commit changes with message", "git commit -m \"Finalize Flyora Cloud-Native Flight Booking System CI/CD Project\""),
            ("Set remote repository", "git remote add origin https://github.com/Gokul7176/prepare.git"),
            ("Push commits to remote master branch", "git push -u origin master")
        ])
    ]

    for section_title, cmd_list in cmds:
        doc.add_heading(section_title, level=2)
        for label, cmd_text in cmd_list:
            p_lbl = doc.add_paragraph()
            p_lbl.add_run(f"{label}:\n").bold = True
            p_cmd = doc.add_paragraph(cmd_text)
            p_cmd.paragraph_format.left_indent = Inches(0.4)
            p_cmd.runs[0].font.name = 'Consolas'
            p_cmd.runs[0].font.size = Pt(10)
            p_cmd.runs[0].font.color.rgb = RGBColor(30, 30, 30)

    # ==========================================
    # 20. ADVANTAGES & 21. LIMITATIONS
    # ==========================================
    doc.add_heading("20. ADVANTAGES", level=1)
    adv_points = [
        "End-to-End Automation: Eliminates manual build, test, and deployment errors through Jenkins and Ansible.",
        "Zero Downtime Deployment: Automated container recreation with restart policies ensures high availability.",
        "Persistent Data Safety: Decoupled Docker volumes safeguard SQLite passenger manifests from container restarts.",
        "Comprehensive Test Coverage: Automated Pytest gates ensure code quality before container deployment.",
        "Realistic Aviation Architecture: Supports 70+ Indian airports, DGCA baggage norms, and DigiYatra boarding passes.",
        "Lightweight & Resource-Efficient: Containerized Python 3.11 environment runs seamlessly across local and cloud environments."
    ]
    for pt in adv_points:
        doc.add_paragraph(f"• {pt}", style='List Bullet')

    doc.add_heading("21. LIMITATIONS", level=1)
    lim_points = [
        "The current implementation utilizes SQLite for embedded storage; high-traffic production would benefit from PostgreSQL or MySQL clusters.",
        "Payment gateways operate in simulated sandbox mode rather than live banking APIs.",
        "The continuous integration pipeline is currently hosted in a local lab environment rather than a multi-node Kubernetes cluster."
    ]
    for pt in lim_points:
        doc.add_paragraph(f"• {pt}", style='List Bullet')

    # ==========================================
    # 22. FUTURE ENHANCEMENTS & 23. CONCLUSION
    # ==========================================
    doc.add_heading("22. FUTURE ENHANCEMENTS", level=1)
    enh_points = [
        "Kubernetes (K8s) Orchestration: Deploying Flyora pods with Helm charts and Horizontal Pod Autoscalers (HPA).",
        "Cloud Migration: Deploying the containerized workflow on AWS Elastic Container Service (ECS) or Google Kubernetes Engine (GKE).",
        "Live Payment Gateway: Integrating Razorpay and PayU webhooks for real-time INR transaction settlement.",
        "Monitoring & Observability: Integrating Prometheus and Grafana dashboards for container resource metrics and HTTP request latency."
    ]
    for pt in enh_points:
        doc.add_paragraph(f"• {pt}", style='List Bullet')

    doc.add_heading("23. CONCLUSION", level=1)
    p_conc = doc.add_paragraph(
        "The Flyora Cloud-Native Flight Booking System successfully demonstrates the seamless integration of a modern, "
        "responsive web application with comprehensive DevOps practices. By implementing an automated pipeline spanning "
        "Git, GitHub, Jenkins, Docker, Pytest, Ansible, and Docker Volumes, the project eliminates manual operational bottlenecks "
        "and ensures predictable, test-validated application delivery.\n\n"
        "The application provides rich flight search, dynamic INR fare computation, seat selection, and DigiYatra boarding pass generation, "
        "while the administrative portal facilitates real-time passenger manifest tracking. The successful verification of the CI/CD pipeline "
        "validates the core DevOps objectives outlined for the 23IT723 DevOps Laboratory, establishing a scalable, repeatable, and "
        "production-ready software engineering workflow."
    )
    p_conc.paragraph_format.line_spacing = 1.5
    p_conc.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # Save document
    output_path = "c:\\Users\\ELCOT\\Downloads\\devops cat 001\\Flyora_DevOps_Final_Project_Report.docx"
    doc.save(output_path)
    print(f"Project Report successfully generated at: {output_path}")

if __name__ == '__main__':
    create_report()
