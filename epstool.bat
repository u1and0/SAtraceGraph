::## epstool.bat ver1.0
::
::__UPDATE1.0__
::First commit
::
::__USAGE__
::引数%1は作業ディレクトリ
::%2は日付
::
::__INTRODUCTION__
::epstoolでepsファイルのトリミング
::
::__ACTION__
::サーバー上のディレクトリをマウントpushdでマウント
::allplt_wtf<日付>.eps,allplt_wtfMAX<日付>.epsというファイルの余白を取り除く
::fix_<仮のファイル名>としてから`move`コマンドでfix_<仮のファイル名>を消す
::
::
::__TODO__
::None



pushd %1
epstool --copy --bbox allplt_wtf%2.eps fix_allplt_wtf%2.eps
move /y fix_allplt_wtf%2.eps allplt_wtf%2.eps
epstool --copy --bbox allplt_wtfMAX%2.eps fix_allplt_wtfMAX%2.eps
move /y fix_allplt_wtfMAX%2.eps allplt_wtfMAX%2.eps
popd