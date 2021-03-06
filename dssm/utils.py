import paddle

UNK = 0

logger = logging.getLogger("paddle")
logger.setLevel(logging.INFO)


def mode_attr_name(mode):
    return mode.upper() + '_MODE'


def create_attrs(cls):
    for id, mode in enumerate(cls.modes):
        setattr(cls, mode_attr_name(mode), id)


def make_check_method(cls):
    '''
    create methods for classes.
    '''

    def method(mode):
        def _method(self):
            return self.mode == getattr(cls, mode_attr_name(mode))

        return _method

    for id, mode in enumerate(cls.modes):
        setattr(cls, 'is_' + mode, method(mode))


def make_create_method(cls):
    def method(mode):
        @staticmethod
        def _method():
            key = getattr(cls, mode_attr_name(mode))
            return cls(key)

        return _method

    for id, mode in enumerate(cls.modes):
        setattr(cls, 'create_' + mode, method(mode))


def make_str_method(cls, type_name='unk'):
    def _str_(self):
        for mode in cls.modes:
            if self.mode == getattr(cls, mode_attr_name(mode)):
                return mode

    def _hash_(self):
        return self.mode

    setattr(cls, '__str__', _str_)
    setattr(cls, '__repr__', _str_)
    setattr(cls, '__hash__', _hash_)
    cls.__name__ = type_name


def _init_(self, mode, cls):
    if isinstance(mode, int):
        self.mode = mode
    elif isinstance(mode, cls):
        self.mode = mode.mode
    else:
        raise Exception("wrong mode type, get type: %s, value: %s" %
                        (type(mode), mode))


def build_mode_class(cls):
    create_attrs(cls)
    make_str_method(cls)
    make_check_method(cls)
    make_create_method(cls)


class TaskType(object):
    modes = 'train test infer'.split()

    def __init__(self, mode):
        _init_(self, mode, TaskType)


class ModelType:
    modes = 'classification rank regression'.split()

    def __init__(self, mode):
        _init_(self, mode, ModelType)


class ModelArch:
    modes = 'fc cnn rnn'.split()

    def __init__(self, mode):
        _init_(self, mode, ModelArch)


build_mode_class(TaskType)
build_mode_class(ModelType)
build_mode_class(ModelArch)


def sent2ids(sent, vocab):
    '''
    transform a sentence to a list of ids.

    @sent: str
        a sentence.
    @vocab: dict
        a word dic
    '''
    return [vocab.get(w, UNK) for w in sent.split()]


def load_dic(path):
    '''
    word dic format:
      each line is a word
    '''
    dic = {}
    with open(path) as f:
        for id, line in enumerate(f):
            w = line.strip()
            dic[w] = id
    return dic


if __name__ == '__main__':
    t = TaskType(1)
    t = TaskType.create_train()
    print t
    print 'is', t.is_train()
