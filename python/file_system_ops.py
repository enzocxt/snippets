# -*- coding: utf-8 -*-

import os
import sys


def list_dir_tree(startpath):
    for root, dirs, files in sorted(os.walk(startpath)):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        num_files = len(files)
        print "{}{}/ : {} files".format(indent, os.path.basename(root), num_files)
        subindent = ' ' * 4 * (level + 1)
        # for f in files:
        #    print "{}{}".format(subindent, f)


if __name__ == '__main__':
    path = "/home/enzocxt/Projects/QLVL/corp/nl/LeNC-alpino"
    prepath = "/home/enzocxt/Projects/QLVL/other_tasks/corpus_convert"
    # list_dir_tree(path)
    cmd = "java -cp {path}/saxon9he/saxon9he.jar net.sf.saxon.Query "\
    "-q:{path}/universal_dependencies_2.0-LeNC-final.xq MODE=conll "\
    "DIR={path}/data/LeNC/test -o:/home/enzocxt/tmp/tmp.txt ".format(path=prepath)
    # "> /home/enzocxt/tmp/log.txt
    res = os.system(cmd)
    print res
