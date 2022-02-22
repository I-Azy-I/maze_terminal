import random
import os
from getkey import getkey, keys

WALL_CHR_FULL = chr(9608)
WALL_CHR_UP = chr(9600)
WALL_CHR_DOWN = chr(9604)
PATH_CHR = ' '

def maze_gen(size, show_creation = False):
    while True:
        empty_line = [0 for _ in range(size[0]+4)]
        full_line = [1 for _ in range(size[0]+2)]
        full_line.insert(0, 0)
        full_line.append(0)
        maze_scheme = [[1 for _ in range(size[0])] for _ in range(size[1])]
        for i in range(len(maze_scheme)):
            maze_scheme[i].insert(0, 1) 
            maze_scheme[i].append(1)
            maze_scheme[i].insert(0, 0) 
            maze_scheme[i].append(0)
        maze_scheme.insert(0, full_line)
        maze_scheme.append(full_line)
        maze_scheme.insert(0, empty_line)
        maze_scheme.append(empty_line)
        memory_path = []
        pos_ant = (size[1]//2, size[0]//2)
        memory_path.append(pos_ant)
        # 0: ^   1: >   2: v   3: <
        while True:
            posibility_next_move = []
            if (maze_scheme[pos_ant[0]-1][pos_ant[1]-2] and maze_scheme[pos_ant[0]][pos_ant[1]-2] and maze_scheme[pos_ant[0]+1][pos_ant[1]-2] and maze_scheme[pos_ant[0]-1][pos_ant[1]-1] and maze_scheme[pos_ant[0]+1][pos_ant[1]-1]):
                posibility_next_move.append(0)
            if (maze_scheme[pos_ant[0]+2][pos_ant[1]-1] and maze_scheme[pos_ant[0]+2][pos_ant[1]] and maze_scheme[pos_ant[0]+2][pos_ant[1]+1] and maze_scheme[pos_ant[0]+1][pos_ant[1]-1] and maze_scheme[pos_ant[0]+1][pos_ant[1]+1]):
                posibility_next_move.append(1)
            if (maze_scheme[pos_ant[0]-1][pos_ant[1]+2] and maze_scheme[pos_ant[0]][pos_ant[1]+2] and maze_scheme[pos_ant[0]+1][pos_ant[1]+2] and maze_scheme[pos_ant[0]-1][pos_ant[1]+1] and maze_scheme[pos_ant[0]+1][pos_ant[1]+1]):
                posibility_next_move.append(2)
            if (maze_scheme[pos_ant[0]-2][pos_ant[1]-1] and maze_scheme[pos_ant[0]-2][pos_ant[1]] and maze_scheme[pos_ant[0]-2][pos_ant[1]+1] and maze_scheme[pos_ant[0]-1][pos_ant[1]-1] and maze_scheme[pos_ant[0]-1][pos_ant[1]+1]):
                posibility_next_move.append(3)
            if len(posibility_next_move) == 0:
                if len(memory_path) == 0:
                    break
                else:
                    pos_ant = memory_path.pop()
            else:
                next_move = random.choice(posibility_next_move)
                if next_move == 0:
                    new_pos = (pos_ant[0], pos_ant[1]-1)
                    memory_path.append(new_pos)
                    maze_scheme[new_pos[0]][new_pos[1]] = 0
                    pos_ant = new_pos
                elif next_move == 1:
                    new_pos = (pos_ant[0]+1, pos_ant[1])
                    memory_path.append(new_pos)
                    maze_scheme[new_pos[0]][new_pos[1]] = 0
                    pos_ant = new_pos
                elif next_move == 2:
                    new_pos = (pos_ant[0], pos_ant[1]+1)
                    memory_path.append(new_pos)
                    maze_scheme[new_pos[0]][new_pos[1]] = 0
                    pos_ant = new_pos
                elif next_move == 3:
                    new_pos = (pos_ant[0]-1, pos_ant[1])
                    memory_path.append(new_pos)
                    maze_scheme[new_pos[0]][new_pos[1]] = 0
                    pos_ant = new_pos
                else:
                    print("C'est la grand mère")
                #os.system('clear')
                if show_creation:
                    print('\033[A'*10)
                    display_maze(maze_scheme, rewrite=True)
        maze_scheme.pop(0)
        maze_scheme.pop(0)
        maze_scheme.pop()
        maze_scheme.pop()
        for i in range(len(maze_scheme)):
            maze_scheme[i].pop(0)
            maze_scheme[i].pop(0)
            maze_scheme[i].pop()
            maze_scheme[i].pop()
        if not maze_scheme[0][0] and not maze_scheme[-1][-1]:
            break
    return maze_scheme

def create_line(l1, l2, last_empty=False, l_hist_path = None):
        if last_empty:
            line = WALL_CHR_UP
        else:
            line = WALL_CHR_FULL
        if l_hist_path is None:
            
            for a, b in zip(l1, l2):
                if a and b:
                    line = line + WALL_CHR_FULL
                elif a and not b:
                    line = line + WALL_CHR_UP
                elif not a and b:
                    line = line + WALL_CHR_DOWN
                else :
                    line = line + ' '
            if last_empty:
                line = line + WALL_CHR_UP
            else:
                line = line + WALL_CHR_FULL
        else:
            l_h1 = l_hist_path[0]
            l_h2 = l_hist_path[1]
            for a, b ,h1 ,h2 in zip(l1, l2, l_h1, l_h2):
                if a and b:
                    line = line + WALL_CHR_FULL
                elif a and not b:
                    if h2:
                        line = line + '\x1b[44m' + WALL_CHR_UP + '\x1b[0m'
                    else:
                        line = line +   WALL_CHR_UP 
                elif not a and b:
                    if h1:
                        line = line + '\x1b[44m' + WALL_CHR_DOWN + '\x1b[0m'
                    else:    
                        line = line + WALL_CHR_DOWN
                else :
                    if h1 and h2:
                        line = line + '\x1b[44m' + ' '+ '\x1b[0m'
                    elif h1 and not h2:
                        line = line + '\x1b[34m' + WALL_CHR_UP + '\x1b[0m'
                    elif not h1 and h2:
                        line = line + '\x1b[34m' + WALL_CHR_DOWN + '\x1b[0m'
                    else:
                        line = line + ' '
            if last_empty:
                line = line + WALL_CHR_UP
            else:
                line = line + WALL_CHR_FULL

        return line
def display_maze(maze_scheme, hist_path=None, rewrite=False):
    
    if rewrite:
        if len(maze_scheme)%2:
            print('\033[A'*(len(maze_scheme)//2 + 1))
        else:
            print('\033[A'*(len(maze_scheme)//2 + 2))
    first_l = [0]
    first_l.extend([1 for _ in range(len(maze_scheme[0])-1)])
    if hist_path is None:
        print(create_line(first_l, maze_scheme[0]))
    else:
        print(create_line(first_l, maze_scheme[0], l_hist_path=(first_l, hist_path[0])))
    for i in range((len(maze_scheme)-1)//2):
            if hist_path is None:
                print(create_line(maze_scheme[(i*2)+1], maze_scheme[(i*2)+2]))
            else:
                l_hist_path = (hist_path[(i*2)+1], hist_path[(i*2)+2])
                print(create_line(maze_scheme[(i*2)+1], maze_scheme[(i*2)+2],l_hist_path=l_hist_path))
    if len(maze_scheme) % 2 == 1:
        
        last_l = [1 for _ in range(len(maze_scheme[0])-1)]
        last_l.append(0)
        very_last_l = [0 for _ in range(len(maze_scheme[0]))]
        print(create_line(last_l, very_last_l, last_empty=True))
    else:

        last_l = [1 for _ in range(len(maze_scheme[0]))]
        last_l[-1] = 0
        if hist_path is None:
            print(create_line(maze_scheme[-1], last_l))
        else:
            print(create_line(maze_scheme[-1], last_l, l_hist_path=(hist_path[-1], last_l)))

size = os.get_terminal_size()
x = size[0] - 2
y = size[1]*2 - 6

maze_scheme = maze_gen((x, y))
display_maze(maze_scheme)
want_play = input('Do you want to solve this maze?[y/n] ')
if want_play == 'y':
    hist_path = [[0 for _ in range(len(maze_scheme[0]))] for __ in range(len(maze_scheme))]
    hist_path[0][0] = 1
    display_maze(maze_scheme, hist_path=hist_path)
    pos = (0,0)
    while True:
        key = getkey()
        if key == 'w':
            if pos[0] >= 1 and not maze_scheme[pos[0]-1][pos[1]]:
                if hist_path[pos[0]-1][pos[1]]:
                    hist_path[pos[0]][pos[1]] = 0
                    pos = (pos[0]-1, pos[1])
                else:
                    hist_path[pos[0]-1][pos[1]] = 1
                    pos = (pos[0]-1, pos[1])
                display_maze(maze_scheme, hist_path=hist_path, rewrite=True)
        elif key == 'a':
            if pos[1] >= 1 and not maze_scheme[pos[0]][pos[1]-1]:
                if hist_path[pos[0]][pos[1]-1]:
                    hist_path[pos[0]][pos[1]] = 0
                    pos = (pos[0], pos[1]-1)
                else:
                    hist_path[pos[0]][pos[1]-1] = 1
                    pos = (pos[0], pos[1]-1)
                display_maze(maze_scheme, hist_path=hist_path, rewrite=True)

        elif key == 's':

            if pos[0] < len(maze_scheme) -1 and not maze_scheme[pos[0]+1][pos[1]]:
                if hist_path[pos[0]+1][pos[1]]:
                    hist_path[pos[0]][pos[1]] = 0
                    pos = (pos[0]+1, pos[1])
                else:
                    hist_path[pos[0]+1][pos[1]] = 1
                    pos = (pos[0]+1, pos[1])
                display_maze(maze_scheme, hist_path=hist_path, rewrite=True)

        elif key == 'd':
            if pos[1] < len(maze_scheme[0])-1 and not maze_scheme[pos[0]][pos[1]+1]:
                if hist_path[pos[0]][pos[1]+1]:
                    hist_path[pos[0]][pos[1]] = 0
                    pos = (pos[0], pos[1]+1)
                else:
                    hist_path[pos[0]][pos[1]+1] = 1
                    pos = (pos[0], pos[1]+1)
                display_maze(maze_scheme, hist_path=hist_path, rewrite=True)
            
        
        if pos == (len(maze_scheme)-1, len(maze_scheme[0])-1):
            print('Compagnie Bravo!!!')
            break