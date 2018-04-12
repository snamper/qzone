from json import JSONEncoder, JSONDecoder

class Ant:
    def __init__(self, name, password):
        self.__name__ = name
        self.__password__ = password

    def __str__(self):
        return 'ant: name = {0!r}, password = {1!r}'.format(self.__name__, self.__password__)

    def __repr__(self):
        return 'data.Ant({0!r}, {1!r})'.format(self.__name__, self.__password__)

    def __eq__(self, other):
        if isinstance(other, Ant):
            return self.__name__ == other.__name__ and self.__password__ == other.__password__
        else:
            return object.__eq__(self, other)

    def __hash__(self):
        return hash((self.__name__, self.__password__))

class Boss:
    def __init__(self, name):
        self.__name__ = name

    def __str__(self):
        return 'boss: name = {0!r}'.format(self.__name__)

    def __repr__(self):
        return 'data.Boss({0!r})'.format(self.__name__)

    def __eq__(self, other):
        if isinstance(other, Boss):
            return self.__name__ == other.__name__
        else:
            return object.__eq__(self, other)

    def __hash__(self):
        return hash(self.__name__)

class QQEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Ant):
            return {'__class__': 'data.Ant',
                    '__name__': obj.__name__,
                    '__password__': obj.__password__
                    }
        elif isinstance(obj, Boss):
            return {'__class__': 'data.Boss',
                    '__name__': obj.name,
                    }
        else:
            JSONEncoder.default(self, obj)

class QQDecoder(JSONDecoder):
    def __init__(self, *, parse_float=None,
            parse_int=None, parse_constant=None, strict=True,
            object_pairs_hook=None):
        JSONDecoder.__init__(self, self.object_hook, parse_float,
                parse_int, parse_constant, strict, object_pairs_hook)

    def object_hook(self, obj_dict):
        if '__class__' in obj_dict:
            cls = obj_dict['__class__']

            if cls == 'data.Ant':
                return Ant(obj_dict['__name__'], obj_dict['__password__'])
            elif cls == 'data.Boss':
                return Boss(obj_dict['__name__'])

        return obj_dict
