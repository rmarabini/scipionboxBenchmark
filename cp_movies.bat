set number=0
set source=C:\Users\pitts_2\Downloads\1.mrc
set target=Z:
:loop
 if /I "%number%" EQU "3" goto end
 set /a number = %number%+1
 echo movie_%number%
 copy %source% %target%\%number%.mrc
 timeout 5
goto loop
:end