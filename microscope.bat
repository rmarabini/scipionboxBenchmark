@echo off
set number=0
set source=C:\Users\pitts_2\Downloads\32.mrc
set target=Z:\inbox\20170622_rob_motioncor\GRID_01\DATA

:loop
 if /I "%number%" EQU "100" goto end

 set STARTTIME=%TIME%
 set /a number = %number%+1
 echo movie_%number%
 copy %source% %target%\%number%.mrc
 set ENDTIME=%TIME%
 call:print_time "%STARTTIME%","%ENDTIME%"
 rem write takes 9sec + 9 one movie each 18 secs
 timeout 9
 set STARTTIME=%TIME%
 set /a number = %number%+1
 echo movie_%number%
 copy %source% %target%\%number%.mrc
 set ENDTIME=%TIME%
 call:print_time "%STARTTIME%","%ENDTIME%"
 rem write takes 9sec + 9 one movie each 18 secs
 timeout 9
 set STARTTIME=%TIME%
 set /a number = %number%+1
 echo movie_%number%
 copy %source% %target%\%number%.mrc
 set ENDTIME=%TIME%
 call:print_time "%STARTTIME%","%ENDTIME%"
 rem write takes 9sec + 90 one movie each 100 secs
 timeout 90

goto loop
:end
pause


:print_time

    set STARTTIME2=%~1
    set ENDTIME2=%~2
    rem Change formatting for the start and end times
    for /F "tokens=1-4 delims=:.," %%a in ("%STARTTIME2%") do (
       set /A "start=(((%%a*60)+1%%b %% 100)*60+1%%c %% 100)*100+1%%d %% 100"
    )

    for /F "tokens=1-4 delims=:.," %%a in ("%ENDTIME2%") do (
       set /A "end=(((%%a*60)+1%%b %% 100)*60+1%%c %% 100)*100+1%%d %% 100"
    )

    rem Calculate the elapsed time by subtracting values
    set /A elapsed=end-start

    rem Format the results for output
    set /A hh=elapsed/(60*60*100), rest=elapsed%%(60*60*100), mm=rest/(60*100), rest%%=60*100, ss=rest/100, cc=rest%%100
    if %hh% lss 10 set hh=0%hh%
    if %mm% lss 10 set mm=0%mm%
    if %ss% lss 10 set ss=0%ss%
    if %cc% lss 10 set cc=0%cc%

    set DURATION=%hh%:%mm%:%ss%,%cc%

    echo Start    : %STARTTIME2%
    echo Finish   : %ENDTIME2%
    echo          ---------------
    echo Duration : %DURATION% 

goto:eof
