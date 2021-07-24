from path_planning import set_destination
import numpy as np


class Hospital:
    '''
        builds hospital
    
        Defines hospital and returns wall coordinates for 
        the hospital, as well as coordinates for a red cross
        above it
        
        Keyword arguments
        -----------------
        xmin : int or float
        xmax : int or float
        ymin : int or float
        ymax : int or float
        location showing below:

        (xmin,ymax)----------(xmax,ymax)
            |                   |
            |     Hosipital     |
            |                   |
        (xmin,ymin)----------(xmax,ymin)

        plt : matplotlib.pyplot object
            the plot object to which to append the hospital drawing
            if None, coordinates are returned
            
        Returns
        -------
        None
    '''
    def __init__(self,xmin, xmax, ymin, ymax, plt,addcross):
        #plot walls
        plt.plot([xmin, xmin], [ymin, ymax], color = 'black')
        plt.plot([xmax, xmax], [ymin, ymax], color = 'black')
        plt.plot([xmin, xmax], [ymin, ymin], color = 'black')
        plt.plot([xmin, xmax], [ymax, ymax], color = 'black')
        #TODO: setting the hosptial location
        self.destinations_location = []
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        #plot red cross
        if addcross:
            xmiddle = xmin + ((xmax - xmin) / 2)
            height = np.min([0.3, (ymax - ymin) / 5])
            plt.plot([xmiddle, xmiddle], [ymax, ymax + height], color='red',
                    linewidth = 3)
            plt.plot([xmiddle - (height / 2), xmiddle + (height / 2)],
                    [ymax + (height / 2), ymax + (height / 2)], color='red',
                    linewidth = 3)
    
    def go_to_Hospital(self, population, pop_tracker):
        #check infection
        if len(pop_tracker.infectious) > 0:
            #some people who infected will go to the hospital
            active_dests = np.unique(population[:,6][population[:,6] == 1])
            

            #Go to hospital:
            for d in active_dests:
                dest_x = np.random.random(self.xmin,self.xmax)
                dest_y = np.random.random(self.ymin,self.ymax)

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

        return population

    #TODO: stay in hospital
            
            