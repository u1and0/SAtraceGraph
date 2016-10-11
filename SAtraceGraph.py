'''
## main.py ver1.2

__USAGE__
* 引数:ユーザー入力
    * 最初の日付:yymmdd形式
    * 最後の日付:yymmdd形式
* 戻り値:
    * pngif<日付>.html
    * allplt_wtf<日付>.eps
    * allplt_wtf<日付>.png
    * allplt_wtfMAX<日付>.eps
    * mat<日付>.png
    * mlt2time<日付>.pdf
    * mlt2time<日付>.png
    * waterfall_spectrum<日付>.gif
    * codeディレクトリ
        * allplt_wtf.gp
        * allplt_wtf<日付>.svg
        * allplt_wtfMAX.gp
        * directry_setting.gp
        * gp_image_01.png
        * mat<日付>.svg
        * mat1d.plt
        * mlt2row_time_power.gp
        * mlt2time<日付>.svg
        * name_caller.plt
        * output.gp
        * substr.gp
        * waterfall_spectrum.gp
        * waterfall_spectrum_plotter.gp
        * wtrspc_caller.plt
        * wtrspc_plotter.gp
    * rawdataディレクトリ
        * plot_matrix_data.txt
        * plot_matrix_dataMAX.txt
        * plot_rixmat_data.txt
        * plot_rixmat_dataMAX.txt
        * traceディレクトリ
            * <yyyymmdd_HHMMSS>.txtが288個

まとめはpngif<日付>.html
プレビューはmat<日付>.png

1. Windowsマシンでの使用を想定。
2. コマンドラインで以下を入力。`SAtraceGraph.bat`の内容は`python SAtraceGraph.py`が書いてあるだけ。

    `python SAtraceGraph.py`

    または

    `SAtraceGraph.bat`

3. 以下のメッセージ返される

    空の入力=>昨日の日付が入力されます
    グラフ化する最初の日付(yymmdd)を入力>>>

4. '>>>'の後に日付をyymmdd形式で入力。例えば2016年10月11日を入力するとき、`161011`を入力する。
5. 以下のような日付の確認メッセージが返され、コードの実行状況が標準出力に表示される。

    Date is 161010
    以下略





__INTRODUCTION__
gnuplot
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





__UPDATE1.2__
paramert.jsonからパラメータを引いてくる(param['inn'], param['out'] )
文法をPEP8に準拠

__UPDATE1.1__
* dateのチェック関数`dateinput(comment)`追加
    * 基本はinputコマンド
    6文字の数字かつ日付に変換できるstr形式が入力されるまで無限ループで入力を施して* くる
* 
* 入力された日付のソート`datesort(*arg)`追加
    * 複数の引数*args(str形式yymmdd型)を
    * 日付フォーマットに直して
    * 日付順にソートし
    * 文字列のリストとして返す
* ゴミコード削除
* 日付入力方式に変更


__UPDATE1.0__
First commit





__TODO__
gnuplotファイルをawkとか使って別のところから引っ張ってきたいなぁ
'''

# __BUILTIN MODULE__________________________
import subprocess as sp
import glob
import os
from datetime import timedelta
import pandas as pd
# __INSTALLED MODULE__________________________
import simplejson
# __USER MODULE__________________________
import filefiller as ff
import datemaster as dm  # 最初と最後の日付(yymmdd形式)を引数に、その間の日付をイテレータとして返す

# __PARAMETER__________________________
with open('parameter.json', 'r') as f:
    param = simplejson.load(f)
out = param['out']  # 出力ディレクトリ
inn = param['inn']  # データソース
source1 = os.getcwd() + '\\'  # このファイルのワーキングディレクトリ
source1 = source1.replace('\\', '/')  # バックスラッシュ、スラッシュ変換

# __DATE DEFINITION__________________________
date1 = dm.dateinput('グラフ化する最初の日付(yymmdd)を入力>>> ')
date2 = dm.dateinput('グラフ化する最後の日付(yymmdd)を入力>>> ')
# [dateFirst, dateLast] = dm.datesort(date1, date2)


# __MAKE GRAPH LOOP__________________________
for i in pd.date_range(date1, date2):
    when = i.strftime('%y%m%d')  # datetime形式をyymmddの文字列に変える
    whenlast = (i + timedelta(1)).strftime('%y%m%d')  # whenの次の日付
    print('Date is %s' % when)
    tracedir = out + when + '/rawdata/trace/'

    print('\n__描画に使用するコードをコピーする__________________________')
    cmd = 'robocopy %s %s%s/code *.plt *.gp /NDL /NFL /NP' % (source1, out, when)
    print(cmd)
    sp.call(cmd, shell=True)

    print('\n__グラフ描画に使うコードを書き換えコピーする__________________________')
    gpfile = ['mat1d.plt',
              'allplt_wtf.gp',
              'allplt_wtfMAX.gp',
              'mlt2row_time_power.gp',
              'waterfall_spectrum.gp'
              ]
    # rootcall_rewriter(gpfile)    #sedによる、引数を日付と出力先に書き換え
    rep = (('ARG1', '\"' + when + '\"'), ('ARG2', '\"' + out + '\"'), ('ARG3', '\"' + when + '\"'))

    for gpfor in gpfile:
        sedcmd = 'sed -e \''
        for repfor in rep:
            sedcmd += 's%%%s%%%s%%g; ' % (repfor[0], repfor[1])
        # sed inputfile and outputfile setting
        sedcmd += '\' %s%s>%s%s/code/%s' % (source1, gpfor, out, when, gpfor)
        print(sedcmd)
        # yield sedcmd
        sp.call(sedcmd, shell=True)

    print('\n__生データをコピーする__________________________ ')
    cmd = 'ROBOCOPY_tracecopy.bat %s %s %s %s %s' % (when, whenlast, when, out, inn)
    print(cmd)
    sp.call(cmd, shell=True)

    print('\n__データ数を288個にする__________________________ ')
    filenum = len(glob.glob(tracedir + '*.txt'))
    print('グラフ化対象のファイル数 %d個' % filenum)
    if not filenum == 288:
        ff.filecheck(tracedir)  # ファイル名から時刻差分をとってダミーファイルの作成、リネームしてくれる
        # たまに289ファイルになっちゃう
    else:
        print('ファイルは%d個あるので処理を続行します。' % filenum)

    print('\n__マトリックスデータを作成する__________________________ ')
    plcmd = [('matrix_dBm.pl', 'plot_matrix_data.txt'),
             ('matrix_dBmMAX.pl', 'plot_matrix_dataMAX.txt')]
    for i in plcmd:
        plex = 'perl -w ' + i[0]
        plex += ' %s%s/rawdata/trace/ %s%s/rawdata/' % (out, when, out, when)
        plex += i[1]
        print(plex)
        os.system(plex)

    print('\n__マトリックスデータの行列入れ替え版を作成する__________________________ ')
    plin = [('plot_matrix_data.txt', 'plot_rixmat_data.txt'),
            ('plot_matrix_dataMAX.txt', 'plot_rixmat_dataMAX.txt')]
    for i in plin:
        plex = 'perl rowcolumn_changer.pl \
        %s%s/rawdata/%s > %s%s/rawdata/%s' \
        % (out, when, i[0], out, when, i[1])
        print(plex)
        os.system(plex)

    print('\n__gnuplotによるグラフ描画__________________________')
    gpcmd = ['mat1d.plt',
             'allplt_wtf.gp',
             'allplt_wtfMAX.gp',
             'mlt2row_time_power.gp',
             'waterfall_spectrum.gp']
    for i in gpcmd:
        gpex = 'call gnuplot -p -e "load \'%s%s/code/' % (out, when) + i + '\'"'
        print(gpex)
        sp.call(gpex, shell=True)

    print('\n__epsファイルの余白をカットする__________________________ ')
    out2 = out.replace('/', '\\')
    cmd = 'epstool.bat %s%s %s' % (out2, when, when)
    print(cmd)
    sp.call(cmd, shell=True)

    print('\n__pngif.htmlの中身のタイトル、ファイル名を変えてコピー__________________________')
    rep = [('_' * 5 + 'title' + '_' * 5, when),
           ('_' * 5 + 'date' + '_' * 5, when),
           ('_' * 5 + 'outdrct' + '_' * 5, out + when)]
    sedcmd = 'sed -e \''
    for i in rep:
        sedcmd += 's%%%s%%%s%%g;' % (i[0], i[1])  # 置き換える文字列
    sedcmd += '\' %spngif.html>%s%s/pngif%s.html' % (source1, out, when, when)  # 入力ファイル名>出力ファイル名
    print(sedcmd)
    sp.call(sedcmd, shell=True)
