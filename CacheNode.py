"""

Code for the caching node

"""

import simpy
import json
import Cache.LRUCache as lru

class CacheNode(object):
    """ Caching Node """

    CacheNode_id_counter = 0

    def __init__(self, env, duration,sim_identifier=0, capacity=simpy.core.Infinity):
        self.cache_size = self.config_loader(config_filename='config.json')
        self.env = env
        self.sim_identifier = sim_identifier
        self.id = CacheNode.CacheNode_id_counter
        CacheNode.CacheNode_id_counter += 1
        self.ev_rcv_interest = env.event()
        self.rcv_interests = simpy.Store(env, capacity=capacity)
        self.Cache = lru.LRUCache(env, capacity=self.cache_size, cid=self.id, sim_identifier=self.sim_identifier)
        env.process(self.Cache.generate_data(env, duration - 1.0))
        env.process(self.get_interest(env))

    @staticmethod
    def config_loader(config_filename):
        # Read the cache parameters
        with open(config_filename) as json_data_file:
            data = json.load(json_data_file)
            cache_size = int(data["Cache"]["Size"])
            return cache_size

    def get_interest(self, env):
        while True:
            msg = yield self.rcv_interests.get()
            content = int(msg[2])
            if self.Cache.lookup(env, content):
                self.Cache.insert(env, content)
            else:
                self.Cache.insert(env, content)
            # print('Received interest: %s' % msg[2])
