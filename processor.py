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
        self.running = True
        while self.running:
            for index, option in enumerate(self.options):
                print(f'{index+1}. {option}')
            print(f'0. {self.exit_phrase}')
            try:
                choice = int(input(self.input_phrase))
                if 0 < choice <= len(self.options):
                    choice = list(self.options.keys())[choice-1]
                    self.options[choice]()
                elif choice == 0:
                    self.running = False
                else:
                    self.invalid_choice()
            except ValueError:
                self.invalid_choice()


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


options = {
    'Add matrices': add_matrix,
    'Multiply matrix by a constant': scalar_multiplication,
    'Multiply matrices': matrix_multiplication,
}
input_phrase = 'Your choice: '
exit_phrase = 'Exit'

menu = Menu(input_phrase, exit_phrase, options)
try:
    menu.start()
except (MatrixDimensionMismatch, ValueError, InsufficientInformation, EmptyMatrix, IllegalData):
    print('ERROR')
