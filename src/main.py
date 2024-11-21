#src/main.py
# Código principal: UI, simulación y modelo Markov
import sys
from PyQt5.QtWidgets import QApplication
from markov_model import MarkovModel
from main_ui import MarkovChessBoard

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    # Inicializa el modelo Markov con el archivo filtrado
    markov_model = MarkovModel('data/filtered_ruy_lopez.pgn')
    
    # Pasa el modelo al tablero
    chess_board = MarkovChessBoard(markov_model)
    chess_board.show()
    
    sys.exit(app.exec_())

