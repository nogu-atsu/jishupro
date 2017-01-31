#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pulp
import numpy as np
import time

def Solver(board):
    if type(board)==str:
        board = np.array([int(b) for b in board]).reshape(9,9)
    
    ## initialize
    prob = pulp.LpProblem('Sudoku', pulp.LpMinimize) # or minimize
    
    ## objective
    # No objective function
    prob += 0
    
    # make 
    numbers = range(1, 10)
    xs = range(1, 10)
    ys = range(1, 10)
    choices = pulp.LpVariable.dicts("Choice",(xs, ys, numbers),0,1,pulp.LpInteger)
    
    ## constraints
    #初期配置
    for x in range(9):
        for y in range(9):
            if board[y][x] > 0:
                prob += choices[board[y][x]][x+1][y+1] == 1 
    
    #1つのマスに入るのは1つ
    for y in ys:
        for x in xs:
            prob += pulp.lpSum([choices[v][x][y] for v in numbers]) == 1
    
    # 行・列・ボックス制約
    for v in numbers:
        for y in ys:
            prob += pulp.lpSum([choices[v][x][y] for x in xs]) == 1
    
        for x in xs:
            prob += pulp.lpSum([choices[v][x][y] for y in ys]) == 1
    
        for x in [1, 4, 7]:
            vs = []
            for y in [1, 4, 7]:
                #pint [[choices[v][x+i][y+j] for i in range(3) for j in range(3)]]
                prob += pulp.lpSum([[choices[v][x+i][y+j] for i in range(3) for j in range(3)]]) == 1
    
    s = prob.solve()
    result = np.zeros((9,9),dtype=np.int32)
    for y in ys:
        for x in xs:
            for v in numbers:
                if choices[v][x][y].value() == 1:
                    result[y-1][x-1]=v
    return result

if __name__=="__main__":
    board = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
    print(Solver(board))
