# SAtraceGraph v1.0

__USAGE__
SAtraceGraph.batを実行、または`python SAtraceGraph.py`をコンソールに打ち込む\
param.pyにデータソースや出力フォルダの指定



__INTRODUCTION__

収集したデータをgnuplotによって可視化する\
pythonで制御



__ACTION__

* 描画に使用するコードをコピーする
* グラフ描画に使うコードを書き換えコピーする
* 生データをコピーする
* データ数を288個にする
* マトリックスデータを作成する
* マトリックスデータの行列入れ替え版を作成する
* gnuplotによるグラフ描画
* epsファイルの余白をカットする
* pngif.htmlの中身のタイトル、ファイル名を変えてコピー



__UPDATE v1.0__

First commit



__TODO__

* SAtraceGraph main.py(動かすのはmain.bat)動くようになった
* mian.pyの役割は、今まで動いていたSAtraceGraph_old のmain.batと、日付をループするrun_main.batの役割を合わせたもの
* SAtraceGraphのgpファイルの一部(外に出したくない情報)はawkで引っ張ってくるなど改良の余地あり
* なぜならgithubにあげられない。開発遅れる
* SAtraceGraphのpngだけを1フォルダにおきたい
* SAtraceGraphを他の人にも使わせたい
	* perl環境のインスコをやらせたくない
	* epstoolのインスコもやらせたくない
* SAtraceGraphは自分の環境内でやるならとりあえず完成



## 他人の環境内で実行
言語はpython,gnuplot, awk, sedのみを使用する\
anaconda, gnuplotをインスコすれば使えるようにする\
py2exe使えばpythonのインスコもいらない？？？\





# perlによるfilefiller.plをpythonで行う
## 理由
時間の関数がデフォルトで入っているので、grepしたファイル名から抜けている時間を推測できる

