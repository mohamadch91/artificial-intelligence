import operator
import os
import re
from typing import List, Tuple
from copy import deepcopy
from itertools import permutations
os.system("")


class style():
    BLACK = '\033[30m'
    RED = '\033[41m'
    GREEN = '\033[42m'
    YELLOW = '\033[43m'
    YELLOWF = '\033[43m'
    BLUE = '\033[44m'
    MAGENTA = '\033[45m'
    CYAN = '\033[36m'
    WHITE = '\033[47m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    bold='\033[01m'

class Board:
    def __init__(self, inputs: list, robot_place, foodList: list, butterList: list):
        self.row = len(inputs)
        self.col = len(inputs[0])
        self.inputs = inputs
        self.robot_place = robot_place
        self.foodsList = foodList
        self.butterList = butterList
    def print_board(self):
        for i in range(len(self.inputs)):
            for j in range(len(self.inputs[i])):
                if (i, j) not in self.butterList and (i, j) not in tmp_foodsList and (i, j) != self.robot_place:
                    if self.inputs[i][j][0] == '1':
                        print(style.RED + "   ", end='' + style.RESET)
                    elif self.inputs[i][j][0] == '2':
                        print(style.YELLOW + "   ", end='' + style.RESET)
                    else:
                        print("   ", end='')
                else:
                    if (i, j) in self.butterList:
                        if self.inputs[i][j][0] == '1':
                            print(style.RED, end='')
                        else:
                            print(style.YELLOWF, end='')
                        print("\u0002" + "\U0001F9C8" + "\u0002", end='' + style.RESET)
                    elif (i, j) in tmp_foodsList:
                        if self.inputs[i][j][0] == '1':
                            print(style.RED, end='')
                        else:
                            print(style.YELLOWF, end='')
                        print(style.bold + "\u0002" + "\U0001F37D"+ "\u0002", end='' + style.RESET)
                    elif (i, j) == self.robot_place:
                        if self.inputs[i][j][0] == '1':
                            print(style.RED, end='')
                        else:
                            print(style.YELLOWF, end='')
                        print("\u0002" + "\U0001F916" + "\u0002", end='' + style.RESET)
            print()
        return ""

class Node:

    def __init__(self, board: Board):
        self.board = board
        self.nexts: List[Node] = []
        self.parent = None

    def is_goal(self):
        if  len(self.board.foodsList) == 0 :
            return True
        return False

    def produce_nexts(self):
        temp_robot_place = self.board.robot_place
        moves = [(0, 1), (1, 0,), (0, -1), (-1, 0)]
        for move in moves:
            temp_robot_place = self.board.robot_place
            next_r_place = (temp_robot_place[0] + move[0], temp_robot_place[1] + move[1])
            newButterList = self.board.butterList.copy()
            newFoodList = self.board.foodsList.copy()
            if isValid(self.board, next_r_place[0], next_r_place[1], move):
                temp_robot_place = next_r_place
                if next_r_place not in newButterList:
                    newRobotPlace = next_r_place;
                else:
                    lastI = next_r_place[0] + move[0]
                    lastJ = next_r_place[1] + move[1]
                    newButterList.append((lastI, lastJ))
                    newButterList.remove(next_r_place)
                    if (lastI , lastJ) in newFoodList:
                        newFoodList.remove((lastI , lastJ))
                        newButterList.remove((lastI , lastJ))
            next_node = Node(Board(self.board.inputs, temp_robot_place, newFoodList, newButterList))
            self.nexts.append(next_node)
    def produce_nexts_goal(self):
        temp_robot_place = self.board.robot_place
        moves = [(0, 1), (1, 0,), (0, -1), (-1, 0)]
        for move in moves:
            temp_robot_place = self.board.robot_place
            maybe_butter=(temp_robot_place[0] - move[0], temp_robot_place[1] - move[1])
            next_r_place = (temp_robot_place[0] + move[0], temp_robot_place[1] + move[1])
            newButterList = self.board.butterList.copy()
            newFoodList = self.board.foodsList.copy()
            if isValid_goal(self.board, next_r_place[0], next_r_place[1], move) :
                # and isValid_goal(self.board, maybe_butter[0], maybe_butter[1], move)
                temp_robot_place = next_r_place
                if maybe_butter not in newButterList:
                    newRobotPlace = next_r_place
                    next_node = Node(Board(self.board.inputs, temp_robot_place, newFoodList, newButterList))
                    self.nexts.append(next_node)
                    # next_node.board.print_board()
                    # print()
                else:
                    next_node = Node(Board(self.board.inputs, temp_robot_place, newFoodList, newButterList))
                    self.nexts.append(next_node)
                    # next_node.board.print_board()
                    # print()
                    if(maybe_butter in copyFood):
                        newFoodList.append(maybe_butter)

                    lastI = next_r_place[0] - move[0]
                    lastJ = next_r_place[1] - move[1]
                    newButterList.append((lastI, lastJ))
                    newButterList.remove((lastI-move[0], lastJ-move[1]))
                    next_node = Node(Board(self.board.inputs, temp_robot_place, newFoodList, newButterList))
                    self.nexts.append(next_node)

                    # next_node.board.print_board()
                    # print()

def is_in_explored(a_node: Node, explored: List[Node]):
    # print("a node start")
    # a_node.board.print_board()
    for exp in explored:
        if a_node.board.foodsList == exp.board.foodsList and \
                a_node.board.robot_place == exp.board.robot_place and \
                a_node.board.butterList == exp.board.butterList:
            return exp

        # print()
        # exp.board.print_board()

    return False

def bidirectional(start_node: Node):

    s_frontier: List[Node] = [start_node]
    g_frontier: List[Node] = all_goals

    explored: List[Node] = []
    while s_frontier and g_frontier:
        # print("first while")
        current_node = s_frontier.pop(0)

        same_node = is_in_explored(current_node, g_frontier)
        if same_node:
            path: List[Node] = [current_node]
            while current_node.parent:
                # print("2")
                path.insert(0, current_node.parent)
                current_node = current_node.parent
                path.append(same_node)
                while same_node.parent:
                    # print("3")
                    path.append(same_node.parent)
                    same_node = same_node.parent
            return path

        current_node.produce_nexts()
        explored.append(current_node)
        for child in current_node.nexts:
            # print("f1")
            if not is_in_explored(child, explored):

                s_frontier.append(child)
        current_node = g_frontier.pop(0)

        same_node = is_in_explored(current_node, s_frontier)
        if same_node:
            path: List[Node] = [current_node]
            while current_node.parent:
                # print("4")
                path.append(current_node.parent)
                current_node = current_node.parent
            while same_node.parent:
                # print("5")
                path.insert(0, same_node.parent)
                same_node = same_node.parent
            return path

        current_node.produce_nexts_goal()
        explored.append(current_node)
        for child in current_node.nexts:
            # print("7")
            if not is_in_explored(child, explored):
                g_frontier.append(child)



def isValid(board: Board, i, j, move):
    if isIN(board, i, j) and isPassable(board, i, j, move) :
        return True
    return False
def isValid_goal(board: Board, i, j, move):
    if isIN(board, i, j) and isPassable_goal(board, i, j, move) :
        return True
    return False

def isIN(board: Board, i, j):
    Row = board.row
    Col = board.col
    if i >= 0 and j >= 0 and i < Row and j < Col:
        return True
    return False


def isPassable(board: Board, i, j, move):
    if (i, j) in board.foodsList:
        return False
    if  board.inputs[i][j]== 'x':
        return False
    if (i, j) in board.butterList:
       if (i+move[0],j+move[1]) not in board.butterList and (i+move[0],j+move[1]) != 'x'\
               and isIN(board,i+move[0],j+move[1]):
            return True
       else:
        return False
    return True
def isPassable_goal(board: Board, i, j, move):
    if ((i, j) == robot_place):
        return False
    if  board.inputs[i][j]== 'x':
        return False
    if (i, j) in board.butterList:
       return False
    return True
def is_goal(self):
    if len(self.board.foodsList) == 0:
        return True
    return False
def make_goals():
    butterList_copy=[]
    food_copy=[]
    for x in copyFood:
        butterList_copy.append(x)
    goal_list=[]
    for z in butterList_copy:
        moves = [(0, 1), (1, 0,), (0, -1), (-1, 0)]
        for move in moves:
            if(z[0]+move[0]<row and z[1]+move[1]<col and z[0]+move[0]>=0 and z[1]+move[1]>=0 ):
                if(((z[0]+move[0]),(z[1]+move[1]))  not  in copyFood):
                    if(qu[z[0]+move[0]][z[1]+move[1]]!='x'):
                        goal_list.append(Node(Board(qu,((z[0]+move[0]),(z[1]+move[1])),food_copy,butterList_copy)));
    return goal_list



if __name__ == '__main__':
    # vooroodi gereftan
    foodsList = []
    butterList = []
    row, col = map(int, input().split())
    robot_init_place = ()
    qu = []
    tmp_robot_place = []
    tmp_foodsList = []
    tmp_butterList = []
    for i in range(row):
        q1 = list(input().split())
        nq1 = []
        for j in range(col):
            if q1[j] == 'x':
                nq1.append(q1[j])
            elif len(q1[j]) > 1:
                if q1[j][1] == 'r':
                    robot_init_place = (i, j)
                    robot_place = (i, j)
                if q1[j][1] == 'p':
                    tmp_foodsList.append((i, j))
                if q1[j][1] == 'b':
                    tmp_butterList.append((i, j))
                nq1.append(q1[j][0])
            else:
                nq1.append(q1[j])
        qu.append(nq1)
    # end of getting input

    copyFood = tmp_foodsList.copy()
    copyButter = tmp_butterList.copy()
    all_goals = make_goals()
    # for x in all_goals:
    #     x.board.print_board()
    #     print()
    my_node = Node(Board(qu, robot_place, copyFood, copyButter))
    frontier = bidirectional(my_node)
    for x in frontier:
        x.board.print_board()
if frontier is not None:
    print(len(frontier) - 2)
    last_sq = frontier[0].board.robot_place
    dirs = []
    cost = 0
    for i in range (len(frontier)-1):
        x , y = frontier[i].board.robot_place
        cost = cost +int(qu[x][y][0])
    print("cost : "+ str(cost))
    print()
    print("trace :")
    for i in range(len(frontier)-1):
        direction = (frontier[i].board.robot_place[0] - last_sq[0], frontier[i].board.robot_place[1] - last_sq[1])
        if direction == (0, 1):
            print('R')
            dirs.append('RIGHT')
        elif direction == (0, -1):
            print('L')
            dirs.append('LEFT')
        elif direction == (1, 0):
            print('D')
            dirs.append('DOWN')
        elif direction == (-1, 0):
            print('U')
            dirs.append("UP")
        print(frontier[i].board.print_board())
        last_sq = (frontier[i].board.robot_place[0], frontier[i].board.robot_place[1])
    for i in dirs:
        print(i)

