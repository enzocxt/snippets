from utils import log
from book import Book
from models import User, Admin
from routes import current_user


def template(name):
    """
    根据名字读取 templates 文件夹里的一个文件并返回
    """
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def response_with_headers(headers, code=200):
    """
    Content-Type: text/html
    Set-Cookie: user=gua
    """
    header = 'HTTP/1.1 {} VERY OK\r\n'.format(code)
    header += ''.join(['{}: {}\r\n'.format(k, v)
                           for k, v in headers.items()])
    return header


def redirect(url):
    """
    浏览器在收到 302 响应的时候
    会自动在 HTTP header 里面找 Location 字段并获取一个 url
    然后自动请求新的 url
    """
    headers = {
        'Location': url,
    }
    # 增加 Location 字段并生成 HTTP 响应返回
    # 注意, 没有 HTTP body 部分
    r = response_with_headers(headers, 302) + '\r\n'
    return r.encode('utf-8')


def admin_required(route_function):
    def f(request):
        # 找到当前登录的用户, 如果没登录或不是管理员, 就 redirect 到 /login/admin
        log('\n\n  current cookies', request.cookies)
        uname = current_user(request)
        log('\n  current username ', uname)
        u = User.find_by(username=uname)
        if u is None or not u.validate_admin():
            return redirect('/login/admin')
        return route_function(request)
    return f


def index(request):
    """
    book 首页的路由函数
    """
    headers = {
        'Content-Type': 'text/html',
    }
    book_list = Book.find_all()
    books = []
    for b in book_list:
        edit_link = '<a href="/book/edit?id={}">编辑</a>'.format(b.id)
        delete_link = '<a href="/book/delete?id={}">删除</a>'.format(b.id)
        # detail = b.detail
        # detail.pop('内容概要')
        # detail.pop('作者简介')
        # binfo = ' '.join(map(str, list(detail.values())[:-1]))
        s = '<h5>{}: {} {} {}</h5>'.format(b.id, b.name, edit_link, delete_link)
        books.append(s)
    # book_html = '<h5>' + ' '.join(book_list[0].detail.keys()) + '</h5>'
    book_html = ''.join(books)
    # 替换模板文件中的标记字符串
    body = template('book_index.html')
    body = body.replace('{{books}}', book_html)
    # 下面 3 行可以改写为一条函数, 还把 headers 也放进函数中
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def edit(request):
    """
    book edit 的路由函数
    """
    headers = {
        'Content-Type': 'text/html',
    }
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    # 得到当前编辑的 book 的 id
    book_id = int(request.query.get('id', -1))
    t = Book.find_by(id=book_id)
    if t.user_id != u.id:
        return redirect('/login')
    # if book_id < 1:
    #     return error(404)
    # 替换模板文件中的标记字符串
    body = template('book_edit.html')
    body = body.replace('{{book_id}}', str(t.id))
    body = body.replace('{{book_title}}', str(t.title))
    # 下面 3 行可以改写为一条函数, 还把 headers 也放进函数中
    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def add(request):
    """
    用于增加新 book 的路由函数
    """
    headers = {
        'Content-Type': 'text/html',
    }
    uname = current_user(request)
    u = User.find_by(username=uname)
    if request.method == 'POST':
        # 'title=aaa'
        # {'title': 'aaa'}
        form = request.form()
        t = Book.new(form)
        t.user_id = u.id
        t.save()
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/book')


def update(request):
    """
    用于增加新 book 的路由函数
    """
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    if request.method == 'POST':
        # 修改并且保存 book
        form = request.form()
        print('debug update', form)
        book_id = int(form.get('id', -1))
        t = Book.find_by(id=book_id)
        t.title = form.get('title', t.title)
        t.save()
    # 浏览器发送数据过来被处理后, 重定向到首页
    # 浏览器在请求新首页的时候, 就能看到新增的数据了
    return redirect('/book')


def delete_book(request):
    uname = current_user(request)
    u = User.find_by(username=uname)
    if u is None:
        return redirect('/login')
    # 得到当前编辑的 book 的 id
    book_id = int(request.query.get('id', -1))
    t = Book.find_by(id=book_id)
    if t.user_id != u.id:
        return redirect('/login')
    if t is not None:
        t.remove()
    return redirect('/book')


# 路由字典
# key 是路由(路由就是 path)
# value 是路由处理函数(就是响应)
route_dict = {
    # GET 请求, 显示页面
    '/info': index,
    '/info/edit': edit,
    # POST 请求, 处理数据
    '/info/add': admin_required(add),
    '/info/update': update,
    '/info/delete': delete_book,
}
