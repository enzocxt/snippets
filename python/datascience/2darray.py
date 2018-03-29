# -*- coding: utf-8 -*-
import sys
# sys.path.append("/home/aardvark/code/typetokenQLVL")
sys.path.append("/home/enzocxt/Projects/QLVL/typetoken_workdir/typetokenQLVL")
import logging
import numpy as np
import pandas as pd

from typetoken.Manager import ItemFreqManager, ColFreqManager, MatrixManager, TokVecManager
from typetoken.Config import ConfigLoader
from typetoken.Matrix import SparseMatrix, WCMatrix, WWMatrix


def show_df():
    A = np.random.randint(0, 10, size=36).reshape(6, 6)
    names = [_ for _ in 'abcdef']
    df = pd.DataFrame(A, index=names, columns=names)
    df.to_csv('df.csv', index=True, header=True, sep='\t')


def test():
    # ------- set parameters -------
    # load default settings in 'config.ini' file
    # default_conf = "/home/aardvark/code/typetokenQLVL/config.ini"
    default_conf = "/home/enzocxt/Projects/QLVL/typetoken_workdir/typetokenQLVL/typetoken/config.ini"
    conf = ConfigLoader(default_conf)
    # update settings by user specified config file
    new_conf = "/home/enzocxt/Projects/QLVL/typetoken_workdir/test/config_test.ini"
    settings = conf.updateConfig(new_conf)
    # the better way for setting corpus directory, output directory, etc
    # is setting them in a configuration ini file in advance
    corpusName = 'Brown_wpr-art'
    corpus_path = settings['corpus-path']
    output_path = settings['output-path']

    path = "/home/enzocxt/Projects/QLVL/typetoken_workdir/output"
    mx_fname = '{}/Brown_wpr-art.wwmx.cos.npy'.format(path)
    wordFile = '{}/{}.NounsLowercase.minfreq10.nodefreq'.format(path, corpusName)
    contextFile = '{}/{}.minfreq10.without50mostfreq.nodefreq'.format(path, corpusName)
    cosmx = WWMatrix('Brown_wpr-art', settings,
                     matrix=mx_fname, wordDict=wordFile,
                     fmt='cos')
    filename = "{}/{}.wwmx.cos.csv".format(path, corpusName)
    cosmx.template_save_matrix(filename)


if __name__ == '__main__':
    test()
