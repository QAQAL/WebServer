from models import Model
from models.todo import Todo

import hashlib


class User(Model):
    """
    User 是一个保存用户数据的 model
    """

    def __init__(self, form):
        super().__init__(form)  # self.id = form.get('id', None)
        self.username = form.get('username', '')
        self.password = form.get('password', '')

    @staticmethod   # 得到密码加盐后的hash摘要
    def salted_password(password, salt='$!@><?>HUI&DWQa`'):
        """$!@><?>HUI&DWQa`"""
        salted = password + salt
        hash = hashlib.sha256(salted.encode('ascii')).hexdigest()
        return hash

    def validate_login(self):
        u = User.find_by(username=self.username)
        if u is not None:
            return u.password == self.salted_password(self.password)
        else:
            return False

    def validate_register(self):
        u = User.find_by(username=self.username)
        valid = u is None and len(self.username) > 2 and len(self.password) > 2
        if valid:
            p = self.password
            self.password = self.salted_password(p)
            return True
        else:
            return False

    def todos(self):
        # 列表推倒和过滤
        # return [t for t in Todo.all() if t.user_id == self.id]
        ts = []
        for t in Todo.all():
            if t.user_id == self.id:
                ts.append(t)
        return ts

    @classmethod
    def update(cls, id, form):
        u = cls.find(id)
        valid_names = [
            'password',
        ]
        for key in form:
            if key in valid_names:
                setattr(u, key, form[key])
        u.save()