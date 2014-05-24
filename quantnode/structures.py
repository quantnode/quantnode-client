class DotDict(dict):
    """
    A 'dotted dictionary'
    Simple dictionary wrapper that overrides the dot operator with dictionary getter and setter
    so that instance['value'] is equivalent to instance.value
    """
    def __setattr__(self, k, v):
        if k[0] == '_' or k in self.__dict__:
            return super(DotDict, self).__setattr__(k, v)
        else:
            self[k] = v

    def __getattr__(self, k):
        if k[0] == '_':
            raise AttributeError(k)

        try:
            return self[k]
        except KeyError, err:
            # return None
            return float('nan')
            # raise AttributeError(*err.args)

    @staticmethod
    def ToDotDict(data):
        """
        Recurisvely transforms a dict to a dotted dictionary
        """
        if isinstance(data, dict):
            for k, v in data.iteritems():
                if isinstance(v, dict):
                    data[k] = DotDict(v)
                    DotDict.ToDotDict(data[k])
                elif isinstance(v, list):
                    data[k] = [DotDict.ToDotDict(i) for i in v]
        elif isinstance(data, list):
            return [DotDict.ToDotDict(i) for i in data]
        else:
            return data

        return DotDict(data)

