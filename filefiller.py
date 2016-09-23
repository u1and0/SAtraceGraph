# coding: utf-8
version='filefiller.py ver3.2'
'''
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


import numpy as np
import matplotlib.dates as pltd
# import matplotlib.pyplot as plt
# import seaborn as sns
import pandas as pd
import glob
from more_itertools import pairwise
from datetime import timedelta
from datetime import datetime
import time


# def globfile(directory,extention):
# 	'''
# 	ディレクトリを引数に
# 	%Y%m%d_%H%M%S形式のファイルベースネーム返す
# 	'''
# 	fullpath=glob.glob(directory+'*'+extention)   #ファイル名をリストに格納

# 	filename_without_extention=[i[len(directory):-1*len(extention)] for i in fullpath]   #ファイルベースネーム

# 	datetimeObject=[datetime.strptime(i,'%Y%m%d_%H%M%S') for i in filename_without_extention]   #要素がdatetime形式のリスト作成

# 	return datetimeObject


def makefile(fullpath):
	'''ダミーデータ書き込む'''
	with open(fullpath,mode='w') as f:
		c='# <This is DUMMY DATA made by %s>\n'% version
		for i in range(1001):
			c+=str(i).rjust(6)+('-1000.00'.rjust(11))*3+'\n'
		c+='# <eof>\n'
		f.write(c)


def makeStartPoint(li):
	'''始点要素の作製'''
	while True :
		start=li[0]   #始点を探す
		if start.hour==0 and 0<=start.minute<5:   #始点の条件クリアでループ終了
			print('\nFirst element is',start)
			print('__makeStartPoint END__\n')
			break
		li.insert(0,start-timedelta(minutes=5))   #リストの最初に5分前の値をリストに格納
		print('Inserted',li[0])
		yield li[0].strftime('%Y%m%d_%H%M%S')


def makeStopPoint(li):
	'''終点要素の作製'''
	while True :
		stop=li[-1]   #終点を探す
		if stop.hour==23 and 55<=stop.minute<60:   #終点の条件クリアでループ終了
			print('\nLast element is',stop)
			print('__makeStopPoint END__\n')
			break
		li.append(stop+timedelta(minutes=5))   #リストの最初に5分前の値をリストに格納
		print('Appended',li[-1])
		yield li[-1].strftime('%Y%m%d_%H%M%S')


def makeMiddlePoint(li,delta):
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
	for two in list(pairwise(li)):   #liの中身を2つずつにわける
		if two[-1]-two[0]>=delta +timedelta(minutes=1):   #抜き出したタプルの要素の差がdelta上であれば
			print('\nLack between %s and %s'% (two[0],two[1]))
			print('Substract',abs(two[0]-two[1]))
			insert_point=two[0]+delta
			if insert_point-two[-1] < timedelta(minutes=1):  # 生成された値と、twoのうちの後ろの成分の差が1分未満であればバッティングしない
				li.insert(li.index(two[-1]),insert_point)   #タプルの要素間の場所にdeltaずつ増やした値を入れる
				print('insert',insert_point)
				yield insert_point.strftime('%Y%m%d_%H%M%S')
	print('\nThere is No point to insert')
	print('__makeMiddlePoint END__\n')


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

# def filefiller(directory,extention='.txt'):
# 	'''
# 	file数を288まで増やす
# 	makeMiddlePoint:間の穴あき埋める
# 	makeStartPoint:最初の要素から00:00に向けて5分間隔でデータ作る
# 	makeStopPoint:最後の要素から23:59に向けて5分間隔でデータ作る
# 	'''
# 	filename=glob.glob1(directory,'*')
# 	datetimeObject=[datetime.strptime(i[:-1*len(extention)],'%Y%m%d_%H%M%S') for i in filename]  # filebasenameのみ返す
# 	# datetimeObject=globfile(directory,extention)
# 	print('-'*20)
# 	# i = makeMiddlePoint(datetimeObject,timedelta(minutes=5))  #5分間隔でデータを挿入
# 	# # for i in makeMiddlePoint(datetimeObject,timedelta(minutes=5)):   #5分間隔でデータを挿入
# 	# if i:
# 	# 	makefile(directory+i+extention)
# 	for i in makeMiddlePoint(datetimeObject, timedelta(minutes=5)):
# 		makefile(directory+i+extention)
# 	for i in makeStartPoint(datetimeObject):  # 始点を作製
# 		makefile(directory+i+extention)
# 	for i in makeStopPoint(datetimeObject):  # 終点を作製
# 		makefile(directory+i+extention)

def datetime_list(directory,extention='.txt'):
	filename=glob.glob1(directory,'*')
	datetimeObject=[datetime.strptime(i[:-1*len(extention)],'%Y%m%d_%H%M%S') for i in filename]  # filebasenameのみ返す
	return datetimeObject



def filecheck(directory):
	'''
	ファイル数288 => 何もせずfilefiller.py終了
	ファイル数288未満 => filefillerで288になるまで穴埋め
	ファイル数288より多い => エラー吐き出して処理中断
	'''
	filenum=288
	extention='.txt'
	datetimeObject=datetime_list(directory)
	for i in makeStartPoint(datetimeObject):  # 始点を作製
		makefile(directory+i+extention)
	for i in makeStopPoint(datetimeObject):  # 終点を作製
		makefile(directory+i+extention)


	while not len(glob.glob1(directory, '*'))==filenum:   #globして288個でないなら、288になるまでループ
		get_filenum=len(glob.glob1(directory, '*'))
		print('--Before: Number of Files is %d--' %get_filenum)   #Check number of files
		try:
			if get_filenum > filenum:   #ファイル数が多すぎればエラー
				raise ValueError(get_filenum)
		except ValueError:
			print('ファイル数が%d個！処理を中断します。'% get_filenum)
			print('生データを編集して、"%s/code"内にあるgpファイルを手動で動かしてください。'%directory)
			raise
		else:   #ファイル数が少なければファイル埋め
			# if len(glob.glob(directory+'*'))<filenum:
			print('\n',directory,'内のファイル数を%d個から%d個に調整します\n'% (get_filenum,filenum))
			# filefiller(directory)
			for i in makeMiddlePoint(datetimeObject, timedelta(minutes=5)):
				makefile(directory+i+extention)
	else:  # file数が288であれば、while処理終了
		print('--After: Number of Files is %d --' %len(glob.glob1(directory,'*')))   #Check number of files
		datetimeObject_after=datetime_list(directory)
		# plt.plot_date(datetimeObject_after,range(len(datetimeObject_after)),'-',ms=1)
		# plt.savefig('filefiller_log%s.png' % datetime.today().strftime('%Y%m%d_%H%M%S'))
		# plt.close()
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
'''
directory = 'C:/home/python/SAtraceTestSpace/160813/rawdata/trace/'
filecheck(directory)
