from flask import Flask, flash, request, session, make_response,jsonify
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta
from config import config
from Player.Player import Player
from Games import *

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
            username = decoded.get('username')
            password = decoded.get('password')
            
            if not user_id or not username or not password:
                return jsonify({'error': 'Invalid token payload'}), 401
        
            user = Player(username, password, db)
            
            if not user or not user.get_username():
                return jsonify({'error': 'User not found'}), 40

            # Create a simple user object with id and username
            current_user = Player(username, password, db)

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
            'username': user.get_data().get('username'),
            'password': password,
            'exp': datetime.now() + timedelta(hours=1)  
            }, 
            app.config['SECRET_KEY'], 
            algorithm='HS256')
        
        return make_response(jsonify({
            'message': 'Logged in successfully', 
            'token': token  
            }), 200)
            
@app.route('/bet', methods=['POST'])
@token_required
def place_bet(current_user):
        """Place a bet in the current game session."""
        data = request.get_json()
        bet = data.get('bet')
        player_data = data.get('player_data')
        db_handler = db()
        player = Player.from_data(player_data)
        game = Dice(player, db_handler)

        if bet <= 0 or bet > player.get_balance():
            return jsonify({'error': 'Invalid bet amount'}), 400

        player.update_balance(-bet)
        return jsonify({'bet': bet, 'balance': player.get_balance()})

@app.route('/api/profile', methods=['GET'])
@token_required
def profile(current_user):
    user = current_user.get_data()

    return make_response(jsonify({
        'user': user
    }), 200)
    

@app.route('/api/leaderboard', methods=['GET'])
def leaderboard():
    sort = "DESC"
    filter_column = "user_statistics.total_winnings"
    query = f'''
                SELECT 
                    users.username,
                    user_statistics.total_winnings,
                    user_statistics.games_played,
                    user_statistics.games_won,
                    user_statistics.games_lost
                FROM users
                JOIN user_statistics
                ON users.id = user_statistics.user_id
                ORDER BY {filter_column} {sort}
                LIMIT 10
            '''
    
    data = db.query(query, cursor_settings={'dictionary': True})

    return make_response(jsonify({
        'data': data
    }),200)
    
@app.route('/api/games', methods=['GET', 'POST'])
def games(current_user: Player):
    user = current_user
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

