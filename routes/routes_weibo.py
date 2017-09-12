from models.comment import Comment
from models.user import User
from models.weibo import Weibo
from routes import (
    redirect,
    http_response,
    current_user,
    login_required,
)
from utils import template, log


# 微博相关页面
def index(request):
    u = current_user(request)
    weibos = Weibo.all()
    body = template('weibo_index.html', weibos=weibos, user=u)
    return http_response(body)


def add(request):
    u = current_user(request)
    # 创建微博
    form = request.form()
    w = Weibo.new(form)
    w.user_id = u.id
    w.save()
    return redirect('/weibo/index')


def delete(request):
    # 删除微博
    weibo_id = int(request.query.get('id', None))
    Weibo.delete(weibo_id)
    return redirect('/weibo/index')


def edit(request):
    weibo_id = int(request.query.get('id', -1))
    w = Weibo.find(weibo_id)
    user = current_user(request)

    # 生成一个 edit 页面
    body = template('weibo_edit.html', weibo=w, user=user)
    return http_response(body)


def update(request):
    form = request.form()
    content = form.get('content', '')
    weibo_id = int(form.get('id', -1))
    w = Weibo.find(weibo_id)
    w.content = content
    w.save()
    # 重定向到用户的主页
    return redirect('/weibo/index')


def comment_add(request):
    u = current_user(request)
    # 创建微博
    form = request.form()
    c = Comment.new(form)
    c.user_id = u.id
    c.save()
    return redirect('/weibo/index')


def comment_edit(request):
    comment_id = int(request.query.get('id', -1))
    c = Comment.find(comment_id)
    user = current_user(request)
    # 生成一个 edit 页面
    body = template('comment_edit.html', comment=c, user=user)
    return http_response(body)


def comment_update(request):
    form = request.form()
    comment_id = int(form.get('id', -1))
    Comment.update(comment_id, form)
    return redirect('/weibo/index')


def comment_delete(request):
    # 删除微博
    comment_id = int(request.query.get('id', None))
    Comment.delete(comment_id)
    return redirect('/weibo/index')


def weibo_user_required(route_function):

    def f(request):
        log('same user required', request)
        u = current_user(request)
        if request.method == 'GET':
            weibo_id = int(request.query.get('id'))
        else:
            weibo_id = int(request.form().get('id'))

        w = Weibo.find(weibo_id)
        if w.is_owner(u.id):
            return route_function(request)
        else:
            return redirect('/login')

    return f


def comment_user_required(route_function):

    def f(request):
        log('comment user required', request)
        u = current_user(request)
        if request.method == 'GET':
            comment_id = int(request.query.get('id'))
        else:
            comment_id = int(request.form().get('id'))

        c = Comment.find(comment_id)
        if route_function == comment_delete:
            if c.is_owner(u.id) or Weibo.find(c.weibo_id).user_id == u.id:
                return route_function(request)
            else:
                return redirect('/login')

        else:
            if c.is_owner(u.id):
                return route_function(request)
            else:
                return redirect('/login')
    return f


def route_dict():
    r = {
        '/weibo/index': login_required(index),
        '/weibo/edit': login_required(weibo_user_required(edit)),
        '/weibo/add': login_required(add),
        '/weibo/update': login_required(weibo_user_required(update)),
        '/weibo/delete': login_required(weibo_user_required(delete)),
        # 评论
        '/comment/add': login_required(comment_add),
        '/comment/edit': login_required(comment_user_required(comment_edit)),
        '/comment/update': login_required(comment_user_required(comment_update)),
        '/comment/delete': login_required(comment_user_required(comment_delete)),

    }
    return r
