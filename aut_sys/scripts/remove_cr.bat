@ECHO OFF
REM ===========================================================================
REM File        : remove_cr.bat
REM Author      : Jalil Chavez
REM Descirption : Removes cr symbol from all the files that are used in the unix
REM               environment.
REM ===========================================================================

SET DOS2UNIX_CMD=.\dos2unix.exe

SET SCRIPTS_PATH=./
SET SRC_PATH=../src/
SET LNCH_PATH=../launch/

SET EXT_PY=*.py
SET EXT_SH=*.sh
SET EXT_BASH=*.bash
SET EXT_LNCH=*.launch

set CUR_PATH=%SRC_PATH%
set CURR_EXT=%EXT_PY%
echo ======================================================
echo Removing CR from files in %CUR_PATH% folder
echo ======================================================
echo Processing file extension: %CURR_EXT%
%DOS2UNIX_CMD% %CUR_PATH%%CURR_EXT%
IF ERRORLEVEL 1 GOTO :ERROR

set CUR_PATH=%LNCH_PATH%
set CURR_EXT=%EXT_LNCH%
echo ======================================================
echo Removing CR from files in %CUR_PATH% folder
echo ======================================================
echo Processing file extension: %CURR_EXT%
%DOS2UNIX_CMD% %CUR_PATH%%CURR_EXT%

IF ERRORLEVEL 1 GOTO :ERROR

echo Process completed
echo ===============================
EXIT /B %errorlevel%

:ERROR
echo An error occurred,
echo Not able ro remove CR from
echo %CUR_PATH%%CURR_EXT%.
echo ===============================
