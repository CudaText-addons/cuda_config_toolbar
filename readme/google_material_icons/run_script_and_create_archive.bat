@echo off

set ArchFile="CT-google-material-icons.7z"
set PdsExe=pdScriptCL.exe
set Script=CT_GMD.dpas

rem /////////////////////////////////////////////
del /s black\*.png
del /s white\*.png
del /s gray\*.png

echo ========================= SCRIPT ==========================
%PdsExe% %Script%




rem /////////////////////////////////////////////
echo ========================= ARCHIVE ==========================
del %ArchFile%

7z.exe a %ArchFile% -mx=9 black\* gray\* white\* *.dpas *.log *.bat *.txt



pause