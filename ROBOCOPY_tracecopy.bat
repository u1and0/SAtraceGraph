::-----------------------------------------------------------------------
::# ROBOCOPY_tracecopy.bat ver1.2
::# <<���ȏЉ�>>
::�T�[�o�[��̃~���[�����O�t�H���_����w��t�H���_��
::�w�肳�ꂽ���t�^�C���X�^���v���������f�[�^���R�s�[����
::# <<�g����>>
::when �R�s�[���s���ŏ��̓��t
::whenlast �R�s�[���s���Ō�̓��t
::ttle �^�C�g��
::out1 gif��png�̏o�͐�f�B���N�g��(�p�X�̓o�b�N�X���b�V��)
::<<UPDATE1.2>>
::�\�[�X�f�B���N�g�����O���t�@�C������w��
::	set Source_directory=%5
::<<UPDATE1.1>>
::Copy_options��/XO��ǉ�����
::/XO �R�s�[���ƃR�s�[����r���ăR�s�[�����Â��ꍇ�A���̃t�@�C�������O���܂�
::# <<�����\��>>
::�Ȃ�
::-----------------------------------------------------------------------
@echo off
set when=%1
set whenlast=%2
set ttle=%3
set out1=%4
::-----------------------------------DIRECTRY------------------------------------
::�R�s�[��(�f�[�^�t�@�C���̃��[�g�f�B���N�g��)
set Source_directory=%5
::�R�s�[��(�o�̓f�B���N�g��)
set Destination_directory=%out1%%ttle%\rawdata\trace
	::���O�f�B���N�g��
	::set Log_directory=./hogehogefoobar


::-----------------------------------OPTIONS------------------------------------
::n���O�̃f�[�^�͖���
	set Olddata=20%when%
	set Newdata=20%whenlast%
::���g���C�񐔁A����
	set Retrycount=1
	set Retrytime=1




set Copy_options=/MIR /MAXAGE:%Olddata% /MINAGE:%Newdata% /XO /XX
	::/(MAX|MIN)AGE:n �w�肵�������܂��͓��t���(�Â�|�V����)�X�V�����̃t�@�C�����R�s�[���ɂ���ꍇ�A���������O���܂��Bn �ɂ͉ߋ��ɂ����̂ڂ�����A�܂��͎��ۂ̓��t���uYYYYMMDD�v�̌`���Ŏw�肵�܂�
	::/MIR �~���[�����O(�R�s�[���ƃR�s�[��̃t�@�C�����ƃf�[�^�𓯂���Ԃɂ���)���s���܂��B
	::/XO �R�s�[���ƃR�s�[����r���ăR�s�[�����Â��ꍇ�A���̃t�@�C�������O���܂�
	::/XX �R�s�[��ɂ̂ݑ��݂���t�@�C����f�B���N�g�������O�ΏۂƂ��܂�(eXclude eXtra files and directories)�B/PURGE �ƂƂ��Ɏw�肳��Ă���� /PURGE �̌��ʂ��قڎ����܂��B
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
