from flask import Flask, flash, request, session, make_response,jsonify
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta
from config import config
from Player.Player import Player

from Database.Database import Database

app = Flask(__name__)
app.secret_key = 'your_unique_secret_key'
CORS(app)

blacklisted_tokens = set()
db = Database(config = config(), connect = True, setup = "--setup")

def token_required(f):
    def wrapper(*args, **kwargs):
        # Check if Authorization header exists
        token = request.headers.get('Authorization')
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401

        # Remove 'Bearer ' prefix if present
        if token.startswith('Bearer '):
            token = token.split(' ')[1]

        # Check if token is blacklisted
        if token in blacklisted_tokens:
            return jsonify({'error': 'Token is invalid or expired'}), 401

        try:
            # Use app.config['SECRET_KEY'] for decoding
            decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            user_id = decoded.get('user_id')
            
            if not user_id:
                return jsonify({'error': 'Invalid token payload'}), 401
            
            # Query to fetch user details
            query = '''
                SELECT id, username FROM users WHERE id = %s
            '''
            result = db.query(query, (user_id,))
            
            if not result or not result.get('result_group'):
                return jsonify({'error': 'User not found'}), 404

            # Create a simple user object with id and username
            current_user =  result['result'][0]

        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        except Exception as e:
            return jsonify({'error': f'Server error: {str(e)}'}), 500

        # Call the original function with the current user
        return f(current_user, *args, **kwargs)
    
    wrapper.__name__ = f.__name__
    wrapper.__doc__ = f.__doc__
    wrapper.__module__ = f.__module__

    return wrapper

@app.route('/api/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return jsonify({
            "path": "home",
            "number": 23
        })


@app.route('/api/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.get_json().get('username')
        password = request.get_json().get('password')
        user = Player(username, password, db)

        if not user or user.get_username() is None:
            return make_response(jsonify({
                'error': 'Incorrect username or password.'
                }), 401)
        

        token = jwt.encode({
            'user_id': user.get_data().get('id'),
            'exp': datetime.now() + timedelta(hours=1)  
            }, 
            app.config['SECRET_KEY'], 
            algorithm='HS256')
        
        return make_response(jsonify({
            'message': 'Logged in successfully', 
            'token': token  
            }), 200)
            


@app.route('/api/profile', methods=['GET'])
@token_required
def profile(current_user):
    return make_response(jsonify({
        'id': current_user[0],
        'username': current_user[1]
    }), 200)
    
@app.route('/api/leaderboard', methods=['GET'])
def leaderboard():
    if request.method == 'GET':
        return "Leaderboard"
    
@app.route('/api/games', methods=['GET', 'POST'])
def games():
    if request.method == 'GET': 
        return "Games"

@app.route('/api/logout', methods=['POST'])
@token_required
def logout(current_user):
    token = request.headers.get('Authorization')
    
    if token.startswith('Bearer '):
        token = token.split(' ')[1]
    
    blacklisted_tokens.add(token)
    
    return make_response(jsonify({
        'message': 'Logged out successfully'
    }), 200)
