from models import Model
from models.comment import Comment
from models.user import User


class Weibo(Model):
    """
    微博类
    """
    def __init__(self, form, user_id=-1):
        super().__init__(form)
        self.content = form.get('content', '')
        # 和别的数据关联的方式, 用 user_id 表明拥有它的 user 实例
        self.user_id = form.get('user_id', user_id)

    def is_owner(self, id):
        return self.user_id == id

    def user(self):
        u = User.find_by(id=self.user_id)
        return u

    def comments(self):
        return Comment.find_all(weibo_id=self.id)