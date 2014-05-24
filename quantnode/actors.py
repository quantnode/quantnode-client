import os
import sys
from serialize import deserialize
import atexit
import helpers
import consts
import mlprotocol

def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except Exception:
        return None


class TimeSeriesAggregator(object):
    def __init__(self, name='', data_provider=None, *args, **kwargs):
        self._query_cache = {}
        self.timestamp = None
        self.metrics = []
        self.algorithm = None
        self.name = name

        if data_provider:
            self.data_provider = data_provider
        else:
            import dataproviders
            "TODO: replace this with the API data provider and an API key"
            self.data_provider = dataproviders.DataProvider()
            # self.data_provider = dataproviders.DatabaseDataProvider(name = name, useralgo=self)

    def store_data(self, data):
        return self.data_provider.store_data(data, calctype='aggregation')



class Calculator(object):
    calculate_parallelize = ['instrument']

    def __init__(self, name='', data_provider=None, *args, **kwargs):
        self._query_cache = {}
        self.order_group_id = 0
        self.instrument = None
        self.timestamp = None
        self.metrics = []
        self.algorithm = None
        self.name = name

        if data_provider:
            self.data_provider = data_provider
        else:
            import dataproviders
            "TODO: replace this with the API data provider and an API key"
            self.data_provider = dataproviders.DataProvider()
            # self.data_provider = dataproviders.DatabaseDataProvider(name = name, useralgo=self)

    def query_data(self, symbol='', timestamp=None, n_bars=None, from_timestamp=None):
        return self.data_provider.query_data(
            symbol = symbol, timestamp = timestamp,
            n_bars = n_bars,
            from_timestamp = from_timestamp
        )

    def store_data(self, data):
        return self.data_provider.store_data(data, calctype='calculation')

    def create_trading_signal(self, calculation):
        return self.data_provider.create_trading_signal(calculation)

    def calculate(self, *args, **kwargs):
        """
        Override this method to perform calculations
        """
        pass

    @classmethod
    def methods_implemented(cls):
        """
        Returns a list of overridden methods
        """
        methods = [str(m) for m in dir(cls) if not m.startswith('_') and m != 'methods_implemented']

        overriden = []
        for method in methods:
            this_method = getattr(cls, method)
            base_method = getattr(Calculator, method)
            if hasattr(this_method, '__func__') and hasattr(base_method, '__func__') and\
                this_method.__func__ != base_method.__func__:
                overriden.append(method)
        return overriden


class Algorithm(object):
    """
    Represents the algorithm
    todo:
        class variables for slippage, borrowing costs, etc.
    """
    handle_market_event_parallelize = []

    def __init__(self, name='', data_provider=None, *args, **kwargs):
        if data_provider:
            self.data_provider = data_provider
        else:
            import dataproviders
            self.data_provider = dataproviders.DataProvider(name=name)
            # self.data_provider = dataproviders.DatabaseDataProvider(name = name, useralgo=self)

        self.instrument = None
        self.timestamp = None

    def query_data(self, symbol, timestamp, n_bars, from_timestamp):
        return self.data_provider.query_data(symbol, timestamp, n_bars, from_timestamp)

    def store_data(self, symbol, timestamp, pricebar, data, attach_to_pricebar = True):
        return self.data_provider.store_data(symbol, timestamp, pricebar, data, attach_to_pricebar=attach_to_pricebar)

    def complete_order(self, order, quantity=None, capital=None):
        return self.data_provider.complete_order(order, quantity=quantity, capital=capital)

    def discard_order(self, order):
        return self.data_provider.discard_order(order)

    def place_order(self, price_type, buy_or_sell,
                    instrument=None, symbol='',
                    quantity=None, capital=None, pricebar=None, instream=True, **kwargs):

        return self.data_provider.place_order(price_type, buy_or_sell,
                                              instrument=instrument, symbol=symbol,
                                              quantity=quantity, capital=capital, pricebar = pricebar,
                                              instream = instream, **kwargs)

    def close_positions(self, positions):
        if positions:
            return self.data_provider.close_positions(positions)

    def close_position(self, position):
        return self.data_provider.close_positions([position])

    def handle_market_event(self, *args, **kwargs):
        """
        Override this method to handle market events.
        See documentation for more.
        """
        pass


    @classmethod
    def methods_implemented(cls):
        """
        Returns a list of overridden methods
        """
        methods = [str(m) for m in dir(cls) if not m.startswith('_') and m != 'methods_implemented']

        overriden = []
        for method in methods:
            this_method = getattr(cls, method)
            base_method = getattr(Algorithm, method)
            if hasattr(this_method, '__func__') and hasattr(base_method, '__func__') and\
                this_method.__func__ != base_method.__func__:
                overriden.append(method)
        return overriden



class PortfolioManager(object):
    hedge_symbol = 'IWV'

    beta_min = -0.10
    beta_max = 0.10
    beta_target = 0.0
    max_hedge_capital = None



def invoke_method(userobj, method, params):
    import inspect

    func = getattr(userobj, method, None)
    if not func:
        return

    fargs = inspect.getargspec(func)

    if fargs.keywords:
        "function accepts **kwargs - pass in entire dictionary"
        func(**params)
    else:
        fparams = {}
        arglist = [name for i, name in enumerate(fargs.args) if i > 0]
        for key, value in params.items():
            if key in arglist:
                fparams[key] = params[key]

        for i, arg in enumerate(arglist):
            hasdefault = fargs.defaults and i >= len(arglist) - len(fargs.defaults)
            if arg not in fparams and not hasdefault:
                raise Exception('Argument %s is not available to be passed to %s' % (arg, method))

        func(**fparams)


def run(hostname, calculations=False, backtest=False, portfolio_manager=False, port=consts.PORT):
    from socket import socket, AF_INET, SOCK_STREAM
    from dataproviders import ClientDataProvider
    import inspect
    import json

    frm = inspect.stack()[1]
    mod = inspect.getmodule(frm[0])
    filepath = os.path.dirname(os.path.abspath(mod.__file__))

    s = socket(AF_INET, SOCK_STREAM)
    s.connect((hostname, port))

    atexit.register(close_socket_connection, s)

    "signal to start execution"

    sendmsg = mlprotocol.create_message(json.dumps({
        'calculations': calculations,
        'backtest': backtest,
        'portfolio_manager': portfolio_manager
    }))
    s.send(sendmsg)

    userobj = None
    socket_dataprovider = ClientDataProvider(socket = s)

    "receive data"
    while True:
        data = mlprotocol.get_message(s)
        # data = s.recv(consts.BUFFER_SIZE)

        if data == consts.STOP_FLAG:
            print 'STOPPED'
            break

        socket_dataprovider.reset_ack()

        params = deserialize(data, dotted=True)
        invocation = params.get('_invocation')
        method = invocation['method']
        cls = invocation['class']

        if not userobj:
            usercls = find_implementation(filepath, cls)
            userobj = usercls(data_provider = socket_dataprovider)

        helpers.attach_parameters(socket_dataprovider, params)
        invoke_method(userobj, method, params)

        "send acknowledgement to the server"
        socket_dataprovider.send_ack()


def close_socket_connection(socket):
    socket.send(mlprotocol.end_message())
    socket.close()

