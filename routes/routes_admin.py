from models.user import User
from routes import(
    current_user,
    redirect,
    response_with_headers,
    http_response,
)
from utils import(
    log,
    template,
)


def admin_users(request):
    """
    todo 首页的路由函数
    """
    u = current_user(request)
    # 如果当前用户没有登录
    if u is None:
        log('非登录用户')
        return redirect('/login')

    # 如果当前id不是1
    elif u.id != 0:
        log('非授权用户')
        return redirect('/login')

    # 如果当前id是1
    else:
        log('授权用户')
        user_list = User.all()
        body = template('admin.html', user_list=user_list)
        return http_response(body)


def admin_users_update(request):
    form = request.form()
    form['password'] = User.salted_password(form['password'])
    user_id = int(form.get('id', -1))
    User.update(user_id, form)
    return redirect('/admin/users')


def route_dict():
    """
    路由字典
    key 是路由(路由就是 path)
    value 是路由处理函数(就是响应)
    """
    d = {
        '/admin/users': admin_users,
        '/admin/user/update': admin_users_update,
    }
    return d
