from flask import jsonify, request

from app import app
from app import db
from app.models.package_model import Package


@app.route('/create_package', methods=['POST'])
def create_package():
    package_name = request.form.get('packageName')
    personal_min_fund = request.form.get('personalMinFund')
    personal_max_fund = request.form.get('personalMaxFund')
    rebate_fee = request.form.get('rebateFee')

    new_package = Package(
        packageName=package_name,
        personalMinFund=personal_min_fund,
        personalMaxFund=personal_max_fund,
        rebateFee=rebate_fee
    )

    db.session.add(new_package)
    db.session.commit()

    response_data = {
        'packageName': new_package.packageName,
        'personalMinFund': new_package.personalMinFund,
        'personalMaxFund': new_package.personalMaxFund,
        'rebateFee': new_package.rebateFee,
        'packageID': new_package.packageID,
        'message': 'Package added',
        'code': 200
    }

    return jsonify(response_data), 200


@app.route('/update_package', methods=['POST'])
def update_package():
    package_id = request.form.get('packageID')
    package_name = request.form.get('packageName')
    personal_min_fund = request.form.get('personalMinFund')
    personal_max_fund = request.form.get('personalMaxFund')
    rebate_fee = request.form.get('rebateFee')

    package = Package.query.get(package_id)
    if not package:
        return jsonify({'message': 'Package not found', 'code': 404}), 404

    package.packageName = package_name
    package.personalMinFund = personal_min_fund
    package.personalMaxFund = personal_max_fund
    package.rebateFee = rebate_fee

    db.session.commit()

    response_data = {
        'packageName': package.packageName,
        'personalMinFund': package.personalMinFund,
        'personalMaxFund': package.personalMaxFund,
        'rebateFee': package.rebateFee,
        'packageID': package.packageID,
        'message': 'Update Success',
        'code': 200
    }

    return jsonify(response_data), 200


@app.route('/search_package', methods=['POST'])
def search_package():
    package_id = request.form.get('packageID')

    package = Package.query.get(package_id)
    if not package:
        return jsonify({'message': 'Package not found', 'code': 404}), 404

    response_data = {
        'packageName': package.packageName,
        'personalMinFund': package.personalMinFund,
        'personalMaxFund': package.personalMaxFund,
        'rebateFee': package.rebateFee,
        'packageID': package.packageID,
        'message': 'Package Found',
        'code': 200
    }

    return jsonify(response_data), 200


@app.route('/get_packages', methods=['GET'])
def get_packages():
    packages = Package.query.all()

    response_data = []
    for package in packages:
        package_data = {
            'packageName': package.packageName,
            'personalMinFund': package.personalMinFund,
            'personalMaxFund': package.personalMaxFund,
            'rebateFee': package.rebateFee,
            'packageID': package.packageID
        }
        response_data.append(package_data)

    return jsonify(response_data)
