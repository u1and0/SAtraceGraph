# -*- coding: utf-8 -*-
'''
## filefiller.py v5.0

__USAGE__
directoryにはtxtファイルが詰まったディレクトリ名(最後に/必須)
extentionには拡張子
以上を入れてbuild

__INTRODUCTION__
あるディレクトリ内のtxtファイル(ファイル名=yyyymmdd_HHMMSS.txt)が00時00分～00時04分に始まり、23時55分～23時59分に終わるようにファイルを追加していく

__ACTION__
変数セット
datetimeObjectというリスト作成
datetimeObjectが5分間隔に並ぶように以下を行う
    makeStartPoint()
    makeMiddlePoint()
    makeStopPoint()

__UPDATE5.0__
time_checker.pyでtime_difference_tupleを返してくる
filefillerでエラーが発生したとき(288よりファイル数が多くなったとき)、そのときの時刻を標準出力に表示する


__UPDATE4.0__
makeMiddlePointはyieldするたびにglobしてファイル数チェック
ファイル数が288を超えたらエラー出す
生成した時刻との差が1分未満だったらinsertしない


__UPDATE3.2__
外部ファイルから呼び出せるようにMAINも関数化


__UPDATE3.1__
一番最後にプリントしているdatetimeObjectはディレクトリ上のファイルをgrepしたものではないので
再度ファイル数をgrepする
↓
grepする部分を関数化する


__UPDATE3.0__
yieldでファイル名吐き出し
そのたびにmakefile


__UPDATE2.0__
makefileの機能追加


__UPDATE1.0__
First commit

__TODO__
makeMiddlePoint()が不完全
    最後から2番目以前のデータを2以上消したときに288ファイルに埋めてくれない
    for文の繰り返しがいけないと思う
    while文にすべきか
'''


# __BUILTIN MODULES__________________________
import glob
from more_itertools import pairwise
from datetime import timedelta
from datetime import datetime
# __USER MODULES__________________________
from time_checker import tracefile
# __PARAMETER__________________________
import json
with open('parameter.json', 'r') as f:
    param = json.load(f)

version = 'filefiller.py ver4.1'


def makefile(fullpath):
    '''ダミーデータ書き込む'''
    linenum = param['swe_poin']
    with open(fullpath, mode='w') as f:
        c = '# <This is DUMMY DATA made by %s>\n' % version
        for i in range(linenum):
            c += str(i).rjust(6) + ('-1000.00'.rjust(11)) * 3 + '\n'
        c += '# <eof>\n'
        f.write(c)


def makeStartPoint(li):
    '''始点要素の作製'''
    while True:
        start = li[0]  # 始点を探す
        if start.hour == 0 and 0 <= start.minute < 5:  # 始点の条件クリアでループ終了
            print('\nFirst element is', start)
            print('__makeStartPoint END__\n')
            break
        li.insert(0, start - timedelta(minutes=5))  # リストの最初に5分前の値をリストに格納
        print('Inserted', li[0])
        yield li[0].strftime('%Y%m%d_%H%M%S')


def makeStopPoint(li):
    '''終点要素の作製'''
    while True:
        stop = li[-1]  # 終点を探す
        if stop.hour == 23 and 55 <= stop.minute < 60:  # 終点の条件クリアでループ終了
            print('\nLast element is', stop)
            print('__makeStopPoint END__\n')
            break
        li.append(stop + timedelta(minutes=5))  # リストの最初に5分前の値をリストに格納
        print('Appended', li[-1])
        yield li[-1].strftime('%Y%m%d_%H%M%S')


def makeMiddlePoint(li, delta):
    '''
    引数:
            li:日付を表した値の入ったリスト
            delta:datetime.timedelta

    戻り値:
            insert_point.strftime('%Y%m%d_%H%M%S'):
                    twoの間に入れる値をyield
                    %Y%m%d_%H%M%S形式にして返す

    実行内容:
            makeMiddlePointは1個ずつしか吐き出さないジェネレータ
    '''
    for two in list(pairwise(li)):  # liの中身を2つずつにわける
        if two[-1] - two[0] >= delta + timedelta(minutes=1):  # 抜き出したタプルの要素の差がdelta上であれば
            print('\nLack between %s and %s' % (two[0], two[1]))
            print('Substract', abs(two[0] - two[1]))
            insert_point = two[0] + delta
            # 生成された値と、twoのうちの後ろの成分の差が1分未満であればバッティングしない
            if insert_point - two[-1] < timedelta(minutes=1):
                li.insert(li.index(two[-1]), insert_point)  # タプルの要素間の場所にdeltaずつ増やした値を入れる
                print('insert', insert_point)
                yield insert_point.strftime('%Y%m%d_%H%M%S')
    # print('\nThere is No point to insert')
    # print('__makeMiddlePoint END__\n')


'''TEST makeMiddlePoint
for _ in range(10):
    dali=pd.date_range('20160813', '20160814', freq='5T%sS'%np.random.randint(0,60))
    dali_droped=dali.drop(np.random.choice(dali))
    # daliからランダムな値を抽出(choice)し
    # ランダムな値をdaliから削除
    i = makeMiddlePoint(list(dali_droped), timedelta(minutes=5))
    print(i)
'''


# __MAIN__________________________
def datetime_list(directory, extention='.txt'):
    filename = glob.glob1(directory, '*')
    datetimeObject = [datetime.strptime(i[:-1 * len(extention)], '%Y%m%d_%H%M%S')
                      for i in filename]  # filebasenameのみ返す
    return datetimeObject


def filecheck(directory):
    '''
    ファイル数288 => メッセージを出してfilefiller.py終了
    ファイル数288未満 => filefillerで288になるまで穴埋め
    ファイル数288より多い => エラー吐き出して処理中断

    makeMiddlePointはyieldするたびにglobしてファイル数チェック
    ファイル数が288を超えたらエラー出す
    生成した時刻との差が1分未満だったらinsertしない
    '''
    filenum = 288
    extention = '.txt'
    datetimeObject = datetime_list(directory)
    print('--Before: Number of Files is %d--' % len(datetimeObject))  # Check number of files
    print('\n', directory, '内のファイル数を%d個から%d個に調整します\n' % (len(datetimeObject), filenum))
    for i in makeStartPoint(datetimeObject):  # 始点を作製
        makefile(directory + i + extention)
    for i in makeStopPoint(datetimeObject):  # 終点を作製
        makefile(directory + i + extention)

    while not len(glob.glob1(directory, '*')) == filenum:  # globして288個でないなら、288になるまでループ
        get_filenum = len(glob.glob1(directory, '*'))
        try:
            if get_filenum > filenum:  # ファイル数が多すぎればエラー
                raise ValueError(get_filenum)
        except ValueError:
            print('ファイル数が%d個！処理を中断します。' % get_filenum)
            print('生データを編集して、"%s/code"内にあるgpファイルを手動で動かしてください。' % directory)
            for time_difference_tuple in tracefile(directory):
                print('\nヒント！')
                print('時間差', time_difference_tuple[1] - time_difference_tuple[0])
                print('時間差エラーの生じた時刻', time_difference_tuple)
                print('')
            raise
        else:  # ファイル数が少なければファイル埋め
            # if len(glob.glob(directory+'*'))<filenum:
            # filefiller(directory)
            for i in makeMiddlePoint(datetimeObject, timedelta(minutes=5)):
                makefile(directory + i + extention)
    else:  # file数が288であれば、while処理終了
        print('--After: Number of Files is %d --' %
              len(glob.glob1(directory, '*')))  # Check number of files
        print('ファイル数を288個にできました。グラフ化処理を続行します。')


'''
TEST
filefiller('C:/home/gnuplot/SAout/160717/')
'''


'''
TEST2
directory='C:/home/gnuplot/SAout/160717/'
extention='.txt'
datetimeObject=globfile(directory,extention)
print('Before',len(datetimeObject))

function=[
                    'makeMiddlePoint(datetimeObject,timedelta(minutes=5))',
                    'makeStartPoint()',
                    'makeStopPoint()']
for func in function:
    for filename in eval(func):
        pass
        # makefile(directory+filename+extention)

# datetimeObject=globfile(directory,extention)
print('After',len(datetimeObject))
'''


'''TEST3 filefiller.py
directory = 'C:/home/python/SAtraceTestSpace/160813/rawdata/trace/'
filecheck(directory)
'''
