import itertools
import numpy as np
import matplotlib.pyplot as plt
import json
import Plots.Process_data as pd
import ApproximatedModel as am

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


def Calculate_hit(R, N, alpha):
    # set of elements creation
    S = [(i) for i in range(1, R + 1)]

    # let start by generating the combinations
    C = list(itertools.permutations(S, N))
    len_C = len(C)
    print(C)

    # probability for each content
    sum_pr = 0.0

    for i in range(1, R + 1):
        sum_pr += pow(i, -alpha)

    Pr = {}
    for i in range(1, R + 1):
        Pr[i] = pow(i, -alpha) / sum_pr

    # transition probability matrix creation
    # Cond 1: if the cache doesn't change ... means that the first element came
    # Cond 2: if the cache move means that we have a new element at the new position or the last one came
    # Cond 3: cover the case when an existing element in the cache came (so we check if the first new element was in
    #         the cache in other position that the first and if the order of the other elements stay the same

    T = np.zeros((len_C, len_C))

    for i in range(len_C):
        for j in range(len_C):
            # Cond 1
            if C[i] == C[j]:
                T[i, j] = Pr[C[j][0]]
                continue
            # Cond 2
            if C[i][:len(C[i]) - 1] == C[j][1:]:
                T[i, j] = Pr[C[j][0]]
                continue
            # Cond 3
            if C[j][0] in C[i]:
                Ci = list(C[i])
                Cj = list(C[j])
                Ci.remove(Cj[0])
                Cj.remove(Cj[0])
                if Ci == Cj:
                    T[i, j] = Pr[C[j][0]]
                    continue

    print(T)

    # initial state creation
    S_ = []
    pr_ = 1. / len_C
    sum_pr_ = pr_ * (len_C - 1)
    for i in range(len_C - 1):
        S_.append(pr_)
    S_.append(1 - sum_pr_)

    S = np.asarray(S_)

    # Obtaining S the stationary matrix (steady state)
    # Our markov chain is regular so there is a unique stationary matrix
    """
     Let P be the transition matrix of a regular Markov chain
        (1) there is a unique stationary matrix S, solving S.P=S
        (2) given any initial state matrix S0, the state matrix converges to the stationary matrix S
        (3) the matrix P^k approach a limiting P^bar, where each raw of P^bar is equal to S
    
    For our case the matrix is regular as we can easily find a power n for which P has no 0 entries.
    
    """

    for i in range(30):
        S = np.matmul(S, T)
        #print(S)

    R_ = np.copy(T)
    for i in range(150):
        R_ = np.matmul(R_, T)
        #print("***")
        #print(R_)

    # Compute the probability of a hit
    Hit = {}
    for i in range(1, R + 1):
        Hit[i] = 0.0
        for c in range(len_C):
            if i in C[c]:
                Hit[i] += S[c]
    return Hit

"""
print(Hit)

Hit_result = np.array(list(Hit.values()))
Hit_keys = np.array(list(Hit.keys()))

Approx_hit = am.Calculate_approx_hit(R, N, alpha)

approx_Hit_result = np.array(list(Approx_hit.values()))
approx_Hit_keys = np.array(list(Approx_hit.keys()))
"""

"""
y_pos = np.arange(len(Hit_keys))
# performance = [10,8,6,4,2,1]

plt.bar(y_pos, Hit_result, align='center', alpha=0.5)
plt.xticks(y_pos, Hit_keys)
plt.ylabel('Hit rate probability')
plt.xlabel('Content rank')

# plt.title('Programming language usage')
plt.show()
"""
######################

"""

# Generate the simulator data
X, Y = pd.launch()

# create plot
fig, ax = plt.subplots()
index = np.arange(len(Hit_keys))
bar_width = 0.15
opacity = 0.8

rects1 = plt.bar(index, Hit_result, bar_width,
                 alpha=opacity,
                 color='b',
                 label='Model')

rects2 = plt.bar(index + bar_width, Y, bar_width,
                 alpha=opacity,
                 color='g',
                 label='Simulation')

rects3 = plt.bar(index + 2 * bar_width, approx_Hit_result, bar_width,
                 alpha=opacity,
                 color='r',
                 label='Approximated model')

plt.xlabel('File rank')
plt.ylabel('Hit rate')
plt.xticks(index + bar_width, Hit_keys)
plt.legend()

plt.tight_layout()
plt.show()

"""