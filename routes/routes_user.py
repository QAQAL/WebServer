from models.session import Session
from routes import (
    random_str,
    redirect,
    http_response,
    current_user,
)
from utils import log
from utils import template
from models.user import User


def route_login(request):
    """
    登录页面的路由函数
    """
    log('login, cookies', request.cookies)
    if request.method == 'POST':
        form = request.form()
        u = User(form)
        if u.validate_login():
            session_id = random_str()
            u = User.find_by(username=u.username)
            s = Session.new(dict(
                session_id=session_id,
                user_id=u.id,
            ))
            s.save()
            log('session', s)
            headers = {
                'Set-Cookie': 'sid={}'.format(session_id)
            }
            # 登录后定向到 /
            return redirect('/', headers)
        else:
            username = '请重新登录'
            result = '用户名或密码不正确'
            body = template('login.html', username=username, result=result)
            return http_response(body)

    # 显示登录页面
    u = current_user(request)
    if u is None:
        username = '游客'
        result = '请登录'
    else:
        username = u.username
        result = '登录成功'

    body = template('login.html', username=username, result=result)
    return http_response(body)


def route_register(request):
    """
    注册页面的路由函数
    """
    if request.method == 'POST':
        form = request.form()
        u = User.new(form)
        if u.validate_register():
            u.save()
            # 注册成功后 定向到登录页面
            return redirect('/login')
        else:
            # 注册失败 定向到注册页面
            return redirect('/register')
    # 显示注册页面
    body = template('register.html')
    return http_response(body)


def update_user_password(request):
    form = request.form()
    form['password'] = User.salted_password(form['password'])
    user_id = int(form.get('id', -1))
    User.update(user_id, form)
    return redirect('/login')


def edit_password(request):
    u = current_user(request)
    body = template('admin_password_edit.html', user=u)
    return http_response(body)


def route_dict():
    r = {
        '/login': route_login,
        '/register': route_register,
        '/admin_password_edit': edit_password,
        '/update_user_password': update_user_password,
    }
    return r
