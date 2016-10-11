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




### sed
    rootcall_rewriter.plの代わりに、gpファイルの引数(ARG1,ARG2,ARG3)を日付と出力先に書き換える

    ```
    `sed -e s/<<foo>>/<<bar>>/g <<infile.txt>> ><<outfile.txt>>`
    sed     -e sedを使うときのおまじない
    s/<<foo>>/<<bar>>/g    fooというすべての文字列をbarにかえる
    <<infile.txt>> ><<outfile.txt>>    infile.txtを上記のようなルールで置換してoutfile.txtに出力する
    sed コマンドを1ファイルに対して連続処理するときはセミコロンで区切り、最初と最後にクォーテーションを入れる
    ```





__UPDATE1.2__
* paramert.jsonからパラメータを引いてくる(param['inn'], param['out'] )
* 文法をPEP8に準拠
日付のイテレーションをユーザーモジュール`datemaster.dateiter()`から`pandas.date_range()`に変更

__UPDATE1.1__
* dateのチェック関数`dateinput(comment)`追加
    * 基本はinputコマンド
    6文字の数字かつ日付に変換できるstr形式が入力されるまで無限ループで入力を施して* くる
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









## filefiller.py v1.0


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







## 他人の環境内で実行
言語はpython,gnuplot, awk, sedのみを使用する\
anaconda, gnuplotをインスコすれば使えるようにする\
py2exe使えばpythonのインスコもいらない？？？\





# perlによるfilefiller.plをpythonで行う
## 理由
時間の関数がデフォルトで入っているので、grepしたファイル名から抜けている時間を推測できる

