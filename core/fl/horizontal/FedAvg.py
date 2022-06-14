"""
Basic federated average algorithm

"""


def fed_avg(weights: list):
    try:
        return sum(weights)/len(weights)
    except:
        raise ArithmeticError("Sum or Len operation not supported")
        return None
