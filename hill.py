
import numpy as np


# Create Custom Exception Class MatrixNotInvertible
class MatrixNotInvertible(Exception):
    pass


class HillCipher:

    def __init__(self, mod):
        self.mod = mod

    # determinant() calculates determinant of inputted matrix
    # raises MatrixNotInvertible if needed
    def determinant(self, matrix):
        dim = matrix.shape
        if dim[0] != dim[1]:
            raise MatrixNotInvertible
        if np.linalg.det(matrix) == 0:
            raise MatrixNotInvertible
        return np.linalg.det(matrix)

    # invertible() checks to see if matrix is invertible or not.  returns boolean
    def invertible(self, matrix):
        det = self.determinant(matrix)
        if det != 0:
            return True
        else:
            return False

    # matrix_mod calculates new matrix based on mod division from matrix that is input into function
    # returns new matrix from division
    def matrix_mod(self, matrix):
        shape = matrix.shape
        mod_matrix = np.empty([shape[0], shape[1]], dtype=int)

        for i in range(shape[0]):
            for j in range(shape[1]):
                mod_matrix[i, j] = matrix[i, j] % self.mod

        return mod_matrix

    # matrix_transform creates new matrix from letter_key dictionary.  Either string or int matrix
    def matrix_transform(self, phrase_matrix):
        letter_key = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7, "I": 8, "J": 9, "K": 10,
                      "L": 11, "M": 12, "N": 13, "O": 14, "P": 15, "Q": 16, "R": 17, "S": 18, "T": 19, "U": 20,
                      "V": 21, "W": 22, "X": 23, "Y": 24, "Z": 25}

        shape = phrase_matrix.shape
        row = shape[0]
        column = shape[1]
        new_int_matrix = np.empty([row, column], dtype=int)
        new_string_matrix = np.empty([row, column], dtype=str)

        # if matrix input into method is strings convert all strings into associated numbers in dictionary
        # returns new int matrix
        if isinstance(phrase_matrix[0, 0], str):
            for i in range(row):
                for j in range(column):
                    new_int_matrix[i, j] = letter_key[phrase_matrix[i, j]]

            return new_int_matrix

        # if matrix input into method is ints convert all strings into associated letters in dictionary
        # returns new string matrix
        else:
            key_list = list(letter_key.keys())
            value_list = list(letter_key.values())
            for i in range(row):
                for j in range(column):
                    index = value_list.index(phrase_matrix[i, j])
                    new_string_matrix[i, j] = key_list[index]

            return new_string_matrix

    # convert string matrix from array to string
    # returns the array as a string
    def toString(self, string_matrix):
        cipher_string = ""
        shape = string_matrix.shape
        for x in range(shape[1]):
            for row in range(shape[0]):
                cipher_string += string_matrix[row, x]

        return cipher_string

    # encrypt phrase with the key_matrix
    def encrypt(self, key_matrix, phrase):

        length = len(phrase)
        column = int(length / 2)
        i = 0

        # create empty array based on length of the phrase
        phrase_matrix = np.empty([2, column], dtype=str)

        # populate new array sequentially from each letter in phrase
        for x in range(column):
            for row in range(2):
                phrase_matrix[row, x] = phrase[i]
                i += 1
        print(f'PlainText: {phrase}')
        print(f'PlainText Array:\n {self.matrix_transform(phrase_matrix)}\n')

        # transform letter matrix into numbers
        message_array = self.matrix_transform(phrase_matrix)

        encrypted_array = np.empty([2, column], dtype=int)

        # encrypt message array using dot products and mod division
        for n in range(column):
            # column of message array taken
            vector = np.array([[message_array[0, n]], [message_array[1, n]]])

            # dot product performed
            dot = np.dot(key_matrix, vector)

            # mod division performed
            new_vector = self.matrix_mod(dot)

            # mod divistion arrays combined into encrypted array
            encrypted_array[0, n] = new_vector[0, 0]
            encrypted_array[1, n] = new_vector[1, 0]

            # encrypted array numbers changed to strings
            cipher_array = self.matrix_transform(encrypted_array)

        # print new encrypted string and numerical array
        print(f'CipherText: {self.toString(cipher_array)}')
        print(f'CipherText Array:\n {encrypted_array}\n')

        # returns the cipher text string array
        return self.matrix_transform(encrypted_array)

    # decrypts encrypted aray using given key
    def decrypt(self, cipher_key, cipher_array):
        det = int(self.determinant(cipher_key))

        # inverse of key matrix taken
        key_inverse = np.empty([2, 2], dtype=int)
        key_inverse[0, 0] = cipher_key[1, 1] % self.mod
        key_inverse[1, 0] = -cipher_key[1, 0] % self.mod
        key_inverse[0, 1] = -cipher_key[0, 1] % self.mod
        key_inverse[1, 1] = cipher_key[0, 0] % self.mod

        # multiplicative modular matrix multiplier determined
        for multiplier in range(self.mod):
            if ((det * multiplier) % self.mod == 1):
                break  # once first value is found loop is stopped

        # inverse matrix has modular division performed on it
        k_inverse = self.matrix_mod(multiplier * key_inverse)

        # encrypted cypher array (strings) is converted to ints
        cipher_array_num = self.matrix_transform(cipher_array)

        # new empty array initialized
        decrypted_array = np.empty([cipher_array_num.shape[0], cipher_array_num.shape[1]], dtype=int)
        for n in range(cipher_array.shape[1]):
            vector = np.array([[cipher_array_num[0, n]], [cipher_array_num[1, n]]],)
            dot = np.dot(k_inverse, vector)
            new_vector = self.matrix_mod(dot)
            decrypted_array[0, n] = new_vector[0, 0]
            decrypted_array[1, n] = new_vector[1, 0]

            # modular division performed on decrypted array
            decrypted_int = self.matrix_mod(decrypted_array)

        # int array transformed and string of original message put in an array
        og_message_matrix = self.matrix_transform(decrypted_int)

        # string array turned into string (original message)
        og_message = self.toString(og_message_matrix)

        # original message and array displayed
        print(f'PlainText: {og_message}')
        print(f'PlainText Array: \n{decrypted_int}\n')

        return og_message


if __name__ == "__main__":
    key1 = np.array([[19, 8, 4], [3, 12, 7]])
    key2 = np.array([[7, 8], [11, 11]])
    key3 = np.array([[5, 15], [4, 12]])

    keys = [key1, key2, key3]

    # new class created
    code = HillCipher(26)

    # loop over all the arrays
    for key in keys:
        try:
            if code.invertible(key):
                print("\nMatrix is Invertible\n")
                encrypted = code.encrypt(key, 'ATTACKATDAWN')
                decrypted = code.decrypt(key, encrypted)

        # exception raised if matrix is not invertible messages displayed
        except MatrixNotInvertible:
            if key.shape[0] != key.shape[1]:
                print('\nMatrix is not a square')
            else:
                print('The determinant = 0')


