'''
Matrix utility functions.
'''

def get_array_shape(array):
    '''
    Determine the dimensions of the array for error handling.
    '''
    if len(array) < 1:
        return [0]

    if isinstance(array[0], list):
        for i in array:
            if len(i) != len(array[0]):
                raise TypeError("Must be a valid tensor.")

        return [len(array)] + get_array_shape(array[0])
    
    else:
        return [len(array)]

class Matrix:
    '''
    Very basic Matrix class.

    Could easily be replaced with numpy.
    '''
    def __init__(self, array):
        if len(get_array_shape(array)) != 2: # Unnecessary error handling.
            raise TypeError("Must be a valid matrix.")

        self.array = array

    @property
    def shape(self):
        return get_array_shape(self.array)

    @property
    def T(self):
        '''
        Return the transposed matrix.
        '''
        t = [[] for i in range(len(self.array[0]))]

        for j in range(len(self.array)):
            for i in range(len(self.array[0])):
                t[i].append(self.array[j][i])

        return Matrix(t)

    def __mul__(self, other):
        '''
        Compute dot product of two matrices.
        '''
        if self.shape[1] != other.shape[0]: # Check that matrices are n x m and m x p.
            raise ValueError("Incompatible matrix shapes.")

        t = [[0 for p in range(other.shape[1])] for n in range(self.shape[0])] # Initialize an n x p matrix.

        for n in range(self.shape[0]):
            for p in range(other.shape[1]):
                t[n][p] = sum([self[(n, k)] * other[(k, p)] for k in range(self.shape[1])])

        return Matrix(t)

    def __getitem__(self, args): # *args is not supported in python3 for getitem
        if len(args) == 1:
            return self.array[args[0]]

        elif len(args) == 2:
            return self.array[args[0]][args[1]]

        else:
            raise IndexError("Invalid index.") 

    def __repr__(self):
        '''
        Print matrix for debugging.
        '''
        return str(self.array)

    def __eq__(self, other):
        '''
        Check if a value is in the matrix.
        '''
        return any([any([i == other for i in j]) for j in self.array])

    @property
    def trace(self):
        '''
        Sum of primary diagonal
        '''
        if self.shape[0] != self.shape[1]:
            raise TypeError('Must be a square matrix')

        return sum([self.array[i][i] for i in range(self.shape[0])])

    @property
    def sec_trace(self):
        '''
        Sum of secondary diagonal
        '''
        if self.shape[0] != self.shape[1]:
            raise TypeError('Must be a square matrix')

        return sum([self.array[i][self.shape[0]-1-i] for i in range(self.shape[0])])

'''
Actual tictactoe starts here.
'''

board = Matrix([
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0]
])

def check_winner(board):
    '''
    Check if the game has a winner.
    Matrices are more elegant and efficient than brute force.
    '''
    rows = board * Matrix([[1, 1, 1]]).T # if any row has same values.
    columns = board.T * Matrix([[1, 1, 1]]).T # if any column has same values.

    if rows == 3 or columns == 3 or board.trace == 3 or board.sec_trace == 3: return 1 # and check the diagonals.
    elif rows == -3 or columns == -3 or board.trace == -3 or board.sec_trace == -3: return -1
    
    return 0 

def pretify_board(board):
    '''
    Convert the board into a printable string.
    '''
    strings = [' ', 'X', 'O']
    return '\n-+-+-\n'.join(['|'.join([strings[i] for i in j]) for j in board.array])

turn = 1

while check_winner(board) == 0:
    print(pretify_board(board))

    i = int(input(f'\n {"X " if turn > 0 else "O "}'))

    if board.array[i//3][i % 3] != 0: # Make sure that the square isn't already taken.
        while board.array[i//3][i % 3] != 0:
            print('This square is already taken')
            i = int(input(f'\n {"X " if turn > 0 else "O "}'))

    board.array[i//3][i % 3] = turn

    turn = turn * -1

print(pretify_board(board))
print(f'The winner is {"O" if turn > 0 else "X"}')