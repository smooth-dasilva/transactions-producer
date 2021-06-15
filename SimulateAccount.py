from dataclasses import dataclass, field
import numpy as np
import random

@dataclass
class SimulateTransactions:

    """
    Helper class for simulating spending and balance over a period of N days
        
        Parameters: 
        
            earner_status/spending_status - categories to distinguish different types of earning and spending habits

            N - number of days the simulation will run for 

        Class properties:  

            money earned/spent - random number generated bound by upper and lower threshold. chosen from a normal distribution 
            
            low/moderate/high threshold - each day there is a chance to earn/spend. 
                                          if a self.random_roll() is below this threshold, generate a random float for money earned/spent
                    
            low/moderate/high intervals - soft bound for money to be earnt or spent. used to calculate mean in normal distribution. 
    """
     
    earner_status : str
    spender_status : str

    money_earned : float = 0
    money_spent : float = 0

    N : int = 100

    low_threshold : int = field(repr = False, default = 16)
    moderate_threshold : int =field(repr = False, default = 50)
    high_threshold : int = field(repr = False, default = 80)

    low_interval : tuple =  field(repr = False, default =(0, 100))
    moderate_interval : tuple = field(repr = False, default =(30, 150))
    high_interval : tuple =  field(repr = False, default =(50, 300))

    def __post_init__(self):
        self.low_threshold  = int(self.N/6)
        self.moderate_threshold  = int(self.N/2)
        self.high_threshold  = int(self.N*4/5)

    def get_random_roll(self):
        return random.randint(1, self.N)

    def simulate_one_day(self):
        
        self.money_earned = 0
        self.money_spent = 0

        if self.earner_status == "low" and self.get_random_roll() < self.low_threshold :
            self.money_earned = round(np.random.normal( (self.low_interval[1] - self.low_interval[0])/2, self.low_interval[1] ), 2)
        if self.spender_status == "low" and self.get_random_roll() < self.low_threshold :
            self.money_spent = round(np.random.normal((self.low_interval[1] - self.low_interval[0])/2, self.low_interval[1] ), 2)
            
        if self.earner_status == "moderate" and self.get_random_roll() < self.moderate_threshold:
            self.money_earned = round(np.random.normal( (self.moderate_interval[1] - self.moderate_interval[0])/2, self.moderate_interval[1]), 2)
        if self.spender_status == "moderate" and self.get_random_roll() < self.moderate_threshold :
            self.money_spent = round(np.random.normal((self.moderate_interval[1] - self.moderate_interval[0])/2, self.moderate_interval[1]), 2)
            
        if self.earner_status == "high" and self.get_random_roll() < self.high_threshold:
            self.money_earned = round(np.random.normal((self.high_interval[1] - self.high_interval[0])/2, self.high_interval[1]), 2)
        if self.spender_status == "high" and self.get_random_roll() < self.high_threshold:
            self.money_spent = round(np.random.normal((self.high_interval[1] - self.high_interval[0])/2, self.high_interval[1]), 2)

