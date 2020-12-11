from collections import OrderedDict


# Matrix Base Exceptions
class MatrixDimensionMismatch(Exception):
    pass


class EmptyMatrix(Exception):
    pass


class InsufficientInformation(Exception):
    pass


class IllegalData(Exception):
    pass


class ImpossibleDeterminant(Exception):
    pass

class Matrix:
    supported_data = [int, float]

    def __init__(self, x: int = 0, y: int = 0, matrix=None):
        if x and y:
            if not (isinstance(matrix, list) and isinstance(matrix[0], list)):
                matrix = [[0 for _ in range(y)] for __ in range(x)]
        else:
            raise EmptyMatrix
        self.x: int = x
        self.y: int = y
        self.__matrix__ = matrix

    @classmethod
    def empty_matrix(cls, x, y):
        return cls(x, y, True)

    @property
    def main_transpose(self):
        matR = Matrix(self.y, self.x)
        for i in range(matR.x):
            for j in range(matR.y):
                matR.__matrix__[i][j] = self.__matrix__[j][i]
        return matR

    @property
    def side_transpose(self):
        matR = Matrix(self.y, self.x)
        for i in range(matR.x):
            for j in range(matR.y):
                matR.__matrix__[i][j] = self.__matrix__[self.y-j-1][self.x-i-1]
        return matR

    @property
    def vertical_transpose(self):
        matR = Matrix(self.x, self.y)
        for i in range(matR.x):
            for j in range(matR.y):
                matR.__matrix__[i][j] = self.__matrix__[i][self.y-j-1]
        return matR

    @property
    def horizontal_transpose(self):
        matR = Matrix(self.x, self.y)
        for i in range(matR.x):
            for j in range(matR.y):
                matR.__matrix__[i][j] = self.__matrix__[self.x-i-1][j]
        return matR

    def minor(self, i, j):
        matS = Matrix(self.x-1, self.y-1)
        for k in range(self.x):
            for l in range(self.y):
                if k < i and l < j:
                    matS.__matrix__[k][l] = self.__matrix__[k][l]
                if k < i and l > j:
                    matS.__matrix__[k][l-1] = self.__matrix__[k][l]
                if k > i and l < j:
                    matS.__matrix__[k-1][l] = self.__matrix__[k][l]
                if k > i and l > j:
                    matS.__matrix__[k-1][l-1] = self.__matrix__[k][l]
        return matS.determinant

    def cofactor(self, i, j):
        return (-1) ** (i + j) * self.minor(i, j)

    @property
    def determinant(self):
        if self.x != self.y:
            raise ImpossibleDeterminant
        if self.x == 1:
            return self.__matrix__[0][0]
        det = 0
        for j in range(self.y):
            det += self.cofactor(0, j) * self.__matrix__[0][j]
        return det

    def get_matrix(self):
        for i in range(self.x):
            try:
                row: list = list(map(float, input().split()))
            except ValueError:
                raise IllegalData
            if len(row) == self.y:
                self.__matrix__[i] = row
            else:
                raise InsufficientInformation

    def __add__(self, mat):
        if self.x == mat.x and self.y == mat.y:
            matR = Matrix.empty_matrix(self.x, self.y)
            for i in range(self.x):
                for j in range(self.y):
                    matR.__matrix__[i][j] = self.__matrix__[i][j] + mat.__matrix__[i][j]
            return matR
        else:
            raise MatrixDimensionMismatch

    def __repr__(self):
        return "\n".join([" ".join([str(self.__matrix__[x][y]) for y in range(self.y)]) for x in range(self.x)])

    def __str__(self):
        return "\n".join([" ".join([str(self.__matrix__[x][y]) for y in range(self.y)]) for x in range(self.x)])

    def __mul__(self, y):
        if isinstance(y, Matrix):
            mat = y
            if self.y == mat.x:
                matR = Matrix(self.x, mat.y)
                for i in range(self.x):
                    for j in range(mat.y):
                        for k in range(self.y):
                            matR.__matrix__[i][j] += self.__matrix__[i][k] * mat.__matrix__[k][j]
                return matR
            else:
                raise MatrixDimensionMismatch
        elif type(y) in self.supported_data:
            matR = Matrix.empty_matrix(self.x, self.y)
            for i in range(self.x):
                for j in range(self.y):
                    matR.__matrix__[i][j] = self.__matrix__[i][j] * y
            return matR


class Menu:

    def __init__(self, input_phrase: str = '', exit_phrase: str = '', options=None):
        if not options:
            options = OrderedDict()
        self.options: OrderedDict = options
        self.exit_phrase: str = exit_phrase
        self.input_phrase: str = input_phrase
        self.running: bool = False

    def invalid_choice(self):
        print('Invalid Choice')
        print(f'Enter a Number Between 0-{len(self.options)}')

    def start(self):
        for index, option in enumerate(self.options):
            print(f'{index + 1}. {option}')
        print(f'0. {self.exit_phrase}')
        try:
            choice = int(input(self.input_phrase))
            if 0 < choice <= len(self.options):
                choice = list(self.options.keys())[choice - 1]
                self.options[choice]()
            elif choice == 0:
                self.running = False
            else:
                self.invalid_choice()
        except ValueError:
            self.invalid_choice()

    def loop(self):
        self.running = True
        while self.running:
            self.start()



def add_matrix():
    matA = Matrix(*map(int, input('Enter size of first matrix: ').split()))
    print('Enter first matrix:')
    matA.get_matrix()
    matB = Matrix(*map(int, input('Enter size of second matrix: ').split()))
    print('Enter second matrix:')
    matB.get_matrix()
    matC = matA + matB
    print('The result is')
    print(matC)
    print()


def scalar_multiplication():
    matA = Matrix(*map(int, input('Enter size of matrix: ').split()))
    print('Enter matrix:')
    matA.get_matrix()
    scalar = float(input('Enter constant: '))
    matC = matA * scalar
    print('The result is')
    print(matC)
    print()


def matrix_multiplication():
    matA = Matrix(*map(int, input('Enter size of first matrix: ').split()))
    print('Enter first matrix:')
    matA.get_matrix()
    matB = Matrix(*map(int, input('Enter size of second matrix: ').split()))
    print('Enter second matrix:')
    matB.get_matrix()
    matC = matA * matB
    print('The result is')
    print(matC)
    print()


def matrix_determinant():
    matA = Matrix(*map(int, input('Enter size of matrix: ').split()))
    print('Enter matrix:')
    matA.get_matrix()
    print('The result is')
    print(matA.determinant)
    print()

def matrix_transpose():
    # Default Transpose Type
    print()
    global transpose_type

    def main_transpose():
        global transpose_type
        transpose_type = 'main'

    def side_transpose():
        global transpose_type
        transpose_type = 'side'

    def vertical_transpose():
        global transpose_type
        transpose_type = 'vertical'

    def horizontal_transpose():
        global transpose_type
        transpose_type = 'horizontal'

    transpose_options = {
        'Main diagonal': main_transpose,
        'Side diagonal': side_transpose,
        'Vertical line': vertical_transpose,
        'Horizontal line': horizontal_transpose,
    }
    input_phrase = 'Your choice: '
    exit_phrase = 'Exit'
    transpose_menu = Menu(input_phrase, exit_phrase, transpose_options)
    try:
        transpose_menu.start()
    except (MatrixDimensionMismatch, ValueError, InsufficientInformation, EmptyMatrix, IllegalData):
        print('ERROR')
    matA = Matrix(*map(int, input('Enter size of matrix: ').split()))
    print('Enter matrix:')
    matA.get_matrix()
    print(f"{transpose_type}_transpose")
    print('The result is')
    print(getattr(matA, f"{transpose_type}_transpose"))
    print()


options = {
    'Add matrices': add_matrix,
    'Multiply matrix by a constant': scalar_multiplication,
    'Multiply matrices': matrix_multiplication,
    'Transpose matrix': matrix_transpose,
    'Calculate a determinant': matrix_determinant,
}
input_phrase = 'Your choice: '
exit_phrase = 'Exit'
transpose_type = 'main'
menu = Menu(input_phrase, exit_phrase, options)
try:
    menu.loop()
except (MatrixDimensionMismatch, ValueError, InsufficientInformation, EmptyMatrix, IllegalData):
    print('ERROR')
