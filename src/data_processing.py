#src/data_processing.py
#Procesamiento de datos PGN para filtrar partidas de la Ruy López
import chess
import chess.pgn

def filter_games_for_ruy_lopez(pgn_path, output_path):
    with open(pgn_path) as f, open(output_path, 'w') as out:
        while True:
            game = chess.pgn.read_game(f)
            if game is None:
                break
            board = game.board()
            moves = list(game.mainline_moves())
            # Verificar si las primeras jugadas coinciden con la Ruy López
            if len(moves) >= 3 and moves[:3] == [
                chess.Move.from_uci('e2e4'),
                chess.Move.from_uci('e7e5'),
                chess.Move.from_uci('g1f3')
            ]:
                out.write(str(game) + '\n')

# Ejecuta el filtro para generar un archivo reducido
if __name__ == '__main__':
    filter_games_for_ruy_lopez('data/RuyLopezClassical.pgn', 'data/filtered_ruy_lopez.pgn')
