=pod
入力されたファイルの行列を入れ替えるpl
スペース2つ以上で区切られているファイルに対応
=cut

while (<>) {
    next unless (/\s{2}/);  #スペース2つ並ばなければ次のループへ進む。並べば以下の処理
    chomp;
    $i = 0;
    @list = split('\s+');   #スペースで区切る
    foreach $a (@list) {
        $b{$i} .= ('  '.$a);  #リスト内の値の頭にスペース二つ並べる
        $i++;
    }
}
	# 1行目が改行から始まっちゃうからjの初期条件を1にした
for ($j = 1; $j < $i; $j++) {   #リスト内の値まで繰り返し
    print $b{$j} . "\n";
}