import random

class ICRTools(object):
    @staticmethod
    def generate_sample_for_icr(data,sample_size, random_generator=None):

        if random_generator is None:
            random_generator = random
        if len(data) < sample_size:
            print("Warning: the size of the ICR data ({} items) is less than the requested sample_size"
                "({} items). returning all the input data as ICR".format(len(data),sample_size))
            sample_size = len(data)
        
        return random_generator.sample(data, sample_size)
        