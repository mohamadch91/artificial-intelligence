class colors:
    OK = '\033[92m' #GREEN
    FAIL = '\033[91m' #RED
    RESET = '\033[0m'  # RESET COLOR
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
    bold = '\033[01m'

class Node:
    def __init__(self, number, x,y):
        self.number = number
        self.x=x
        self.y=y

def read_input():
    row,column=[int(x) for x in input("plase insert row and column : ").split()]

    map=[]
    for i in range (row):
        z=input().split()
        inner_list=[]
        for s in range(len(z)):
            # we use -1 for - homes
            if(z[s]=='-'):
                node=Node(-1,i,s)
            else:
                node=Node(int(z[s]),i,s)
            inner_list.append(node)
        map.append(inner_list)

    return row,column,map
def print_map(map,row,column):
    for z in range(row):
        for p in range(column):
            print(map[z][p].number,end="")
        print()
    for i in range(row):
        for j in range(2):
            for k in range (column):
                if(map[i][k].number==0):
                    print(colors.FAIL+style.RED+"       "+colors.RESET+style.RESET,end="")
                elif (map[i][k].number==1 or map[i][k].number==-1):
                    print(colors.OK +style.GREEN+ "       " + colors.RESET+style.RESET, end="")
            print()


if __name__ == '__main__':
    row,column,map=read_input()
    print_map(map,row,column)