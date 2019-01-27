from oxogame.GameBoard import Oxo_board
from random import randint



def dumb_play(game_board):
    for i in range(10):
        game_board.place_bubble(randint(1, 3), randint(1, 3))
        game_board.place_cross(randint(1, 3), randint(1, 3))
        if game_board.check_oxo():
            game_board.printBoard()
            break
        elif game_board.has_move():
            game_board.printBoard()
            break


class Not_So_Smart_Machine:

    def __init__(self,reward,penalty):
        self.game_board = Oxo_board()
        orig =  state(self.game_board)
        self.states = dict([(orig.state,orig)])
        self.victories = 0
        self.total_victories = 0
        self.losses = 0
        self.total_losses = 0
        self.draws = 0
        self.total_draws = 0
        self.overal_fitness = 0
        self.best_fitness = 0
        self.reward = reward
        self.penalty = penalty
        orig =  state(self.game_board)
        self.states = dict([(orig.state,orig)])
        self.origin = orig
        self.fintesses = []


    def smarter_play(self,simulations):
        print("Starting simulation: ", simulations , " runs planned with R: ", self.reward, " P",  self.penalty)
        #100 games
        for i in range(simulations):
            self.play_many_games()
        print("------------------------------------------")
        print("Simulation ended")
        print("Games won:" , self.total_victories,"draws : ", self.total_draws, " losses: " ,self.total_losses)
        print("Best fitness:",self.best_fitness)

    def play_many_games(self):
        self.play_games(100)
        self.overal_fitness = self.total_victories / (self.total_draws + self.total_losses + self.total_victories)
        print("Overall fitness: ", self.overal_fitness)

    def play_games(self, number_of_games):
        for i in range(number_of_games):
            game_states = dict()
            while self.game_board.has_move():
                hasho = self.ultimate_bubble(game_states)
                if self.game_board.check_oxo():
                    self.states[hasho].win = True
                    self.victories = self.victories + 1
                    for winning_state in game_states:
                        winning_state.apply_bonus(game_states[winning_state])
                    break
                self.random_cross()
                if self.game_board.check_oxo():
                    for losing_state in game_states:
                        losing_state.apply_penalty(game_states[losing_state])
                        self.losses = self.losses + 1
                    break
            if not self.game_board.has_move():
                for losing_state in game_states:
                    losing_state.apply_penalty(game_states[losing_state])
                    self.draws = self.draws + 1

            self.game_board.reset()

        self.adjustRewards()
        fitness = self.victories / (self.losses + self.victories + self.draws)
        self.fintesses.append(fitness)
        if fitness> self.best_fitness:
            self.best_fitness = fitness
            print("New best fitness level!", fitness)
        self.total_victories = self.total_victories + self.victories
        self.total_losses = self.total_losses + self.losses
        self.total_draws = self.total_draws + self.draws
        self.victories = 0
        self.draws = 0
        self.losses = 0

    def ultimate_bubble(self, game_states):
        current_hash = self.game_board.get_hash()
        current_state = self.get_state(current_hash)
        move_number = 0
        while current_hash == self.game_board.get_hash():
            move_number = current_state.move()
            self.smart_bubble(move_number)
            if current_hash == self.game_board.get_hash():
                if current_hash == self.origin.state and move_number == 4:
                    print("Something went wrong")
                current_state.disable_move_number(move_number)
        game_states[current_state]  = move_number
        return current_hash



    def get_state(self, current_hash):
        if current_hash not in self.states:
            new_state = state(self.game_board)
            self.states[new_state.state] = new_state
        return self.states[current_hash]

    def smart_bubble(self, numb):
        x = numb%3 + 1
        y = int(numb/3) +1
        self.game_board.place_bubble(x,y)

    def random_cross(self):
        hasho = self.game_board.get_hash()
        while self.game_board.get_hash() == hasho and self.game_board.has_move():
            self.game_board.place_cross(randint(1,3),randint(1,3))
        return hasho

    def adjustRewards(self):
        for key,st in self.states.items():
            st.reward = self.reward
            st.penalty = self.penalty


class state:
    def __init__(self,game_board):
        self.state = game_board.get_hash()
        self.moves = [250,250,250,250,250,250,250,250,250]
        self.win = False
        self.reward = 10
        self.penalty = 4

    def move(self):
        while True:
            numb = randint(0,8)
            if self.moves[numb] > randint(0,500):
                return numb
            yap = 0
            for i  in self.moves:
                yap = yap + i
            if yap <9:
                return numb

    def disable_move_number(self, move_number):
        self.moves[move_number] = 0
        pass
    def apply_penalty(self,move_number):
        self.moves[move_number] = self.moves[move_number] - self.penalty
        if(self.moves[move_number])<0:
            self.moves[move_number] = 0
    def apply_bonus(self,move_number):
        for m in range(8):
            if m == move_number:
                self.moves[m] = self.moves[move_number] + self.reward
            else:
                self.moves[m] = int(self.moves[m] - self.penalty/2)
                if(self.moves[m])<0:
                    self.moves[m] = 0

