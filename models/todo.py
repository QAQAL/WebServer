import time

from models import Model
from utils import formatted_time


class Todo(Model):
    def __init__(self, form, user_id=-1):
        super().__init__(form)
        self.task = form.get('task', '')
        self.completed = False
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = form.get('user_id', user_id)
        self.created_time = form.get('created_time')
        self.updated_time = form.get('updated_time')

    @classmethod
    def new(cls, form, user_id=-1):
        form['user_id'] = user_id
        m = super().new(form)  # m = Todo(form)
        t = int(time.time())
        m.created_time = t
        m.updated_time = t
        m.save()
        return m

    @classmethod
    def update(cls, id, form):
        t = cls.find(id)
        valid_names = [
            'task',
            'completed'
        ]
        for key in form:
            if key in valid_names:
                setattr(t, key, form[key])
        t.updated_time = int(time.time())
        t.save()

    def is_owner(self, id):
        return self.user_id == id

    def formatted_created_time(self):
        return formatted_time(self.created_time)

    def formatted_updated_time(self):
        return formatted_time(self.updated_time)
