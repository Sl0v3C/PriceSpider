@if exist %windir%\SysWOW64 ( @copy A64\geckodriver.exe %windir%\SysWOW64\ & @copy A64\IEDriverServer.exe %windir%\SysWOW64\ & @copy A64\chromedriver.exe %SYSTEMROOT%\SYSTEM32\
) else ( @copy X86\geckodriver.exe %SYSTEMROOT%\SYSTEM32\ & @copy X86\IEDriverServer.exe %SYSTEMROOT%\SYSTEM32\ & @copy X86\chromedriver.exe %SYSTEMROOT%\SYSTEM32\ )
process.exe

pause
