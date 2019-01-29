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
        self.total_games_played = 0
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
        self.all_bubble_states = dict([(orig.state, orig)])
        self.all_cross_states = dict([(orig.state, orig)])
        self.origin = orig
        self.fintesses = []

    def reset_stats(self):
        self.total_draws = 0
        self.total_losses = 0
        self.total_victories = 0
        self.victories = 0
        self.draws = 0
        self.losses = 0


    def smarter_play(self,simulations):
        #100 games
        for i in range(simulations):
            self.play_many_games('better_random')
        self.print_sim_message(simulations)

    def print_sim_message(self,simulations):
        print("Starting simulation: ", simulations , " runs planned with R: ", self.reward, " P",  self.penalty)
        print("------------------------------------------")
        print("Simulation ended")
        print("Games won:", self.total_victories, "draws : ", self.total_draws, " losses: ", self.total_losses)
        print("Best fitness:", self.best_fitness)

    def dumber_play(self,simulations):
        #100 games
        for i in range(simulations):
            self.play_many_games('random')
        self.print_sim_message(simulations)

    def play_many_games(self,type):
        if type== 'random':
            self.play_random_games(100)
        elif type == 'better_random':
            self.play_less_random_games(100)
        self.overal_fitness = self.total_victories / (self.total_draws + self.total_losses + self.total_victories)
        print("Overall fitness: ", self.overal_fitness)

    def play_random_games(self, number_of_games):
        for i in range(number_of_games):
            self.total_games_played = self.total_games_played + 1
            bubble_states = dict()
            cross_states = dict()
            while self.game_board.has_move():
                hasho = self.ultimate_bubble(bubble_states)
                if self.game_board.check_oxo():
                    self.apply_rewards(bubble_states, cross_states, 'bubble')
                    break
                if self.game_board.has_move():
                    self.random_cross()
                    hasho = ""
                    if self.game_board.check_oxo():
                        self.apply_rewards(cross_states,bubble_states,'cross')
                        break
            if not self.game_board.has_move() and not self.game_board.check_oxo():
                self.end_draw(bubble_states,cross_states)
            self.game_board.reset()
        self.end_simulation()

    def play_less_random_games(self, number_of_games):
        for i in range(number_of_games):
            self.total_games_played = self.total_games_played + 1
            bubble_states = dict()
            cross_states = dict()
            while self.game_board.has_move():
                hasho = self.ultimate_bubble(bubble_states)
                if self.game_board.check_oxo():
                    self.apply_rewards(bubble_states, cross_states, 'bubble')
                    break
                if self.game_board.has_move():
                    self.ultimate_cross(cross_states)
                    hasho = ""
                    if self.game_board.check_oxo():
                        self.apply_rewards(cross_states,bubble_states,'cross')
                        break
            if not self.game_board.has_move() and not self.game_board.check_oxo():
                self.end_draw(bubble_states,cross_states)
            self.game_board.reset()
        self.end_simulation()

    def end_simulation(self):
        self.adjustRewards()
        fitness = self.victories / (self.losses + self.victories + self.draws)
        self.fintesses.append(fitness)
        if fitness > self.best_fitness:
            self.best_fitness = fitness
            print("New best fitness level!", fitness)
        self.total_victories = self.total_victories + self.victories
        self.total_losses = self.total_losses + self.losses
        self.total_draws = self.total_draws + self.draws
        self.victories = 0
        self.draws = 0
        self.losses = 0

    def end_draw(self, game_states,cross_states):
        self.draws = self.draws + 1
        for bubble in game_states:
            bubble.apply_penalty(game_states[bubble])
        for cross in cross_states:
            cross.apply_win(cross_states[cross])


    def apply_rewards(self, winner, loser, hasho):
        if hasho == 'bubble':
            self.victories = self.victories + 1
        else:
            self.losses = self.losses +1
        for winning_state in winner:
            winning_state.apply_win(winner[winning_state])
        for losing_state in loser:
            losing_state.apply_penalty(loser[losing_state])

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

    def ultimate_cross(self, game_states):
        current_hash = self.game_board.get_hash()
        current_state = self.get_cross_state(current_hash)
        move_number = 0
        while current_hash == self.game_board.get_hash():
            move_number = current_state.move()
            self.smart_cross(move_number)
            if current_hash == self.game_board.get_hash():
                current_state.disable_move_number(move_number)
        game_states[current_state]  = move_number
        return current_hash


    def get_cross_state(self, current_hash):
        if current_hash not in self.all_cross_states:
            new_state = state(self.game_board)
            self.all_cross_states[new_state.state] = new_state
        return self.all_cross_states[current_hash]


    def get_state(self, current_hash):
        if current_hash not in self.all_bubble_states:
            new_state = state(self.game_board)
            self.all_bubble_states[new_state.state] = new_state
        return self.all_bubble_states[current_hash]

    def smart_bubble(self, numb):
        x = numb%3 + 1
        y = int(numb/3) +1
        self.game_board.place_bubble(x,y)
    def smart_cross(self, numb):
        x = numb%3 + 1
        y = int(numb/3) +1
        self.game_board.place_cross(x,y)
    def random_cross(self):
        hasho = self.game_board.get_hash()
        while self.game_board.get_hash() == hasho and self.game_board.has_move():
            self.game_board.place_cross(randint(1,3),randint(1,3))
        return hasho

    def adjustRewards(self):
        for key,st in self.all_bubble_states.items():
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
    def apply_win(self, move_number):
        for m in range(8):
            if m == move_number:
                self.moves[m] = self.moves[move_number] + self.reward
            else:
                self.moves[m] = int(self.moves[m] - self.penalty/2)
                if(self.moves[m])<0:
                    self.moves[m] = 0
    def apply_draw(self):
        for m in range(8):
            self.moves[m] = self.moves[m] + randint(-self.penalty,self.reward)

