import random


class Maze():
    #TODO: implement end

    def __init__(self, xDim, yDim, start=(-1,-1), end=(-1,-1)):
        """
        Summary:
            initializes an instance
        Description:
            sets defaults and generates a maze for the instance
        Parameters
        _________

        xDim: Int
            X dimension for the maze

        yDim: Int
            Y dimension for the maze

        start: Tuple
            (x, y) starting pos to generate from

        end: Tuple
            (x, y) Where the "Finish" is

        Returns
        _______
        None

        """

        self.xDim = xDim
        self.yDim = yDim
        self.start = start
        self.end = end
        self.maze = self.generateMaze()

    def printMaze(self):
        """
        Summary:
            prints a graphical version of the maze to the console
        Description:
            iterates through the maze list and prints it to console
        Parameters
        _________
        None

        Returns
        _______
        None

        """
        for i in self.maze:
            for j in i:
                if j == 1:
                    print("·", end=" ")
                else:
                    print("█", end="█")
            print()

    #@classmethod #TODO: make _populate work with this
    def generateMaze(self, x=-1, y=-1):
        """
        Summary:
            Generates a maze with dimensions x,y
        Description:
            generates and populates a maze with dimensions - iterative
        Parameters
        _________

        x: Int
            X dimension for the maze - if left at default self.xDim will be used
        y: Int
            Y dimension for the maze - if left at defualt self.yDim will be used

        Returns
        _______
        List
            List of lists containing bits for maze structure

        """
        if x <= 0 or y <= 0:
            x = self.xDim
            y = self.yDim
        else:
            self.xDim = x
            self.yDim = y

        mazeGen = [[0 for i in range(x)] for i in range(y)]

        self._populate(mazeGen) #carve the path

        return mazeGen

    def regenerateMaze(self, x=-1, y=-1):
        """
        Summary:
            Create a new maze for the instance
        Description:
            recalls generateMaze(x, y)
        Parameters
        _________

        x: Int
            X dimension of the maze - if left default self.xDim will be used

        y: Int
            Y dimension of the maze - if left default self.yDim will be used

        Returns
        _______
        None

        """
        self.maze = self.generateMaze(x, y)

    def _populate(self, board):
        """
        Summary:
            Populates a list of list
        Description:
            Populates a list of lists using DFS - creates the path not walls
        Parameters
        _________

        board: List
            A "blank" maze - there is no path yet
            This is a list of lists that defines the dimensions of the maze

        Returns
        _______
        None

        """
        if self.start != (-1,-1):
            stack = [self.start]
        else:
            stack = [(random.randint(0, self.xDim - 1), random.randint(0, self.yDim - 1))] #stack to store where weve been for back tracking - start at a random spot

        xDirect = [-1, 1, 0, 0] # use these with nested for loops below
        yDirect = [0, 0, -1, 1]

        while len(stack) > 0:
            #TODO: to prevent zigags we want to check if we changed direction last move - if we did dont change it again
            (x,y) = stack[-1] # set the coods to the last element of the stack
            board[y][x] = 1 #make the the working point part of the path
            neighbors = [] # create a list of neighbors available to pick from
            #FIND AVAILABLE MOVES
            for i in range(4): #once left once right # one up one down
                newX = x+xDirect[i] # first 2 iters check left right
                newY = y+yDirect[i] # second 2 iters check up down
                if newX >= 0 and newX < self.xDim and newY >= 0 and newY < self.yDim: #check left
                    if board[newY][newX] == 0: #if its a wall check if the wall has
                        count = 0 # we want to count if there are any paths already next to where we want to move
                        for j in range(4): #check if only one neighbor is path - ensures were still connected to the path
                            testX = newX+xDirect[j]
                            testY = newY+yDirect[j]
                            if testX >= 0 and testX < self.xDim and newY >= 0 and testY < self.yDim:
                                if board[testY][testX] == 1: #if its path count it
                                    count += 1
                        if count == 1: #if theres only one path
                            neighbors.append(i) # record what move index we found the available neighbor at
            #MOVE TO ONE OF THE FOUND AVAILABLE NEIGHBORS
            if len(neighbors) > 0: # if theres a neighbor we can go to pick a random one
                direction = neighbors[random.randint(0, len(neighbors)-1)] # pick a random index in the range
                stack.append((x+xDirect[direction], y+yDirect[direction]))
            else: # there are no neighbors so we need to go back and pick a new direction
                stack.pop()

class SolveMaze():

    def __init__(self, maze, start, end): # maze is a list of lists start and end are tuples (x, y)
        """
        Summary:
            Initialize the solver
        Description:
            Initialize solver variables
        Parameters
        _________

        maze: List
            List of lists that contains the maze

        start: Tuple
            (x,y) - coordinates for where the start of the maze is

        end: Tuple
            (x,y) - coordinates for the end of the maze

        Returns
        _______
        None
        """
        self.maze = maze
        self.start = start
        self.end = end
        self.xDim = len(maze[0])
        self.yDim = len(maze)
        self.solution = []

    def solve(self):
        """
        Summary:
            Solve the maze
        Description:
            Iteratively solve the maze using DFS

        Returns
        _______
        List or None
           Returns the solution to the maze as a list of tuples corresponding to coordinates in the maze
           returns None if no solution is found

        """
        stack = [(self.start[0], self.start[1])] # start a stack for keeping track of where weve gone
        xDirect = [-1, 1, 0, 0] # Directions [-x,+x, -y, +y]
        yDirect = [0, 0, -1, 1]
        visited = stack[:] # keep track of where we were - initialize with starting position since we've been there
        while len(stack) > 0 and stack[-1] != self.end:
            neighbors = []
            (x, y) = stack[-1]
            end = False
            for i in range(4): # this is the direction checking
                newX = x + xDirect[i]
                newY = y + yDirect[i]

                if newX >= 0 and newX < self.xDim and newY >= 0 and newY < self.yDim and not (newX, newY) in visited: # we didnt find the end so check around
                    if self.maze[newY][newX] == 1:
                        if newX == self.end[0] and newY == self.end[1]: # if we found the end mark that we have it
                            end = True
                            break # theres no need to check the other cells - We found the end
                        count = 0 #Im not sure I need to even count neighbors - actually if there is only one neighbor that is path weve reached a dead end
                        for j in range(4):
                            neighborX = newX + xDirect[j]
                            neighborY = newY + yDirect[j]
                            if neighborX >= 0 and neighborX < self.xDim and neighborY >= 0 and neighborY < self.yDim and not (neighborX, neighborY) in visited:
                                if self.maze[neighborY][neighborX] == 1: #were on the path - but dont make available any places weve already been to
                                    count += 1
                        if count >= 1: #keep following the path if theres more than one way to go
                            neighbors.append(i) # identify that we can move
            #MOVE DOWN THE PATH
            if len(neighbors) >= 1:
                direction = neighbors[random.randint(0, len(neighbors) - 1)] # TODO: would it be faster to prioritize  
                newX = x + xDirect[direction]
                newY = y + yDirect[direction]
                stack.append((newX, newY))
                visited.append((newX, newY))
                #move to the unvisited neighbor
            elif end:
                stack.append(self.end)
            else: # there is only one neighbor that is path(The way we came from)
                stack.pop()

        if len(stack) == 0:
            print("NO PATH FOUND")
            return
        else:
            self.solution = stack
            return self.solution # this is the path we too k to the end

    def printSolved(self):
        if len(self.solution) == 0:
            print("No solution yet")
            solve = input("Should I attempt to solve?").lower()
            answer = ["y", "yes", "n", "no"]
            while not solve in answer:
                solve = input("Should I attempt to solve?").lower()
            if solve == answer[0] or solve == answer[1]:
                self.solve()
            else:
                return

        print(self.solution)
        solvedMaze = self.maze[:] #TODO: This line will overwrite self.maze for some reason
        for coord in self.solution: #mark the solution path
            solvedMaze[coord[1]][coord[0]] = 2

        for row in solvedMaze:
            for col in row:
                coord = (col, row)
                if col == 0:
                    print("█", end="█")
                elif col == 1:
                    print("·", end=" ")
                elif col == 2:
                    print("*", end=" ")
            print()

        for coord in self.solution: #change the path back - a work around for the above TODO
            solvedMaze[coord[1]][coord[0]] = 1

if __name__ == "__main__":
    mazes = []
    testMaze = [[1, 1, 0, 0], [0, 1, 0, 0], [1, 1, 1, 0], [1, 0, 1, 1]]
    #[1, 1, 0, 0]
    #[0, 1, 0, 0]
    #[1, 1, 1, 0]
    #[1, 0, 1, 1]
    print("generating 4x4 maze with random start")
    maze0 = Maze(4,4)
    mazes.append(maze0)
    print("generating 4x4 maze with start at 0,0")
    maze1 = Maze(4,4, (0,0))
    mazes.append(maze1)
    solve = SolveMaze(maze1.maze, (0,0), (3,3))
    print("Printing mazes in maze array")
    for i in range(len(mazes)):
        maze = mazes[i]
        print("Maze #{}".format(i))
        maze.printMaze()

    print("Solving maze1")
    print(solve.solve())

    print("solving test maze")
    solve1 = SolveMaze(testMaze, (0,0), (3,3))
    print(solve1.solve())

    maze2 = Maze(10, 10, (0,0))
    solve2 = SolveMaze(maze2.maze, (0,0), (9, 9))
    maze2.printMaze()
    solve2.printSolved()
