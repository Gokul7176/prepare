"""
Automated Pytest Suite for Flyora Cloud-Native Flight Booking System
Executes automated functional and API validation during the Jenkins CI/CD pipeline.
"""

import pytest
import json
import os
from app import app, init_db, get_db_connection

@pytest.fixture
def client():
    app.config['TESTING'] = True
    # Use testing database
    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

def test_home_page(client):
    """Verify that the home page loads successfully (HTTP 200)."""
    response = client.get('/')
    assert response.status_code == 200

def test_health_check(client):
    """Verify the health check endpoint for container probes and Jenkins verification."""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'
    assert 'database' in data

def test_create_flight_booking(client):
    """Verify flight booking API creates a record and returns 201 with confirmed PNR."""
    booking_payload = {
        'flight_number': '6E-2041',
        'airline': 'IndiGo',
        'origin': 'DEL',
        'destination': 'BOM',
        'depart_date': '2026-10-15',
        'depart_time': '07:30',
        'passenger_name': 'Gokul R',
        'email': 'gokul@example.com',
        'phone': '+91 98765 43210',
        'seat_number': '14B',
        'cabin_class': 'Economy',
        'fare_amount': 4850.0,
        'currency': 'INR',
        'payment_method': 'UPI'
    }
    response = client.post('/api/book', 
                           data=json.dumps(booking_payload),
                           content_type='application/json')
    assert response.status_code == 201
    data = json.loads(response.data)
    assert data['success'] is True
    assert 'pnr' in data
    assert len(data['pnr']) == 6
    assert data['passenger_name'] == 'Gokul R'

def test_get_all_bookings(client):
    """Verify retrieval of stored booking records from SQLite."""
    response = client.get('/api/bookings')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['success'] is True
    assert isinstance(data['bookings'], list)

def test_admin_dashboard(client):
    """Verify that the admin portal renders successfully (HTTP 200)."""
    response = client.get('/admin')
    assert response.status_code == 200
    assert b'Flyora' in response.data
