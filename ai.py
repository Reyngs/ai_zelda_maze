from random import randint
import networkx as nx

# targetPosition returns the position in the arrangement of an object or character
def targetPosition(target, board):
    pos = [0,0]
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j]==target:
                pos=[i,j]
    return pos

# canExpand returns a list "canList" where position
# 0 represents top
# 1 represents right
# 2 represents bottom
# 3 represents left
# If the position is free for that character, it is represented by 1, otherwise it is 0
# For Link if any position is occupied by an enemy, then it is marked with a 2
def canExpand(pos,board,chart):
    i=pos[0]
    j=pos[1]
    canList=[0,0,0,0] # The list starts with zeros
    # Positions are stored depending on the character
    up=board[i-1][j]
    right=board[i][j+1]
    down=board[i+1][j]
    left=board[i][j-1]
    if chart==4: # Link is represented as 4
        if up==0 or up==4 or up==3 or up==5:
            canList[0]=1
        elif up==2 or up==-2:
            canList[0]=2
        if right==0 or right==4 or right==3 or right==5:
            canList[1]=1
        elif right==2 or right==-2:
            canList[1]=2
        if down==0 or down==4 or down==3 or down==5:
            canList[2]=1
        elif down==2 or down==-2:
            canList[2]=2
        if left==0 or left==4 or left==3 or left==5:
            canList[3]=1
        elif left==2 or left==-2:
            canList[3]=2
    elif chart==2: # Enemy one is represented as 2
        if up==0 or up==2:
            canList[0]=1
        if right==0 or right==2:
            canList[1]=1
        if down==0 or down==2:
            canList[2]=1
        if left==0 or left==2:
            canList[3]=1
    elif chart==-2: # Enemy two is represented as -2
        if up==0 or up==-2:
            canList[0]=1
        if right==0 or right==-2:
            canList[1]=1
        if down==0 or down==-2:
            canList[2]=1
        if left==0 or left==-2:
            canList[3]=1
    return canList

# manhattanDistance clearly returns the manhattan distance between the target and the indicated pos
def manhattanDistance(board, pos, target):
    targetPos=targetPosition(target,board)
    distance=abs(pos[0]-targetPos[0])+abs(pos[1]-targetPos[1])
    return distance

# nodeToExpand returns the node to be expanded in the graph
# Since an A * algorithm is used
# the node to be expanded must be the leaf with the lowest value of "gh" 
# (the sum between g (the weight) and h (the heuristic, which in this case is the manhattan distance)) 
def nodeToExpand(G):
    if len(G)==1:
        return 0
    else:
        # this is the way to get the leaves
        leaves_nodes=[node for node in G.nodes() if G.in_degree(node)!=0 and G.out_degree(node)==0]
        node=leaves_nodes[0]
        for i in range(len(leaves_nodes)):
            if G.nodes[leaves_nodes[i]]['gh']<G.nodes[node]['gh']:
                node = leaves_nodes[i]
        return node

# changePos returns a position depending on the direction where you want to go
# 0 for up, 1 for right, 2 for down, 3 for left
def changePos(pos,i):
    if i==0:
        pos[0]-=1
    if i==1:
        pos[1]+=1
    if i==2:
        pos[0]+=1
    if i==3:
        pos[1]-=1
    return pos

# expand is the most important funtion for the Link moves
# Since it gathers the other functions to return the direction where Link should move
# The input G is the graph to expand
def expand(G, board, chart):
    while True:
        node = nodeToExpand(G) # We find the node to expand
        print("-----------------------------------")
        print("node to expand: ", node)
        # We create the variable pos with the position it represents
        pos=[0,0]
        pos[0]=G.nodes[node]['pos'][0]
        pos[1]=G.nodes[node]['pos'][1]
        # We create the list of positions you can go to
        listWays = canExpand(pos, board, chart)
        # In case it doesn't have somewhere to go, it returns -1
        if listWays==[0,0,0,0]:
            return -1
        print(listWays)
        print("Nodos expandidos:")
        for i in range(len(listWays)):
            # Possible positions for the leaf are expanded
            if listWays[i]!=0:
                # If the h value is 0, Link is in the target
                # Therefore it returns the label of the node
                if chart==4:
                    if G.nodes[node]['h']==0:
                        return G.nodes[node]['label']
                elif chart==2:
                    if G.nodes[node]['h']==1:
                        return G.nodes[node]['label']

                # If the graph exceeds 10000 expanded nodes, it returns -2
                if node>=10000:
                    return -2
                labelNode=len(G.nodes) # The label is de node number

                print("Input:",G.nodes[node])
                
                pos=[0,0]
                pos[0]=G.nodes[node]['pos'][0]
                pos[1]=G.nodes[node]['pos'][1]
                # We create the variable pos with the position changed depending on the direction it will expand
                pos=changePos(pos,i)

                # Its weight will be the sum of the value of the parent node plus 1
                g=G.nodes[node]['g']+1
                # If the position where it expands there is an enemy then 1 more is added for a total of 2
                if listWays[i]==2:
                    g+=1
                # By default the objective will be the exit of the maze
                target=5
                # If the key is in the labyrinth then the objective will be this
                if targetPosition(3,board)!=[0,0]:
                    target=3
                # sf
                if chart==2:
                    target=4

                # It is created h
                h=manhattanDistance(board,pos,target)
                
                # Total cost
                gh=g+h
                
                # The edge and the graph node are added with the information from this
                G.add_node(labelNode, label=labelNode, pos=pos, dir=i, g=g, h=h,  gh=gh)
                G.add_edge(node, labelNode)
                print("outpt:", G.nodes[labelNode])

# A_start_algorithm returns a list where 
# the first position will indicate to the gui when it is necessary to finish 
# the process since it will take too long, 1 to continue, 0 to finish
# the second position will indicate the number of expanded nodes expanded
# the third position will indicate the direction that the algorithm found to be the most optimal
def A_start_algorithm(board, chart):
    posChart=targetPosition(chart,board)
    if chart==4:
        if targetPosition(5,board)==[0,0]:
            return [0,0,0]
    # The graph is created
    G = nx.DiGraph()
    # The first node with a high value in gh is added so that the algorithm does not detect that this is the goal
    G.add_node(0, pos=posChart, way=0, g=0, h=999999, gh=99999)
    # The graph is expanded
    target=expand(G,board,chart)
    # When "expand" returns -1 it means there is no place to move
    if target==-1:
        return [1, target, 4]
    # When "expand" returns -2 it means that I exceed 10,000 expanded nodes
    elif target==-2:
        return [0,0,0]
    # road will be a list that will contain the way to the goal
    # It is obtained by means of the dijkstra algorithm
    road = nx.dijkstra_path(G, 0, target) #road = nx.all_shortest_paths(G, aux, 0)
    return [1, target, G.nodes[road[1]]['dir']]

# Simple funtion for return a random way depending on the positions where it can be moved
def randomWay(board, chart):
    enemy=targetPosition(chart,board)
    way=4
    listWays = canExpand(enemy, board,chart)
    if listWays==[0,0,0,0]:
        return way
    while True:
        way=randint(0,3)
        if listWays[way]!=0:
            return way