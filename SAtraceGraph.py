'''
## main.py ver1.2

__UPDATE1.2__
dateのチェック関数`dateinput(comment)`追加
	基本はinputコマンド
	6文字の数字　かつ　日付に変換できる　str形式が入力されるまで無限ループで入力を施してくる

入力された日付のソート`datesort(*arg)`追加
	複数の引数*args(str形式yymmdd型)を
	日付フォーマットに直して
	日付順にソートし
	文字列のリストとして返す


__UPDATE1.1__
ゴミコード削除
日付入力方式に変更


__UPDATE1.0__
First commit

__USAGE__
Just build

__INTRODUCTION__
日付の入力(yymmdd形式)
 ~~ワイルドカード可能~~ 
 ~~例えば2016/06/01から2016/06/10をグラフ化したいのであれば~~ 
 ~~*1606[0[1-9]]*~~ 

__ACTION__
* 関数の定義
	 ~~* ディレクトリ作成(sh)~~ ←robocopyでやってくれる
	~~* コードの書き換えコピー(perl)~~ ←sedで書く方が簡単便利
	* コードの書き換えコピー(sed)
	* 生データコピー(robocopy)
	* データ数を288個にする ~~(perl)~~ (python)
	* マトリックスデータの作成(perl)
	* 転置行列の作製(perl)
	* グラフの描画(gnuplot)
	* epsファイルの余白をカットする(epstool)
	* htmlの作成(perl)
* gnuplotの制御
* グラフ化する日付としてwhenを入力する(yymmdd形式)
* robocopyコマンドで必要なディレクトリを作成する
* ディレクトリの作成からgnuplotの呼び出し、htmlファイルの生成まで、このバッチ一つで1日のプレビューを作成してくれる
* perlによるファイル操作やgnuplotによるグラフ描画スクリプトを組織する親スクリプト




# sed
	rootcall_rewriter.plの代わりに、gpファイルの引数(ARG1,ARG2,ARG3)を日付と出力先に書き換える

	```
	`sed -e s/<<foo>>/<<bar>>/g <<infile.txt>> ><<outfile.txt>>`
	sed     -e sedを使うときのおまじない
	s/<<foo>>/<<bar>>/g    fooというすべての文字列をbarにかえる
	<<infile.txt>> ><<outfile.txt>>    infile.txtを上記のようなルールで置換してoutfile.txtに出力する
	sed コマンドを1ファイルに対して連続処理するときはセミコロンで区切り、最初と最後にクォーテーションを入れる
	```


__TODO__
gnuplotファイルをawkとか使って別のところから引っ張ってきたいなぁ



'''




## __USER MODULE__________________________
# import sys
# sys.path.append('./filefiller')  #importできるディレクトリ追加
import filefiller as ff

import param
param=param.param()
out1=param['out1']    #出力ディレクトリ
in1=param['in1']    #データソース



## __BUILTIN MODULE__________________________
import glob
import os
source1=os.getcwd()+'\\'    #このファイルのワーキングディレクトリ
source1=source1.replace('\\','/')    #バックスラッシュ、スラッシュ変換



'''
__DATE DEFINITION__________________________
日付の指定
yymmdd形式をmain.batに渡す
'''

import datemaster as dm   #最初と最後の日付(yymmdd形式)を引数に、その間の日付をイテレータとして返す
date1=dm.dateinput('グラフ化する最初の日付を入力>>> ')
date2=dm.dateinput('グラフ化する最後の日付を入力>>> ')
[dateFirst,dateLast]=dm.datesort(date1,date2)

import datetime
d=datetime


for i in dm.dateiter(dateFirst, dateLast):
	when=i.strftime('%y%m%d')
	whenlast=(i+d.timedelta(1)).strftime('%y%m%d')  #whenの次の日付
	print('Date is %s'% when)
	tracedir=out1+when+'/rawdata/trace/'



	print('\n__描画に使用するコードをコピーする__________________________')
	cmd='robocopy %s %s%s/code *.plt *.gp /NDL /NFL /NP'% (source1,out1,when)
	print(cmd)
	import subprocess as sp
	sp.call(cmd,shell=True)





	print('\n__グラフ描画に使うコードを書き換えコピーする__________________________')
	gpfile=['mat1d.plt',
		'allplt_wtf.gp',
		'allplt_wtfMAX.gp',
		'mlt2row_time_power.gp',
		'waterfall_spectrum.gp'
		]
	# rootcall_rewriter(gpfile)    #sedによる、引数を日付と出力先に書き換え
	rep=(('ARG1','\"'+when+'\"'),('ARG2','\"'+out1+'\"'),('ARG3','\"'+when+'\"'))


	for gpfor in gpfile:
		sedcmd='sed -e \''
		for repfor in rep:
			sedcmd+='s%%%s%%%s%%g; '% (repfor[0],repfor[1])
		sedcmd+='\' %s%s>%s%s/code/%s'% (source1,gpfor,out1,when,gpfor)    #sed inputfile and outputfile setting
		print(sedcmd)
		# yield sedcmd
		sp.call(sedcmd,shell=True)






	print('\n__生データをコピーする__________________________ ')
	cmd='ROBOCOPY_tracecopy.bat %s %s %s %s %s'%(when, whenlast,when,out1,in1)
	print(cmd)
	sp.call(cmd,shell=True)




	print('\n__データ数を288個にする__________________________ ')
	filenum=len(glob.glob(tracedir+'*.txt'))
	print('グラフ化対象のファイル数 %d個' %filenum)
	if not filenum==288:
		ff.filecheck(tracedir)   #ファイル名から時刻差分をとってダミーファイルの作成、リネームしてくれる
					   #たまに289ファイルになっちゃう
	else:print('ファイルは%d個あるので処理を続行します。' %filenum)


	print('\n__マトリックスデータを作成する__________________________ ')
	plcmd=[('matrix_dBm.pl','plot_matrix_data.txt'),('matrix_dBmMAX.pl','plot_matrix_dataMAX.txt')]
	for i in plcmd:
		plex='perl -w '+i[0]
		plex+=' %s%s/rawdata/trace/ %s%s/rawdata/'%(out1,when,out1,when)
		plex+=i[1]
		print(plex)
		os.system(plex)





	print('\n__マトリックスデータの行列入れ替え版を作成する__________________________ ')
	plin=[('plot_matrix_data.txt','plot_rixmat_data.txt'),('plot_matrix_dataMAX.txt','plot_rixmat_dataMAX.txt')]
	for i in plin:
		plex='perl rowcolumn_changer.pl %s%s/rawdata/%s > %s%s/rawdata/%s'%(out1,when,i[0],out1,when,i[1])
		print(plex)
		os.system(plex)




	print('\n__gnuplotによるグラフ描画__________________________')
	gpcmd=['mat1d.plt',
		'allplt_wtf.gp',
		'allplt_wtfMAX.gp',
		'mlt2row_time_power.gp',
		'waterfall_spectrum.gp']
	for i in gpcmd:
		gpex='call gnuplot -p -e "load \'%s%s/code/'%(out1,when)+i+'\'"'
		print(gpex)
		sp.call(gpex,shell=True)




	print('\n__epsファイルの余白をカットする__________________________ ')
	out2=out1.replace('/','\\')
	cmd='epstool.bat %s%s %s'%(out2,when,when)
	print(cmd)
	sp.call(cmd,shell=True)






	print('\n__pngif.htmlの中身のタイトル、ファイル名を変えてコピー__________________________')
	rep=[('_'*5+'title'+'_'*5,when),('_'*5+'date'+'_'*5,when),('_'*5+'outdrct'+'_'*5,out1+when)]
	sedcmd='sed -e \''
	for i in rep:
		sedcmd+='s%%%s%%%s%%g;'%(i[0],i[1])    #置き換える文字列
	sedcmd+='\' %spngif.html>%s%s/pngif%s.html'% (source1,out1,when,when)    #入力ファイル名>出力ファイル名
	print(sedcmd)
	sp.call(sedcmd,shell=True)
