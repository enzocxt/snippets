# -*- coding: utf-8 -*-

import cgi
from HTMLParser import HTMLParser

from xml.sax.saxutils import escape, unescape, quoteattr


def show_xml():
    # (un)escape 默认不处理单双引号
    s = escape("< & > '")
    print(s)
    s = unescape("&lt; &amp; &gt; &apos; &quot;")
    print(s)
    s = quoteattr('some value containing " a double-quote')
    print(s)

    # can use a dict for replacement
    s = escape("abc", {"b": "&#98"})
    print(s)
    s = unescape("&apos; &quot;", {"&apos;": "'", "&quot;": '"'})
    print(s)
    # escape(text, html_escape_table)
    # unescape(text, html_unescape_table)
    html_escape_table = {
        "&": "&amp;",
        '"': "&quot;",
        "'": "&apos;",
        ">": "&gt;",
        "<": "&lt;",
    }
    html_unescape_table = {v:k for k, v in html_escape_table.items()}


def show_html():
    # 这个模块没有 unescape
    s = cgi.escape("""& < > """)
    print(s)
    # 如果要转义 " 则使参数 quote 为 True
    # 单引号永远不转义
    # 如果需要转义单引号，可以使用 xml.sax.saxutils 的 quoteattr()
    s = cgi.escape("""& < > " ' """, quote=True)
    print(s)
    s = HTMLParser.unescape.__func__(HTMLParser, 'ss&copy;')
    print(s)
    s = HTMLParser.unescape.__func__(HTMLParser, 'ss&amp;')
    print(s)

    # manual defined method
    html_escape_table = {
        "&": "&amp;",
        '"': "&quot;",
        "'": "&apos;",
        ">": "&gt;",
        "<": "&lt;",
    }
    text = '''abcd&ef<hi>k'm"n'''
    s = ''.join(html_escape_table.get(c, c) for c in text)
    print(s)


if __name__ == '__main__':
    show_xml()
