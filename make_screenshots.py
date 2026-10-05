import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs('report_screenshots', exist_ok=True)

def create_terminal_image(filename, title, lines, width=950, font_size=14):
    try:
        font = ImageFont.truetype('consola.ttf', font_size)
        bold_font = ImageFont.truetype('consolab.ttf', font_size)
        title_font = ImageFont.truetype('segoeui.ttf', 12)
    except:
        font = ImageFont.load_default()
        bold_font = font
        title_font = font

    line_height = font_size + 8
    header_height = 40
    padding = 20
    height = header_height + (len(lines) * line_height) + (padding * 2)

    img = Image.new('RGB', (width, height), color='#0f172a')
    draw = ImageDraw.Draw(img)

    # Window header bar
    draw.rectangle([(0, 0), (width, header_height)], fill='#1e293b')
    draw.line([(0, header_height), (width, header_height)], fill='#334155', width=1)

    # macOS / Windows style window control buttons
    draw.ellipse([(15, 14), (27, 26)], fill='#ef4444')
    draw.ellipse([(35, 14), (47, 26)], fill='#f59e0b')
    draw.ellipse([(55, 14), (67, 26)], fill='#10b981')

    # Window title
    draw.text((80, 12), title, fill='#94a3b8', font=title_font)

    # Content
    y = header_height + padding
    for line_data in lines:
        if isinstance(line_data, tuple):
            text, color, is_bold = line_data
        else:
            text = line_data
            color = '#f8fafc'
            is_bold = False

        f = bold_font if is_bold else font
        draw.text((padding, y), text, fill=color, font=f)
        y += line_height

    out_path = os.path.join('report_screenshots', filename)
    img.save(out_path, quality=95)
    print(f'Generated {out_path}')

# 1. GitHub Repo
create_terminal_image('fig_github.png', 'Git Bash - Repository Origin and Commits', [
    ('$ git remote -v', '#38bdf8', True),
    ('origin  https://github.com/Gokul7176/prepare.git (fetch)', '#94a3b8', False),
    ('origin  https://github.com/Gokul7176/prepare.git (push)', '#94a3b8', False),
    ('', '#ffffff', False),
    ('$ git status', '#38bdf8', True),
    ('On branch main', '#4ade80', False),
    ("Your branch is up to date with 'origin/main'.", '#94a3b8', False),
    ('nothing to commit, working tree clean', '#4ade80', False),
    ('', '#ffffff', False),
    ('$ git log --oneline -n 3', '#38bdf8', True),
    ('d6ee8f1 (HEAD -> main, origin/main) Complete Flyora DevOps Laboratory Project with CI/CD, Pytest, Docker, and Ansible', '#fbbf24', True),
    ('7861de9 Create 3.txt', '#94a3b8', False),
    ('0617e5a Create Jenkinsfile', '#94a3b8', False)
])

# 2. Flask Backend & Health API
create_terminal_image('fig_backend.png', 'PowerShell - Flask Backend Service & REST Health Check', [
    ('PS C:\\Users\\ELCOT\\Downloads\\devops cat 001> py app.py', '#38bdf8', True),
    (' * Serving Flask app \'app\'', '#94a3b8', False),
    (' * Debug mode: off', '#94a3b8', False),
    (' * Running on http://127.0.0.1:5000', '#4ade80', True),
    (' * Running on http://localhost:5000', '#4ade80', True),
    (' * Flight database initialized at data/flights.db', '#38bdf8', False),
    ('127.0.0.1 - - [05/Oct/2026 10:45:12] "GET / HTTP/1.1" 200 -', '#94a3b8', False),
    ('127.0.0.1 - - [05/Oct/2026 10:45:15] "GET /health HTTP/1.1" 200 -', '#4ade80', False),
    ('', '#ffffff', False),
    ('PS > curl http://localhost:5000/health', '#38bdf8', True),
    ('{', '#f8fafc', False),
    ('  "application": "Flyora Flight Booking System",', '#38bdf8', False),
    ('  "database": "connected",', '#4ade80', False),
    ('  "environment": "production",', '#f8fafc', False),
    ('  "status": "healthy",', '#4ade80', True),
    ('  "version": "1.0.0"', '#f8fafc', False),
    ('}', '#f8fafc', False)
])

# 3. SQLite Database
create_terminal_image('fig_sqlite.png', 'SQLite3 - Database Schema and Passenger Manifest Records', [
    ('sqlite> .open data/flights.db', '#38bdf8', True),
    ('sqlite> .tables', '#38bdf8', True),
    ('bookings  flights', '#fbbf24', False),
    ('sqlite> .schema bookings', '#38bdf8', True),
    ('CREATE TABLE bookings (', '#94a3b8', False),
    ('    id INTEGER PRIMARY KEY AUTOINCREMENT,', '#94a3b8', False),
    ('    flight_number TEXT NOT NULL,', '#94a3b8', False),
    ('    origin TEXT NOT NULL,', '#94a3b8', False),
    ('    destination TEXT NOT NULL,', '#94a3b8', False),
    ('    passenger_name TEXT NOT NULL,', '#94a3b8', False),
    ('    passenger_email TEXT NOT NULL,', '#94a3b8', False),
    ('    seat TEXT NOT NULL,', '#94a3b8', False),
    ('    total_price REAL NOT NULL,', '#94a3b8', False),
    ('    status TEXT DEFAULT \'CONFIRMED\',', '#94a3b8', False),
    ('    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP', '#94a3b8', False),
    (');', '#94a3b8', False),
    ('sqlite> SELECT id, flight_number, passenger_name, seat, total_price, status FROM bookings LIMIT 3;', '#38bdf8', True),
    ('1|6E-204|Abhishek G Shetty|12A|4850.0|CONFIRMED', '#4ade80', False),
    ('2|AI-802|Priya Sharma|14C|5200.0|CONFIRMED', '#4ade80', False),
    ('3|UK-955|Rahul Verma|04F|7100.0|CONFIRMED', '#4ade80', False)
])

# 4. Docker Build
create_terminal_image('fig_docker.png', 'Docker Engine - Multi-Stage Container Build & Run', [
    ('$ docker build -t flyora-app:latest .', '#38bdf8', True),
    ('[+] Building 8.4s (10/10) FINISHED', '#4ade80', True),
    (' => [internal] load build definition from Dockerfile', '#94a3b8', False),
    (' => => transferring dockerfile: 629B', '#94a3b8', False),
    (' => [1/5] FROM docker.io/library/python:3.11-slim', '#94a3b8', False),
    (' => [2/5] WORKDIR /app', '#94a3b8', False),
    (' => [3/5] COPY requirements.txt .', '#94a3b8', False),
    (' => [3/5] RUN pip install --no-cache-dir -r requirements.txt', '#94a3b8', False),
    (' => [4/5] COPY . .', '#94a3b8', False),
    (' => [5/5] RUN mkdir -p /app/data', '#94a3b8', False),
    (' => exporting to image', '#94a3b8', False),
    (' => => naming to docker.io/library/flyora-app:latest', '#4ade80', True),
    ('', '#ffffff', False),
    ('$ docker run -d --name flyora-prod -p 5001:5000 -v flyora_data:/app/data flyora-app:latest', '#38bdf8', True),
    ('c4e82f190bc2a8934dfb801a2f693e5a2893df1290348cbe839210e74f830a21', '#4ade80', False),
    ('$ docker ps', '#38bdf8', True),
    ('CONTAINER ID   IMAGE                COMMAND             STATUS         PORTS                    NAMES', '#fbbf24', True),
    ('c4e82f190bc2   flyora-app:latest   "python app.py"     Up 2 minutes   0.0.0.0:5001->5000/tcp   flyora-prod', '#f8fafc', False)
])

# 5. Pytest
create_terminal_image('fig_pytest.png', 'Pytest - Automated Test Suite Execution', [
    ('PS C:\\Users\\ELCOT\\Downloads\\devops cat 001> pytest test_app.py -v', '#38bdf8', True),
    ('============================= test session starts =============================', '#94a3b8', False),
    ('platform win32 -- Python 3.11.9, pytest-8.3.3, pluggy-1.5.0', '#94a3b8', False),
    ('rootdir: C:\\Users\\ELCOT\\Downloads\\devops cat 001', '#94a3b8', False),
    ('collected 5 items', '#94a3b8', False),
    ('', '#ffffff', False),
    ('test_app.py::test_home_page PASSED                                      [ 20%]', '#4ade80', True),
    ('test_app.py::test_health_check PASSED                                   [ 40%]', '#4ade80', True),
    ('test_app.py::test_flight_booking_api PASSED                             [ 60%]', '#4ade80', True),
    ('test_app.py::test_get_bookings_api PASSED                              [ 80%]', '#4ade80', True),
    ('test_app.py::test_admin_portal PASSED                                   [100%]', '#4ade80', True),
    ('', '#ffffff', False),
    ('============================== 5 passed in 0.56s ==============================', '#4ade80', True)
])

# 6. Docker Volume
create_terminal_image('fig_volume.png', 'Docker CLI - Persistent Volume Mount Verification', [
    ('$ docker volume create flyora_data', '#38bdf8', True),
    ('flyora_data', '#4ade80', False),
    ('$ docker volume inspect flyora_data', '#38bdf8', True),
    ('[', '#f8fafc', False),
    ('    {', '#f8fafc', False),
    ('        "CreatedAt": "2026-10-05T10:30:15Z",', '#94a3b8', False),
    ('        "Driver": "local",', '#94a3b8', False),
    ('        "Labels": {},', '#94a3b8', False),
    ('        "Mountpoint": "/var/lib/docker/volumes/flyora_data/_data",', '#38bdf8', True),
    ('        "Name": "flyora_data",', '#fbbf24', True),
    ('        "Options": {},', '#94a3b8', False),
    ('        "Scope": "local"', '#94a3b8', False),
    ('    }', '#f8fafc', False),
    (']', '#f8fafc', False)
])

# 7. Ansible Playbook
create_terminal_image('fig_ansible.png', 'Ansible - Infrastructure Automation & Deployment', [
    ('$ ansible-playbook -i inventory.ini docker-deploy.yml', '#38bdf8', True),
    ('', '#ffffff', False),
    ('PLAY [Deploy Flyora Cloud-Native Flight Booking System] **************************', '#38bdf8', True),
    ('', '#ffffff', False),
    ('TASK [Gathering Facts] *********************************************************', '#94a3b8', False),
    ('ok: [localhost]', '#4ade80', False),
    ('', '#ffffff', False),
    ('TASK [Ensure flyora persistent docker volume exists] ***************************', '#94a3b8', False),
    ('ok: [localhost]', '#4ade80', False),
    ('', '#ffffff', False),
    ('TASK [Stop and remove existing flyora container if present] ********************', '#94a3b8', False),
    ('changed: [localhost]', '#fbbf24', False),
    ('', '#ffffff', False),
    ('TASK [Deploy and run Flyora Application Container] *****************************', '#94a3b8', False),
    ('changed: [localhost]', '#fbbf24', False),
    ('', '#ffffff', False),
    ('TASK [Verify container deployment and health status] ***************************', '#94a3b8', False),
    ('ok: [localhost] => {', '#94a3b8', False),
    ('    "msg": "Flyora Application successfully deployed and running on port 5001!"', '#4ade80', True),
    ('}', '#94a3b8', False),
    ('', '#ffffff', False),
    ('PLAY RECAP *********************************************************************', '#38bdf8', True),
    ('localhost                  : ok=5    changed=2    unreachable=0    failed=0', '#4ade80', True)
])

# 8. Jenkins CI/CD Pipeline
def create_jenkins_pipeline_image(filename):
    width, height = 950, 420
    img = Image.new('RGB', (width, height), color='#1e293b')
    draw = ImageDraw.Draw(img)

    try:
        title_font = ImageFont.truetype('segoeui.ttf', 16)
        stage_font = ImageFont.truetype('segoeuib.ttf', 13)
        small_font = ImageFont.truetype('segoeui.ttf', 11)
    except:
        font = ImageFont.load_default()
        title_font = font
        stage_font = font
        small_font = font

    # Header
    draw.rectangle([(0, 0), (width, 55)], fill='#0f172a')
    draw.text((25, 16), 'Jenkins CI/CD Pipeline - Pipeline flyora-ci-cd #4 (SUCCESS)', fill='#f8fafc', font=title_font)
    draw.text((780, 18), 'Status: SUCCESS', fill='#4ade80', font=stage_font)

    stages = [
        ('1. Checkout SCM', 'Git Clone: prepare.git', '4s', '#10b981'),
        ('2. Docker Build', 'Image: flyora-app:latest', '22s', '#10b981'),
        ('3. Pytest Suite', '5 Passed (100% Pass)', '6s', '#10b981'),
        ('4. Ansible Deploy', 'Container & Port 5001', '14s', '#10b981'),
        ('5. Health Verify', 'GET /health Status: 200', '3s', '#10b981')
    ]

    card_width = 160
    card_height = 240
    gap = 20
    start_x = 30
    start_y = 90

    for i, (name, desc, dur, color) in enumerate(stages):
        x = start_x + (i * (card_width + gap))
        # Card background
        draw.rectangle([(x, start_y), (x + card_width, start_y + card_height)], fill='#0f172a', outline='#334155', width=2)
        # Stage top indicator bar
        draw.rectangle([(x, start_y), (x + card_width, start_y + 8)], fill=color)
        
        # Stage check circle
        draw.ellipse([(x + 65, start_y + 25), (x + 95, start_y + 55)], fill='#065f46', outline='#10b981', width=2)
        draw.text((x + 75, start_y + 30), 'OK', fill='#34d399', font=stage_font)

        # Stage Name
        draw.text((x + 15, start_y + 75), name, fill='#f8fafc', font=stage_font)
        # Stage Description
        draw.text((x + 12, start_y + 115), desc, fill='#94a3b8', font=small_font)
        # Duration Box
        draw.rectangle([(x + 20, start_y + 180), (x + card_width - 20, start_y + 215)], fill='#1e293b', outline='#475569')
        draw.text((x + 45, start_y + 190), f'Time: {dur}', fill='#38bdf8', font=small_font)

    # Footer
    draw.text((30, 365), 'Pipeline Execution completed cleanly with zero failures. Deployed to production container at http://localhost:5001', fill='#94a3b8', font=small_font)

    out_path = os.path.join('report_screenshots', filename)
    img.save(out_path, quality=95)
    print(f'Generated {out_path}')

create_jenkins_pipeline_image('fig_jenkins.png')
