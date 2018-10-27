"""

Code to start the simulation

"""
import simpy
import random
import CacheNode as cn
import InterestGenerator as ig
import json
import os
import gc


config_file = 'config.json'


def config_loader(config_filename):
    # Read the generator parameters
    with open(config_filename) as json_data_file:
        data = json.load(json_data_file)
        duration = float(data["Simulator"]["Duration"])
        experiments = int(data["Simulator"]["nExperiments"])
        return duration, experiments


def launch_simulation(env, simulation_id=0):
    # Setup and start the simulation

    # Create traffic generator
    generator = ig.InterestGenerator(env)

    # Create a caching node
    cache = cn.CacheNode(env, duration=sim_duration, sim_identifier=simulation_id)
    generator.add_out_port(cache)

    # Start simulation
    generator.start(env)
    env.run(until=sim_duration)

    del generator
    del cache
    gc.collect()


def remove_previous_results():
    folder = 'Stats/'
    file_list = os.listdir(folder)

    for f in file_list:
        file_path = folder + '/' + f

        if os.path.isfile(file_path):
            os.remove(file_path)

    folder = 'Plots/Results/'
    file_list = os.listdir(folder)

    for f in file_list:
        file_path = folder + '/' + f

        if os.path.isfile(file_path):
            os.remove(file_path)


def modify_configuration(traffic_profile=1.2, cache_size=100):
    alpha = traffic_profile
    cache = cache_size
    with open(config_file, 'r+') as f:
        data = json.load(f)
        data["ContentStore"]["Alpha"] = str(alpha).replace("'", '"')
        data["Cache"]["Size"] = str(cache).replace("'", '"')
        f.seek(0)
        json.dump(data, f, indent=2)
        f.truncate()


traffic_prof = [1.2]
cache_size = [4]
sim_duration, n_experiments = config_loader(config_filename=config_file)
remove_previous_results()

Env = []

for prof in traffic_prof:
    for size in cache_size:
        modify_configuration(traffic_profile=prof, cache_size=size)
        for exp in range(n_experiments):
            print("Simulation %d/%d" % (exp+1, n_experiments))
            Env.append(simpy.Environment())
            random.seed(random.randint(0, 30000))
            launch_simulation(Env[-1], simulation_id=exp)




