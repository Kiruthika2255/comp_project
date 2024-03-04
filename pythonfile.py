from flask import Flask, request, jsonify

app = Flask(__name__)

# Sample data structure to store user information and their allocated seats
train_data = {
    'section_A': [],
    'section_B': [],
}

# API to submit a purchase for a ticket
@app.route('/purchase', methods=['POST'])
def purchase_ticket():
    data = request.get_json()

    # Validate required fields
    if 'user' not in data or 'from' not in data or 'to' not in data:
        return jsonify({'error': 'Missing required fields'}), 400

    user = data['user']
    user_seat = allocate_seat(user)

    # Store user information and seat allocation
    section = user_seat[0]
    train_data[section].append({'user': user, 'from': data['from'], 'to': data['to'], 'price_paid': 5, 'seat': user_seat[1]})

    return jsonify({'message': 'Purchase successful', 'seat_allocation': user_seat})


# API to show the details of the receipt for the user
@app.route('/receipt/<string:user>', methods=['GET'])
def get_receipt(user):
    for section, users in train_data.items():
        for u in users:
            if u['user'] == user:
                return jsonify(u)
    
    return jsonify({'error': 'User not found'}), 404


# API to view users and seat allocation by section
@app.route('/view/<string:section>', methods=['GET'])
def view_users_by_section(section):
    if section not in train_data:
        return jsonify({'error': 'Invalid section'}), 400

    return jsonify(train_data[section])


# API to remove a user from the train
@app.route('/remove/<string:user>', methods=['DELETE'])
def remove_user(user):
    for section, users in train_data.items():
        for u in users:
            if u['user'] == user:
                train_data[section].remove(u)
                return jsonify({'message': 'User removed successfully'})
    
    return jsonify({'error': 'User not found'}), 404


# API to modify a user's seat
@app.route('/modify/<string:user>/<string:new_seat>', methods=['PUT'])
def modify_seat(user, new_seat):
    for section, users in train_data.items():
        for u in users:
            if u['user'] == user:
                u['seat'] = new_seat
                return jsonify({'message': 'Seat modified successfully', 'new_seat': new_seat})
    
    return jsonify({'error': 'User not found'}), 404


# Helper function to allocate a seat in a section
def allocate_seat(user):
    for section, users in train_data.items():
        if len(users) < 2:
            seat = f"{section}_{len(users) + 1}"
            return section, seat
    return None, None


if __name__ == '__main__':
    app.run(debug=True)
