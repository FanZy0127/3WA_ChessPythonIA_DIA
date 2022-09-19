import os
import chess
import chess.engine
import numpy
import pydotplus
import keras.utils
import keras.models as models
import keras.layers as layers
from keras.utils import plot_model
import keras.callbacks as callbacks
import keras.optimizers as optimizers

os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz/bin/'
keras.utils.vis_utils.pydot = pydotplus

SQUARE_INDEXES = {
    'a': 0,
    'b': 1,
    'c': 2,
    'd': 3,
    'e': 4,
    'f': 5,
    'g': 6,
    'h': 7
}


def generate_board_from_fen(fen: str):
    return chess.Board(fen)


def get_current_score(board, depth):
    with chess.engine.SimpleEngine.popen_uci('stockfish/stockfish_15_x64_popcnt') as sf:
        result = sf.analyse(board, chess.engine.Limit(depth=depth))
        score = result['score'].white().score()

        return score


# example: h3 -> 17
def square_to_index(square):
    letter = chess.square_name(square)
    return 8 - int(letter[1]), SQUARE_INDEXES[letter[0]]


def split_dims(board):
    # this is the 3d matrix
    board3d = numpy.zeros((14, 8, 8), dtype=numpy.int8)

    # here we add the pieces's view on the matrix
    for piece in chess.PIECE_TYPES:
        for square in board.pieces(piece, chess.WHITE):
            idx = numpy.unravel_index(square, (8, 8))
            board3d[piece - 1][7 - idx[0]][idx[1]] = 1
        for square in board.pieces(piece, chess.BLACK):
            idx = numpy.unravel_index(square, (8, 8))
            board3d[piece + 5][7 - idx[0]][idx[1]] = 1

    # add attacks and valid moves too
    # so the network knows what is being attacked
    aux = board.turn
    board.turn = chess.WHITE
    for move in board.legal_moves:
        i, j = square_to_index(move.to_square)
        board3d[12][i][j] = 1
    board.turn = chess.BLACK
    for move in board.legal_moves:
        i, j = square_to_index(move.to_square)
        board3d[13][i][j] = 1
    board.turn = aux

    return board3d


def build_model(conv_size, conv_depth):
    board3d = layers.Input(shape=(14, 8, 8))

    # adding the convolutional layers
    x = board3d
    for _ in range(conv_depth):
        x = layers.Conv2D(filters=conv_size, kernel_size=3, padding='same', activation='relu')(x)
    x = layers.Flatten()(x)
    x = layers.Dense(64, 'relu')(x)
    x = layers.Dense(1, 'sigmoid')(x)

    return models.Model(inputs=board3d, outputs=x)


def build_model_residual(conv_size, conv_depth):
    board3d = layers.Input(shape=(14, 8, 8))

    # adding the convolutional layers
    x = layers.Conv2D(filters=conv_size, kernel_size=3, padding='same')(board3d)
    for _ in range(conv_depth):
        previous = x
        x = layers.Conv2D(filters=conv_size, kernel_size=3, padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Activation('relu')(x)
        x = layers.Conv2D(filters=conv_size, kernel_size=3, padding='same')(x)
        x = layers.BatchNormalization()(x)
        x = layers.Add()([x, previous])
        x = layers.Activation('relu')(x)
    x = layers.Flatten()(x)
    x = layers.Dense(1, 'sigmoid')(x)

    return models.Model(inputs=board3d, outputs=x)


def get_dataset():
    container = numpy.load('data/dataset/dataset.npz')
    b, v = container['b'], container['v']
    v = numpy.asarray(v / abs(v).max() / 2 + 0.5, dtype=numpy.float32)  # normalization (0 - 1)
    return b, v


def train_model(model, x_train, y_train):
    model.compile(optimizer=optimizers.Adam(5e-4), loss='mean_squared_error')
    model.summary()
    model.fit(x_train, y_train,
              batch_size=2048,
              epochs=20,
              verbose=1,
              validation_split=0.1,
              callbacks=[callbacks.ReduceLROnPlateau(monitor='loss', patience=10),
                         callbacks.EarlyStopping(monitor='loss', patience=15, min_delta=1e-4)])

    model.save('models/ai_models/model.h5')


# used for the minimax algorithm
def minimax_eval(board, model):
    board3d = split_dims(board)
    board3d = numpy.expand_dims(board3d, 0)
    return model(board3d)[0][0]


def minimax(board, depth, alpha, beta, maximizing_player):
    # model = build_model(32, 4)
    # plot_model(model, to_file='model_plot.png', show_shapes=True, show_layer_names=False)
    model = build_model_residual(32, 4)
    # plot_model(model, to_file='model_plot.png', show_shapes=True, show_layer_names=False)

    if depth == 0 or board.is_game_over():
        return minimax_eval(board, model)

    if maximizing_player:
        max_eval = -numpy.inf
        for move in board.legal_moves:
            board.push(move)
            min_max_eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, min_max_eval)
            alpha = max(alpha, min_max_eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = numpy.inf
        for move in board.legal_moves:
            board.push(move)
            min_max_eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, min_max_eval)
            beta = min(beta, min_max_eval)
            if beta <= alpha:
                break
        return min_eval


# this is the actual function that gets the move from the neural network
def get_ai_move(fen, depth):
    board = generate_board_from_fen(fen)
    print(f'BOARD AS READ BY THE NETWORK : \n{board}')
    best_move = None
    max_eval = -numpy.inf

    for move in board.legal_moves:
        board.push(move)
        min_max_eval = minimax(board, depth - 1, -numpy.inf, numpy.inf, False)
        board.pop()
        if min_max_eval > max_eval:
            max_eval = min_max_eval
            best_move = move

    return best_move
