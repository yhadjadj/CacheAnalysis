import itertools
import numpy as np
import matplotlib.pyplot as plt
import json
import Plots.Process_data as pd
import ApproximatedModel as am
import Model as em

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

Hit = em.Calculate_hit(R, N, alpha)
Hit_result = np.array(list(Hit.values()))
Hit_keys = np.array(list(Hit.keys()))

Approx_hit = am.Calculate_approx_hit(R, N, alpha)
approx_Hit_result = np.array(list(Approx_hit.values()))
approx_Hit_keys = np.array(list(Approx_hit.keys()))

######################
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

