#Maite Flores, Christina Torres, Ferdi Lesporis 
import math
import random
import numpy as np
from tkinter import *
from graphics import *
from CatAi import *
from MouseAi import *

dif_actions = [0,1,2,3]
time_lapse = 15
amount = 25

epsilon = 0.7
learning_rate = 0.7
discount = 0.9

class Maze(object):
    def __init__(self, maze, runner = (0,0), useMouseAi=True):
        self.window = GraphWin("Cat and Mouse", 640, 640, autoflush=False)
        self.row_size = 0
        self.col_size = 0
        self.mazeOutline = []
        self.createOutline(maze)
        self.goal = (self.row_size-1, self.col_size-1)

        self.mouse = MouseAi(self.row_size-1, self.col_size-1)
        # self.is_mouse= random.choice([True, False])
        self.cat = CatAi(self.row_size-1, self.col_size-1)

        self.restart()
        #draws maze
        self.renderWindow = True
        self.createMaze()
        self.createAgent()


    def restart(self) :
        self.mouse.visited_square.clear()
        self.mouse.actions.clear()
        self.cat.visited_square.clear()
        self.cat.actions.clear()
        runner_xcor = 0
        runner_ycor = 0
        self.mouse.state = (runner_xcor, runner_ycor, 'start')
        self.min_reward = (-.6 * (self.col_size*self.row_size))
        self.mouse.final_reward = 0
        self.catCorner()
        self.cat.final_reward = 0


    def catCorner(self) :
        x = self.row_size-1
        y = self.col_size-1
        if self.mazeOutline[0][y] == ' ' :
            self.cat.state = (0, y, 'start')
        elif self.mazeOutline[1][y] == ' ' :
            self.cat.state = (1, y, 'start')
        elif self.mazeOutline[0][y-1] == ' ' :
            self.cat.state = (0, y-1, 'start')
        elif self.mazeOutline[1][y-1] == ' ' :
            self.cat.state = (1, y-1, 'start')


    #######draw to window section
    def createOutline(self, fileName) :
        mazeFile = open(fileName, 'r')
        row_size = 0
        col_size = 0
        while True:
            row = mazeFile.readline()
            curLine = []
            if row =='' :
                break
            for i in row :
                if not(i == '\n') :
                    curLine.append(i)
            row_size += 1
            col_size= len(curLine)
            self.mazeOutline.append(curLine)
        self.row_size = row_size
        self.col_size = col_size
        mazeFile.close()

    def createAgent(self) :
        mousePosition = (0,0)
        goal = (self.row_size-1, self.col_size-1)
        mousex, mousey = mousePosition
        goalx, goaly = goal

        catx, caty, mode = self.cat.state

        self.mouse.object = Oval(Point(mousey*amount, mousex*amount), Point(mousey*amount+amount,mousex*amount+amount))
        self.mouse.object.setFill("pink")

        self.cat.object = Oval(Point(caty*amount, catx*amount), Point(caty*amount+amount,catx*amount+amount))
        self.cat.object.setFill("purple")

        self.cheese = Rectangle(Point(goaly*amount, goalx*amount), Point(goaly*amount+amount,goalx*amount+amount))
        self.cheese.setFill("yellow")


        ##opens window
        if self.renderWindow == True :
            self.mouse.object.draw(self.window)
            self.cheese.draw(self.window)
            self.cat.object.draw(self.window)
            update(1) 

    def createMaze(self) :
        for x in range(self.row_size) :
            for y in range(self.col_size) :
                mazeSquare = Rectangle(Point(y*amount, x*amount), Point(y*amount+amount, x*amount+amount))
                if self.mazeOutline[x][y] =='#' :
                    mazeSquare.setFill("black")
                    mazeSquare.draw(self.window)
                else :
                    mazeSquare.setFill("light grey")
                    mazeSquare.draw(self.window)

    def drawState(self) :
        #get new mouse position
        mousex, mousey, mouseMode = self.mouse.state
        #translate it to the size of the display
        mousex = mousex * amount
        mousey = mousey * amount

        catx, caty, catMode = self.cat.state
        catx = catx * amount
        caty = caty * amount
        self.mouse.object.undraw()
        self.mouse.object = Oval(Point(mousey, mousex), Point(mousey+amount,mousex+amount))
        self.mouse.object.setFill("pink")

        self.cat.object.undraw()
        self.cat.object = Oval(Point(caty, catx), Point(caty+amount,catx+amount))
        self.cat.object.setFill("purple")

        self.mouse.object.draw(self.window)
        update(time_lapse)

        self.cat.object.draw(self.window)
        update(time_lapse)


       
    #Movement Section
    def change_state(self,is_mouse, move):
        if is_mouse :
            new_xcor,new_ycor, new_mode = runner_xcor, runner_ycor, mode = self.mouse.state
            if self.mazeOutline[runner_xcor][runner_ycor] != '#':
                self.mouse.visited_square.append((runner_xcor, runner_ycor))
            
        else :
            new_xcor,new_ycor, new_mode = runner_xcor, runner_ycor, mode = self.cat.state
            if self.mazeOutline[runner_xcor][runner_ycor] != '#':
                self.cat.visited_square.append((runner_xcor, runner_ycor))

        is_valid = self.check_move((new_xcor, new_ycor))

        if not is_valid:
            new_mode = 'barrier'
        elif move in is_valid:
            new_mode = 'running'
            if move == 0: #left
                new_ycor-=1
            elif move == 1: #up
                new_xcor -=1
            if move == 2: #right
                new_ycor +=1
            elif move == 3: #down
                new_xcor+=1
        else:
            new_mode = 'stop'

        if is_mouse :
            cat_x, cat_y, cat_mode = self.cat.state
            if cat_x == new_xcor and cat_y == new_ycor :
                new_mode = 'dead'
                self.cat.state = (cat_x, cat_y, 'eating')
            self.mouse.state = (new_xcor,new_ycor, new_mode)
        else :
            mouse_x, mouse_y, mouse_mode = self.mouse.state
            if new_xcor == mouse_x and new_ycor == mouse_y :
                new_mode = 'eating'
                self.mouse.state = (mouse_x, mouse_y, 'dead')
            self.cat.state = (new_xcor,new_ycor, new_mode)

               
    def get_next_action(self, is_mouse):
        if is_mouse :
            cur_x, cur_y, cur_mode = self.mouse.state
        else :
            cur_x, cur_y, cur_mode = self.cat.state

        valid_actions = self.check_move((cur_x, cur_y))
        
        # Get next action
        if np.random.rand() > epsilon:
            action = random.choice(valid_actions)

        else:
            if is_mouse:
                action = np.argmax(self.mouse.q_vals[cur_x, cur_y])
            else : 
                action = np.argmax(self.cat.q_vals[cur_x, cur_y])
        return action

    #does the action
    def moves(self, is_mouse, decision):
        self.change_state(is_mouse, decision)
        if is_mouse :
            score = self.mouse.reward(self.mouse.state, self.min_reward,self.row_size, self.col_size)
            self.mouse.final_reward += score
        else :
            score = self.cat.reward(self.cat.state, self.min_reward,self.row_size, self.col_size)
            self.cat.final_reward += score
        maze_state = self.check_state()
        check_is_over = self.is_over()
        return maze_state,score, check_is_over


    #Enviroment Checking Section
    def is_over(self):
        if self.mouse.final_reward < self.min_reward:
            return 'Lost'
        runner_xcor,runner_ycor, mode = self.mouse.state
        x_axis = self.row_size
        y_axis = self.col_size
        if runner_xcor == x_axis-1 and runner_ycor == y_axis-1:
            return 'MouseGoal'
        catx, caty, cat_mode = self.cat.state
        if runner_xcor == catx and runner_ycor == caty:
            return 'CatGoal'
        return 'Playing'
       
    def check_state(self):
        pic = self.create()
        maze_state = pic#.reshape((1,-1))
        return maze_state


    # creates the environment
    def create(self):
        pic = self.mazeOutline.copy()

        for i in range (self.row_size):
            for j in range (self.col_size):
                if pic[i][j] != '#' :
                    pic[i][j] = ' '

        #place runner
        run_x,run_y,running = self.mouse.state
        pic[run_x][run_y] = 'M'

        cat_x,cat_y,mode = self.cat.state
        pic[cat_x][cat_y] = 'C'

        return pic

    def check_move(self, cell = NONE):

        cur_xcor, cur_ycor = cell

        valid_actions = [0,1,2,3]
        #Up, down, left, right
        x_axis = self.row_size
        y_axis = self.col_size

        if cur_xcor == 0:
            valid_actions.remove(1)
        elif cur_xcor == x_axis-1:
            valid_actions.remove(3)
        if cur_ycor == 0:
            valid_actions.remove(0)
        elif cur_ycor == y_axis - 1:
            valid_actions.remove(2)

        if cur_xcor > 0 and self.mazeOutline[cur_xcor-1][cur_ycor] == '#':
            valid_actions.remove(1)
        if cur_xcor < x_axis-1 and self.mazeOutline[cur_xcor+1][cur_ycor] == '#':
            valid_actions.remove(3)
        if cur_ycor > 0 and self.mazeOutline[cur_xcor][cur_ycor-1] == '#':
            valid_actions.remove(0)
        if cur_ycor < y_axis-1 and self.mazeOutline[cur_xcor][cur_ycor+1] == '#':
            valid_actions.remove(2)

        return valid_actions

    def findRandomSpot(self) :
        freeSpaces = []
        for x in range(self.row_size) :
            for y in range(self.col_size) :
                if (not(x==self.row_size-1) and not(y == self.col_size-1)) and (not(x==0) and not(y==0)):
                    if self.mazeOutline[x][y] == ' ' :
                        freeSpaces.append([x,y])
        posx, posy = random.choice(freeSpaces)
        return posx, posy



    def nStepMouse(self, steps) :
        n_step_agent_1 = Oval(Point(0,0), Point(0,0))
        n_step_agent_2 = Oval(Point(0,0), Point(0,0))
        n_step_agent_3 = Oval(Point(0,0), Point(0,0))
        n_step_agent_4 = Oval(Point(0,0), Point(0,0))
        cur_x, cur_y, mode = self.mouse.state
        valid_actions = self.check_move((cur_x, cur_y))
        up = 0
        down = 0
        right = 0
        left = 0
        
        left_open = True
        right_open = True
        down_open = True
        up_open = True

        cur_left = 0
        cur_right = 0
        cur_up = 0 
        cur_down = 0

        if 0 not in valid_actions :
            left_open = False
        if 1 not in valid_actions :
            up_open = False
        if 2 not in valid_actions :
            right_open = False
        if 3 not in valid_actions :
            down_open = False

        for step in range(steps) :
            n_step_agent_1.undraw()
            n_step_agent_2.undraw()
            n_step_agent_3.undraw()
            n_step_agent_4.undraw()
            
            if left_open == True :
                if ((cur_y - step) < 0) :
                    left_open = False
                elif ((cur_x == self.row_size-1)&((cur_y - step) == self.col_size-1)) :
                    return 0
                elif (cur_x, cur_y- step) in self.mouse.visited_square :
                    n_step_agent_1 = Oval(Point(((cur_y - step)*amount), (cur_x*amount)), Point(((cur_y - step)*amount)+amount, (cur_x*amount)+amount))
                elif self.mazeOutline[cur_x][cur_y- step] == '#' :
                    left_open = False
                else :
                    cur_left =  self.mouse.q_vals[cur_x, (cur_y - step), 0]
                    if cur_left > left :
                        left = cur_left
                    n_step_agent_1 = Oval(Point(((cur_y - step)*amount), (cur_x*amount)), Point(((cur_y - step)*amount)+amount, (cur_x*amount)+amount))
            
            if up_open == True :
                if((cur_x - step) < 0) :
                    up_open = False
                elif (((cur_x - step) == self.row_size-1)&((cur_y) == self.col_size-1)) :
                    return 1
                elif (cur_x-step, cur_y) in self.mouse.visited_square :
                    n_step_agent_2 = Oval(Point(((cur_y)*amount), ((cur_x-step)*amount)), Point(((cur_y)*amount)+amount, ((cur_x-step)*amount)+amount))
                elif self.mazeOutline[cur_x- step][cur_y] == '#' :
                    up_open = False 
                else :
                    cur_up = self.mouse.q_vals[(cur_x - step), cur_y, 1]
                    if cur_up > up :
                        up = cur_up
                    n_step_agent_2 = Oval(Point(((cur_y)*amount), ((cur_x-step)*amount)), Point(((cur_y)*amount)+amount, ((cur_x-step)*amount)+amount))
            
            if right_open == True :
                if ((cur_y + step) >= self.row_size) :
                    right_open= False
                elif ((cur_x == self.row_size-1)&((cur_y + step) == self.col_size-1)) :
                    return 2
                elif (cur_x, cur_y+step) in self.mouse.visited_square :
                    n_step_agent_3 = Oval(Point(((cur_y + step)*amount), (cur_x*amount)), Point(((cur_y + step)*amount)+amount, (cur_x*amount)+amount))
                elif self.mazeOutline[cur_x][cur_y + step] == '#' :
                    right_open = False
                else : 
                    cur_right = self.mouse.q_vals[cur_x, (cur_y+ step), 2]
                    if cur_right > right :
                        right = cur_right
                    n_step_agent_3 = Oval(Point(((cur_y + step)*amount), (cur_x*amount)), Point(((cur_y + step)*amount)+amount, (cur_x*amount)+amount))
            
            if down_open == True :
                if ((cur_x + step) >= self.col_size) :
                    down_open = False
                elif (((cur_x + step) == self.row_size-1)&((cur_y) == self.col_size-1)) :
                    return 3
                elif (cur_x+step, cur_y) in self.mouse.visited_square :
                    n_step_agent_4 = Oval(Point(((cur_y)*amount), ((cur_x+step)*amount)), Point(((cur_y)*amount)+amount, ((cur_x+step)*amount)+amount))
                elif self.mazeOutline[cur_x + step][cur_y] == '#' :
                    down_open = False
                else :
                    cur_down = self.mouse.q_vals[(cur_x+step), cur_y, 3]
                    if cur_down > down :
                        down = cur_down
                    n_step_agent_4 = Oval(Point(((cur_y)*amount), ((cur_x+step)*amount)), Point(((cur_y)*amount)+amount, ((cur_x+step)*amount)+amount))

            n_step_agent_1.draw(self.window)
            n_step_agent_2.draw(self.window)
            n_step_agent_3.draw(self.window)
            n_step_agent_4.draw(self.window)
            update(time_lapse)
            
        max_dir = max(up, down, left, right)

        n_step_agent_1.undraw()
        n_step_agent_2.undraw()
        n_step_agent_3.undraw()
        n_step_agent_4.undraw()
        update(time_lapse)

        if ((max_dir == up) & (1 in valid_actions)) :
            return 1
        elif ((max_dir == down) & (3 in valid_actions)) :
            return 3
        elif ((max_dir == left) & (0 in valid_actions)) :
            return 0
        elif ((max_dir == right) & (2 in valid_actions)) :
            return 2
            

    def nStepCat(self, steps) :
        n_step_agent_1 = Oval(Point(0,0), Point(0,0))
        n_step_agent_2 = Oval(Point(0,0), Point(0,0))
        n_step_agent_3 = Oval(Point(0,0), Point(0,0))
        n_step_agent_4 = Oval(Point(0,0), Point(0,0))
        pic = self.create()
        cur_x, cur_y, mode = self.cat.state
        valid_actions = self.check_move((cur_x, cur_y))
        up = 0
        down = 0
        right = 0
        left = 0
        
        left_open = True
        right_open = True
        down_open = True
        up_open = True

        cur_left = 0
        cur_right = 0
        cur_up = 0 
        cur_down = 0

        if 0 not in valid_actions :
            left_open = False
        if 1 not in valid_actions :
            up_open = False
        if 2 not in valid_actions :
            right_open = False
        if 3 not in valid_actions :
            down_open = False
        

        for step in range(steps) :
            n_step_agent_1.undraw()
            n_step_agent_2.undraw()
            n_step_agent_3.undraw()
            n_step_agent_4.undraw()
            
            if left_open == True :
                if ((cur_y - step) < 0) :
                    left_open = False
                elif self.mazeOutline[cur_x][cur_y- step] == '#' :
                    left_open = False
                elif pic[cur_x][cur_y-step] == 'M' :
                    return 0
                else :
                    n_step_agent_1 = Oval(Point(((cur_y - step)*amount), (cur_x*amount)), Point(((cur_y - step)*amount)+amount, (cur_x*amount)+amount))
            
            if up_open == True :
                if((cur_x - step) < 0) :
                    up_open = False
                elif self.mazeOutline[cur_x- step][cur_y] == '#' :
                    up_open = False 
                elif pic[cur_x-step][cur_y] == 'M' :
                    return 1
                else :
                    n_step_agent_2 = Oval(Point(((cur_y)*amount), ((cur_x-step)*amount)), Point(((cur_y)*amount)+amount, ((cur_x-step)*amount)+amount))
            
            if right_open == True :
                if ((cur_y + step) >= self.row_size) :
                    right_open = False
                elif self.mazeOutline[cur_x][cur_y + step] == '#' :
                    right_open = False
                elif pic[cur_x][cur_y+step] == 'M' :
                    return 2
                else : 
                    n_step_agent_3 = Oval(Point(((cur_y + step)*amount), (cur_x*amount)), Point(((cur_y + step)*amount)+amount, (cur_x*amount)+amount))
            
            if down_open == True :
                if ((cur_x + step) >= self.col_size) :
                    down_open = False
                elif self.mazeOutline[cur_x + step][cur_y] == '#' :
                    down_open = False

                elif pic[cur_x+step][cur_y] == 'M' :
                    return 3
                else :
                    n_step_agent_4 = Oval(Point(((cur_y)*amount), ((cur_x+step)*amount)), Point(((cur_y)*amount)+amount, ((cur_x+step)*amount)+amount))
            n_step_agent_1.draw(self.window)
            n_step_agent_2.draw(self.window)
            n_step_agent_3.draw(self.window)
            n_step_agent_4.draw(self.window)
            update(time_lapse)

        n_step_agent_1.undraw()
        n_step_agent_2.undraw()
        n_step_agent_3.undraw()
        n_step_agent_4.undraw()
        update(time_lapse)
        
        
        action = self.get_next_action(False)
        return action

        
    
    

    