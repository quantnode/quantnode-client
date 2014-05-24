from structures import DotDict
from encoders import QuantnodeDecoder, QuantnodeEncoder

def deserialize(data, dotted=True):
    ddata = QuantnodeDecoder().decode(data)

    if dotted:
        return DotDict.ToDotDict(ddata)
    return ddata


def serialize(data):
    return QuantnodeEncoder().encode(data)

