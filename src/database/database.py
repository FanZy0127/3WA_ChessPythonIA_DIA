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
        print(f'-----------------------------------------------')
        print(f'Requesting board to the Chess database')
        # print(f'BOARD STATE BEFORE JSONIFY : {board_state}')
        # print(f'BOARD STATE AFTER JSONIFY : {json.dumps(board_state)}')
        print(
            f'REQUEST RESULT : '
            f'{db.session.query(BoardState).filter(BoardState.board_state == json.dumps(board_state)).first()}'
        )
        if db.session.query(BoardState).filter(BoardState.board_state == json.dumps(board_state)).first():
            print('TRUE ==> THE REQUEST WORKED OUT !!!')
            return True

        print('FALSE ==> THE REQUEST FAILED !!!')
        return False

    @staticmethod
    def query_best_move_based_on_board_state_and_player(board_state, next_player_color):
        # print(f'-----------------------------------------------')
        # print(f'Requesting BEST MOVE to the Chess database')
        # print(f'BOARD STATE : {json.dumps(board_state)}')
        # print(f'PLAYER COLOR : {next_player_color}')

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
