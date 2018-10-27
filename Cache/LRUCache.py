"""

Code for the cache

"""
import logging
# import atexit
import pickle


class LRUCache(object):

    cache = {}
    stats_hit = {}
    stats_miss = {}

    def __init__(self, env, capacity, cid, sim_identifier):
        self.capacity = capacity
        self.id = cid
        self.sim_id = sim_identifier
        # log configuration
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.logger.propagate = False
        log_file_name = "Stats/cache_%d_%d.log" % (self.sim_id, self.id)
        handler = logging.FileHandler(log_file_name)
        self.logger.addHandler(handler)
        # atexit.register(self.generate_data)

    def generate_data(self, env, time_out):
        yield env.timeout(time_out)
        file_hit = "Stats/cache_hit_%d_%d.pkl" % (self.sim_id, self.id)
        pickle.dump(self.stats_hit, open(file_hit, "wb"))
        file_miss = "Stats/cache_miss_%d_%d.pkl" % (self.sim_id, self.id)
        pickle.dump(self.stats_miss, open(file_miss, "wb"))

    def insert(self, env, content):
        # insert a content if it is not in cache
        if len(self.cache) >= self.capacity:
            if not(content in self.cache):
                # oldest content should be removed before insertion
                idx_oldest, time_oldest = min(self.cache.items(), key=lambda x: x[1])
                self.cache.pop(idx_oldest)
                self.logger.info('-> %f %d out %d' % (env.now, self.id, idx_oldest))
                # self.logger.info(self.cache)

        # insert the new content
        self.cache[content] = env.now
        # self.logger.info(self.cache)

    def lookup(self, env, content):
        if content in self.cache:
            self.logger.info('%f %d hit %d' % (env.now, self.id, content))
            if content in self.stats_hit:
                self.stats_hit[content] += 1
            else:
                self.stats_hit[content] = 1
            return True
        else:
            self.logger.info('%f %d miss %d' % (env.now, self.id, content))
            if content in self.stats_miss:
                self.stats_miss[content] += 1
            else:
                self.stats_miss[content] = 1
            return False

    @staticmethod
    def save_obj(obj, name):
        with open(name, 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)




