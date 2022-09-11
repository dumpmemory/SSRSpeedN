@echo off&
set bin=%~dp0
for %%a in ("%bin:~0,-1%") do set SSRSpeed=%%~dpa
set PYTHONPATH=%SSRSpeed%;%PYTHONPATH%
cd %SSRSpeed%
echo.
echo ================== SSRSpeedN ==================
if exist "%SSRSpeed%\venv\Scripts\activate.bat" ( call "%SSRSpeed%\venv\Scripts\activate.bat" )
if defined VIRTUAL_ENV ( echo 当前环境 %VIRTUAL_ENV% ) else ( echo 当前目录 %SSRSpeed% )
if exist "%SystemRoot%\SysWOW64" path %path%;%windir%\SysNative;%SystemRoot%\SysWOW64;%SSRSpeed%
bcdedit >nul
if '%errorlevel%' NEQ '0' ( echo 当前权限 普通用户 ) else ( echo 当前权限 管理员 )
if exist "%SSRSpeed%\resources\clients\v2ray-core\v2ray.exe" ( set v1=1 ) else ( set v1=0 )
if exist "%SSRSpeed%\resources\clients\v2ray-core\v2ctl.exe" ( set v2=1 ) else ( set v2=0 )
set /a v3=v1+v2
if %v3%==2 ( echo 已经安装 V2ray-core ) else ( echo 尚未安装 V2ray-core )
:start
echo ===============================================
echo [1] 开始测速（自定义设置）
echo [2] 首次运行安装 pip 和相关支持（需管理员权限）
echo [3] 参数查阅
echo [4] 当前 SSRSpeed 版本
echo [5] 为本次运行获取管理员权限
echo ===============================================
echo 请选择 [1-5]: 
choice /c 12345
if %errorlevel%==5 ( goto :uac )
if %errorlevel%==4 ( goto :ver )
if %errorlevel%==3 ( goto :help )
if %errorlevel%==2 ( goto :pip )
if %errorlevel%==1 ( goto :test2 )


:pip
if exist "%SystemRoot%\SysWOW64" path %path%;%windir%\SysNative;%SystemRoot%\SysWOW64;%SSRSpeed%
bcdedit >nul
if '%errorlevel%' NEQ '0' ( echo X 当前无管理员权限，无法安装。 && echo. && echo * 您可以通过命令 5 获取权限，或右键以管理员权限启动。 && pause && goto :start ) else ( goto :pip2 )
:pip2
python -m pip install --upgrade pip
pip3 install -r "%SSRSpeed%\requirements.txt"
:: pip3 install aiofiles
:: pip3 install aiohttp-socks
:: pip3 install beautifulsoup4
:: pip3 install Flask-Cors
:: pip3 install geoip2
:: pip3 install loguru
:: pip3 install Pillow
:: pip3 install pynat
:: pip3 install PySocks
:: pip3 install PyYAML
:: pip3 install requests
:: pip3 install selenium
:: pip3 install webdriver-manager
pause
goto :start

:ver
python -m ssrspeed --version
pause
goto :start

:help
echo.
echo [1] 原文（en）
echo [2] 翻译（zh）
choice /c 12
if %errorlevel%==2 ( goto :fy )
if %errorlevel%==1 ( goto :yw )

:yw

echo.
echo usage: ssrspeed [-h] [--version] [-c GUICONFIG] [-u URL] [-m TEST_METHOD]
echo                   [-M TEST_MODE] [--include FILTER [FILTER ...]]
echo                   [--include-remark REMARKS [REMARKS ...]]
echo                   [--include-group GROUP [GROUP ...]]
echo                   [--exclude EFLITER [EFLITER ...]]
echo                   [--exclude-group EGFILTER [EGFILTER ...]]
echo                   [--exclude-remark ERFILTER [ERFILTER ...]] [--use-ssr-cs]
echo                   [-g GROUP_OVERRIDE] [-y] [-C RESULT_COLOR] [-s SORT_METHOD]
echo                   [-i IMPORT_FILE] [--skip-requirements-check] [--debug]
echo                   [--paolu]
echo.
echo Options:
echo.
echo  --version                              show program's version number and exit
echo  -h, --help                             show this help message and exit
echo  -c GUICONFIG, --config=GUICONFIG       Load config generated by shadowsocksr-csharp.
echo  -u URL, --url=URL                      Load ssr config from subscription url.
echo  -m TEST_METHOD, --method=TEST_METHOD   Select test method in in [speedtestnet, fast, socket, stasync].
echo  -M TEST_MODE, --mode=TEST_MODE         Select test mode in [default, pingonly, stream, all, wps].
echo  --include                              Filter nodes by group and remarks using keyword.
echo  --include-remark                       Filter nodes by remarks using keyword.
echo  --include-group                        Filter nodes by group name using keyword.
echo  --exclude                              Exclude nodes by group and remarks using keyword.
echo  --exclude-group                        Exclude nodes by group using keyword.
echo  --exclude-remark                       Exclude nodes by remarks using keyword.
echo  --use-ssr-cs                           Replace the ShadowsocksR-libev with the ShadowsocksR-C# (Only Windows)
echo  -g GROUP                               Manually set group.
echo  -y, --yes                              Skip node list confirmation before test.
echo  -C RESULT_COLOR, --color=RESULT_COLOR  Set the colors when exporting images..
echo  -S SORT_METHOD, --sort=SORT_METHOD     Select sort method in [speed, rspeed, ping, rping], default not sorted.
echo  -i IMPORT_FILE, --import=IMPORT_FILE   Import test result from json file and export it.
echo  --skip-requirements-check              Skip requirements check.
echo  --debug                                Run program in debug mode.
echo.
echo  Test Modes
echo  Mode                 Remark
echo  DEFAULT              Freely configurable via ssrspeed.json
echo  TCP_PING             Only tcp ping, no speed test
echo  STREAM               Only streaming unlock test
echo  ALL                  Full speed test (exclude web page simulation)
echo  WEB_PAGE_SIMULATION  Web page simulation test
echo.
echo  Test Methods
echo  Methods              Remark
echo  ST_ASYNC             Asynchronous download with single thread
echo  SOCKET               Raw socket with multithreading
echo  SPEED_TEST_NET       Speed Test Net speed test
echo  FAST                 Fast.com speed test
echo.
pause
goto :start

:fy

echo.
echo 用法：ssrspeed [-h] [--version] [-c GUICONFIG] [-u URL] [-m TEST_METHOD]
echo                   [-M TEST_MODE] [--include FILTER [FILTER ...]]
echo                   [--include-remark REMARKS [REMARKS ...]]
echo                   [--include-group GROUP [GROUP ...]]
echo                   [--exclude EFLITER [EFLITER ...]]
echo                   [--exclude-group EGFILTER [EGFILTER ...]]
echo                   [--exclude-remark ERFILTER [ERFILTER ...]] [--use-ssr-cs]
echo                   [-g GROUP_OVERRIDE] [-y] [-C RESULT_COLOR] [-s SORT_METHOD]
echo                   [-i IMPORT_FILE] [--skip-requirements-check] [--debug]
echo                   [--paolu]
echo.
echo 选项：
echo.
echo  --version                               显示程序的版本号并退出
echo  -h，--help                              显示此帮助消息并退出
echo  -c GUICONFIG，--config = GUICONFIG      加载由 shadowsocksr-csharp 生成的配置。
echo  -u URL，--url = URL                     从订阅 URL 加载 ssr 配置。
echo  -m TEST_METHOD，--method = TEST_METHOD  在 [speedtestnet, fast, socket, stasync] 中选择测试方法。
echo  -M TEST_MODE，--mode = TEST_MODE        在 [default, pingonly, stream, all, wps] 中选择测试模式。
echo  --include                               按组过滤节点，并使用关键字注释。
echo  --include-remark                        使用关键字通过注释过滤节点。
echo  --include-group                         使用关键字按组名过滤节点。
echo  --exclude                               按组排除节点，并使用关键字进行注释。
echo  --exclude-group                         使用关键字按组排除节点。
echo  --exclude-remark                        通过使用关键字的注释排除节点。
echo  --use-ssr-cs                            用 ShadowsocksR-C＃ 替换 ShadowsocksR-libev（仅 Windows）
echo  -g GROUP                                手动设置组。
echo  -y，--yes                               测试前跳过节点列表确认。
echo  -C RESULT_COLOR，--color = RESULT_COLOR 导出图像时设置颜色。
echo  -S SORT_METHOD，--sort = SORT_METHOD    在 [speed, rspeed, ping, rping] 中选择排序方法，默认不排序。
echo  -i IMPORT_FILE，--import = IMPORT_FILE  从 json 文件导入测试结果并导出。
echo  -skip-requirements-check                跳过要求检查。
echo  --debug                                 在调试模式下运行程序。
echo.
echo  测试模式
echo  模式                 备注
echo  DEFAULT              可以通过 ssrspeed.json 自由配置
echo  TCP_PING             仅 tcp ping，无速度测试
echo  STREAM               仅流媒体解锁测试
echo  ALL                  全速测试（不包括网页模拟）
echo  WEB_PAGE_SIMULATION  网页模拟测试
echo.
echo  测试方法
echo  方法                 备注
echo  ST_ASYNC             单线程异步下载
echo  SOCKET               具有多线程的原始套接字
echo  SPEED_TEST_NET       SpeedTest.Net 速度测试
echo  FAST                 Fast.com 速度测试
echo.
pause
goto :start

:test2
echo.
echo * 以下自定义选项留空回车即可跳过
echo.
:test3
set /p a="请输入您的订阅链接（不可留空）: "
if "%a%"=="" (
goto :test3
) else (
goto :jx1
)
:jx1
echo.
echo * 以下 2 项可以通过空格分隔关键词
echo.
set /p e="1. 使用关键字通过注释筛选节点: "
set /p i="2. 通过使用关键字的注释排除节点: "
set /p k="3. 请输入测速组名: "
set /p m="4. 导出图像时设置颜色 [origin, poor]，默认 origin: "
set /p n="5. 在 [speed, rspeed, ping, rping] 中选择输入排序方法，默认不排序，如默认请跳过: "
echo.
if "%e%"=="" (
set e= && goto :jx1
) else (
set e=--include-remark %e% && goto :jx1
)
:jx1
if "%i%"=="" (
set i= && goto :jx2
) else (
set i=--exclude-remark %i% && goto :jx2
)
:jx2
if "%k%"=="" (
set k= && goto :jx3
) else (
set k=-g %k% && goto :jx3
)
:jx3
set l=-y && goto :jx4
:jx4
if "%m%"=="" (
set m= && goto :jx5
) else (
set m=-C %m% && goto :jx5
)
:jx5
if "%n%"=="" (
set n= && goto :jx6
) else (
set n=-s %n% && goto :jx6
)
:jx6
set o=--skip-requirements-check && goto :jx7
:jx7
echo python -m ssrspeed -u "%a%" %e% %i% %k% %y% %m% %n%  %o%
echo.
python -m ssrspeed -u "%a%" %e% %i% %k% %y% %m% %n%  %o%
pause
set a=
set e=
set i=
set k=
set y=
set m=
set n=
set o=
goto :start

:uac
echo.
if exist "%SystemRoot%\SysWOW64" path %path%;%windir%\SysNative;%SystemRoot%\SysWOW64;%SSRSpeed%
bcdedit >nul
if '%errorlevel%' NEQ '0' ( goto UACPrompt ) else ( goto UACAdmin )
:UACPrompt
echo 提示：通用依赖安装需要管理员权限（命令 4）
echo.
echo       尝试获取管理员权限，程序将重启
ping -n 3 127.0.0.1>nul && %1 start "" mshta vbscript:createobject("shell.application").shellexecute("""%~0""","::",,"runas",1)(window.close)&exit
exit /B
:UACAdmin
cd /d "%SSRSpeed%"
echo.
echo 已获取管理员权限
echo.
pause
goto :start