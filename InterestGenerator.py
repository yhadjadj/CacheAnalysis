"""

Code for generating interests

"""
import json
import math
import random
from random import randrange
import Common.Randoms as rnd

# import numpy as np


class InterestGenerator(object):
    """ The object generating Interests """

    # caches connected to the generator
    out_ports = []

    def __init__(self, env):
        self.env = env
        self.ContentStoreSize, self.ContentProfile, self.MeanTimeBetweenArrivals = self.config_loader(config_filename='config.json')
        # print("Store=%d Alpha=%f MTBA=%f" % (self.ContentStoreSize, self.ContentProfile, self.MeanTimeBetweenArrivals))

    @staticmethod
    def config_loader(config_filename):
        # Read the generator parameters
        with open(config_filename) as json_data_file:
            data = json.load(json_data_file)
            content_store_size = int(data["ContentStore"]["Size"])
            content_profile = float(data["ContentStore"]["Alpha"])
            mean_time_between_arrival = float(data["ContentStore"]["MeanTimeBetweenArrivals"])
            return content_store_size, content_profile, mean_time_between_arrival

    @staticmethod
    def interest_sender(self, out_pipe, msg):
        out_pipe.rcv_interests.put(msg)

    def get_out_port(self):
        return randrange(len(self.out_ports))

    def get_content(self):
        return rnd.zip_f2(self.ContentProfile, self.ContentStoreSize)

    def add_out_port(self, port):
        self.out_ports.append(port)

    def next_time(self):
        return - self.MeanTimeBetweenArrivals * math.log(random.random())

    def generator(self, env):
        id = 0
        while True:
            yield env.timeout(self.next_time())
            rq_content = self.get_content()
            self.out_ports[self.get_out_port()].rcv_interests.put((env.now, id, rq_content))
            id += 1

    def start(self, env):
        env.process(self.generator(env))

"""
test

import simpy

env = simpy.Environment()
Ig = InterestGenerator(env)

"""