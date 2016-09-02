::-----------------------------------------------------------------------
::# ROBOCOPY_tracecopy.bat ver1.3
::# <<自己紹介>>
::サーバー上のミラーリングフォルダから指定フォルダへ
::指定された日付タイムスタンプがついた生データをコピーする
::# <<使い方>>
::when コピーを行う最初の日付
::whenlast コピーを行う最後の日付
::ttle タイトル
::out1 gifやpngの出力先ディレクトリ(パスはバックスラッシュ)
::<<UPDATE1.3>>
::/MIN:40000:40kB未満のファイルはコピーしない
::<<UPDATE1.2>>
::ソースディレクトリも外部ファイルから指定
::	set Source_directory=%5
::<<UPDATE1.1>>
::Copy_optionsに/XOを追加した
::/XO コピー元とコピー先を比較してコピー元が古い場合、そのファイルを除外します
::# <<改造予定>>
::なし
::-----------------------------------------------------------------------
@echo off
set when=%1
set whenlast=%2
set ttle=%3
set out1=%4
::-----------------------------------DIRECTRY------------------------------------
::コピー元(データファイルのルートディレクトリ)
set Source_directory=%5
::コピー先(出力ディレクトリ)
set Destination_directory=%out1%%ttle%\rawdata\trace
	::ログディレクトリ
	::set Log_directory=./hogehogefoobar


::-----------------------------------OPTIONS------------------------------------
::n日前のデータは無視
	set Olddata=20%when%
	set Newdata=20%whenlast%
::リトライ回数、時間
	set Retrycount=1
	set Retrytime=1




set Copy_options=/MIR /MAXAGE:%Olddata% /MINAGE:%Newdata% /XO /XX /MIN:40000
	::/(MAX|MIN)AGE:n 指定した日数または日付より(古い|新しい)更新日時のファイルがコピー元にある場合、それらを除外します。n には過去にさかのぼる日数、または実際の日付を「YYYYMMDD」の形式で指定します
	::/MIR ミラーリング(コピー元とコピー先のファイル数とデータを同じ状態にする)を行います。
	::/XO コピー元とコピー先を比較してコピー元が古い場合、そのファイルを除外します
	::/XX コピー先にのみ存在するファイルやディレクトリを除外対象とします(eXclude eXtra files and directories)。/PURGE とともに指定されていると /PURGE の効果がほぼ失われます。
set Retry_options=/R:%Retrycount% /W:%Retrytime%
::-----------------------------------SET TIME------------------------------------
::	set YYYYMMDD=%date:~0,4%%date:~5,2%%date:~8,2%
::	set Time_edit=%time: =0%
::	set HHMMSS=%Time_edit:~0,2%%Time_edit:~3,2%%Time_edit:~6,2%
::	set Log_file="%Log_directory%\ROBOLOG_%YYYYMMDD%_%HHMMSS%.log"
::set Logging_options=/NFL /NDL /NP /TEE /LOG:%Log_file%
::set Error_options="& if errorlevel 8 goto error"


::-----------------------------------Auto made command------------------------------------
set SSource="%Source_directory%"
set Destination="%Destination_directory%"
set Options=%Copy_options% %Retry_options%
::%Logging_options%
::%Error_options%


	rem _________________________EXCUTE COPY__________________________
ROBOCOPY %SSource% %Destination% %Options%
