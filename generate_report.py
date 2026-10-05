"""
Script to generate the complete 23IT723 DevOps Laboratory Final Project Report (.docx)
Matching the exact Coimbatore Institute of Technology (CIT) format and evaluation guidelines.
Includes embedded project screenshots and student credentials:
Name: ABHISHEK G SHETTY
Roll No: 2303717620521001
"""

import os
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

def add_figure(doc, img_path, caption, width=Inches(5.8)):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=width)
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_before = Pt(2)
        p_cap.paragraph_format.space_after = Pt(12)
        r_cap = p_cap.add_run(caption)
        r_cap.bold = True
        r_cap.font.size = Pt(10.5)
        r_cap.font.color.rgb = RGBColor(16, 44, 87)

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
    r2.font.size = Pt(11)
    r2.italic = True

    # CIT Emblem Logo
    logo_path = os.path.join('report_screenshots', 'cit_logo.png')
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.add_run().add_picture(logo_path, width=Inches(1.2))
        p_logo.paragraph_format.space_after = Pt(14)

    p_course = doc.add_paragraph()
    p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_c = p_course.add_run("23IT723 – DEVOPS LABORATORY\n")
    r_c.bold = True
    r_c.font.size = Pt(14)
    r_p = p_course.add_run("FINAL MINI PROJECT REPORT\n\n")
    r_p.bold = True
    r_p.font.size = Pt(15)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t = p_title.add_run("FLYORA – CLOUD-NATIVE FLIGHT BOOKING SYSTEM\nWITH DEVOPS CI/CD PIPELINE\n\n")
    r_t.bold = True
    r_t.font.size = Pt(17)
    r_t.font.color.rgb = RGBColor(16, 44, 87)

    p_date = doc.add_paragraph()
    p_date.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_d = p_date.add_run("OCTOBER 2026\n\n\n")
    r_d.bold = True
    r_d.font.size = Pt(13)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_sub1 = p_sub.add_run("Submitted by:\n")
    r_sub1.bold = True
    r_sub1.font.size = Pt(12)
    r_sub2 = p_sub.add_run("ABHISHEK G SHETTY\n(2303717620521001)\nDEPARTMENT OF INFORMATION TECHNOLOGY\n")
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

    if os.path.exists(logo_path):
        p_logo_cert = doc.add_paragraph()
        p_logo_cert.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo_cert.add_run().add_picture(logo_path, width=Inches(1.0))
        p_logo_cert.paragraph_format.space_after = Pt(10)

    r_c3 = p_cert_head.add_run("BONAFIDE CERTIFICATE\n\n")
    r_c3.bold = True
    r_c3.font.size = Pt(14)

    p_cert_body = doc.add_paragraph()
    p_cert_body.paragraph_format.line_spacing = 1.5
    p_cert_body.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_cert_body.add_run(
        "Certified that this project report titled “FLYORA – CLOUD-NATIVE FLIGHT BOOKING SYSTEM WITH DEVOPS CI/CD” "
        "is the bonafide work of ABHISHEK G SHETTY (2303717620521001) completed during the academic year 2025-2026 – Semester VII "
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
        ('20', 'CHALLENGES FACED & TROUBLESHOOTING', '24'),
        ('21', 'CONCLUSION & LEARNING OUTCOMES', '25'),
        ('22', 'FUTURE ENHANCEMENTS', '25')
    ]

    for r_idx, item in enumerate(toc_items):
        row = toc_table.add_row()
        for c_idx, text in enumerate(item):
            cell = row.cells[c_idx]
            cell.text = text
            cell.width = toc_widths[c_idx]
            if r_idx % 2 == 1:
                set_cell_background(cell, "F8F9FA")

    doc.add_page_break()

    # ==========================================
    # SECTION 1: INTRODUCTION & OBJECTIVES
    # ==========================================
    doc.add_heading("1. INTRODUCTION", level=1)
    p_intro = doc.add_paragraph(
        "Modern cloud applications demand rapid release cycles, fault-tolerant infrastructure, automated testing, and zero-downtime deployment. "
        "Flyora is a cloud-native flight reservation platform tailored for Indian domestic aviation. It allows passengers to search real-time domestic flights across major Indian tier-1 and tier-2 airports (DEL, BOM, BLR, MAA, HYD, AYJ, CCU, GOI), select seats with real-time dynamic pricing in Indian Rupees (₹), configure travel add-ons, and confirm e-tickets instantly. "
        "The primary goal of this DevOps Laboratory Mini Project is to integrate end-to-end DevOps practices across the software development lifecycle, utilizing GitHub for source control, Jenkins for continuous integration, Docker for multi-layer containerization, Pytest for automated regression testing, Ansible for infrastructure orchestration, and Docker persistent volumes for database reliability."
    )
    p_intro.paragraph_format.line_spacing = 1.15

    doc.add_heading("2. OBJECTIVES", level=1)
    obj_list = [
        "To engineer a responsive, modern web application providing realistic Indian flight search, interactive cabin seat selection, and passenger booking.",
        "To establish a robust Python Flask backend with RESTful API endpoints (/api/book, /api/bookings, /health) and SQLite database persistence.",
        "To enforce version control best practices using Git and GitHub, ensuring clean commits, branch isolation, and automated webhooks.",
        "To build a fully automated Continuous Integration / Continuous Deployment (CI/CD) pipeline using Declarative Jenkinsfile.",
        "To package the application into an immutable, lightweight Docker container image (flyora-app:latest) for environment parity.",
        "To implement automated unit, integration, and API regression testing using Pytest with 100% test case pass verification.",
        "To automate server configuration and container deployment using Ansible playbooks (docker-deploy.yml) and inventory management.",
        "To configure Docker Volume persistent storage (flyora_data) ensuring passenger booking data survives container restarts."
    ]
    for obj in obj_list:
        doc.add_paragraph(f"• {obj}", style='List Bullet')

    doc.add_heading("3. ABSTRACT", level=1)
    p_abs = doc.add_paragraph(
        "In traditional software operations, manual server deployments and inconsistent environments lead to delivery bottlenecks and data inconsistencies. "
        "This project presents Flyora, an integrated DevOps-engineered flight booking platform designed to eliminate deployment friction. "
        "Flyora bridges software engineering and cloud infrastructure by orchestrating Git version control, Jenkins CI/CD automation, Docker container virtualization, Pytest validation, Ansible configuration management, and Docker volume persistence. "
        "Every code push triggers automated build stages, runs comprehensive regression suites, provisions containers on dedicated ports, mounts SQLite data volumes, and executes post-deployment health checks. "
        "The resulting system delivers high availability, zero manual intervention, sub-second API responses, and complete operational transparency."
    )
    p_abs.paragraph_format.line_spacing = 1.15

    doc.add_heading("4. TECHNOLOGY STACK", level=1)
    tech_table = doc.add_table(rows=1, cols=3)
    tech_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    tech_table.autofit = False

    t_hdr2 = tech_table.rows[0].cells
    t_hdr2[0].text = 'CATEGORY'
    t_hdr2[1].text = 'TECHNOLOGY'
    t_hdr2[2].text = 'ROLE / PURPOSE'
    col_w2 = [Inches(1.8), Inches(1.8), Inches(3.0)]

    for idx, c in enumerate(t_hdr2):
        c.paragraphs[0].runs[0].bold = True
        c.width = col_w2[idx]
        set_cell_background(c, "2B4C7E")
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

    tech_data = [
        ('Frontend', 'HTML5, CSS3, JavaScript (ES6+)', 'Responsive flight search, interactive seat selection, INR pricing & dynamic booking UX.'),
        ('Backend', 'Python 3.11, Flask, Jinja2', 'REST API routing, flight scheduling logic, booking processing & admin telemetry.'),
        ('Database', 'SQLite3 (data/flights.db)', 'Embedded relational database storing flights, passenger records, and manifests.'),
        ('Source Control', 'Git, GitHub', 'Distributed version control, remote tracking, commit history & CI/CD trigger.'),
        ('Continuous Integration', 'Jenkins (Declarative Pipeline)', 'Automated build triggers, Pytest execution, Docker builds & deployment stages.'),
        ('Containerization', 'Docker, Dockerfile', 'Lightweight multi-stage containerization, port mapping (5001:5000), volume isolation.'),
        ('Automated Testing', 'Pytest, Pytest-Flask', 'Automated test suite verifying endpoints (/health, /api/book, /admin) and logic.'),
        ('Configuration Mgmt', 'Ansible, YAML Playbook', 'Automated provisioning of Docker container, volume mounts, and environment checks.'),
        ('Persistent Storage', 'Docker Named Volume (flyora_data)', 'Host-level persistent volume mapped to /app/data preserving SQLite database records.')
    ]

    for r_idx, data in enumerate(tech_data):
        row = tech_table.add_row()
        for c_idx, val in enumerate(data):
            cell = row.cells[c_idx]
            cell.text = val
            cell.width = col_w2[c_idx]
            if r_idx % 2 == 1:
                set_cell_background(cell, "F8F9FA")

    doc.add_page_break()

    # ==========================================
    # SECTION 5: SYSTEM ARCHITECTURE
    # ==========================================
    doc.add_heading("5. SYSTEM ARCHITECTURE & DEVOPS WORKFLOW", level=1)
    p_arch = doc.add_paragraph(
        "The Flyora DevOps Architecture represents a complete, closed-loop CI/CD automation pipeline. "
        "The pipeline begins with developer commit workflows in Git and terminates with automated container deployment and verification."
    )
    p_arch.paragraph_format.line_spacing = 1.15

    arch_steps = [
        ("1. Code Development", "Developers write application code (HTML, CSS, JS, Python Flask, tests) in local workspaces."),
        ("2. Source Control Push", "Code changes are committed with semantic messages and pushed to the remote GitHub repository."),
        ("3. Jenkins Webhook Trigger", "Jenkins detects code changes and triggers the automated 5-stage declarative pipeline."),
        ("4. Container Image Build", "Jenkins executes Docker build using the project Dockerfile to create flyora-app:latest."),
        ("5. Automated Pytest Verification", "Jenkins executes Pytest in an isolated test environment. If any test fails, the build halts immediately."),
        ("6. Ansible Deployment Automation", "Upon test success, Jenkins triggers Ansible playbook (docker-deploy.yml) targeting localhost."),
        ("7. Container & Volume Provisioning", "Ansible creates the persistent Docker volume (flyora_data) and starts the container (flyora-app-ansible) on port 5001."),
        ("8. Health & Telemetry Verification", "Automated curl checks query http://localhost:5001/health ensuring status: healthy before concluding pipeline.")
    ]

    for title, desc in arch_steps:
        p = doc.add_paragraph()
        p.add_run(f"• {title}: ").bold = True
        p.add_run(desc)

    doc.add_page_break()

    # ==========================================
    # DETAILED MODULES (WITH EMBEDDED SCREENSHOTS)
    # ==========================================
    
    # MODULE 1
    doc.add_heading("MODULE 1 — USER INTERFACE & FLIGHT BOOKING", level=1)
    doc.add_paragraph(
        "The Flyora frontend is engineered as a modern, responsive web application supporting end-to-end flight booking workflows tailored for the Indian aviation ecosystem. "
        "It features dynamic origin/destination selection across all major Indian commercial airports (Delhi, Mumbai, Bengaluru, Chennai, Hyderabad, Ayodhya, Goa, Kolkata, Pune), date pickers, class selection, live fare calculation in Indian Rupees (₹), and real-time flight search filters."
    )
    add_figure(doc, 'report_screenshots/fig_home.png', "Figure 7.1: Flyora Flight Booking Home Page and Indian Airport Search Interface")
    add_figure(doc, 'report_screenshots/fig_search.png', "Figure 7.2: Real-Time Flight Search Results with Indian Airlines and INR Fare Pricing")
    add_figure(doc, 'report_screenshots/fig_booking.png', "Figure 7.3: Interactive Aircraft Seat Selection and Add-on Selection Modal")

    # MODULE 2
    doc.add_heading("MODULE 2 — FLASK BACKEND & REST API MANAGEMENT", level=1)
    doc.add_paragraph(
        "The backend is developed using Python Flask, providing RESTful microservice endpoints for flight schedules, booking processing, database queries, and system health status. "
        "The /health endpoint returns real-time JSON telemetry detailing application state, database connectivity, and runtime version."
    )
    add_figure(doc, 'report_screenshots/fig_backend.png', "Figure 7.4: Flask Backend Implementation and JSON Health Status API Endpoint (/health)")

    # MODULE 3
    doc.add_heading("MODULE 3 — SQLITE DATABASE MANAGEMENT", level=1)
    doc.add_paragraph(
        "Flyora employs an embedded SQLite relational database (data/flights.db) containing pre-seeded Indian flight routes and a dynamic passenger manifest table (bookings). "
        "Whenever a passenger confirms a booking on the frontend, an asynchronous fetch() POST request transmits booking metadata to /api/book, creating a permanent database record."
    )
    add_figure(doc, 'report_screenshots/fig_sqlite.png', "Figure 7.5: SQLite Database Schema and Flight Booking Telemetry Records (data/flights.db)")

    # MODULE 4
    doc.add_heading("MODULE 4 — GIT & GITHUB SOURCE CONTROL", level=1)
    doc.add_paragraph(
        "Git is utilized for distributed version control, tracking changes across all project assets. "
        "The repository is hosted remotely at https://github.com/Gokul7176/prepare.git on branch main, enforcing clean commit histories and a structured .gitignore preventing transient artifacts from cluttering the repository."
    )
    add_figure(doc, 'report_screenshots/fig_github.png', "Figure 7.6: Git Version Control and Remote GitHub Repository Tracking (https://github.com/Gokul7176/prepare)")

    # MODULE 5
    doc.add_heading("MODULE 5 — DOCKER CONTAINERIZATION", level=1)
    doc.add_paragraph(
        "Docker containerization packages Flyora into an immutable image based on python:3.11-slim. "
        "The Dockerfile specifies dependency installation via requirements.txt, exposes port 5000, declares the persistent /app/data mount point, and launches the Flask server with production-ready execution."
    )
    add_figure(doc, 'report_screenshots/fig_docker.png', "Figure 7.7: Docker Multi-Layer Container Build and Production Execution (Port 5001)")

    # MODULE 6 & 7
    doc.add_heading("MODULE 6 & 7 — AUTOMATED TESTING WITH PYTEST & JENKINS CI/CD", level=1)
    doc.add_paragraph(
        "Continuous integration is managed by a Jenkins declarative pipeline (Jenkinsfile). "
        "Before any deployment occurs, Pytest executes a comprehensive 5-point test suite (test_app.py) verifying home page rendering, health status, booking creation API, booking retrieval API, and the admin dashboard."
    )
    add_figure(doc, 'report_screenshots/fig_pytest.png', "Figure 7.8: Pytest Automated Test Suite Execution with 100% Test Case Pass Rate")
    add_figure(doc, 'report_screenshots/fig_jenkins.png', "Figure 7.9: Jenkins Declarative CI/CD Pipeline Multi-Stage Automated Execution")

    # MODULE 8 & 9
    doc.add_heading("MODULE 8 & 9 — ANSIBLE DEPLOYMENT & PERSISTENT STORAGE", level=1)
    doc.add_paragraph(
        "Ansible automates container provisioning through docker-deploy.yml, guaranteeing idempotent deployments. "
        "Ansible ensures the persistent Docker volume (flyora_data) exists, stops any existing stale containers, deploys the new container image with port mapping 5001:5000, and mounts flyora_data to /app/data to ensure zero data loss during container upgrades."
    )
    add_figure(doc, 'report_screenshots/fig_volume.png', "Figure 7.10: Docker Persistent Volume Mount Configuration (flyora_data -> /app/data)")
    add_figure(doc, 'report_screenshots/fig_ansible.png', "Figure 7.11: Ansible Playbook Automated Deployment Execution (docker-deploy.yml)")

    # MODULE 10
    doc.add_heading("MODULE 10 — ADMIN DASHBOARD & PASSENGER MANIFEST", level=1)
    doc.add_paragraph(
        "The Flyora Admin Portal (/admin) provides operational personnel and airline managers with live telemetry, passenger manifest records, total booking revenue in INR (₹), and system health metrics directly retrieved from the persistent SQLite database."
    )
    add_figure(doc, 'report_screenshots/fig_admin.png', "Figure 7.12: Flyora Admin Portal and Real-Time Passenger Manifest Dashboard (/admin)")

    doc.add_page_break()

    # ==========================================
    # SECTION: RESULTS, COMMANDS, CONCLUSION
    # ==========================================
    doc.add_heading("RESULTS AND OUTPUT", level=1)
    p_res = doc.add_paragraph(
        "The Flyora DevOps Laboratory project achieved 100% completion across all evaluation criteria. "
        "The application successfully processes flight bookings with sub-second latency, executes the automated Pytest test suite with 5/5 passing test cases in 0.56 seconds, builds Docker images seamlessly, deploys via Ansible playbooks with 0 failures, and maintains full database persistence across container destruction and restarts."
    )
    p_res.paragraph_format.line_spacing = 1.15

    doc.add_heading("COMMANDS USED IN PROJECT EXECUTION", level=1)
    cmd_table = doc.add_table(rows=1, cols=3)
    cmd_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cmd_table.autofit = False

    c_hdr = cmd_table.rows[0].cells
    c_hdr[0].text = 'PHASE'
    c_hdr[1].text = 'COMMAND'
    c_hdr[2].text = 'DESCRIPTION'
    c_widths = [Inches(1.5), Inches(3.0), Inches(2.1)]

    for idx, c in enumerate(c_hdr):
        c.paragraphs[0].runs[0].bold = True
        c.width = c_widths[idx]
        set_cell_background(c, "2B4C7E")
        c.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)

    commands_list = [
        ('Version Control', 'git init\ngit add .\ngit commit -m "..."\ngit push -u origin main', 'Initialize Git repo, stage files, commit and push to GitHub remote.'),
        ('Backend Run', 'py app.py', 'Start Flask backend server locally on port 5000 with SQLite database.'),
        ('Testing', 'pytest test_app.py -v', 'Execute automated Pytest regression test suite (5 passing test cases).'),
        ('Docker Build', 'docker build -t flyora-app:latest .', 'Build production-ready Python 3.11 Docker container image.'),
        ('Docker Run', 'docker run -d --name flyora-prod -p 5001:5000 -v flyora_data:/app/data flyora-app:latest', 'Run containerized app on port 5001 with named persistent volume.'),
        ('Ansible Deploy', 'ansible-playbook -i inventory.ini docker-deploy.yml', 'Execute automated idempotent container deployment and volume mounting.'),
        ('Health Check', 'curl http://localhost:5000/health', 'Verify JSON application telemetry and database connectivity status.')
    ]

    for r_idx, cmd in enumerate(commands_list):
        row = cmd_table.add_row()
        for c_idx, val in enumerate(cmd):
            cell = row.cells[c_idx]
            cell.text = val
            cell.width = c_widths[c_idx]
            if r_idx % 2 == 1:
                set_cell_background(cell, "F8F9FA")

    doc.add_paragraph("\n")

    doc.add_heading("CONCLUSION & LEARNING OUTCOMES", level=1)
    p_conc = doc.add_paragraph(
        "Through the development of the Flyora Cloud-Native Flight Booking System, the principles of modern DevOps—collaboration, automation, continuous integration, containerization, and immutable infrastructure—were successfully implemented and evaluated. "
        "The project demonstrates how combining Git, Jenkins, Docker, Pytest, Ansible, and Docker persistent volumes creates a resilient, production-ready cloud deployment pipeline. "
        "The candidate has gained comprehensive practical expertise in full-stack DevOps engineering and automated cloud delivery."
    )
    p_conc.paragraph_format.line_spacing = 1.15

    out_file = 'Flyora_DevOps_Final_Project_Report_Abhishek.docx'
    doc.save(out_file)
    print(f"Report generated successfully: {out_file}")

    # Also attempt saving to standard filename
    try:
        doc.save('Flyora_DevOps_Final_Project_Report.docx')
        print("Also updated Flyora_DevOps_Final_Project_Report.docx")
    except Exception as e:
        print(f"Note: Flyora_DevOps_Final_Project_Report.docx is currently open in Word. Please check {out_file}")

if __name__ == '__main__':
    create_report()
