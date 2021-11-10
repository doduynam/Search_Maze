import os
import matplotlib.pyplot as plt
import queue

def visualize_maze(matrix, bonus, start, end, route = None):
    """
    Args:
      1. matrix: The matrix read from the input file,
      2. bonus: The array of bonus points,
      3. start, end: The starting and ending points,
      4. route: The route from the starting point to the ending one, defined by an array of (x, y), e.g. route = [(1, 2), (1, 3), (1, 4)]
    """
    #1. Define walls and array of direction based on the route
    walls = [(i,j) for i in range(len(matrix)) for j in range(len(matrix[0])) if matrix[i][j]=='x']

    if route:
        direction = []
        for i in range(1,len(route)):
            if route[i][0] - route[i-1][0] > 0:
                direction.append('^') #^
            elif route[i][0]-route[i-1][0] < 0:
                direction.append('v') #v        
            elif route[i][1]-route[i-1][1] > 0:
                direction.append('<')
            else:
                direction.append('>')

        direction.pop(0)

    #2. Drawing the map
    ax = plt.figure(dpi = 100).add_subplot(111)

    for i in ['top', 'bottom', 'right', 'left']:
        ax.spines[i].set_visible(False)

    plt.scatter([i[1] for i in walls], [-i[0] for i in walls],
                marker = 'X', s = 100, color = 'black')
    
    plt.scatter([i[1] for i in bonus], [-i[0] for i in bonus],
                marker = 'P', s = 100, color = 'green')

    plt.scatter(start[1], -start[0], marker = '*',
                s = 100, color = 'gold')

    if route:
        for i in range(len(route)-2):
            plt.scatter(route[i+1][1], -route[i+1][0],
                        marker = direction[i], color = 'silver')

    plt.text(end[1], -end[0], 'EXIT', color = 'red',
         horizontalalignment = 'center',
         verticalalignment = 'center')
    plt.xticks([])
    plt.yticks([])
    plt.show()

    #print(f'Starting point (x, y) = {start[0], start[1]}')
    #print(f'Ending point (x, y) = {end[0], end[1]}')
    
    #for _, point in enumerate(bonus):
      #print(f'Bonus point at position (x, y) = {point[0], point[1]} with point {point[2]}')

def read_file(file_name: str = 'maze.txt'):
  f = open(file_name, 'r')
  n_bonus_points = int(next(f)[:-1])
  bonus_points = []
  for i in range(n_bonus_points):
    x, y, reward = map(int, next(f)[:-1].split(' '))
    bonus_points.append((x, y, reward))

  text = f.read()
  matrix = [list(i) for i in text.splitlines()]
  f.close()

  return bonus_points, matrix

file_namee = {'maze_map.txt', 'maze_map_1.txt', 'maze_map_2.txt'}

bonus_points, matrix = read_file('maze_map_2.txt')

#print(f'The height of the matrix: {len(matrix)}')
#print(f'The width of the matrix: {len(matrix[0])}')

for i in range(len(matrix)):
    for j in range(len(matrix[0])):
        if matrix[i][j] == 'S':
            start = (i,j)
        elif matrix[i][j] == ' ':
            if (i == 0) or (i == len(matrix)-1) or (j == 0) or (j == len(matrix[0])-1):
                end = (i,j) 
        else:
            pass

def get_neighbor(matrix, cur):
    nei = []
    e = (cur[0], cur[1]+1)
    w = (cur[0], cur[1]-1)
    s = (cur[0]+1, cur[1])
    n = (cur[0]-1, cur[1])
    x = e[0]
    y = e[1]
    if matrix[x][y] != 'x':
        nei.append(e)
    x = w[0]
    y = w[1]
    if matrix[x][y] != 'x':
        nei.append(w)
    x = s[0]
    y = s[1]
    if matrix[x][y] != 'x':
        nei.append(s)
    x = n[0]
    y = n[1]
    if matrix[x][y] != 'x':
        nei.append(n)
    return nei

def DFS(matrix, start, end):
  previous = [] 
  for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] != 'x':
                it = (i,j)
                previous.append((it, None))
  previous = dict(previous)

  def _DFS(_start): 
    for node in get_neighbor(matrix, _start): 
      if previous[node] == None: 
        previous[node] = _start 
        if node == end:
          return True  
        elif _DFS(node):
          return True
    return False
  
  if (_DFS(start)):
    path = []
    path.append(end)
    curNode = end
    while curNode != start:
        curNode = previous[curNode]
        path.append(curNode)
    return path
  else:
    return None

def BFS(matrix, start, end):
    q = queue.deque() 
    q.append(start)  
    previous = [] 
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] != 'x':
                it = (i,j)
                previous.append((it, None))
    previous = dict(previous)
    while 1:
        cur = q.popleft()
        for node in get_neighbor(matrix, cur):
            if previous[node] == None:
                q.append(node)
                previous[node] = cur
                if node == end:
                    path = []
                    path.append(end)
                    curNode = end
                    while curNode != start:
                        curNode = previous[curNode]
                        path.append(curNode)
                    return path
        if len(q) == 0:
            return None

def manha_heur(node, end):
    dx = abs(node[0] - end[0])
    dy = abs(node[1] - end[1])
    return (dx + dy)
def cheby_heur(node, end):
    dx = abs(node[0] - end[0])
    dy = abs(node[1] - end[1])
    return (dx + dy) - min(dx, dy)
def eucli_heur(node, end):
    dx = abs(node[0] - end[0])
    dy = abs(node[1] - end[1])
    return sqrt(dx * dx + dy * dy)
def breaktie_heur(node, start, end):
    dx1 = node[0] - end[0]
    dy1 = node[1] - end[1]
    dx2 = start[0] - end[0]
    dy2 = start[1] - end[1]
    cross = abs(dx1*dy2 - dx2*dy1)
    heuristic += cross*0.001
    return heuristic

def greedy_search(matrix, start, end, heuristic = 0):
    q = queue.deque()
    q.append(start)
    previous = []
    for i in range(len(matrix)):
        for j in range(len(matrix[0])):
            if matrix[i][j] != 'x':
                it = (i,j)
                previous.append((it, {'from': None, 'heuristic': cheby_heur(it, end)}))
    previous = dict(previous)
    while 1:
        cur = q.popleft()
        if cur == end:
            path = []
            path.append(end)
            curNode = end
            while curNode != start:
                curNode = previous[curNode]['from']
                path.append(curNode)
            return path

        for node in get_neighbor(matrix, cur):
            if previous[node]['from'] == None:
                q.append(node)
                previous[node]['from'] = cur
        if len(q) == 0:
            return None   
        #q = queue.deque(aweSomeSort(q, previous, 'heuristic'))

def menu():
    print("")
    print("Nhan 0 de THOAT")
    print("Nhan 1 de chay thuc hien bang DFS (khong diem thuong)")
    print("Nhan 2 de chay thuc hien bang BFS (khong diem thuong)")
    print("Nhan 3 de chay thuc hien bang GBFS (khong diem thuong)")
    print("Nhan 4 de chay thuc hien bang A* (khong diem thuong)")

menu()
choose = int(input("Chon: "))
while 1:
    if choose == 1:
        visualize_maze(matrix, bonus_points, start, end, route = DFS(matrix, start, end))
        print("DFS")
        menu()
        choose = int(input("Chon: "))
    if choose == 2:
        visualize_maze(matrix, bonus_points, start, end, route = BFS(matrix, start, end))
        print("BFS")
        menu()
        choose = int(input("Chon: "))
    if choose == 3:
        visualize_maze(matrix, bonus_points, start, end, route = greedy_search(matrix, start, end))
        print("GBFS")
        menu()
        choose = int(input("Chon: "))
    if choose > 3 or choose < 1:
        break

