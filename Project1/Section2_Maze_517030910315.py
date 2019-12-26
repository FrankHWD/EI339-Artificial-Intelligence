import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpathes
import collections

class MazeProblem:
    def __init__(self, maze_file = ''):
        self.map = self.loadMap(maze_file)
        self.map2= self.loadMap(maze_file)  #Store the value of each square to draw the path image
        self.former = np.zeros(self.map.shape) #Store the value of each square to represent the predecessor
        self.discovered = np.zeros(self.map.shape) #Store the value of each square to represent whether it has been explored or not
    def loadMap(self, file):
        # Load map txt as matrix.
        # 0: path, 1: obstacle, 2: start point, 3: end point
        f = open(file)
        lines = f.readlines()
        numOfLines = len(lines)
        returnMap = np.zeros((numOfLines, 40))
        A_row = 0
        for line in lines:
            list = line.strip().split(' ')
            returnMap[A_row:] = list[0:40]
            A_row += 1
        return returnMap

    def bfs(self):
        que = collections.deque()
        dir=[[1,0],[0,1],[-1,0],[0,-1]]
        max1=len(self.map)
        max2=len(self.map[0])
        self.former[0][0]=-1
        self.discovered[0][0]=1
        que.append([0,0])         #initialization

        while len(que)>0:
            point0=que.popleft()
            x0=point0[0]
            y0=point0[1]

            if self.map[x0][y0]==3:   #reach the ending state
                f1=x0
                f2=y0
                path=collections.deque()
                while self.former[f1][f2] != -1:   #form the path according to the self.former matrix
                    path.append([f1,f2])
                    if self.former[f1][f2]==1:
                        f1-=1
                    elif self.former[f1][f2] == 2:
                        f2-=1
                    elif self.former[f1][f2] == 3:
                        f1+=1
                    elif self.former[f1][f2] == 4:
                        f2+=1
                while len(path)>0:  #form the self.map2 in order to draw the path image
                    pathpoint=path.pop()
                    px=pathpoint[0]
                    py=pathpoint[1]
                    if self.map[px][py]==2 or self.map[px][py]==3:
                        continue
                    self.map2[px][py]=4
                self.drawpath()
                return path

            for i in range(4):   #squares on the four directions
                x=x0+dir[i][0]
                y=y0+dir[i][1]
                point=[x,y]
                if x>-1 and x<max1 and y>-1 and y<max2:  #if it does not exceed the boundery
                    if self.map[x][y]!=1:                 #if it is not a wall
                        if self.discovered[x][y]==0:      #if it has not been explored
                            self.discovered[x][y]=1          #set the value to make it being explored
                            que.append(point)                #put the new point into the queue
                            self.former[x][y]=i+1            #mark its predecessor

    def drawMap(self):
        # Visulize the maze map.
        # Draw obstacles(1) as red rectangles. Draw path(0) as white rectangles. Draw starting point(2) and ending point(3) as circles.
        rowNum = len(self.map)
        print(rowNum)
        colNum = len(self.map[0])
        print(colNum)
        ax = plt.subplot()
        param = 1
        for col in range(colNum):
            for row in range(rowNum):
                if self.map[row, col] == 2:
                    circle = mpathes.Circle([param * col + param/2.0, param * row + param/2.0], param/2.0, color='g')
                    ax.add_patch(circle)
                elif self.map[row,col] == 3:
                    circle = mpathes.Circle([param * col + param/2.0, param * row + param/2.0], param/2.0, color='y')
                    ax.add_patch(circle)
                elif self.map[row, col] == 1:
                    rect = mpathes.Rectangle([param * col, param * row], param, param, color='r')
                    ax.add_patch(rect)
                else:
                    rect = mpathes.Rectangle([param * col, param * row], param, param, color='w')
                    ax.add_patch(rect)
        # Improve visualization
        plt.xlim((0,colNum))
        plt.ylim((0,rowNum))
        my_x_ticks = np.arange(0,colNum+1, 1)
        my_y_ticks = np.arange(0,rowNum+1, 1)
        plt.xticks(my_x_ticks)
        plt.yticks(my_y_ticks)
        axx = plt.gca()
        axx.xaxis.set_ticks_position('top')
        axx.invert_yaxis()
        plt.grid()
        # Save maze image.
        plt.savefig('./maze.png')

    def drawpath(self):
        rowNum = len(self.map)
        print(rowNum)
        colNum = len(self.map[0])
        print(colNum)
        ax = plt.subplot()
        param = 1
        for col in range(colNum):
            for row in range(rowNum):
                if self.map2[row, col] == 2:
                    circle = mpathes.Circle([param * col + param/2.0, param * row + param/2.0], param/2.0, color='g')
                    ax.add_patch(circle)
                elif self.map2[row,col] == 3:
                    circle = mpathes.Circle([param * col + param/2.0, param * row + param/2.0], param/2.0, color='y')
                    ax.add_patch(circle)
                elif self.map2[row,col] == 4:
                    circle = mpathes.Circle([param * col + param/2.0, param * row + param/2.0], param/2.0, color='b')
                    ax.add_patch(circle)
                elif self.map2[row, col] == 1:
                    rect = mpathes.Rectangle([param * col, param * row], param, param, color='r')
                    ax.add_patch(rect)
                else:
                    rect = mpathes.Rectangle([param * col, param * row], param, param, color='w')
                    ax.add_patch(rect)
        plt.xlim((0,colNum))
        plt.ylim((0,rowNum))
        my_x_ticks = np.arange(0,colNum+1, 1)
        my_y_ticks = np.arange(0,rowNum+1, 1)
        plt.xticks(my_x_ticks)
        plt.yticks(my_y_ticks)
        axx = plt.gca()
        axx.xaxis.set_ticks_position('top')
        axx.invert_yaxis()
        plt.grid()
        plt.savefig('./path.png')

if __name__ == "__main__":
    Solution = MazeProblem(maze_file = 'maze.txt')
    #Solution.drawMap()
    Solution.bfs()
