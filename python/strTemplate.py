# -*- coding: utf-8 -*-

from string import Template

def tmplSub(filename):
    with open(filename, 'r') as inf:
        tmpl = Template(inf.read())
        res = tmpl.substitute(NEUTRALWORD='***\nword\n***', TOKENS='---\ntokens\n---')

    print res
    return res


if __name__ == '__main__':
    tmplSub('/home/enzocxt/Dropbox/CT/snippets/python/html.template')
