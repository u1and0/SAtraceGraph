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
import glob
from itertools import *
from more_itertools import *
from datetime import datetime, timedelta
import time
import matplotlib.dates as pltd




def globfile(directory,extention):
	'''
	ディレクトリを引数に
	%Y%m%d_%H%M%S形式のファイルベースネーム返す
	'''
	fullpath=glob.glob(directory+'*'+extention)   #ファイル名をリストに格納

	filename_without_extention=[i[len(directory):-1*len(extention)] for i in fullpath]   #ファイルベースネーム

	datetimeObject=[datetime.strptime(i,'%Y%m%d_%H%M%S') for i in filename_without_extention]   #要素がdatetime形式のリスト作成

	return datetimeObject


def makefile(fullpath):
	'''ダミーデータ書き込む'''
	with open(fullpath,mode='w') as f:
		c='# <This is DUMMY DATA made by %s>\n'% version
		for i in range(1001):
			c+=str(i).rjust(6)+('-1000.00'.rjust(11))*3+'\n'
		c+='# <eof>\n'
		f.write(c)



def makeMiddlePoint(li,delta):
	'''
	引数:
		li:リスト
		delta:datetime
	戻り値：twoの間に入れる値をyield
	'''
	for two in list(pairwise(li)):   #liの中身を2つずつにわける
		if two[-1]-two[0]>=delta +timedelta(minutes=1):   #抜き出したタプルの要素の差がdelta上であれば
			print('\nLack between %s and %s'% (two[0],two[1]))
			print('Substract',abs(two[0]-two[1]))
			for i in pltd.drange(two[0]+delta,two[-1],delta):
				li.insert(li.index(two[-1]),pltd.num2date(i))   #タプルの要素間の場所にdeltaずつ増やした値を入れる
				print('insert',pltd.num2date(i))
				yield pltd.num2date(i).strftime('%Y%m%d_%H%M%S')
	print('\nThere is No point to insert')
	print('makeMiddlePoint END\n')






'''try-except-else　で条件に見合うまでfor文に戻ろうと思ったやつ'''
# def makeMiddlePoint(li,delta):
# 	'''
# 	引数:
# 		li:リスト
# 		delta:datetime
# 	戻り値：twoの間に入れる値をyield
# 	'''
# 	# flag=True
# 	while True:
# 		try:
# 			for two in list(pairwise(li)):   #liの中身を2つずつにわけて差分を調べる
# 				if two[-1]-two[0]>=delta +timedelta(minutes=1):   #抜き出したタプルの要素の差がdelta以上であれば
# 					print('\nLack between %s and %s'% (two[0],two[1]))
# 					print('Substract',abs(two[0]-two[1]))
# 					for i in pltd.drange(two[0]+delta,two[-1],delta):
# 						li.insert(li.index(two[-1]),pltd.num2date(i))   #タプルの要素間の場所にdeltaずつ増やした値を入れる
# 						print('insert',pltd.num2date(i))

# 						# print(li)

# 						yield pltd.num2date(i).strftime('%Y%m%d_%H%M%S')   #insertした値を外に渡して
# 						raise   #yieldしたらもう一度pairwiseにもどる
# 		except:
# 			print('TryAgain')
# 			# pass
# 		else:   #一度もraiseがでない(差分がdelta以上にならない)ければ
# 			# flag=False   #flagをFalseにしてwhile True抜ける
# 			print('\nThere is No point to insert')
# 			print('makeMiddlePoint END\n')
# 			break   #if節に一度も引っかからなければflagをFalseにしてwhileから抜ける
















def makeStartPoint(li):
	'''始点要素の作製'''
	while True :
		start=li[0]   #始点を探す
		if start.hour==0 and 0<=start.minute<5:   #始点の条件クリアでループ終了
			print('\nFirst element is',start)
			print('makeStartPoint END\n')
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
			print('makeStopPoint END\n')
			break
		li.append(stop+timedelta(minutes=5))   #リストの最初に5分前の値をリストに格納
		print('Appended',li[-1])
		yield li[-1].strftime('%Y%m%d_%H%M%S')



# __MAIN__________________________

def filefiller(directory,extention='.txt'):
	'''
	file数を288まで増やす
	makeMiddlePoint:間の穴あき埋める
	makeStartPoint:最初の要素から00:00に向けて5分間隔でデータ作る
	makeStopPoint:最後の要素から23:59に向けて5分間隔でデータ作る
	'''
	datetimeObject=globfile(directory,extention)
	print('\n',directory,'内のファイル数を調整します','\n')
	print('Before:Number of Files is',len(datetimeObject))   #Check number of files
	print('-'*20)
	for i in makeMiddlePoint(datetimeObject,timedelta(minutes=5)):   #5分間隔でデータを挿入
		makefile(directory+i+extention)
	print('-'*20)
	for i in makeStartPoint(datetimeObject):   #始点を作製
		makefile(directory+i+extention)
	print('-'*20)
	for i in makeStopPoint(datetimeObject):   #終点を作製
		makefile(directory+i+extention)
	print('-'*20)


def filecheck(directory):
	'''
	ファイル数288 => 何もせずfilefiller.py終了
	ファイル数288未満 => filefillerで288になるまで穴埋め
	ファイル数288より多い => エラー吐き出して処理中断
	'''
	filenum=288
	while not len(glob.glob(directory+'*'+'.txt'))==filenum:   #globして288個ならココは実行しない
		try:
			if len(glob.glob(directory+'*'+'.txt'))>filenum:
				raise ValueError
		except ValueError:
			print('ファイル数が%d個以上！処理を中断します。'% filenum)
			print('生データを編集して、"%s/code"内にあるgpファイルを手動で動かしてください。'% out1+when)
		else:
			if len(glob.glob(directory+'*'+'.txt'))<filenum:
				filefiller(directory)
	else:
		print('After:Number of Files is',len(globfile(directory,extention='.txt')))   #Check number of files
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



