import json
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/chess'

app.app_context().push()

db = SQLAlchemy(app)


class BoardState(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    board_state = db.Column(db.Text, nullable=False)
    active_player = db.Column(db.Enum('black', 'white'), nullable=False)
    best_move = db.Column(db.Text, nullable=False)

    def __init__(self, board_state, active_player, best_move):
        self.board_state = board_state
        self.active_player = active_player
        self.best_move = best_move

    @staticmethod
    def create_database():
        return db.create_all()

    @staticmethod
    def query_board_state(board_state):
        return BoardState.query(BoardState).filter_by(BoardState.board_state == json.dumps(board_state)).first()

    @staticmethod
    def query_board_state_based_on_player(board_state, next_player_color):
        return BoardState.query(BoardState.best_move).filter_by(
            BoardState.board_state == json.dumps(board_state) and BoardState.active_player is not next_player_color)

    @staticmethod
    def save_board_state(board_state, next_player_color, best_move):
        board_state = BoardState(
            json.dumps(board_state),
            next_player_color,
            json.dumps(best_move)
        )

        db.session.add(board_state)

        return db.session.commit()
