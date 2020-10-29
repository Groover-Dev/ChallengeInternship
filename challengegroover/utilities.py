from sqlalchemy.ext.declarative import DeclarativeMeta
import json
import datetime
import sqlalchemy
from ast import literal_eval

class AlchemyJsonEncoder(json.JSONEncoder):

    #Encoder to convert alchemy model to json
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):

            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                if not hasattr(data, '__call__') and data != 'null' :
                    data = obj.__getattribute__(field)
                    #handle data type
                    if isinstance(data,datetime.datetime):
                        date_time = data.strftime("%m/%d/%Y, %H:%M:%S")
                        fields[field] = date_time
                    #handle array of models
                    elif isinstance(data,sqlalchemy.orm.collections.InstrumentedList):
                        fields[field] = literal_eval(json.dumps(data,cls=AlchemyJsonEncoder))
                    else:
                        try:
                            #general handling
                            json.dumps(data)
                            fields[field] = data
                        #pass other typing exceptions
                        except TypeError:
                            pass
            # dic: json-encodable
            return fields

        return json.JSONEncoder.default(self, obj)
