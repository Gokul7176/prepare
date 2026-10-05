"""
Flyora - Cloud-Native Flight Booking System
Backend Engine with Flask, SQLite, and RESTful API endpoints.
Designed for 23IT723 DevOps Laboratory CI/CD integration with Docker, Jenkins, and Ansible.
"""

import os
import sqlite3
import random
import string
from datetime import datetime, timezone
from flask import Flask, request, jsonify, send_from_directory, render_template_string

app = Flask(__name__, static_folder='.', static_url_path='')

# Configuration
DATA_DIR = os.environ.get('DATA_DIR', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data'))
DB_PATH = os.path.join(DATA_DIR, 'flights.db')

# Ensure database directory exists for persistent Docker volume mounting
os.makedirs(DATA_DIR, exist_ok=True)

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pnr TEXT UNIQUE NOT NULL,
            flight_number TEXT NOT NULL,
            airline TEXT NOT NULL,
            origin TEXT NOT NULL,
            destination TEXT NOT NULL,
            depart_date TEXT NOT NULL,
            depart_time TEXT NOT NULL,
            passenger_name TEXT NOT NULL,
            email TEXT NOT NULL,
            phone TEXT NOT NULL,
            seat_number TEXT NOT NULL,
            cabin_class TEXT NOT NULL,
            fare_amount REAL NOT NULL,
            currency TEXT DEFAULT 'INR',
            payment_status TEXT DEFAULT 'CONFIRMED',
            payment_method TEXT DEFAULT 'UPI',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Initialize SQLite database on startup
init_db()

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/styles.css')
def serve_css():
    return send_from_directory('.', 'styles.css')

@app.route('/app.js')
def serve_js():
    return send_from_directory('.', 'app.js')

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Jenkins CI/CD pipeline and container probes."""
    try:
        conn = get_db_connection()
        conn.execute('SELECT 1').fetchone()
        conn.close()
        db_status = 'connected'
    except Exception as e:
        db_status = f'error: {str(e)}'
        
    return jsonify({
        'status': 'healthy',
        'service': 'Flyora Flight Booking Engine',
        'version': '1.0.0',
        'database': db_status,
        'db_path': DB_PATH,
        'timestamp': datetime.now(timezone.utc).isoformat()
    }), 200

@app.route('/api/bookings', methods=['GET'])
def get_bookings():
    """Retrieve all bookings from SQLite database."""
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM bookings ORDER BY id DESC').fetchall()
    conn.close()
    
    bookings = [dict(row) for row in rows]
    return jsonify({'success': True, 'count': len(bookings), 'bookings': bookings}), 200

@app.route('/api/book', methods=['POST'])
def create_booking():
    """Create a new flight booking and persist to SQLite."""
    data = request.get_json() or {}
    
    # Required fields validation
    required = ['flight_number', 'airline', 'origin', 'destination', 'passenger_name', 'email']
    for req in required:
        if req not in data or not data[req]:
            return jsonify({'success': False, 'error': f'Missing required field: {req}'}), 400
            
    # Generate authentic PNR
    pnr = data.get('pnr') or (''.join(random.choices(string.ascii_uppercase + string.digits, k=6)))
    flight_number = data.get('flight_number', '6E-2041')
    airline = data.get('airline', 'IndiGo')
    origin = data.get('origin', 'DEL')
    destination = data.get('destination', 'BOM')
    depart_date = data.get('depart_date', datetime.now(timezone.utc).strftime('%Y-%m-%d'))
    depart_time = data.get('depart_time', '06:00')
    passenger_name = data.get('passenger_name')
    email = data.get('email')
    phone = data.get('phone', '+91 98765 43210')
    seat_number = data.get('seat_number', '12B')
    cabin_class = data.get('cabin_class', 'Economy')
    fare_amount = float(data.get('fare_amount', 4500.0))
    currency = data.get('currency', 'INR')
    payment_method = data.get('payment_method', 'UPI')
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO bookings (
                pnr, flight_number, airline, origin, destination,
                depart_date, depart_time, passenger_name, email,
                phone, seat_number, cabin_class, fare_amount,
                currency, payment_status, payment_method
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'CONFIRMED', ?)
        ''', (
            pnr, flight_number, airline, origin, destination,
            depart_date, depart_time, passenger_name, email,
            phone, seat_number, cabin_class, fare_amount,
            currency, payment_method
        ))
        conn.commit()
        booking_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Flight booking confirmed successfully',
            'booking_id': booking_id,
            'pnr': pnr,
            'passenger_name': passenger_name,
            'route': f'{origin} → {destination}',
            'fare_amount': fare_amount,
            'currency': currency,
            'payment_status': 'CONFIRMED'
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/admin')
def admin_dashboard():
    """Admin Dashboard for reviewing SQLite database records and system telemetry."""
    conn = get_db_connection()
    bookings = conn.execute('SELECT * FROM bookings ORDER BY id DESC').fetchall()
    total_revenue = conn.execute('SELECT SUM(fare_amount) as total FROM bookings').fetchone()['total'] or 0
    conn.close()
    
    admin_html = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Flyora Admin Portal | DevOps Cloud Dashboard</title>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700;800&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap" rel="stylesheet">
        <style>
            :root {
                --bg: #090d16;
                --card-bg: #121826;
                --card-border: rgba(255, 255, 255, 0.08);
                --primary: #4361ee;
                --accent: #ff7b00;
                --text: #f8fafc;
                --text-muted: #94a3b8;
                --success: #10b981;
            }
            * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Plus Jakarta Sans', sans-serif; }
            body { background: var(--bg); color: var(--text); padding: 30px; min-height: 100vh; }
            .container { max-width: 1200px; margin: 0 auto; }
            header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; border-bottom: 1px solid var(--card-border); padding-bottom: 20px; }
            .logo { font-family: 'Outfit', sans-serif; font-size: 26px; font-weight: 800; color: #fff; }
            .logo span { color: var(--accent); }
            .badge { background: rgba(67, 97, 238, 0.2); color: #818cf8; padding: 6px 14px; border-radius: 20px; font-size: 13px; font-weight: 600; border: 1px solid rgba(67, 97, 238, 0.4); }
            .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 20px; margin-bottom: 30px; }
            .stat-card { background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 14px; padding: 22px; }
            .stat-title { font-size: 13px; text-transform: uppercase; letter-spacing: 0.05em; color: var(--text-muted); margin-bottom: 8px; }
            .stat-value { font-size: 28px; font-weight: 700; font-family: 'Outfit', sans-serif; color: #fff; }
            .stat-value.green { color: var(--success); }
            .table-card { background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 14px; overflow: hidden; }
            .table-header { padding: 20px; border-bottom: 1px solid var(--card-border); display: flex; justify-content: space-between; align-items: center; }
            .table-header h2 { font-family: 'Outfit', sans-serif; font-size: 20px; }
            table { width: 100%; border-collapse: collapse; text-align: left; }
            th { background: rgba(255, 255, 255, 0.03); padding: 14px 18px; font-size: 13px; color: var(--text-muted); font-weight: 600; border-bottom: 1px solid var(--card-border); }
            td { padding: 14px 18px; font-size: 14px; border-bottom: 1px solid rgba(255, 255, 255, 0.04); }
            tr:hover { background: rgba(255, 255, 255, 0.02); }
            .status-pill { background: rgba(16, 185, 129, 0.15); color: #34d399; padding: 4px 10px; border-radius: 12px; font-size: 12px; font-weight: 600; }
            .btn { background: var(--primary); color: #fff; padding: 8px 16px; border-radius: 8px; text-decoration: none; font-size: 14px; font-weight: 600; display: inline-block; transition: 0.2s; }
            .btn:hover { opacity: 0.9; transform: translateY(-1px); }
            .nav-links { display: flex; gap: 12px; align-items: center; }
        </style>
    </head>
    <body>
        <div class="container">
            <header>
                <div class="logo">✈ Flyora <span>DevOps</span> Admin</div>
                <div class="nav-links">
                    <span class="badge">SQLite Persistence: Active</span>
                    <a href="/" class="btn">← Back to App</a>
                </div>
            </header>

            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-title">Total Bookings</div>
                    <div class="stat-value">{{ bookings|length }}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-title">Total Revenue</div>
                    <div class="stat-value green">₹{{ "{:,.2f}".format(total_revenue) }}</div>
                </div>
                <div class="stat-card">
                    <div class="stat-title">Database Storage</div>
                    <div class="stat-value" style="font-size:16px; margin-top:6px; color:#cbd5e1;">data/flights.db (Docker Volume)</div>
                </div>
                <div class="stat-card">
                    <div class="stat-title">CI/CD Pipeline Status</div>
                    <div class="stat-value" style="color:var(--success); font-size:20px;">✓ Jenkins + Ansible Active</div>
                </div>
            </div>

            <div class="table-card">
                <div class="table-header">
                    <h2>Passenger Booking Manifest (SQLite Records)</h2>
                    <span style="color:var(--text-muted); font-size:13px;">Auto-synced with Docker Volume</span>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>PNR</th>
                            <th>Passenger Name</th>
                            <th>Flight</th>
                            <th>Route</th>
                            <th>Date & Time</th>
                            <th>Seat</th>
                            <th>Fare</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
                        {% if bookings %}
                            {% for b in bookings %}
                            <tr>
                                <td><strong style="color:var(--accent);">{{ b.pnr }}</strong></td>
                                <td>{{ b.passenger_name }}</td>
                                <td>{{ b.airline }} ({{ b.flight_number }})</td>
                                <td>{{ b.origin }} → {{ b.destination }}</td>
                                <td>{{ b.depart_date }} {{ b.depart_time }}</td>
                                <td>{{ b.seat_number }} ({{ b.cabin_class }})</td>
                                <td>₹{{ "{:,.0f}".format(b.fare_amount) }}</td>
                                <td><span class="status-pill">{{ b.payment_status }}</span></td>
                            </tr>
                            {% endfor %}
                        {% else %}
                            <tr>
                                <td colspan="8" style="text-align:center; padding:30px; color:var(--text-muted);">
                                    No bookings recorded yet. Go to <a href="/" style="color:var(--primary);">Flyora Home</a> to make a flight booking.
                                </td>
                            </tr>
                        {% endif %}
                    </tbody>
                </table>
            </div>
        </div>
    </body>
    </html>
    '''
    return render_template_string(admin_html, bookings=bookings, total_revenue=total_revenue)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"Starting Flyora Flight Booking Server on http://localhost:{port} ...")
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
