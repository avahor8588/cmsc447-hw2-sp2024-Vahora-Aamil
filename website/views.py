#views.py
from flask import Blueprint, request, render_template, redirect, url_for, flash
from .model import User
from . import db
from . import socketio
from flask import jsonify
views = Blueprint('views', __name__)

# Assuming you have an existing route for the home page
@views.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        search_name = request.form.get('search_name', '')
        users = User.query.filter(User.name.contains(search_name)).all()
    else:
        users = User.query.all()
    return render_template('index.html', users=users)

@views.route('/create_user', methods=['POST'])
def create_user():
    # Since you're sending the data as JSON, use request.get_json() to access the data
    data = request.get_json() if request.is_json else None
    if data:
        user_id = data.get('id')
        name = data.get('name')
        points = data.get('points')
        existing_user = User.query.get(user_id)
        if existing_user:
            # If the user exists, return an error message as JSON
            return jsonify({'success': False, 'message': 'A user with this ID already exists.'}), 400

        new_user = User(id=user_id, name=name, points=points)
        db.session.add(new_user)
        try:
            db.session.commit()
            # Emit the socketio event after committing to the database
            socketio.emit('user_update', {'action': 'create', 'id': new_user.id, 'name': new_user.name, 'points': new_user.points}, namespace='/data')
            return jsonify({'success': True, 'message': 'User added successfully', 'user': {'id': new_user.id, 'name': new_user.name, 'points': new_user.points}})
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': 'Failed to add the user to the database. Please try again.'}), 500
    else:
        return jsonify({'success': False, 'message': 'Invalid data format.'}), 400
@views.route('/search_user', methods=['POST'])
def search_user():
    return home()

@views.route('/delete_user', methods=['POST'])
def delete_user():
    
    user_id = request.form['user_id']
    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('views.home', message='User not found'))
    if user:
        db.session.delete(user)
        db.session.commit()
        socketio.emit('user_update', {'action': 'delete', 'id': user_id}, namespace='/data')
        return redirect(url_for('views.home'))
    else:
        # Handle case where user is not found
        flash('User not found!', 'error')
        return redirect(url_for('views.home'))

@views.route('/update_user', methods=['POST'])
def update_user():
    user_id = request.form['user_id']
    new_points = request.form['new_points']

    user = User.query.get(user_id)
    if not user:
        return redirect(url_for('views.home', message='User not found'))

    user.points = new_points
    db.session.commit()
    socketio.emit('user_update', {'action': 'update', 'id': user_id, 'name': user.name, 'points': new_points}, namespace='/data')
    return redirect(url_for('views.home', message='User points updated successfully'))