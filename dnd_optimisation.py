from pickle import TRUE
import scipy

class Character:
    def __init__(self,str,dex,con,int,wis,cha):
        import numpy as np
        self.ability_score= np.array([str,dex,con,int,wis,cha])
        self.modifier = np.floor((self.ability_score - 10)/2)
    
    def set_level(self,char_level=1):
        import numpy as np
        self.level=char_level
        self.proficiency_bonus=1+np.ceil(char_level/4)

    def return_ability_score(self,ability_name):
        self.ability=['STR', 'DEX', 'CON','INT','WIS', 'CHA']
        return(self.ability_score[self.ability.index(ability_name)])

    def set_other_bonus(self,ob=0):
        self.other_bonus=ob

    def set_advantages(self,advantage=0,luck_point=0,elven_accuracy=0,hexblade_curse=0):
        #checks
        advantage=(advantage==1)
        luck_point=(luck_point==1)
        elven_accuracy=(elven_accuracy==1)
        hexblade_curse=(hexblade_curse==1)
        #assignments
        self.advantage=advantage
        self.luck_point=luck_point
        self.elven_accuracy=elven_accuracy
        self.hexblade_curse=hexblade_curse
        
        #calcuate probability of critical hit
        __critit=1/20*(1-hexblade_curse)+2/20*hexblade_curse  
        p=advantage+luck_point+advantage*elven_accuracy+1
        self.critit=round(1-(1-__critit)**p,5)


    def set_hex(self,hex=0):
        hex=(hex==1)
        self.hex=3.5*hex

        

    def set_eldrich_blast(self,eb=0,max_eb_dice=0,agonising_eb=0,eb_bonus=0):
        import math
        from statistics import mean
        eb=(eb==1)
        #if eb=0 everything else should be 0
        self.eldrich_blast=eb
        self.eldrich_blast_beams=eb*min(math.floor(self.level/5)+1,4)
        self.eldrich_blast_hit_bonus=eb*eb_bonus #example rod of pact keeper
        self.eldrich_blast_mean_damage=eb*(mean(range(1,max_eb_dice+1,1))+self.modifier[self.ability.index("CHA")]*agonising_eb)
        self.eldirch_blast_hit=eb*(self.modifier[self.ability.index("CHA")]+self.proficiency_bonus+self.eldrich_blast_hit_bonus)
    

    def hit_opponent_probability(self,opponent_AC=1,modifiers=0):
        p_miss= min(max((opponent_AC-modifiers-1),1),19)/20
        p=self.advantage+self.luck_point+self.advantage*self.elven_accuracy+1
        p_hit=round(1-(p_miss)**p,5)
        p_hit=round(p_hit,5)
        return p_hit

    def total_average_damage(self,opponent_AC=1,modifiers=0,repetitions=1,average_damage_per_hit=0):
        import scipy.stats
        total_damage=0
        index_repetitions = 1
        p_hit=self.hit_opponent_probability(opponent_AC,modifiers)
        p_crit_hit=self.critit 
        #The logic of the loop below is the following. I am calculating the probability of having 1 repetition of the weapon or spell succesful (say 1 eldirch blast ray) times the damage that the weapon will do plus the probability of having two repetitions succesfull times twice the damage etc.
        while index_repetitions < (repetitions+1):
              total_damage+=scipy.stats.binom.pmf(index_repetitions,repetitions,p_hit)*index_repetitions*average_damage_per_hit+scipy.stats.binom.pmf(index_repetitions,repetitions,p_crit_hit)*index_repetitions*average_damage_per_hit
              index_repetitions += 1
        total_damage=round(total_damage,5)
        return total_damage



def probability_of_crtical_hit(advantage,luck_point,elven_accuracy,hexblade_curse):
    #advantage,luck_point,elven_accuracy,hexblade_curse take values 1 or 0.
    #if they are given a value different to 1, this is converted to 0 in the checks.
    
    #checks
    advantage=(advantage==1)
    luck_point=(luck_point==1)
    elven_accuracy=(elven_accuracy==1)
    hexblade_curse=(hexblade_curse==1)

    #calcuate probability of critical hit
    critit=1/20*(1-hexblade_curse)+2/20*hexblade_curse  
    p=advantage+luck_point+advantage*elven_accuracy+1
    critit=round(1-(1-critit)**p,5)
    
    return critit

def probability_of__hitting_opponent(opponent_AC,modifiers,advantage,luck_point,elven_accuracy):
    #advantage,luck_point,elven_accuracy, take values 1 or 0.
    #if they are given a value different to 1, this is converted to 0 in the checks.
    #opponent_AC must be > 0 and integer. It is rounded and, if negative, converted to 0 in the checks.
    #modifiers can be positive and negative integres. It is rounded in the checks.
    #checks
    advantage=(advantage==1)
    luck_point=(luck_point==1)
    elven_accuracy=(elven_accuracy==1)
    opponent_AC=round(opponent_AC*(opponent_AC>0))
    modifiers=round(modifiers)

    #calcuate probability of hit
    #probability of miss cannot be above 19/20 - critical hit 1/20
    #probability of miss cannot be below 1/20  - critical miss 1/20
    p_miss= min(max((opponent_AC-modifiers-1),1),19)/20
    p=advantage+luck_point+advantage*elven_accuracy+1
    p_hit=round(1-(p_miss)**p,5)
    p_hit=round(p_hit,5)
    return p_hit

def average_damage(repetitions,average_damage_per_hit,opponent_AC,modifiers,advantage,luck_point,elven_accuracy,hexblade_curse):
    #repetitions and average damage have to be positive. Repetitions must be an integer >0. During checks repetitions get rounded and become 1 if negative value is given. average_damage_per_hit becomes 0 if negative.
    #TotalDamage= (WeaponAverageDamage+Smite+BonusSmite+HexAverageDamage+oddbonous/2)*PrHitAd+ (WeaponAverageDamage+Smite+BonusSmite+HexAverageDamage+oddbonous/2) *CrititA
    
    #checks
    repetitions=round(repetitions*(repetitions>0)+1*(repetitions<=0))
    average_damage_per_hit=(average_damage_per_hit*(average_damage_per_hit>0))

    total_damage=0
    index_repetitions = 1
    p_hit=probability_of__hitting_opponent(opponent_AC,modifiers,advantage,luck_point,elven_accuracy)
    p_crit_hit= probability_of_crtical_hit(advantage,luck_point,elven_accuracy,hexblade_curse)
    #The logic of the loop below is the following. I am calculating the probability of having 1 repetition of the weapon or spell succesful (say 1 eldirch blast ray) times the damage that the weapon will do plus the probability of having two repetitions succesfull times twice the damage etc.
    while index_repetitions < (repetitions+1):
        total_damage+=scipy.stats.binom.pmf(index_repetitions,repetitions,p_hit)*index_repetitions*average_damage_per_hit+scipy.stats.binom.pmf(index_repetitions,repetitions,p_crit_hit)*index_repetitions*average_damage_per_hit
        index_repetitions += 1
    total_damage=round(total_damage,5)
    return total_damage
