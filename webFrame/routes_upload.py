from utils import log
from upload import Upload
from models import User
from routes import current_user


def template(name):
    """
    based on name, read a file in templates dir and return
    :param name:
    :return:
    """
    path = 'templates/' + name
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def response_with_headers(headers, code=200):
    """
    Content-Type: image/png
    Set-Cookie: user=admin
    :param headers:
    :param code:
    :return:
    """
    header = 'HTTP/1.1 {} OK\r\n'.format(code)
    header += ''.join(['{}: {}\r\n'.format(k, v)
                       for k, v in headers.items()])
    return header


def redirect(url):
    """
    after receiving 302 response,
    automatically search Location segment in HTTP header
    and return an url
    :param url:
    :return:
    """
    headers = {
        'Location': url,
    }
    # add Location segment and generate HTTP response
    # note, no HTTP body
    r = response_with_headers(headers, 302) + '\r\n'
    return r.encode('utf-8')


def index(request):
    headers = {
        'Content-Type': 'text/html',
    }
    upload_list = Upload.find_all()
    uploads = []
    for up in upload_list:
        # edit_link = '<a href="/upload/edit">编辑</a>'
        # delete_link = '<a href="/upload/delete">删除</a>'
        # s = '<img href="/static/uploads/{}"> {} {}'.format(up.name, edit_link, delete_link)
        s = '<img src="/static/uploads?file={}"/>'.format(up)
        uploads.append(s)
    upload_html = '\n'.join(uploads)
    # substitute marked string in template file
    body = template('upload_index.html')
    body = body.replace('{{uploads}}', upload_html)

    header = response_with_headers(headers)
    r = header + '\r\n' + body
    return r.encode(encoding='utf-8')


def add(request):
    """
    add new upload
    :param request:
    :return:
    """
    headers = {
        'Content-Type': 'text/html',
    }
    if request.method == 'POST':
        form = request.form()
        up = Upload.new(form)
        up.save()
    return redirect('/upload')


def edit(request):
    pass


def update(request):
    pass


def delete_upload(request):
    pass


# route dict
# key is route (path)
# value is route function (response)
route_dict = {
    # GET request, present page
    '/upload': index,
    '/upload/edit': edit,
    # POST request, process data
    '/upload/add': add,
    '/upload/update': update,
    '/upload/delete': delete_upload,
}
