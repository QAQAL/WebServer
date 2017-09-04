import json

from utils import log


def save(data, path):
    """
    data 是 dict 或者 list
    path 是保存文件的路径
    """
    s = json.dumps(data, indent=2, ensure_ascii=False)
    with open(path, 'w+', encoding='utf-8') as f:
        log('save', path, s, data)
        f.write(s)


def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        s = f.read()
        log('load', s)
        return json.loads(s)


class Model(object):
    def __init__(self, form):
        self.id = form.get('id', None)

    @classmethod   # 返回 User.txt
    def db_path(cls):
        classname = cls.__name__
        path = 'data/{}.txt'.format(classname)
        return path

    @classmethod   # 得到一个新类的所有属性
    def _new_from_dict(cls, d):
        # 因为子元素的 __init__ 需要一个 form 参数
        # 所以这个给一个空字典
        m = cls({})   # 一个类实例
        for k, v in d.items():
            # setattr 是一个特殊的函数
            setattr(m, k, v)
        return m

    @classmethod  # 得到所有类的所有属性(列表)
    def all(cls):
        """
        all 方法(类里面的函数叫方法)使用 load 函数得到所有的 models
        """
        path = cls.db_path()
        models = load(path)
        # 用列表推导生成一个包含所有 实例 的 list
        # m 是 dict, 用 cls._new_from_dict(m) 可以初始化一个 cls 的实例
        ms = [cls._new_from_dict(m) for m in models]
        return ms

    @classmethod  # 得到一个类实例
    def new(cls, form):
        m = cls(form)
        return m

    @classmethod   # 得到指定的一个类的所有属性
    def find_by(cls, **kwargs):
        log('kwargs, ', kwargs, type(kwargs))
        for m in cls.all():
            exist = False
            for key, value in kwargs.items():
                k, v = key, value
                if v == getattr(m, k):
                    exist = True
                else:
                    exist = False
            if exist:
                return m
        return None

    @classmethod   # 得到指定id的一个类的所有属性
    def find(cls, id):
        return cls.find_by(id=id)

    @classmethod   # 得到指定的所有类的所有属性(列表)
    def find_all(cls, **kwargs):
        log('kwargs, ', kwargs, type(kwargs))
        models = []
        for m in cls.all():
            exist = False
            for key, value in kwargs.items():
                k, v = key, value
                if v == getattr(m, k):
                    exist = True
                else:
                    exist = False
            if exist:
                models.append(m)
        return models

    def __repr__(self):
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} \n>\n'.format(classname, s)

    # 保存数据，并生成id
    def save(self):
        """
        用 all 方法读取文件中的所有 model 并生成一个 list
        把 self 添加进去并且保存进文件
        """
        log('debug save')
        # 相当于 models = self.__class__.all()
        models = self.all()
        log('models', models)

        first_index = 0
        if self.id is None:
            log('id is None')
            if len(models) > 0:
                self.id = models[-1].id + 1
            else:
                log('first index', first_index)
                self.id = first_index
            models.append(self)
        else:
            log('id is not None')
            # 有 id 说明已经是存在于数据文件中的数据
            # 那么就找到这条数据并替换
            for i, m in enumerate(models):
                if m.id == self.id:
                    models[i] = self

        # 保存
        l = [m.__dict__ for m in models]
        path = self.db_path()
        save(l, path)

    @classmethod   # 删除指定id的一个类
    def delete(cls, id):
        ms = cls.all()
        for i, m in enumerate(ms):
            if m.id == id:
                del ms[i]
                break
        # 保存
        l = [m.__dict__ for m in ms]
        path = cls.db_path()
        save(l, path)