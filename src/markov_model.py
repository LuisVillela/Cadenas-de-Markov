#src/markov_model.py
# Funciones para manejar la matriz de transición y jugadas
import chess
import chess.pgn
from collections import defaultdict

class MarkovModel:
    def __init__(self, pgn_path):
        self.transition_matrix = self.build_transition_matrix(pgn_path)

    def build_transition_matrix(self, pgn_path):
        matrix = defaultdict(lambda: defaultdict(int))
        with open(pgn_path) as f:
            while True:
                game = chess.pgn.read_game(f)
                if game is None:
                    break
                board = game.board()
                for move in game.mainline_moves():
                    state = board.fen()
                    board.push(move)
                    next_state = board.fen()
                    matrix[state][move.uci()] += 1

        # Convertir frecuencias a probabilidades
        for state, transitions in matrix.items():
            total = sum(transitions.values())
            for move in transitions:
                transitions[move] /= total
        return dict(matrix)

    def get_best_move(self, state, legal_moves):
        if state in self.transition_matrix:
            probabilities = self.transition_matrix[state]
            moves = [(move, probabilities.get(move.uci(), 0)) for move in legal_moves]
            moves = sorted(moves, key=lambda x: x[1], reverse=True)
            return moves[0][0] if moves else None
        return None
