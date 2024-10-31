from random import randint

from flask import jsonify, request
from flask_mail import Mail, Message
from flask import render_template
from datetime import datetime

from app import app
from app import db
from app.models.admin_model import Admin

mail = Mail(app)

def render_otp_email(otp, user_name):
    # Fill in the HTML template with the OTP and year
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
      <meta charset="UTF-8">
      <meta name="viewport" content="width=device-width, initial-scale=1.0">
      <title>MyWealth OTP</title>
      <style>
        body, html {{
          margin: 0;
          padding: 0;
          width: 100%;
          background-color: #f5f8fa;
          font-family: Arial, sans-serif;
        }}
        .container {{
          width: 100%;
          max-width: 600px;
          margin: auto;
          background-color: #ffffff;
          border-radius: 8px;
          overflow: hidden;
        }}
        .header {{
          background-color: #007AFF;
          padding: 20px;
          text-align: center;
        }}
        .header img {{
          max-width: 150px;
          height: auto;
        }}
        .content {{
          padding: 20px;
          color: #333;
          text-align: center;
        }}
        .otp {{
          display: inline-block;
          padding: 10px 20px;
          background-color: #007AFF;
          color: #fff;
          font-size: 24px;
          font-weight: bold;
          border-radius: 5px;
          margin: 20px 0;
        }}
        .footer {{
          padding: 10px 20px;
          text-align: center;
          font-size: 12px;
          color: #999;
        }}
        @media (max-width: 600px) {{
          .header, .content, .footer {{
            padding: 10px;
          }}
          .otp {{
            font-size: 20px;
          }}
        }}
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <img src="https://private-user-images.githubusercontent.com/60685269/382091791-d40c2b08-04ce-4875-b7aa-5a89c8b12194.svg?jwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3MzA0MDM2OTgsIm5iZiI6MTczMDQwMzM5OCwicGF0aCI6Ii82MDY4NTI2OS8zODIwOTE3OTEtZDQwYzJiMDgtMDRjZS00ODc1LWI3YWEtNWE4OWM4YjEyMTk0LnN2Zz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNDEwMzElMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQxMDMxVDE5MzYzOFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWVlOWJkMDg1NDY3MDVmN2M3YWMxNmE3OGRhZmE1ZWQ3MGFlM2M1NmE5MWM0MzkyYjIwMTlmMTA0ZWU3MTAzMjYmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.w4dLh2yKOMtq7roKI98ELJ5Z0fGL6ACv-ghvVkwntGs" alt="MyWealth Logo">
        </div>
        <div class="content">
          <h1>One-Time Password (OTP)</h1>
          <p>Hello {user_name},</p>
          <p>To complete your registration, please use the following One-Time Password:</p>
          <div class="otp">{otp}</div>
          <p>This code is valid for the next 10 minutes. If you did not request this OTP, please ignore this message or contact support.</p>
          <p>Thank you for choosing MyWealth!</p>
        </div>
        <div class="footer">
          © {datetime.now().year} MyWealth. All rights reserved. <br>
          MyWealth, Investing made for everyone.
        </div>
      </div>
    </body>
    </html>
    """

def generate_otp():
    return randint(1000, 9999)


def send_otp_email(email, otp, user_name):
    msg = Message('New Admin Registration OTP', recipients=[email])
    msg.html = render_otp_email(otp, user_name)  # Set the HTML content
    mail.send(msg)


@app.route('/admin_register', methods=['POST'])
def create_admin():
    SEND_OTP_EMAIL = 'investment.mywealth@gmail.com'
    user_name = request.json.get('user_name')
    email = request.json.get('email')
    password = request.json.get('password')

    existing_admin = Admin.query.filter_by(email=email).first()
    if existing_admin:
        return jsonify({'message': 'Admin already exists with the given email', 'code': 400}), 400

    otp = generate_otp()
    new_admin = Admin(user_name=user_name, email=email,
                      password=password, otp=otp)
    db.session.add(new_admin)
    db.session.commit()

    send_otp_email(SEND_OTP_EMAIL, otp, user_name)

    new_admin.otp = otp
    db.session.commit()

    return jsonify({'message': 'Admin created successfully', 'code': 201}), 201


@app.route('/check_otp', methods=['POST'])
def check_otp():
    data = request.json
    email = data.get('email')
    otp = data.get('otp')

    admin = Admin.query.filter_by(email=email).first()
    if not admin:
        return jsonify({'message': 'Admin not found with the given email', 'code': 404}), 404

    if otp != admin.otp:
        return jsonify({'message': 'Invalid OTP', 'code': 400}), 400

    admin.is_verified = True
    db.session.commit()

    return jsonify({'message': 'OTP verified successfully', 'code': 200}), 200


@app.route('/admin_login', methods=['POST'])
def admin_login():
    email = request.json.get('email')
    password = request.json.get('password')

    admin = Admin.query.filter_by(email=email).first()

    if not admin:
        return jsonify({'message': 'Email not found', 'code': 404}), 404

    if admin.password != password:
        return jsonify({'message': 'Invalid  Password', 'code': 401}), 401

    response_data = {
        'user_id': admin.admin_id,
        'user_name': admin.user_name,
        'email': admin.email,
        'if_verify': admin.is_verified,

        'message': 'Login successful',
        'code': 200
    }

    return jsonify(response_data), 200


@app.route('/admin_delete/<int:admin_id>', methods=['DELETE'])
def delete_admin(admin_id):
    admin = Admin.query.get(admin_id)

    if not admin:
        return jsonify({'message': 'Admin not found with the given ID', 'code': 404}), 404

    db.session.delete(admin)
    db.session.commit()

    return jsonify({'message': 'Admin deleted successfully', 'code': 200}), 200
