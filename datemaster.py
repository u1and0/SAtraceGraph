'''
## dateiter ver1.1

__USAGE__
ジェネレータ式に引数date1, date2(ともに文字列yymmdd形式の日付)を入れる
戻り値 イテレータとしてdatetime形式ddate1が返される

__INTRODUCTION__
date1からdate2の日付を一日ずつイテレータで出力

__ACTION__
1. date2がNoneであればdate1と同じにする
2. 引数をdatetime形式に変換
3. ddate1, ddate2の大きさ検証(小→大の順番になっているか)、ddate1がddate2と同じになるまで以下を実行
    3.1. datetime形式のddate1をyeild
    3.2. ddate1に1日足す

__UPDATE1.1__
* yyyymmdd形式で返す
> pandas.date_rangeで使用したいので
* datesortは御役御免

__UPDATE1.0__
First commit



__TODO__
None
'''
import datetime
d = datetime


def dateiter(date1, date2):
    '''date1からdate2の日付を一日ずつイテレータで出力'''
    if not date2:
        date2 = date1
    ddate1 = d.datetime.strptime(date1, '%y%m%d')  # 文字列をdatetimeに変換
    ddate2 = d.datetime.strptime(date2, '%y%m%d')
    while ddate1 <= ddate2:
        try:
            yield ddate1
            ddate1 += d.timedelta(1)  # ddate1の次の日
        except ValueError:
            print('Oops!  That was no valid number.  Try again...')


'''TEST
# 実行するとdate1, date2の入力施される
# 出てきたdatetimeフォーマットをstrftimeで文字列にする
date1=input('date1>>>')
date2=input('date2>>>')

for i in datelist(date1,date2):
    when=i.strftime('%y%m%d')
    print(when)
'''


def dateinput(comment):
    '''
    引数:
        comment: input時に表示する文字列
    戻り値:
        x: yyyymmdd形式の日付(文字列型)
    欲しい値のチェック
    日付6桁(yymmdd形式)が入力されるまで無限ループ'''
    while True:
        x = input('空の入力=>昨日の日付が入力されます\n' + comment)
        if not x:  # 入力がNoneであれば昨日の日付を返す
            x = d.date.today() - d.timedelta(1)
            x = x.strftime('%Y%m%d')
            break
        elif len(x) == 6 and x.isdigit():
            try:  # 時間として扱える文字列であればbreak
                x = d.datetime.strptime(x, '%y%m%d').strftime(
                    '%Y%m%d')  # 引数として受け取った文字列をdatetime文字列→文字列に変換して確かめる
                break
            except:  # 時間として扱えなかったらbreakしないでもう一回ループ
                pass
    return x


'''TEST
print(check('頼むから日付を入力してくれ>>>'))
'''


def datesort(*arg):
    '''
    複数の引数*args(str形式yymmdd型)を
    日付フォーマットに直して
    日付順にソートし
    文字列のリストとして返す
    '''
    a = sorted([d.datetime.strptime(i, '%y%m%d') for i in arg])  # datetimeにフォーマットなおして日付順に並べる
    b = [i.strftime('%y%m%d') for i in a]  # 文字列に直して返す
    return b


'''
TEST
a=str(dateinput('first>>>'))
b=str(dateinput('last>>>'))
print(datesort(a,b))
'''
