from datetime import datetime, date, timedelta
from dateutil.parser import parse as parsedt
from json import JSONDecoder, JSONEncoder
try:
    "properly imports on the server - not necessarily on the client"
    from bson.objectid import ObjectId
except Exception:
    ObjectId = None


class QuantnodeEncoder(JSONEncoder):
    def default(self, obj):
        # if obj is None:
        #     return {
        #         '__type__': 'none'
        #     }
        if isinstance(obj, datetime):
            return {
                '__type__': 'datetime',
                'value': obj.isoformat()
            }
        elif isinstance(obj, date):
            return {
                '__type__': 'date',
                'value': obj.isoformat()
            }
        elif isinstance(obj, timedelta):
            return {
                '__type__': 'timedelta',
                'value': obj.total_seconds()
            }
        elif isinstance(obj, object) and '_meta' in dir(obj):
            if hasattr(obj, 'to_json'):
                tojson = getattr(obj, 'to_json')
                if tojson:
                    if callable(tojson):
                        return tojson()
                    else:
                        return tojson
            return obj
        # elif isinstance(obj, ObjectId):
        elif type(obj).__name__ == 'ObjectId':
            return {
                '__type__': 'objectid',
                'value': str(obj)
            }
        else:
            return super(QuantnodeEncoder, self).default(obj)



class QuantnodeDecoder(JSONDecoder):
    def __init__(self):
            JSONDecoder.__init__(self, object_hook=self.dict_to_object)

    def dict_to_object(self, d):
        if '__type__' not in d:
            return d

        thetype = d.pop('__type__')
        thevalue = d['value']
        if thetype == 'datetime':
            return parsedt(thevalue)
        elif thetype == 'date':
            return parsedt(thevalue).date()
        elif thetype == 'timedelta':
            return timedelta(seconds = float(thevalue))
        elif thetype == 'objectid' and ObjectId is not None:
            return ObjectId(oid = thevalue)
        else:
            d['__type__'] = thetype
            return d

