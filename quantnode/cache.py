import patterns

class DataCache(patterns.Singleton):
    """
    Temporary in-memory storage for queried data
    """
    def __init__(self, *args, **kwargs):
        super(DataCache, self).__init__(*args, **kwargs)
        if not hasattr(self, 'query_cache'):
            self.query_cache = {}

