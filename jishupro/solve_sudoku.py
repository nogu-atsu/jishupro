import tensorflow as tf
import numpy as np
from recog_sudoku3 import Recog_Sudoku
from classifier2 import CNN
from sudoku2 import Solver

if __name__ == "__main__":
    cnn = CNN()
    y=np.zeros((81,10))
    for i in range(1):
        sudoku,_,_ = Recog_Sudoku(mode=1,image="DSC_0289.jpg")
        sudoku = sudoku.reshape(81,32,32,1)
        y+= cnn(sudoku)
    digits = np.argmax(y,axis=1).reshape(9,9)
        
    print(digits)
    print(Solver(digits))
    
