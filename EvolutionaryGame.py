import numpy as np

class Game:

    def __init__(self, n_agents=100):
        self.players = [[0.3, 0.7], [0.7, 0.3]]
        self.n_agents = n_agents
        self.population = []
        for i in range(int(n_agents/2)):
            self.population.append([0.3, 0.7])
        for i in range(int(n_agents/2)):
            self.population.append([0.7, 0.3])
        self.A = np.array(([0.3, 0.0],
                           [0.5, 0.1]))
        self.B = np.array(([0.3, 0.5], 
                           [0.0, 0.1]))


    # GAME WITH RANDOM SAMPLING FOR OPPONENTS
    def play_random_pair_mutant_game(self, n_rounds = 200, n_int_rounds = 10, n_reproduce=5, n_mutate=5, mutant_freq=10):
        for round in range(1, n_rounds + 1):
            N = np.random.permutation(100)
            U = []
            for ind in range(50):
                self.U1_tmp = 0
                self.U2_tmp = 0
                p1 = self.population[N[ind * 2]]
                p2 = self.population[N[(ind *2) + 1]]
                for round_ in range(1, n_int_rounds + 1):
                    s1 = np.random.choice((0, 1), p = self.population[N[ind * 2]])
                    s2 = np.random.choice((0, 1), p = self.population[N[(ind *2) + 1]])
                    self.U1_tmp += self.A[s1][s2]
                    self.U2_tmp += self.B.T[s2][s1]
                U.append(self.U1_tmp)
                U.append(self.U2_tmp)


            U_sorted = np.argsort(U) # Sort index values with respect to their payoff
            U_rm = list(U_sorted[-(n_reproduce + n_mutate):]) # Cut bottom n performers out
            U_n = []
            if round % mutant_freq == 0: # Mutation every n_rounds
                for index in list(U_sorted[:n_reproduce]):
                    self.population.append(self.population[index])
                for i_, ind_ in enumerate(U_rm):
                    del self.population[ind_ - i_]
                mutant_strategy = np.random.random(2) # Generate randomly mutated strategy
                mutant_strategy = list(mutant_strategy / (np.sum(mutant_strategy)))
                for i in range(n_mutate):
                    self.population.append(mutant_strategy)
            
            else:
                for index in list(U_sorted[:n_reproduce]):
                    self.population.append(self.population[index])
                for i_, ind_ in enumerate(U_rm[-n_reproduce:]):
                    del self.population[ind_ - i_]
            

            print("{} / {}".format(round, n_rounds))

    #GAME AGAINST EACH OPPONENT IN EACH ROUND
    def play_full_pair_mutant_game(self, n_rounds = 200, n_sub_rounds = 10, n_reproduce=10, n_mutate=5, mutant_freq=10,
                                   show_table=False):
        for round in range(1, n_rounds + 1):
            U = []
            full_index_range = [i for i in range(self.n_agents)] # Range of player indices
            for index1 in full_index_range:
                full_index_range.remove(index1)
                tmp_ind = full_index_range # Temp index list without current player's index
                self.U1_tmp = 0
                self.U2_tmp = 0
                for index2 in tmp_ind: # Iterate over other player's indices.
                    for sub_round in range(1, n_sub_rounds + 1):
                        s1 = np.random.choice((0, 1), p = self.population[index2])
                        s2 = np.random.choice((0, 1), p = self.population[index2])
                        self.U1_tmp += self.A[s1][s2]
                        self.U2_tmp += self.B.T[s2][s1]
                U.append(self.U1_tmp)
                U.append(self.U2_tmp)


            U_sorted = np.argsort(U) # Sort index values with respect to their payoff
            U_rm = list(U_sorted[:(n_reproduce + n_mutate)]) # Cut bottom n performers out
            U_n = []

            if round % mutant_freq == 0: # Mutation every n_rounds
                U_rm.sort(reverse=True)
                for index3 in list(U_sorted[-n_reproduce:]):
                    self.population.append(self.population[index3])
                for index4 in U_rm:
                    del self.population[index4]
                mutant_strategy = np.random.random(2) # Generate randomly mutated strategy
                mutant_strategy = list(mutant_strategy / (np.sum(mutant_strategy)))
                for i in range(n_mutate):
                    self.population.append(mutant_strategy)
            
            else:
                U_rm = U_rm[:n_reproduce]
                U_rm.sort(reverse=True)
                for index5 in list(U_sorted[:n_reproduce]):
                    self.population.append(self.population[index5])
                
                for index6 in U_rm:
                    del self.population[index6]
        

            print("{} / {}".format(round, n_rounds))
        
        if show_table:
            self.strategy_table = {}
            for strat in self.population:
                if str(strat) in self.strategy_table.keys():
                    self.strategy_table[str(strat)] += 1
                else:
                    self.strategy_table[str(strat)] = 1
            
            print(self.strategy_table)



    




if __name__=="__main__":

    game = Game(n_agents=30)
    game.play_full_pair_mutant_game(n_rounds=599, n_reproduce=5, n_mutate=3, show_table=True)    
    
