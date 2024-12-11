from flask import Flask, flash, request, session, make_response,jsonify
from flask_cors import CORS
import jwt
from datetime import datetime, timedelta
from config import config
from Player.Player import Player
from Player.Auth import Auth
from Games import *

from Database.Database import Database

app = Flask(__name__)
app.secret_key = config().get('secret_key')
CORS(app, resources={r"/api/*": {"origins": "*"}})

blacklisted_tokens = set()
db = Database(config = config())
auth_handler = Auth(db)

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
            
            # Get the current user's data
            current_user = Player(user_id, db)
            
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


@app.route('/api/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        data = request.json
        
        username = data.get('username')
        password = data.get('password')
        
        username_in_use = auth_handler.user_exists(username)
        
        # username is in use
        if username_in_use:
            login_result = auth_handler.login(username, password)
            
            if not login_result:
                return make_response(jsonify({'message': 'Väärä salasana!'}), 401)
            else:
                user_id = login_result
                
        # username is not in use -> create a new user
        else:
            user_id = auth_handler.create_user(username, password)
            
        token = jwt.encode({
            'user_id': user_id,
            'exp': datetime.now() + timedelta(hours=1)  
            }, 
            app.config['SECRET_KEY'], 
            algorithm='HS256')
        
        return make_response(jsonify({
            'message': f'Tervetuloa, {username}!', 
            'token': token,
            'user_id': user_id,
            }), 200)
            
@app.route('/api/profile', methods=['GET'])
@token_required
def profile(current_user: Player):
    return make_response(jsonify(current_user.get_data()), 200)
    
@app.route('/api/gamehistory', methods=['GET'])
@token_required
def gamehistory(current_user):
    user_id = current_user.get_data().get('id')
    query = f'''
        SELECT
            game_history.bet,
            game_history.win_amount,
            game_history.played_at,
            game_types.name
        FROM game_history
        JOIN game_types
        ON game_history.game_type_id = game_types.id
        WHERE game_history.user_id = {user_id}
        ORDER BY game_history.played_at DESC
        LIMIT 10
    '''

    result = db.query(query, cursor_settings={'dictionary': True})
    
    return result['result']

@app.route('/api/leaderboard', methods=['GET'])
def leaderboard():
    args = request.args
    filter = args.get('filter', 'total_winnings')
    sort = args.get('sort', 'DESC')
    
    # sanitation
    valid_columns = ('total_winnings', 'games_played', 'games_won', 'games_lost')
    if filter not in valid_columns:
        filter = 'total_winnings'
    if sort.lower() not in ('asc', 'desc'):
        sort = 'DESC'
    
    query = f'''
        SELECT 
            u.username as 'käyttäjänimi',
            s.total_winnings as 'kokonaisvoitot',
            s.games_played as 'pelejä pelattu',
            s.games_won as 'pelejä voitettu',
            s.games_lost as 'pelejä hävitty'
        FROM users u
        JOIN user_statistics s
        ON u.id = s.user_id
        WHERE u.hidden = 0
        ORDER BY {filter} {sort}
        LIMIT 10
    '''
    
    result = db.query(query, cursor_settings={'dictionary': True})
    
    return result['result']
    
@app.route('/api/games', methods=['GET', 'POST'])
def games(current_user: Player):
    user = current_user
    if request.method == 'GET': 

        return "Games"
    
@app.route('/api/games/dice', methods=['POST'])
@token_required
def dice_play(current_user: Player):
    data = request.json
    user = current_user

    try:
        bet = int(data.get('bet'))
        dice_amount = int(data.get('dice_amount'))
        guess = int(data.get('guess'))

        if bet<= 0 or bet > current_user.get_balance():
            return jsonify({'error': 'Invalid bet amount'}), 400

        playgame = Dice(user,db)

        outcome = playgame.start_game(bet,dice_amount, guess)

        return make_response(jsonify({
            'message': 'Game played successfully!',
            **outcome
        }), 200)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

@app.route('/api/games/coinflip', methods=['POST'])
@token_required
def coinflip_play(current_user: Player):
    data = request.json
    user = current_user
    
    try:
        bet = int(data.get('bet'))
        guess = data.get('guess') # 'k' or 'c'
        
        if bet <= 0 or bet > current_user.get_balance():
            return jsonify({'error': 'Invalid bet amount'}), 400
        
        playgame = Coinflip(user, db)
        
        outcome = playgame.start_game(bet, guess)
        
        return make_response(jsonify({
            'message': 'Game played successfully!',
            **outcome
        }), 200)
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

@app.route('/api/games/slots', methods=['POST'])
@token_required
def slots_play(current_user: Player):
    """
    Endpoint to play the Slots game.
    """
    data = request.json
    user = current_user

    try:
        # Retrieve bet amount from request
        bet = int(data.get('bet'))

        # Validate bet amount
        if bet <= 0 or bet > current_user.get_balance():
            return jsonify({'error': 'Invalid bet amount or insufficient balance'}), 400

        # Create a Slots game instance and play the game
        playgame = Slots(user, db)
        outcome = playgame.start_game(bet)

        # Respond with the game outcome
        return make_response(jsonify({
            'message': 'Slots game played successfully!',
            **outcome
        }), 200)

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Unexpected error: {str(e)}'}), 500

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

@app.route('/api/player/<int:id>', methods=['GET'])
def player(id):
    query = '''
        SELECT 
            u.username,
            s.balance,
            s.total_winnings,
            s.games_played,
            s.games_won,
            s.games_lost
        FROM users u
        JOIN user_statistics s
        ON u.id = s.user_id
        WHERE u.id = %s
    '''
    
    result = db.query(query, (id,), cursor_settings={'dictionary': True})
    
    return result['result'][0]