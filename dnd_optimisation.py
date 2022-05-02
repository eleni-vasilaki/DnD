from pickle import TRUE
import scipy

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
    p_hit=1-( opponent_AC-modifiers-1)/20
    p=advantage+luck_point+advantage*elven_accuracy+1
    p_hit=round(1-(1-p_hit)**p,5)

    #probability of hit cannot be above 19/20 -critical miss 1/20
    p_hit=min(19/20,p_hit)

    #probability of hit cannott be below 1/20 - critical hit 1/20
    p_hit=max(1/20,p_hit)

    p_hit=round(p_hit,5)
    
    return p_hit

def average_damage(repetitions,average_damage_per_hit,opponent_AC,modifiers,oddbonus,advantage,luck_point,elven_accuracy,hexblade_curse):
    #repetitions and average damage have to be positive. Repetitions must be an integer >0. During checks repetitions get rounded and become 1 if negative value is given. average_damage_per_hit becomes 0 if negative.

    #checks
    repetitions=round(repetitions*(repetitions>0)+1*(repetitions<=0))
    average_damage_per_hit=(average_damage_per_hit*(average_damage_per_hit>0))
    oddbonus=oddbonus*(oddbonus>0)

    total_damage=0
    index_repetitions = 1
    p_hit=probability_of__hitting_opponent(opponent_AC,modifiers,advantage,luck_point,elven_accuracy)
    p_crit_hit= probability_of_crtical_hit(advantage,luck_point,elven_accuracy,hexblade_curse)
    #The logic of the loop below is the following. I am calculating the probability of having 1 repetition of the weapon or spell succesful (say 1 eldirch blast ray) times the damage that the weapon will do plus the probability of having two repetitions succesfull times twice the damage etc.
    #Now, if there is a bonus added to the odd numbered repetitions only (say when I use weapons with two hands), then this should be multiplied with a index_repetitions*oddbonus*2/repetitions
    while index_repetitions < (repetitions+1):
        total_damage+=scipy.stats.binom.pmf(index_repetitions,repetitions,p_hit)*index_repetitions*(average_damage_per_hit+2*oddbonus/repetitions)+scipy.stats.binom.pmf(index_repetitions,repetitions,p_crit_hit)*index_repetitions*(average_damage_per_hit+2*oddbonus/repetitions)
        index_repetitions += 1
    total_damage=round(total_damage,5)
    return total_damage

    #TotalDamage= (WeaponAverageDamage+Smite+BonusSmite+HexAverageDamage+oddbonous/2)*PrHitAd+ (WeaponAverageDamage+Smite+BonusSmite+HexAverageDamage+oddbonous/2) *CrititA