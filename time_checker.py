# -*- coding: utf-8 -*-
import datetime
from more_itertools import pairwise
import glob
import doctest
import simplejson

with open('parameter.json', 'r') as f:
    param = simplejson.load(f)


def tracefile(dirname):
    '''
    ## time_checker ver1.0

    __USAGE__
    引数:
        dirname : datetimeがファイル名になったファイルが詰まったディレクトリの場所(string型)
    戻り値:
        timepair : datetime2つが入ったタプル(tuple型)

    __INTRODUCTION__
    あるファイル名から次のファイルが作成された時刻の差分を出す。

    __ACTION__
    SAtraceGraph.pyのサブプロセスのfilefiller.filecheck()でエラーが生じたときに実行される。

    __UPDATE1.0__
    First commit

    __TODO__
    None

    __TEST__

    >>> [i for i in tracefile(param['out']+'/160817/rawdata/trace/')]
    (datetime.datetime(1900, 1, 1, 8, 50, 29), datetime.datetime(1900, 1, 1, 8, 59, 12))

    '''
    line = glob.glob1(dirname, '*')
    ttlist = [datetime.datetime.strptime(i[:-4], '%Y%m%d_%H%M%S') for i in line]
    for timepair in pairwise(ttlist):
        sub = timepair[1] - timepair[0]
        if not datetime.timedelta(minutes=4) < sub < datetime.timedelta(minutes=6):
            yield timepair  # 時間差の生じたとこ


if __name__ == '__main__':
    doctest.testmod()
