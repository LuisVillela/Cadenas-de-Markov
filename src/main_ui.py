#src/main_ui.py
import chess
import random
from PyQt5.QtWidgets import QMainWindow, QLabel, QPushButton
from PyQt5.QtGui import QPainter, QColor, QPixmap
from PyQt5.QtCore import Qt
import os

class MarkovChessBoard(QMainWindow):
    def __init__(self, markov_model):
        super().__init__()
        self.board = chess.Board()
        self.markov_model = markov_model
        self.piece_images = self.load_piece_images()
        self.selected_piece = None
        self.selected_piece_square = None
        self.current_drag_position = None
        self.init_ui()

    def load_piece_images(self):
        base_path = os.path.abspath('images')
        return {
            'P': QPixmap(f'{base_path}/wp.png'), 'p': QPixmap(f'{base_path}/bp.png'),
            'R': QPixmap(f'{base_path}/wr.png'), 'r': QPixmap(f'{base_path}/br.png'),
            'N': QPixmap(f'{base_path}/wn.png'), 'n': QPixmap(f'{base_path}/bn.png'),
            'B': QPixmap(f'{base_path}/wb.png'), 'b': QPixmap(f'{base_path}/bb.png'),
            'Q': QPixmap(f'{base_path}/wq.png'), 'q': QPixmap(f'{base_path}/bq.png'),
            'K': QPixmap(f'{base_path}/wk.png'), 'k': QPixmap(f'{base_path}/bk.png'),
        }

    def init_ui(self):
        self.setWindowTitle('Chess Game with Markov Model')
        self.setGeometry(100, 100, 800, 800)
        self.status_label = QLabel('Turn: White', self)
        self.status_label.setGeometry(650, 750, 140, 30)
        self.restart_button = QPushButton('Restart', self)
        self.restart_button.setGeometry(650, 20, 140, 30)
        self.restart_button.clicked.connect(self.restart_game)

    def restart_game(self):
        self.board.reset()
        self.selected_piece = None
        self.selected_piece_square = None
        self.current_drag_position = None
        self.update_status()
        self.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            square_size = self.width() // 8
            col = event.x() // square_size
            row = 7 - (event.y() // square_size)
            self.selected_piece_square = chess.square(col, row)
            self.selected_piece = self.board.piece_at(self.selected_piece_square)
            if self.selected_piece and (self.selected_piece.color == self.board.turn):
                self.current_drag_position = (event.x(), event.y())

    def mouseMoveEvent(self, event):
        if self.selected_piece is not None:
            self.current_drag_position = (event.x(), event.y())
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.selected_piece is not None:
            square_size = self.width() // 8
            col = event.x() // square_size
            row = 7 - (event.y() // square_size)
            target_square = chess.square(col, row)
            move = chess.Move(self.selected_piece_square, target_square)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.selected_piece = None
                self.selected_piece_square = None
                self.current_drag_position = None
                self.update_status()
                self.update()
                self.computer_move()
            else:
                self.selected_piece = None
                self.selected_piece_square = None
                self.current_drag_position = None
                self.update()

    def update_status(self):
        if self.board.is_checkmate():
            winner = 'White' if not self.board.turn else 'Black'
            self.status_label.setText(f'Checkmate! {winner} wins.')
        elif self.board.is_stalemate():
            self.status_label.setText('Stalemate! It\'s a draw.')
        elif self.board.is_insufficient_material():
            self.status_label.setText('Draw! Insufficient material.')
        else:
            turn = 'White' if self.board.turn else 'Black'
            self.status_label.setText(f'Turn: {turn}')

    def computer_move(self):
        if self.board.is_game_over():
            return
        state = self.board.fen()
        legal_moves = list(self.board.legal_moves)
        best_move = self.markov_model.get_best_move(state, legal_moves)
        if best_move:
            self.board.push(best_move)
        else:
            self.board.push(random.choice(legal_moves))
        self.update_status()
        self.update()

    def paintEvent(self, event):
        qp = QPainter(self)
        self.draw_board(qp)
        if self.current_drag_position and self.selected_piece:
            piece_pixmap = self.piece_images.get(self.selected_piece.symbol())
            if piece_pixmap:
                square_size = self.width() // 8
                qp.drawPixmap(
                    self.current_drag_position[0] - square_size // 2,
                    self.current_drag_position[1] - square_size // 2,
                    square_size, square_size,
                    piece_pixmap
                )

    def draw_board(self, qp):
        board_size = 8
        square_size = self.width() // board_size
        colors = [QColor(240, 217, 181), QColor(181, 136, 99)]
        for row in range(board_size):
            for col in range(board_size):
                color = colors[(row + col) % 2]
                qp.setBrush(color)
                qp.drawRect(col * square_size, (7 - row) * square_size, square_size, square_size)
                piece = self.board.piece_at(chess.square(col, row))
                if piece and not (self.selected_piece and self.selected_piece_square == chess.square(col, row)):
                    piece_pixmap = self.piece_images.get(piece.symbol())
                    if piece_pixmap:
                        qp.drawPixmap(
                            col * square_size,
                            (7 - row) * square_size,
                            square_size,
                            square_size,
                            piece_pixmap
                        )
