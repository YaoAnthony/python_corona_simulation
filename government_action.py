from abc import abstractclassmethod
from motion import out_of_bounds, update_positions, update_randoms
import numpy as np

'''
Under an epidemic, different governments will have different policy behaviors, 
so I created a class for selecting government policies by separating government behaviors.
'''
class GovernmentAction():

    def __init__(self, strategy):
        self._strategy = strategy
    
    @property
    def strategy(self):
        return self._strategy

    @strategy.setter
    def strategy(self, strategy):
        self._strategy = strategy

    def government_action(self,population, destinations,Config,pop_tracker):
        # All government actions will be realized here
        self._strategy.action(population, destinations,Config,pop_tracker)


class Strategy():
    @abstractclassmethod
    def action(self,population, destinations,Config,pop_tracker):
        pass


class Mandatory_measures(Strategy):
    '''
    Here the government will adopt some mandatory policies to 
    prevent the epidemic, such as the closure of the city.
    '''
    #*here we just have lockdown
    def action(self,population, destinations,Config,pop_tracker):
              
        if Config.lockdown:
            if len(pop_tracker.infectious) == 0:
                mx = 0
            else:
                mx = np.max(pop_tracker.infectious)

            if len(population[population[:,6] == 1]) >= len(population) * Config.lockdown_percentage or\
            mx >= (len(population) * Config.lockdown_percentage):
                #reduce speed of all members of society
                population[:,5] = np.clip(population[:,5], a_min = None, a_max = 0.001)
                #set speeds of complying people to 0
                population[:,5][Config.lockdown_vector == 0] = 0
            else:
                #update randoms
                population = update_randoms(population, Config.pop_size, Config.speed)
        else:
            #update randoms
            population = update_randoms(population, Config.pop_size, Config.speed)



class Normal_measures(Strategy):
    '''
    Here the government will take some general measures to prevent the virus, 
    such as issuing a news release advising people to stay away from activities.
    '''

    #recommended that people carry masks,and reduce the outdoor activity
    def action(self,population, destinations,Config,pop_tracker):
        if len(population[population[:,6] == 1]) > 50:
            Config.speed = 0.5
                #how many destinations are active
            active_dests = np.unique(population[:,11][population[:,11] != 0])

            #set destination
            for d in active_dests:
                dest_x = destinations[:,int((d - 1) * 2)]
                dest_y = destinations[:,int(((d - 1) * 2) + 1)]

                #compute new headings
                head_x = dest_x - population[:,1]
                head_y = dest_y - population[:,2]

                #head_x = head_x / np.sqrt(head_x)
                #head_y = head_y / np.sqrt(head_y)

                #reinsert headings into population of those not at destination yet
                population[:,3][(population[:,11] == d) &
                                (population[:,12] == 0)] = head_x[(population[:,11] == d) &
                                                                    (population[:,12] == 0)]
                population[:,4][(population[:,11] == d) &
                                (population[:,12] == 0)] = head_y[(population[:,11] == d) &
                                                                    (population[:,12] == 0)]
                #set speed to 0.01
                population[:,5][(population[:,11] == d) &
                                (population[:,12] == 0)] = 0.02
            
            population = update_randoms(population, Config.pop_size, Config.speed)
