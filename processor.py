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

    def __init__(self, x: int = 0, y: int = 0, generate_matrix=False):
        if x and y:
            if generate_matrix:
                matrix = [[0 for _ in range(y)] for __ in range(x)]
            else:
                matrix = []
                for _ in range(x):
                    try:
                        row: list = list(map(int, input().split()))
                    except ValueError:
                        raise IllegalData
                    if len(row) == y:
                        matrix.append(row)
                    else:
                        raise InsufficientInformation
        else:
            raise EmptyMatrix
        self.x: int = x
        self.y: int = y
        self.__matrix__ = matrix

    @classmethod
    def empty_matrix(cls, x, y):
        return cls(x, y, True)

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


try:
    matA = Matrix(*map(int, input().split()))
    matB = Matrix(*map(int, input().split()))
    matC = matA + matB
    print(matC)
except (MatrixDimensionMismatch, ValueError, InsufficientInformation, EmptyMatrix, IllegalData):
    print('ERROR')
