#Maite Flores, Christina Torres, Ferdi Lesporis 

from maze_cat_and_mouse import *

class CatAndMouse():
    def __init__(self, maze):
        self.maze = Maze(maze)

    def catAndMouseTrain(self) :
        cat_win_count = 0
        mouse_win_count = 0
        game_amount=100
        epoch_amount=100
        episode_moves = 0
        max_steps= self.maze.col_size*self.maze.row_size
        turn = 0

        for epoch in range(epoch_amount):
            for episode in range(game_amount):
                self.maze.restart()
                game_over = False

            # n_episodes = 0
                while not game_over:
                    if turn == 0 :
                        cat_x, cat_y, cat_mode = self.maze.cat.state
                        
                        cat_valid_actions = self.maze.check_move((cat_x, cat_y))

                        if not cat_valid_actions: break
                        is_mouse = False
                        cat_action = self.maze.get_next_action(is_mouse)
                    
                        cat_old_x, cat_old_y, cat_mode = self.maze.cat.state
                        # Apply action, get reward and new envstate
                        cat_envstate, cat_reward, cat_game_status = self.maze.moves(is_mouse, cat_action)
                        self.maze.cat.actions.append(cat_action)
                        cat_new_x, cat_new_y, cat_mode = self.maze.cat.state
                        # Store episode (experience)
                        self.maze.cat.calculate_qval(cat_old_x, cat_old_y, cat_action, cat_reward, cat_new_x, cat_new_y)

                        game_status = self.maze.is_over()
                        if game_status == 'MouseGoal':
                            mouse_win_count = mouse_win_count + 1
                            game_over = True
                        elif game_status == 'CatGoal':
                            cat_win_count=cat_win_count+1
                            self.maze.cat.endGame_q_val(self.maze.cat.final_reward)
                            game_over = True
                        elif episode_moves >= max_steps:
                            game_over = True
                        elif game_status == 'Lost':
                            game_over = True
                        else:
                            game_over = False

                    if turn == 1 :
                        is_mouse = True
                        mouse_action = self.maze.get_next_action(is_mouse)
                    
                        mouse_old_x, mouse_old_y, mouse_mode = self.maze.mouse.state
                        # Apply action, get reward and new envstate
                        mouse_envstate, mouse_reward, mouse_game_status = self.maze.moves(is_mouse,mouse_action)
                        self.maze.mouse.actions.append(mouse_action)
                        mouse_new_x, mouse_new_y, mouse_mode = self.maze.mouse.state
                        # Store episode (experience)
                        self.maze.mouse.calculate_qval(mouse_old_x, mouse_old_y, mouse_action, mouse_reward, mouse_new_x, mouse_new_y)

                        game_status = self.maze.is_over()
                        if game_status == 'MouseGoal':
                            mouse_win_count = mouse_win_count + 1
                            game_over = True
                        elif game_status == 'CatGoal':
                            cat_win_count=cat_win_count+1
                            self.maze.cat.endGame_q_val(self.maze.cat.final_reward)
                            game_over = True
                        elif episode_moves >= max_steps:
                            game_over = True
                        elif game_status == 'Lost':
                            game_over = True
                        else:
                            game_over = False
                    episode_moves=episode_moves+1
                    turn = (turn + 1) % 2
                episode_moves = 0
                
            print("Epoch: ",epoch+1,"/",epoch_amount,"    |   Cat win rate: ", cat_win_count/game_amount,"    |   Mouse win rate: ", mouse_win_count/game_amount)
            cat_win_count = 0
            mouse_win_count = 0
        print("Trained!")

    def catTrain(self) :
        cat_win_count = 0
        game_amount=100
        epoch_amount=8
        episode_moves = 0
        max_steps= self.maze.col_size*self.maze.row_size
        turn = 0

        for epoch in range(epoch_amount):
            for episode in range(game_amount):
                self.maze.restart()
                game_over = False
                #x, y = self.maze.findRandomSpot()
                #self.maze.mouse.state = (x, y, 'start')

            # n_episodes = 0
                while not game_over:
                    if turn == 0 :
                        cat_x, cat_y, cat_mode = self.maze.cat.state
                        
                        cat_valid_actions = self.maze.check_move((cat_x, cat_y))

                        if not cat_valid_actions: break
                        is_mouse = False
                        cat_action = self.maze.get_next_action(is_mouse)
                    
                        cat_old_x, cat_old_y, cat_mode = self.maze.cat.state
                        # Apply action, get reward and new envstate
                        cat_envstate, cat_reward, cat_game_status = self.maze.moves(is_mouse, cat_action)
                        self.maze.cat.actions.append(cat_action)
                        cat_new_x, cat_new_y, cat_mode = self.maze.cat.state
                        # Store episode (experience)
                        self.maze.cat.calculate_qval(cat_old_x, cat_old_y, cat_action, cat_reward, cat_new_x, cat_new_y)

                        game_status = self.maze.is_over()
                        if game_status == 'MouseGoal':
                            game_over = True
                        elif game_status == 'CatGoal':
                            cat_win_count=cat_win_count+1
                            self.maze.cat.endGame_q_val(self.maze.cat.final_reward)
                            game_over = True
                        elif episode_moves >= max_steps:
                            game_over = True
                        elif game_status == 'Lost':
                            game_over = True
                        else:
                            game_over = False
                

                    if turn == 1 :
                        mouse_x, mouse_y, mouse_mode = self.maze.mouse.state
                        is_mouse = True
                        mouse_action = self.maze.get_next_action(is_mouse)
                        mouse_envstate, mouse_reward, mouse_game_status = self.maze.moves(is_mouse,mouse_action)
                        

                    game_status = self.maze.is_over()
                    if game_status == 'MouseGoal':
                        game_over = True
                    elif game_status == 'CatGoal':
                        cat_win_count=cat_win_count+1
                        self.maze.cat.endGame_q_val(self.maze.cat.final_reward)
                        game_over = True
                    elif episode_moves >= max_steps:
                        game_over = True
                    elif game_status == 'Lost':
                        game_over = True
                    else:
                        game_over = False
                    episode_moves=episode_moves+1
                    turn = (turn + 1) % 2
                episode_moves = 0
                
            print("Epoch: ",epoch+1,"/",epoch_amount,"    |   Cat win rate: ", cat_win_count/game_amount)
            cat_win_count = 0
        print("Trained!")


    def mouseTrain(self) :
        mouse_win_count=0
        game_amount=100
        epoch_amount=5
        episode_moves = 0
        max_steps= self.maze.col_size*self.maze.row_size
        turn = 0

        for epoch in range(epoch_amount):
            for episode in range(game_amount):
                self.maze.restart() 
                game_over = False
                x, y = self.maze.findRandomSpot()
                self.maze.cat.state = (x, y, 'start')

            # n_episodes = 0
                while not game_over:
                    if turn == 0 :
                        mouse_x, mouse_y, mouse_mode = self.maze.mouse.state
                        mouse_valid_actions = self.maze.check_move((mouse_x, mouse_y))

                        if not mouse_valid_actions: break
                        is_mouse = True
                        mouse_action = self.maze.get_next_action(is_mouse)
                    
                        mouse_old_x, mouse_old_y, mouse_mode = self.maze.mouse.state
                        # Apply action, get reward and new envstate
                        mouse_envstate, mouse_reward, mouse_game_status = self.maze.moves(is_mouse,mouse_action)
                        self.maze.mouse.actions.append(mouse_action)
                        mouse_new_x, mouse_new_y, mouse_mode = self.maze.mouse.state
                        # Store episode (experience)
                        self.maze.mouse.calculate_qval(mouse_old_x, mouse_old_y, mouse_action, mouse_reward, mouse_new_x, mouse_new_y)

                        game_status = self.maze.is_over()
                        if game_status == 'MouseGoal':
                            mouse_win_count = mouse_win_count+1
                            #self.maze.mouse.endGame_q_val(self.maze.mouse.final_reward)
                            game_over = True
                        elif episode_moves >= max_steps:
                            game_over = True
                        elif game_status == 'Lost':
                            game_over = True
                        else:
                            game_over = False

                    if turn == 1 :
                        cat_x, cat_y, cat_mode = self.maze.cat.state
                        cat_valid_actions = self.maze.check_move((cat_x, cat_y))
                        cat_action = random.choice(cat_valid_actions)
                        self.maze.moves(False, cat_action)
                    
                    game_status = self.maze.is_over()
                    if game_status == 'MouseGoal':
                        mouse_win_count = mouse_win_count+1
                        #self.maze.mouse.endGame_q_val(self.maze.mouse.final_reward)
                        game_over = True
                    elif episode_moves >= max_steps:
                        game_over = True
                    elif game_status == 'Lost':
                        game_over = True
                    else:
                        game_over = False
                    episode_moves=episode_moves+1
                    turn = (turn + 1) % 2
                episode_moves = 0

            print("Epoch: ",epoch+1,"/",epoch_amount,"    |   Mouse win rate: ", mouse_win_count/game_amount)
            mouse_win_count=0
        print("Trained!")

    def Battle(self):

        mouse_win_count=0
        cat_win_count = 0
        game_amount=1
        epoch_amount=1
        max_steps= self.maze.col_size*self.maze.row_size
        episode_moves = 0
        ready = input("Ready for demo?")
        turn = 0
        for epoch in range(epoch_amount):
            for episode in range(game_amount):
                self.maze.restart()
                game_over = False

            # n_episodes = 0
                while not game_over:
                    steps = 5
                    if turn == 0 :
                        cat_x, cat_y, cat_mode = self.maze.cat.state
                        cat_valid_actions = self.maze.check_move((cat_x, cat_y))

                        if not cat_valid_actions: break
                        is_mouse = False
                        cat_action = self.maze.nStepCat(steps)
                        self.maze.cat.actions.append(cat_action)
                    
                        cat_old_x, cat_old_y, cat_mode =self.maze.cat.state
                        # Apply action, get reward and new envstate
                        cat_envstate, cat_reward, cat_game_status = self.maze.moves(is_mouse, cat_action)
                        cat_new_x, cat_new_y, cat_mode = self.maze.cat.state
                        # Store episode (experience)
                        self.maze.cat.calculate_qval(cat_old_x, cat_old_y, cat_action, cat_reward, cat_new_x, cat_new_y)

                    if turn == 1 :
                        mouse_x, mouse_y, mouse_mode = self.maze.mouse.state
                        mouse_valid_actions = self.maze.check_move((mouse_x, mouse_y))

                        if not mouse_valid_actions: break
                        is_mouse = True
                        mouse_action = self.maze.nStepMouse(steps)
                        self.maze.mouse.actions.append(mouse_action)
                    
                        mouse_old_x, mouse_old_y, mouse_mode = self.maze.mouse.state
                        # Apply action, get reward and new envstate
                        mouse_envstate, mouse_reward, mouse_game_status = self.maze.moves(is_mouse,mouse_action)
                        mouse_new_x, mouse_new_y, mouse_mode = self.maze.mouse.state
                        # Store episode (experience)
                        self.maze.mouse.calculate_qval(mouse_old_x, mouse_old_y, mouse_action, mouse_reward, mouse_new_x, mouse_new_y)

                    self.maze.drawState()

                    game_status = self.maze.is_over()
                    if game_status == 'MouseGoal':
                        mouse_win_count=mouse_win_count+1
                        #self.maze.mouse.endGame_q_val(self.maze.mouse.final_reward)
                        game_over = True
                    elif game_status == 'CatGoal':
                        cat_win_count=cat_win_count+1
                        #self.maze.cat.endGame_q_val(self.maze.cat.final_reward)
                        game_over = True
                    elif episode_moves >= max_steps:
                        game_over = True
                    elif game_status == 'Lost':
                        game_over = True
                    else:
                        game_over = False

                    episode_moves=episode_moves+1
                    turn = (turn + 1) % 2
                episode_moves=0
                
            print("Epoch: ",epoch+1,"/",epoch_amount,"    |   Mouse win rate: ", mouse_win_count/game_amount,"    |   Cat win rate: ", cat_win_count/game_amount)
            mouse_win_count=0
            cat_win_count = 0

    def multiplayer(self, is_mouse) :
        status = input("Ready?")
        steps = 4
        turn = 0
        if is_mouse == True :
            #play as mouse
            self.maze.restart()
            game_over = False

        # n_episodes = 0
            while not game_over:
                if turn == 0 :
                    cat_x, cat_y, cat_mode = self.maze.cat.state
                    cat_valid_actions = self.maze.check_move((cat_x, cat_y))
                    if not cat_valid_actions: break
                    is_mouse = False
                    cat_action = self.maze.nStepCat(steps)
                    self.maze.cat.actions.append(cat_action)
                
                    cat_old_x, cat_old_y, cat_mode =self.maze.cat.state
                    # Apply action, get reward and new envstate
                    cat_envstate, cat_reward, cat_game_status = self.maze.moves(is_mouse, cat_action)
                    cat_new_x, cat_new_y, cat_mode = self.maze.cat.state
                    # Store episode (experience)
                    self.maze.cat.calculate_qval(cat_old_x, cat_old_y, cat_action, cat_reward, cat_new_x, cat_new_y)

                if turn == 1 :
                    mouse_x, mouse_y, mouse_mode = self.maze.mouse.state
                    mouse_valid_actions = self.maze.check_move((mouse_x, mouse_y))

                    if not mouse_valid_actions: break
                    is_mouse = True
                    mouse_action = self.maze.window.checkKey()
                
                    if ((mouse_action == 'w' or mouse_action == 'W') and (1 in mouse_valid_actions)):
                        mouse_envstate, mouse_reward, mouse_game_status = self.maze.moves(is_mouse,1)
                    elif ((mouse_action == 'a' or mouse_action == 'A') and (0 in mouse_valid_actions)):
                        mouse_envstate, mouse_reward, mouse_game_status = self.maze.moves(is_mouse,0)
                    elif ((mouse_action == 'd' or mouse_action == 'D') and (2 in mouse_valid_actions)):
                        mouse_envstate, mouse_reward, mouse_game_status = self.maze.moves(is_mouse,2)
                    elif ((mouse_action == 's' or mouse_action == 'S') and (3 in mouse_valid_actions)):
                        mouse_envstate, mouse_reward, mouse_game_status = self.maze.moves(is_mouse,3)


                self.maze.drawState()

                game_status = self.maze.is_over()
                if game_status == 'MouseGoal':
                    mouse_win_count=mouse_win_count+1
                    game_over = True
                elif game_status == 'CatGoal':
                    cat_win_count=cat_win_count+1
                    game_over = True
                elif game_status == 'Lost':
                    game_over = True
                else:
                    game_over = False
                turn = (turn + 1) % 2
                

        else :
            #play as cat
            self.maze.restart()
            game_over = False

        # n_episodes = 0
            while not game_over:
                if turn == 0 :
                    cat_x, cat_y, cat_mode = self.maze.cat.state
                    cat_valid_actions = self.maze.check_move((cat_x, cat_y))
                    if not cat_valid_actions: break
                    is_mouse = False
                
                    cat_old_x, cat_old_y, cat_mode =self.maze.cat.state

                    cat_action = self.maze.window.checkKey()
                
                    if ((cat_action == 'w' or cat_action == 'W') and (1 in cat_valid_actions)):
                        cat_envstate, cat_reward, cat_game_status = self.maze.moves(is_mouse,1)
                    elif ((cat_action == 'a' or cat_action == 'A') and (0 in cat_valid_actions)):
                        cat_envstate, cat_reward, cat_game_status = self.maze.moves(is_mouse,0)
                    elif ((cat_action == 'd' or cat_action == 'D') and (2 in cat_valid_actions)):
                        cat_envstate, cat_reward, cat_game_status = self.maze.moves(is_mouse,2)
                    elif ((cat_action == 's' or cat_action == 'S') and (3 in cat_valid_actions)):
                        cat_envstate, cat_reward, cat_game_status = self.maze.moves(is_mouse,3)

                if turn == 1 :
                    mouse_x, mouse_y, mouse_mode = self.maze.mouse.state
                    mouse_valid_actions = self.maze.check_move((mouse_x, mouse_y))

                    if not mouse_valid_actions: break
                    is_mouse = True
                    mouse_action = self.maze.nStepMouse(steps)
                    self.maze.mouse.actions.append(mouse_action)
                
                    mouse_old_x, mouse_old_y, mouse_mode = self.maze.mouse.state
                    # Apply action, get reward and new envstate
                    mouse_envstate, mouse_reward, mouse_game_status = self.maze.moves(is_mouse,mouse_action)
                    mouse_new_x, mouse_new_y, mouse_mode = self.maze.mouse.state
                    # Store episode (experience)
                    self.maze.mouse.calculate_qval(mouse_old_x, mouse_old_y, mouse_action, mouse_reward, mouse_new_x, mouse_new_y)

                self.maze.drawState()

                game_status = self.maze.is_over()
                if game_status == 'MouseGoal':
                    mouse_win_count=mouse_win_count+1
                    game_over = True
                elif game_status == 'CatGoal':
                    cat_win_count=cat_win_count+1
                    game_over = True
                elif game_status == 'Lost':
                    game_over = True
                else:
                    game_over = False
                turn = (turn + 1) % 2



def main() :
    my_maze = CatAndMouse("/Users/jailene/Desktop/idk_maze.txt")
    
    #my_maze.mouseTrain()
    #my_maze.catTrain()
    my_maze.catAndMouseTrain()
    my_maze.Battle()
    #my_maze.multiplayer(False)


main()