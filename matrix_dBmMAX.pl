#---------------------------------------------------------------
#		結果ファイル群から、２次元格子データを抽出する	[matrix_dBm.pl]
#---------------------------------------------------------------
=pod

	<< 使用法 >>

>perl matrix_dBm.pl <入力フォルダ名/> <出力ファイル名>			# 入力フォルダ名の最後に '/' を付けること。

//	012345678901234567890123456789012345678		// 39バイト固定長のデータ行
//	     0     -71.12     -72.76     -65.76		// <ポイント番号> <Clear Write> <Trace Average> <Max Hold>
=cut
#---------------------------------------------------------------

	if ( @ARGV != 2 ) { die( "perl matrix_dBm.pl <from_dir/> <to_matrix>\n" ); }

	$from_dir	= $ARGV[0];										# <入力フォルダ名/>
	$to_matrix	= $ARGV[1];										# <出力ファイル名>

	print "from_dir =" . $from_dir  . "\n";
	print "to_matrix=" . $to_matrix . "\n";

	$fnam_pat = $from_dir . "*.txt";							# 検索パターン指定
	@files = glob( $fnam_pat );									# 指定パターンにマッチする全ファイル名を取得し、@配列名に代入する

	$all_cnt = @files;											# 全ファイル数
	print "  ==> ファイル数$all_cnt 個あります\n";

	open( TR, ">" . $to_matrix );								# <出力ファイル名>

	foreach ( @files ) {										# @配列名に含まれる全てのファイルについて、
		$in_fnam = $_;
		open( IN, $in_fnam );

L1:		while (<IN>) {											# すべての行に関して、
			$L = $_;
			if ( $L =~ /^#/ ) {	next L1; }						# コメント行を飛ばす

			$elem = substr( $L, 29, 10 );						# <Trace Max> を抽出する
			printf TR $elem;									# １行に周波数データを並べる
		}

		printf TR "\n";											# １行が完成しました
		close IN;
	}

	close TR;

#	<< プログラム終了 >>

#---------------------------------------------------------------
#		EOF
#---------------------------------------------------------------
