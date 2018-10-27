import itertools
import numpy as np
import matplotlib.pyplot as plt
import json
import Plots.Process_data as pd


# load config file
def config_loader(config_filename):
    # Read the cache parameters
    with open(config_filename) as json_data_file:
        data = json.load(json_data_file)
        content_store = int(data["ContentStore"]["Size"])
        cache_size = int(data["Cache"]["Size"])
        traf_profile = float(data["ContentStore"]["Alpha"])
        return content_store, cache_size, traf_profile


"""
Alpha: popularity
N: cache size
R: content store size
"""
R, N, alpha = config_loader('config.json')

# probability for each content

def gamma(s, r, R, N, Pi_, Pr_):
    if s == 1:
        return Pr_[r]
    elif s<=N:
        gam = 0.0
        for i in range(1, R+1):
            if i == r:
                continue
            sum = 0.0
            for j in range(1, s):
                sum += Pi_[(j,i)]
            gam += Pr_[i] * sum
        return gam
    elif s == N+1:
        return 1 - Pr_[r]

def Calculate_approx_hit(R, N, alpha):
    sum_pr = 0.0

    for i in range(1, R + 1):
        sum_pr += pow(i, -alpha)

    Pr = {}
    for i in range(1, R + 1):
        Pr[i] = pow(i, -alpha) / sum_pr
    

    # calculate probabilities
    Pi = {}
    for j in range(1, R+1):
        Pi[(1, j)] = Pr[j]
    
    for j in range(1, R+1):
        Pi[(2, j)] = Pr[j] * (1-Pr[j])/(1-gamma(2, j, R, N, Pi, Pr))
    
    for i in range(3, N+2):
        for j in range(1, R+1):
            Pi[(i, j)] = 0.0
    
            prod_num = 1.0
            for k in range(2, i):
                prod_num = prod_num * (1-Pr[j]-gamma(k, j, R, N, Pi, Pr))
            prod_num = prod_num * Pr[j] * (1-Pr[j])
    
            prod_denum = 1.0
            for k in range(2, i + 1):
                prod_denum = prod_denum * (1-gamma(k, j, R, N, Pi, Pr))
    
            Pi[(i, j)] = prod_num/prod_denum

    Hit = {}
    for j in range(1, R+1):
        Hit[j] = 1 - Pi[(N+1, j)]

    return Hit

"""
print(Hit)

Hit_result = np.array(list(Hit.values()))
Hit_keys = np.array(list(Hit.keys()))
"""
