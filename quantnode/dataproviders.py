from datetime import datetime, timedelta
from serialize import serialize
from dateutil.parser import parse as parsedt
from structures import DotDict
import slumber
import consts
import mlprotocol
from cache import DataCache


class DataProvider(object):
    def __init__(self, *args, **kwargs):
        self._query_cache = {}
        self.order_group_id = 0
        self.instrument = None
        self.timestamp = None
        self.metrics = []
        self._earnings_announcements_cache = []
        self._query_cache = {}
        self.api = slumber.API(consts.API_URL)

    def get_initial_metrics(self):
        pass

    def query_data(self, symbol='', timestamp=None, n_bars=None, from_timestamp=None):
        """
        Queries and caches pricebar data
        """
        if not n_bars and not from_timestamp:
            raise Exception('query_data requires oen of n_bars or from_timestamp to be specified')

        if not symbol:
            symbol = self.instrument.symbol
        if not timestamp:
            timestamp = self.timestamp


        if symbol not in DataCache().query_cache:
            print 'querying http server'
            try:
                data = self.api.pricebar.get(symbol = symbol, order_by = 'timestamp', limit=0)
            except Exception, e:
                print 'http server error: %s' % e.message

            for obj in data['objects']:
                if 'timestamp' in obj:
                    obj['timestamp'] = parsedt(obj['timestamp'])
                if 'date' in obj:
                    obj['date'] = parsedt(obj['date']).date()
            DataCache().query_cache[symbol] = [DotDict(i) for i in data['objects']]

        if from_timestamp is None:
            bars = [i for i in DataCache().query_cache[symbol] if i.timestamp < timestamp]
        else:
            bars = [i for i in DataCache().query_cache[symbol] if from_timestamp <= i.timestamp < timestamp]

        total = len(bars)
        print 'found %d bars' % total

        if total > n_bars:
            ls = []
            for i in range(total - n_bars, total):
                ls.append(bars[i])
            return ls
        else:
            return bars


    def store_data(self, data, calctype='calculation'):
        pass


    def has_upcoming_earnings(self, num_days):
        """
        Gets upcoming earnings over API
        TODO: need an API call here
        """
        if not self._earnings_announcements_cache:
            data = self.api.earnings_announcement(instrument__id = self.instrument.id, order_by = 'datestamp')
            for obj in data['objects']:
                if 'datestamp' in obj:
                    obj['datestamp'] = parsedt(obj['datestamp'])
            self._earnings_announcements_cache = [DotDict(i) for i in data['objects']]

        dt = self.timestamp + timedelta(days = num_days)

        for ea in self._earnings_announcements_cache:
            if ea.instrument.id != self.instrument.id:
                continue

            if self.useralgo.timestamp.date() <= ea.datestamp <= dt.date():
                return True

        return False

    def get_order_group_id(self):
        self.order_group_id += 1
        return self.order_group_id

    def complete_position(self, position, shares=None, capital=None):
        pass

    def complete_order(self, order, quantity = None, capital = None):
        pass

    def discard_order(self, order):
        pass

    def place_order(self, price_type, buy_or_sell, instrument=None, symbol='', quantity=None, capital=None, pricebar=None, instream=True, **kwargs):
        pass

    def close_positions(self, positions):
        pass

    def create_trading_signal(self, calculation, instrument):
        pass



class ClientDataProvider(DataProvider):
    def __init__(self, socket=None, *args, **kwargs):
        self.socket = socket
        self.ack_sent = False
        self.acks = []
        self.ack_counter = 0
        super(ClientDataProvider, self).__init__(*args, **kwargs)

    def store_data(self, data, calctype='calculation'):
        self.ack('store_data', {
            # 'symbol': self.instrument.symbol,
            # 'timestamp': self.timestamp,
            # 'pricebar': self.pricebar,
            'calctype': calctype,
            'data': data,
        })


    def complete_position(self, position, shares=None, capital=None):
        self.ack('complete_position', {
            'position': position,
            'shares': shares,
            'capital': capital
        })


    def discard_order(self, order):
        self.ack('discard_order', {
            'order': order
        })

    def complete_order(self, order, quantity=None, capital=None):
        self.ack('complete_order', {
            'order': order,
            'quantity': quantity,
            'capital': capital
        })


    def place_order(self, price_type, buy_or_sell,
                    instrument=None, symbol='',
                    quantity=None, capital=None, pricebar=None, instream=True):
        self.ack('place_order', {
            'placed_timestamp': self.timestamp,
            'price_type': price_type,
            'buy_or_sell': buy_or_sell,
            'quantity': quantity,
            'capital': capital,
            'pricebar': pricebar,
            'instream': True,
            'instrument': instrument,
            'symbol': symbol
        })


    def close_positions(self, positions):
        self.ack('close_positions', {
            'positions': positions
        })

    def create_trading_signal(self, calculation):
        self.ack('create_trading_signal', {
            'calculation': calculation
        })


    def ack(self, method, params):
        self.acks.append({
            'ack': {
                'method': method,
                'params': params,
                'counter': self.ack_counter
            }
        })
        self.ack_counter += 1

    def ack_data(self, data):
        self.acks.append(data)
        self.ack_counter += 1

    def get_acks(self):
        return self.acks

    def reset_ack(self):
        self.ack_counter = 0
        self.ack_sent = False
        self.acks = []

    def send_ack(self):
        if not self.socket or self.ack_sent:
            return False

        sdata = serialize(self.acks)
        sendmsg = mlprotocol.create_message(sdata)
        self.socket.send(sendmsg)
        self.ack_sent = True

        return True

