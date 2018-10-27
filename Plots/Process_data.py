import pickle
import json
import matplotlib.pyplot as plt
import numpy as np


# load config file
def config_loader(config_filename):
    # Read the cache parameters
    with open(config_filename) as json_data_file:
        data = json.load(json_data_file)
        content_store = int(data["ContentStore"]["Size"])
        experiments = int(data["Simulator"]["nExperiments"])
        return content_store, experiments


def process_an_experiment(content_store, experiment_id=0):
    # process data
    caches = [0]

    for cache_id in caches:
        print(experiment_id)
        file_hit = "Stats/cache_hit_%d_%d.pkl" % (experiment_id, experiment_id)
        stats_hit = pickle.load( open(file_hit, "rb"))
        print(stats_hit)
        file_miss = "Stats/cache_miss_%d_%d.pkl" % (experiment_id, experiment_id)
        stats_miss = pickle.load(open(file_miss, "rb"))
        print(stats_miss)

        hit_rate = {}

        for i in range(1, content_store+1):
            if not(i in stats_hit):
                hit_rate[i] = 0
            else:
                hit_rate[i] = stats_hit[i]/(stats_hit[i]+stats_miss[i])

        # plot data
        lists = sorted(hit_rate.items())
        x, y = zip(*lists)
        return x, y


def launch():
    cs, n_experiments = config_loader(config_filename='config.json')
    list_x = []
    list_y = []
    already = False

    for i in range(n_experiments):
        x, y = process_an_experiment(content_store=cs, experiment_id=i)
        list_y.append(y)
        if not already:
            list_x.append(x)
            already = True

    na = np.array(list_y)
    avg = [float(sum(col))/len(col) for col in zip(*na)]
    return list_x[0], avg


def plot_data(x, y):
    y_pos = np.arange(len(list(x)))

    plt.bar(y_pos, y, align='center', alpha=0.5)
    plt.xticks(y_pos, list(x))
    plt.ylabel('Hit rate')
    plt.xlabel('Content rank')
    plt.show()

    hit_rate_file = "Results/cache_hit_rate_%d.eps" % 0
    plt.savefig(hit_rate_file, format='eps', dpi=1000)


"""
test

X, Y = launch()
plot_data(x=X, y=Y)

"""