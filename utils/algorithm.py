#initialize_board -> Das Board wird geladen
#get_valid_moves -> Regelset für die Figuren
#make_move -> Die Bewegung wird ausgeführt
#evaluate_board -> Das neue Board wird übertragen
#is_terminal_state -> Ist das Spiel schon gewonnen?


class Algorithm:
    def __init__(self):
        self.board = self.initialize_board()
        self.current_turn = 1  # 1 for player 1, -1 for player 2


    def minimax(self, board, depth, maximizing_player):
        if depth == 0 or self.is_terminal_state(board):
            return self.evaluate_board(board), None

        valid_moves = self.get_valid_moves(board, 1 if maximizing_player else -1)

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in valid_moves:
                new_board = self.make_move(board, move)
                eval, _ = self.minimax(new_board, depth - 1, False)
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in valid_moves:
                new_board = self.make_move(board, move)
                eval, _ = self.minimax(new_board, depth - 1, True)
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
            return min_eval, best_move


    def find_best_move(self, depth):
        _, best_move = self.minimax(self.board, depth, True if self.current_turn == 1 else False)
        return best_move
