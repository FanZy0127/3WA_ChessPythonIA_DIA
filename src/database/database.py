import os
import json
from os.path import join
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

dotenv_path = join(Path(__file__).parents[1], '.env')
load_dotenv(dotenv_path)

DB_NAME = os.environ.get('DB_NAME')
DB_HOSTNAME = os.environ.get('HOSTNAME')
DB_PASSWORD = os.environ.get('PASSWORD')
ADDRESS = os.environ.get('ADDRESS')
PORT = os.environ.get('PORT')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://' + DB_HOSTNAME + ':' + DB_PASSWORD + '@' + ADDRESS + ':' + \
                                        PORT + '/' + DB_NAME

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
        if db.session.query(BoardState).filter(BoardState.board_state == json.dumps(board_state)).first():
            return True

        return False

    @staticmethod
    def query_best_move_based_on_board_state_and_player(board_state, next_player_color):
        result = db.session.query(BoardState.best_move).filter(
                    BoardState.board_state == json.dumps(board_state),
                    BoardState.active_player == next_player_color).first()

        result_as_dict = result._asdict()

        return json.loads(result_as_dict["best_move"])

    @staticmethod
    def save_board_state(board_state, next_player_color, best_move):
        board_state = BoardState(
            json.dumps(board_state),
            next_player_color,
            json.dumps(best_move)
        )

        db.session.add(board_state)

        return db.session.commit()
