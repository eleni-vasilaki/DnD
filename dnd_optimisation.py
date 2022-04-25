from pickle import TRUE

def probability_of_crtical_hit(advantage,luck_point,elven_accuracy):
    critit=1/20
    p=1
    if advantage is True: p+=1
    if advantage and elven_accuracy is True: p+=1
    if luck_point is True: p+=1
    critit=round(1-(1-critit)**p,4)
    return critit

