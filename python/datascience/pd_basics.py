import operator

from pandas.io.json import json_normalize
import pandas as pd
import json
import time


test_path = "/home/enzocxt/Projects/QLVL/typetoken_workdir/test_data/Brown_wpr-art"


def show1():
    filename = "{}/output/Brown_wpr-art.nodefreq".format(test_path)
    data_str = open(filename).read()

    data_dict = json.loads(data_str)
    df1 = json_normalize(data_dict)
    data_list = sorted(data_dict.iteritems(), key=operator.itemgetter(1), reverse=True)
    df2 = pd.DataFrame(data_list, columns=['item', 'freq'])

    df3 = df2[df2.freq > 10]
    df4 = df2.freq > 10
    print(df4.head())


if __name__ == '__main__':
    show1()
