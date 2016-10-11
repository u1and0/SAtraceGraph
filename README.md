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



__UPDATE v1.2__

* パラメータをjsonファイルから読み込む
> parameter.json
* PEP8に準拠


__UPDATE v1.0__

First commit



__TODO__

* count_file
	* filefiller resultからファイル数カウント？DUMMYファイルの数後から数えるか？
* SAtraceGraphのpngだけを1フォルダにおきたい
* SAtraceGraphを他の人にも使わせたい
	* perl環境のインスコをやらせたくない
	* perlスクリプトをpythonで書く
		* matrix_dBm.py
		* rowcolumn_changer.py
	* epstoolのインスコもやらせたくない




## 他人の環境内で実行
言語はpython,gnuplot, awk, sedのみを使用する\
anaconda, gnuplotをインスコすれば使えるようにする\
py2exe使えばpythonのインスコもいらない？？？\





# perlによるfilefiller.plをpythonで行う
## 理由
時間の関数がデフォルトで入っているので、grepしたファイル名から抜けている時間を推測できる

