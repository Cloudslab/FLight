"""Averaging model weights available"""


from .base_algo import base_fl_algorithm
class federated_average(base_fl_algorithm):
    @staticmethod
    def federate(weights, additional_args=None):
        if not weights:
            return
        sample = weights[0]
        sum_dict = {key: 0 for key in weights[0].keys()}
        for k in sum_dict.keys():
            for w in weights:
                sum_dict[k] += w[k]
            sum_dict[k] /= len(weights)

        return sum_dict
