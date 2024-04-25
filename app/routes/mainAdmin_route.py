import hashlib

from flask import jsonify, request

from app import app
from app import db
from app.models.mainAdmin_model import MainAdmin


@app.route('/main_admin_create', methods=['POST'])
def create_main_admin():
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
    admin_referral = request.form.get('adminReferral')
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    if MainAdmin.query.filter_by(email=email).first():
        return jsonify({'message': 'Email already exists', 'code': 400}), 400

    new_main_admin = MainAdmin(name=name, email=email, password=hashed_password, adminReferral=admin_referral)

    db.session.add(new_main_admin)

    db.session.commit()

    return jsonify({'message': 'Success', 'code': 200}), 200


@app.route('/main_admin_update/<email>', methods=['PUT'])
def update_main_admin(email):
    name = request.form.get('name')
    password = request.form.get('password')
    admin_referral = request.form.get('adminReferral')

    main_admin = MainAdmin.query.filter_by(email=email).first()

    if not main_admin:
        return jsonify({'message': 'Admin not found with the given email', 'code': 404}), 404

    if name:
        main_admin.name = name
    if password:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        main_admin.password = hashed_password
    if admin_referral:
        main_admin.adminReferral = admin_referral

    db.session.commit()

    return jsonify({'name': main_admin.name, 'adminReferral': main_admin.adminReferral, 'email': main_admin.email,
                    'message': 'Update Success', 'code': 200}), 200


@app.route('/search_admin_referral', methods=['GET'])
def search_main_admin():
    admin_referral = request.args.get('adminReferral')

    main_admins = MainAdmin.query.filter_by(adminReferral=admin_referral).all()

    if not main_admins:
        return jsonify({'message': 'Referral not found', 'code': 404}), 404

    return jsonify({'message': 'Found Main Admin', 'code': 200}), 200
