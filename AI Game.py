import random
class Game:
    def __init__(player):
        player.initialize_game()

    def initialize_game(player):
        player.current_state = [[1,-1,0],
                              [1,0,1],
                              [0,1,-1]]
        player.score = player.current_state[2][0]
        player.s = player.score
        player.start = [2,0]
        variable = player.start
        player.turn = 'player'
        player.state = [[1,-1,0],
                        [1,0,1],
                        [0,1,-1]]
    
    def draw_board(player):
        for i in range(0, 3):
            for j in range(0, 3):
                print('{}|'.format(player.current_state[i][j]), end=" ")
            print()
        print()
                    
    def valid(player,r,c,x,y):
        res = player.states(x,y)
        if r < 0 or r > 2 or c < 0 or c > 2:
            return False
        item = [r,c]
        if item in res:
            return True
        else:
            return False
        
    def end(player, moves,goal):
        if moves == 0:
            if player.score >= goal:
                return 'player'
            else:
                return 'fail'
        return None
    available = []
    def states(player,r,c):
        del player.available[:]
        if r > 0 and r <= 2 and c <= 2:
            player.available.append([r-1,c])
            
        if r < 2 and r >= 0 and c <= 2:
            player.available.append([r+1,c])

        if c > 0 and c <= 2 and r <= 2:
            player.available.append([r,c-1])

        if c < 2 and c >= 0 and r <= 2:
            player.available.append([r,c+1])
        return player.available
    green = []
    
    def max_alpha_beta(player,start,green,moves,goal,alpha,beta):
        maxvalue = -1
        result = player.end(moves,goal)
        x = start[0]
        y = start[1]
        green = [x,y]
        pre = player.current_state[x][y]
        states = player.states(x,y)
        if result == 'player':
            return(1,0,0)
        if result == 'fail':
            return(0,0,0)
        for i in range(0,3):
            for j in range(0,3):
                ss = [i,j]
                if ss in states:
                    player.current_state[i][j] += player.current_state[x][y] 
                    player.current_state[x][y] = 100                         
                    moves -= 1                                               
                    goal = player.current_state[i][j]                        
                    start = [i,j]
                    (minv,value) = player.min_alpha_beta(green,start,moves,goal,alpha,beta)  
                    
                    if minv > maxvalue:                                      
                        maxvalue = minv
                        x = i
                        y = j
                        start = [x,y]
                        green = start
                    #prunning
                    goal = pre                                               
                    moves += 1                                               
                    start = green
                    for s in range(0,3):
                        for r in range(0,3):
                            player.current_state[s][r] = player.state[s][r]
                    if maxvalue >= beta:
                        return(maxvalue,x,y)
                    alpha = max(maxvalue,alpha)
                    if alpha >= beta:
                        break
        return (maxvalue,x,y)
    
    def min_alpha_beta(player,start,green,moves,goal,alpha,beta):
        minvalue = 2
        randomNum = [-1,0,1]
        value = None
        result = player.end(moves,goal)
        if result == 'player':
            return(1,0)
        if result == 'fail':
            return(0,0)
        x = start[0]
        y = start[1]
        randomNo = random.randint(-1,1)
        player.current_state[x][y] = randomNo
        (maxv,x,y) = player.max_alpha_beta(green,green,moves,goal,alpha,beta)
        
        if maxv < minvalue:
            minvalue = maxv
            value = randomNo
        
        for s in range(0,3):
            for r in range(0,3):
                player.current_state[s][r] = player.state[s][r]
                
        minvalue = min(minvalue,maxv)
        beta = min(minvalue,beta)
        if minvalue < beta:
            beta = minvalue
                        
        if alpha >= beta:
            return(alpha,value)
            #break
        return(minvalue,value)

    def play(player):
        goal = int(input('Enter minimum number to reach: '))
        moves = int(input('Enter maximum number of moves: '))
        while (True):
            player.draw_board()
            player.result = player.end(moves,goal)
            if player.result != None:
                if player.result == 'player':
                    print('Player wins, score = ', player.score)
                else:
                    print('fail, score = ', player.score)
                player.initialize_game()
                return
       
            if player.turn == 'player':
                print('-----------------------------------------------------------------------------')
                while(player.turn == 'player'):
                    (maxi,x1,y1) = player.max_alpha_beta(player.start,player.start,moves,player.score,-1,2)
                    if player.valid(x1,y1,player.start[0],player.start[1]):
                        variable = player.start
                        player.current_state[x1][y1] += player.score
                        player.current_state[player.start[0]][player.start[1]] = 100
                        player.score = player.current_state[x1][y1]
                        player.state[x1][y1] = player.current_state[x1][y1]
                        player.state[player.start[0]][player.start[1]] = 100
                        player.start = [x1,y1]
                        moves -= 1
                        if player.score == goal:
                            player.s = player.score
                        if player.score < player.s:
                            player.score = player.s
                        elif player.score >= player.s:
                            player.s = player.score
                            player.score = player.s
                        player.turn = 'AI'
                    
            else:
                (mini,value) = player.min_alpha_beta(variable,player.start,moves,player.score,-1,2)
                x = variable[0]
                y = variable[1]
                player.current_state[x][y] = value
                player.state[x][y] = value
                player.turn = 'player'
                
                     
                
def main():
    g = Game()
    g.play()
            

if __name__ == "__main__":
    main()





