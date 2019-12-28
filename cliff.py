import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.patches as mpathes
from matplotlib.pyplot import MultipleLocator


class Environment(object):
    def __init__(self, rows=5, cols=8, barrier_num=3, reward_num=5):
        self.rows = rows
        self.cols = cols
        self.barrier_num = barrier_num
        self.reward_num = reward_num
        self.create_env_default()

    def create_env_default(self):
        # the final matrix of environment in our problem
        # start node = 1, terminal node = 2, cliff = -1, barrier = -2, reward = 3
        # [[1. - 1. - 1. - 1. - 1. - 1. - 1.  2.]
        # [0.  0.  0.  0.  0.  0. - 2.  0.]
        # [0.  0.  0.  3. - 2.  0.  0.  0.]
        # [3.  0.  0.  0. - 2.  0.  0.  3.]
        # [0.  0.  3.  0.  0.  0.  0.  0.]]
        self.env = np.zeros([self.rows, self.cols])
        # start node = 1, terminal node = 2, cliff = -1
        self.env[0][0] = 1
        self.env[0][self.cols - 1] = 2
        self.env[0][1:self.cols - 1] = -1
        # set barrier pos
        barrier_pos = [[3, 4], [2, 4], [1, 6]]
        # set barrier = -2
        for pos in barrier_pos:
            self.env[pos[0]][pos[1]] = -2
        # set reward pos
        reward_pos = [[3, 0], [2, 3], [4, 2], [3, 7]]
        # set reward = 3
        for pos in reward_pos:
            self.env[pos[0]][pos[1]] = 3

    def create_env(self):
        self.env = np.zeros([self.rows, self.cols])
        # start node = 1, terminal node = 2, cliff = -1
        self.env[0][0] = 1
        self.env[0][self.cols - 1] = 2
        self.env[0][1:self.cols - 1] = -1

        # randomly set barrier pos
        barrier_pos = []
        while (len(barrier_pos) < self.barrier_num):
            i = random.randint(1, self.rows - 1)
            j = random.randint(0, self.cols - 1)
            if [i, j] not in barrier_pos and [i, j] not in [[1, 0], [1, self.cols - 1]]:
                barrier_pos.append([i, j])

        # set barrier = -2
        for pos in barrier_pos:
            self.env[pos[0]][pos[1]] = -2

        # randomly set reward pos
        reward_pos = []
        while (len(reward_pos) < self.reward_num):
            i = random.randint(1, self.rows - 1)
            j = random.randint(0, self.cols - 1)
            if [i, j] not in reward_pos and [i, j] not in barrier_pos:
                reward_pos.append([i, j])

        # set reward = 3
        for pos in reward_pos:
            self.env[pos[0]][pos[1]] = 3

    def show_env(self):
        fig,ax = plt.subplots(figsize=(8, 6))
        plt.xlim((0, self.cols))
        plt.ylim((0, self.rows))
        # name: start, terminal, cliff, barrier, reward, others
        # number: 1, 2, -1, -2, 3, 0
        # color: yellow, orange, gray, black, red, white
        color_dict = {-1: "gray", 1: "yellow", 2: "orange", -2: "black", 3: "red", 0: "white"}
        my_x_ticks = np.arange(0, self.cols, 1)
        my_y_ticks = np.arange(0, self.rows, 1)
        plt.xticks(my_x_ticks)
        plt.yticks(my_y_ticks)
        x_major_locator = MultipleLocator(1)
        y_major_locator = MultipleLocator(1)
        ax.xaxis.set_major_locator(x_major_locator)
        ax.yaxis.set_major_locator(y_major_locator)
        ax.xaxis.set_ticks_position('top')
        ax.invert_yaxis()
        plt.grid()
        for i in range(self.rows):
            for j in range(self.cols):
                color = color_dict[int(self.env[i][j])]
                rect = mpathes.Rectangle((j, i), 1, 1, color=color)
                ax.add_patch(rect)
        # plt.savefig('./cliffwalk.jpg')
        plt.show()

class Sarsa():
    def __init__(self, env):
        self.env = env
        self.rows = env.rows
        self.cols = env.cols
        self.map = env.env  # record the cliff,start,terminal,barrier,reward in the graph

    def learning(self, max_episode_num, gamma, epsilons):
        # gamma: the discount factor
        # max_episode_num: total episode num
        qtable = np.zeros((self.rows, self.cols, 4), np.float64)
        for epsilon in epsilons:
            for j in range(max_episode_num):
                print(j)
                x, y = 0, 0

                # find the best way form the four direction
                # at the begining, epsilon is large so the direction is randomly chosen in order to explore more
                # the invalid direction is set to be not allowed
                if random.random() < epsilon:
                    action = random.randrange(4)
                    while (self.valid(x, y, action) == 0):
                        action = random.randrange(4)
                else:
                    res = -10000
                    action = -1
                    for i in range(4):
                        if self.valid(x, y, i) != 0:
                            if qtable[x][y][i] > res:
                                res = qtable[x][y][i]
                                action = i

                # it will keep moving until reach the terminal
                while self.map[x][y] != 2:
                    x1, y1 = self.walk(x, y, action)
                    alpha = 0.5
                    reward = self.rewards(x1, y1, self.map[x1][y1])

                    #find the best way form the four direction
                    if random.random() < epsilon:
                        action1 = random.randrange(4)
                        while (self.valid(x1, y1, action1) == 0):
                            action1 = random.randrange(4)
                    else:
                        res = -10000
                        action1 = -1
                        for i in range(4):
                            if self.valid(x1, y1, i) != 0:
                                if qtable[x1][y1][i] > res:
                                    res = qtable[x1][y1][i]
                                    action1 = i

                    # use the formula to update the q value matrix
                    qtable[x][y][action]=(1-alpha)*qtable[x][y][action]+alpha*(reward+gamma*qtable[x1][y1][action1])
                    x, y, action = x1, y1, action1
        self.draw(qtable)

    def walk(self, x, y, action):
        if (action == 0):  # left
            return x, y - 1
        elif (action == 1):  # down
            return x + 1, y
        elif (action == 2):  # right
            return x, y + 1
        elif (action == 3):  # up
            return x - 1, y

    def rewards(self, x1, y1, type):
        if type == -1:  # cliff
            return -100
        elif type == 2:  # terminal
            return 10
        elif type == 3:  # red
            return -1
        return 0

    def valid(self, x, y, action):
        #0:invlid
        #1:valid
        x1, y1 = self.walk(x, y, action)
        if x1 < 0 or x1 >= self.rows or y1 < 0 or y1 >= self.cols:
            return 0
        elif self.map[x1][y1] == -2:  # barrier
            return 0
        return 1

    # show the graph of the qtable
    # the optimal policy for every state is marked in the graph
    def draw(self, qtable):
        fig,ax = plt.subplots(figsize=(8, 6))
        plt.xlim((0, self.cols))
        plt.ylim((0, self.rows))
        color_dict = {-1: "gray", 1: "yellow", 2: "orange", -2: "black", 3: "red", 0: "white", 4: "blue"}
        my_x_ticks = np.arange(0, self.cols, 1)
        my_y_ticks = np.arange(0, self.rows, 1)
        plt.xticks(my_x_ticks)
        plt.yticks(my_y_ticks)
        x_major_locator = MultipleLocator(1)
        y_major_locator = MultipleLocator(1)
        ax.xaxis.set_major_locator(x_major_locator)
        ax.yaxis.set_major_locator(y_major_locator)
        ax.xaxis.set_ticks_position('top')
        ax.invert_yaxis()
        plt.grid()
        for i in range(self.rows):
            for j in range(self.cols):
                color = color_dict[int(self.map[i][j])]
                rect = mpathes.Rectangle((j, i), 1, 1, color=color)
                ax.add_patch(rect)
                if (self.map[i][j] == 0 or self.map[i][j]==3 or self.map[i][j]==-1 or self.map[i][j]==1):
                    coordinates = ( ((j, i), (j + 0.5, i + 0.5), (j, i + 1)),
                                ((j + 1, i + 1), (j, i + 1), (j + 0.5, i + 0.5)),
                                ((j + 1, i), (j + 1, i + 1), (j + 0.5, i + 0.5)),
                                ((j, i), (j + 0.5, i + 0.5), (j + 1, i)),)
                    tmp = -10000
                    action=-1
                    for k in range(4):
                        if self.valid(i,j,k)==1:
                            if qtable[i][j][k]>tmp:
                                tmp=qtable[i][j][k]
                                action=k
                    for k in range(4):
                        ax.add_patch(mpathes.Polygon(coordinates[k], fill=(k == action), color='0.8', ))
                    ax.text(j + 0.3, i + 0.25, '{:.1f}'.format(qtable[i][j][3]))  # up
                    ax.text(j + 0.6, i + 0.55, '{:.1f}'.format(qtable[i][j][2]))  # right
                    ax.text(j + 0.3, i + 0.95, '{:.1f}'.format(qtable[i][j][1]))  # down
                    ax.text(j + 0.03, i + 0.55, '{:.1f}'.format(qtable[i][j][0]))  # left
        plt.savefig('./qtable.png')
        plt.show()


if __name__ == "__main__":
    Env = Environment()
    Env.show_env()
    sarsa = Sarsa(Env)
    sarsa.learning(500, 0.9, [1, 0.5, 0.01]) # a list of eplison value