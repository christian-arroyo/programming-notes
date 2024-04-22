from typing import List

def isValidSudoku(board: List[List[str]]) -> bool:
    def is_row_valid(lst):
        s = set()
        count = 0
        for c in lst:
            if c != '.':
                s.add(c)
                count += 1
        return True if len(s) == count else False

    def is_column_valid(column_index, board):
        s = set()
        count = 0
        for row_index in range(9):
            cell = board[row_index][column_index]
            if cell != '.':
                s.add(cell)
                count += 1
        return True if len(s) == count else False
        
    def is_square_valid(board, row_index, column_index):
        s = set()
        count = 0
        for i in range(row_index, row_index + 3):
            for j in range(column_index, column_index + 3):
                cell = board[i][j]
                if cell != '.':
                    s.add(cell)
                    count += 1
        return True if len(s) == count else False
    
    # Check that all rows are valid
    for row in board:
        if not is_row_valid(row):
            return False
    
    # Check that all columns are valid
    for column_number in range(0, 9):
        result = is_column_valid(column_number, board)
        if not is_column_valid(column_number, board):
            return False
    
    # Check that all squares are valid
    for i in range(0, 9, 3):
        for j in range(0, 9, 3):
            if not is_square_valid(board, i, j):
                return False
    
    return True

board_true = [["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]
board_false = [["8","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]

print(isValidSudoku(board_true))