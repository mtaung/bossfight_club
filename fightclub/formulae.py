import math

def level_formula(exp):
    #500 exp ~ level 1
    #1'700 ~ level 5
    #8'000 ~ level 10
    #20'000 ~ level 12
    return math.floor((math.log(exp, 400) - 1) * 20) + 1
