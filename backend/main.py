from flask import request, jsonify
from config import app, db
from models import Contact

@app.route('/contacts', methods=['GET'])
def get_contacts():
    contacts = Contact.query.all()
    json_contacts = list(map(lambda x: x.to_json(), contacts))
    return jsonify(json_contacts)

@app.route('/contacts', methods=['POST'])
def create_contact():
    first_name=request.json.get('first_name')
    last_name=request.json.get('last_name')
    email=request.json.get('email')

    if not first_name or not last_name or not email:
        return jsonify({'error': 'Missing required fields'}), 400

    new_contact = Contact(
        first_name=first_name,
        last_name=last_name,
        email=email
    )   
    try:
        db.session.add(new_contact)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    return jsonify({"message":"user created successfully"}), 201

@app.route("/update_contact/<int:id>", methods=['PUT'])
def update_contact(id):
    contact = Contact.query.get(id)
    if not contact:
        return jsonify({"message":"user not found"}), 404
    
    data=request.json
    contact.first_name = data.get('first_name', contact.first_name)
    contact.last_name = data.get('last_name', contact.last_name)
    contact.email = data.get('email', contact.email)

    try:
        db.session.commit()
        return jsonify({"message":"user updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@app.route('/delete_contact/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contact = Contact.query.get(id)
    if not contact:
        return jsonify({"message":"user not found"}), 404
    
    try:
        db.session.delete(contact)
        db.session.commit()
        return jsonify({"message":"user deleted successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
    




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)