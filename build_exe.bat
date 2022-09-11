:: Start
echo Building windows executable ...

@echo off

:: Creates the setup.py file that is used to build the executable
echo .>> setup.py
echo from cx_Freeze import setup, Executable> setup.py
echo from sys import platform>> setup.py
echo, >> setup.py
echo base = None>> setup.py
echo # uncomment below lines to hide command prompt>> setup.py
echo # tqdm prints to command prompt so it needs to be removed for the program to run>> setup.py
echo # Important: if you hide the console, make sure your scripts don't try to print anything, otherwise they might not work as expected>> setup.py
echo Important: if you hide the console, make sure your scripts don't try to print anything, otherwise they might not work as expected!
echo if (platform == "win32"):>> setup.py
echo     base = "Win32GUI">> setup.py
echo, >> setup.py
echo executables = [Executable("EFWA.py", base=base, icon="res/py/ui/Images/althom.ico")]>> setup.py
echo, >> setup.py
echo packages = ["ctypes","imp", "PySide2", "tqdm", "unidecode", "xlsxwriter", "PyPDF4", "pikepdf", "fitz", "pdfrw", "pytz", "colorama", "lxml", "win32com"]>> setup.py
echo excludes = ["PyQt5", "PyQt4", "reportlab", "matplotlib", "numba", "scipy", "sqlalchemy", "sqlite3", "soupsieve", "llvmlite", "black", "bs4", "jupyter", "tornado", "pygments"]>> setup.py
echo options = {>> setup.py
echo     'build_exe': {>> setup.py
echo         'packages': packages,>> setup.py
echo         'excludes': excludes,>> setup.py 
echo     },>> setup.py
echo }>> setup.py
echo setup(>> setup.py
echo     name="<EFW Automation>",>> setup.py
echo     options=options,>> setup.py
echo     version="0.0.2.4",>> setup.py
echo     description='^<EFW Automation is a standalone application for '>> setup.py
echo                 + 'running simple automations for EFW IPC and SRM.'>> setup.py
echo                 + 'Printing, checking etc.^>',>> setup.py
echo     executables=executables>> setup.py
echo     )>> setup.py
echo # Run this to create the exe:>> setup.py
echo # python setup.py build>> setup.py
echo #>> setup.py
echo # Then copy the res folder in the same folder as the .exe>> setup.py

@echo on

:: Runs cmd and waits for finish
call python setup.py build

:: When finished deletes the generated file
del setup.py

:: Create ALTHOM-Publisher folder
if not exist "build\EFW Automation" mkdir "build\EFW Automation"
robocopy "build\exe.win-amd64-3.9" "build\EFW Automation" /E /MOVE

@RD /S /Q "build\EFW Automation\lib\res"
@RD /S /Q "build\EFW Automation\lib\Test"

@RD /S /Q "build\EFW Automation\lib\html"
@RD /S /Q "build\EFW Automation\lib\asyncio"
@RD /S /Q "build\EFW Automation\lib\concurrent"
@RD /S /Q "build\EFW Automation\lib\ctypes"
@RD /S /Q "build\EFW Automation\lib\distutils"
@RD /S /Q "build\EFW Automation\lib\email"
@RD /S /Q "build\EFW Automation\lib\html"
@RD /S /Q "build\EFW Automation\lib\http"
@RD /S /Q "build\EFW Automation\lib\lib2to3"
@RD /S /Q "build\EFW Automation\lib\pydoc_data"
@RD /S /Q "build\EFW Automation\lib\PySide2-5.15.1.dist-info"
@RD /S /Q "build\EFW Automation\lib\shiboken2-5.15.1.dist-info"
@RD /S /Q "build\EFW Automation\lib\QDarkStyle-2.8.1.dist-info"
@RD /S /Q "build\EFW Automation\lib\idna-2.10.dist-info"
@RD /S /Q "build\EFW Automation\lib\lxml-4.5.2.dist-info"
@RD /S /Q "build\EFW Automation\lib\QtPy-1.9.0.dist-info"
@RD /S /Q "build\EFW Automation\lib\unittest"
@RD /S /Q "build\EFW Automation\lib\xmlrpc"
@RD /S /Q "build\EFW Automation\lib\qtpy"

:: PySide2 folder imported with too many files and folders. Deleting unnecessary ones.
del "build\EFW Automation\lib\PySide2\Qt3DExtras.pyd"
del "build\EFW Automation\lib\PySide2\Qt53DExtras.dll"
del "build\EFW Automation\lib\PySide2\Qt5Bluetooth.dll"
del "build\EFW Automation\lib\PySide2\Qt5Multimedia.dll"
del "build\EFW Automation\lib\PySide2\Qt5Quick3D.dll"
del "build\EFW Automation\lib\PySide2\Qt5QuickParticles.dll"
del "build\EFW Automation\lib\PySide2\Qt5RemoteObjects.dll"
del "build\EFW Automation\lib\PySide2\Qt5ScriptTools.dll"
del "build\EFW Automation\lib\PySide2\QtLocation.pyd"
del "build\EFW Automation\lib\PySide2\QtQuick.pyd"
del "build\EFW Automation\lib\PySide2\QtSensors.pyd"
del "build\EFW Automation\lib\PySide2\concrt140.dll"
del "build\EFW Automation\lib\PySide2\libEGL.dll"
del "build\EFW Automation\lib\PySide2\libGLESv2.dll"
del "build\EFW Automation\lib\PySide2\msvcp140_1.dll"
del "build\EFW Automation\lib\PySide2\msvcp140_2.dll"
del "build\EFW Automation\lib\PySide2\msvcp140_codecvt_ids.dll"
del "build\EFW Automation\lib\PySide2\msvcp140.dll"
del "build\EFW Automation\lib\PySide2\py.typed"
del "build\EFW Automation\lib\PySide2\pyside2.abi3.lib"
del "build\EFW Automation\lib\PySide2\qt.conf"
del "build\EFW Automation\lib\PySide2\Qt3DAnimation.pyd"
del "build\EFW Automation\lib\PySide2\Qt3DCore.pyd"
del "build\EFW Automation\lib\PySide2\Qt3DExtras.pyd"
del "build\EFW Automation\lib\PySide2\Qt3DInput.pyd"
del "build\EFW Automation\lib\PySide2\Qt3DLogic.pyd"
del "build\EFW Automation\lib\PySide2\Qt3DRender.pyd"
del "build\EFW Automation\lib\PySide2\Qt53DAnimation.dll"
del "build\EFW Automation\lib\PySide2\Qt53DCore.dll"
del "build\EFW Automation\lib\PySide2\Qt53DExtras.dll"
del "build\EFW Automation\lib\PySide2\Qt53DInput.dll"
del "build\EFW Automation\lib\PySide2\Qt53DLogic.dll"
del "build\EFW Automation\lib\PySide2\Qt53DQuick.dll"
del "build\EFW Automation\lib\PySide2\Qt53DQuickAnimation.dll"
del "build\EFW Automation\lib\PySide2\Qt53DQuickExtras.dll"
del "build\EFW Automation\lib\PySide2\Qt53DQuickInput.dll"
del "build\EFW Automation\lib\PySide2\Qt53DQuickRender.dll"
del "build\EFW Automation\lib\PySide2\Qt53DQuickScene2D.dll"
del "build\EFW Automation\lib\PySide2\Qt5Bluetooth.dll"
del "build\EFW Automation\lib\PySide2\Qt5Bodymovin.dll"
del "build\EFW Automation\lib\PySide2\Qt5Charts.dll"
del "build\EFW Automation\lib\PySide2\Qt5Concurrent.dll"
del "build\EFW Automation\lib\PySide2\Qt5DataVisualization.dll"
del "build\EFW Automation\lib\PySide2\Qt5DBus.dll"
del "build\EFW Automation\lib\PySide2\Qt5Gamepad.dll"
del "build\EFW Automation\lib\PySide2\Qt5Help.dll"
del "build\EFW Automation\lib\PySide2\Qt5Location.dll"
del "build\EFW Automation\lib\PySide2\Qt5Multimedia.dll"
del "build\EFW Automation\lib\PySide2\Qt5MultimediaQuick.dll"
del "build\EFW Automation\lib\PySide2\Qt5MultimediaWidgets.dll"
del "build\EFW Automation\lib\PySide2\Qt5NetworkAuth.dll"
del "build\EFW Automation\lib\PySide2\Qt5Nfc.dll"
del "build\EFW Automation\lib\PySide2\Qt5OpenGL.dll"
del "build\EFW Automation\lib\PySide2\Qt5PdfWidgets.dll"
del "build\EFW Automation\lib\PySide2\Qt5Positioning.dll"
del "build\EFW Automation\lib\PySide2\Qt5PositioningQuick.dll"
del "build\EFW Automation\lib\PySide2\Qt5PrintSupport.dll"
del "build\EFW Automation\lib\PySide2\Qt5Purchasing.dll"
del "build\EFW Automation\lib\PySide2\Qt5QmlModels.dll"
del "build\EFW Automation\lib\PySide2\Qt5QmlWorkerScript.dll"
del "build\EFW Automation\lib\PySide2\Qt5Quick3D.dll"
del "build\EFW Automation\lib\PySide2\Qt5Quick3DAssetImport.dll"
del "build\EFW Automation\lib\PySide2\Qt5Quick3DRender.dll"
del "build\EFW Automation\lib\PySide2\Qt5Quick3DRuntimeRender.dll"
del "build\EFW Automation\lib\PySide2\Qt5Quick3DUtils.dll"
del "build\EFW Automation\lib\PySide2\Qt5QuickControls2.dll"
del "build\EFW Automation\lib\PySide2\Qt5QuickParticles.dll"
del "build\EFW Automation\lib\PySide2\Qt5QuickShapes.dll"
del "build\EFW Automation\lib\PySide2\Qt5QuickTemplates2.dll"
del "build\EFW Automation\lib\PySide2\Qt5QuickTest.dll"
del "build\EFW Automation\lib\PySide2\Qt5QuickWidgets.dll"
del "build\EFW Automation\lib\PySide2\Qt5RemoteObjects.dll"
del "build\EFW Automation\lib\PySide2\Qt5Script.dll"
del "build\EFW Automation\lib\PySide2\Qt5ScriptTools.dll"
del "build\EFW Automation\lib\PySide2\Qt5Scxml.dll"
del "build\EFW Automation\lib\PySide2\Qt5Sensors.dll"
del "build\EFW Automation\lib\PySide2\Qt5SerialBus.dll"
del "build\EFW Automation\lib\PySide2\Qt5SerialPort.dll"
del "build\EFW Automation\lib\PySide2\Qt5Sql.dll"
del "build\EFW Automation\lib\PySide2\Qt5Svg.dll"
del "build\EFW Automation\lib\PySide2\Qt5Test.dll"
del "build\EFW Automation\lib\PySide2\Qt5TextToSpeech.dll"
del "build\EFW Automation\lib\PySide2\Qt5VirtualKeyboard.dll"
del "build\EFW Automation\lib\PySide2\Qt5WebChannel.dll"
del "build\EFW Automation\lib\PySide2\Qt5WebEngine.dll"
del "build\EFW Automation\lib\PySide2\Qt5WebEngineWidgets.dll"
del "build\EFW Automation\lib\PySide2\Qt5WebSockets.dll"
del "build\EFW Automation\lib\PySide2\Qt5WebView.dll"
del "build\EFW Automation\lib\PySide2\Qt5WinExtras.dll"
del "build\EFW Automation\lib\PySide2\QtAxContainer.pyd"
del "build\EFW Automation\lib\PySide2\QtCharts.pyd"
del "build\EFW Automation\lib\PySide2\QtConcurrent.pyd"
del "build\EFW Automation\lib\PySide2\QtDataVisualization.pyd"
del "build\EFW Automation\lib\PySide2\QtHelp.pyd"
del "build\EFW Automation\lib\PySide2\QtLocation.pyd"
del "build\EFW Automation\lib\PySide2\QtMultimedia.pyd"
del "build\EFW Automation\lib\PySide2\QtMultimediaWidgets.pyd"
del "build\EFW Automation\lib\PySide2\QtNetwork.pyd"
del "build\EFW Automation\lib\PySide2\QtOpenGL.pyd"
del "build\EFW Automation\lib\PySide2\QtPositioning.pyd"
del "build\EFW Automation\lib\PySide2\QtPrintSupport.pyd"
del "build\EFW Automation\lib\PySide2\QtQml.pyd"
del "build\EFW Automation\lib\PySide2\QtQuick.pyd"
del "build\EFW Automation\lib\PySide2\QtQuickControls2.pyd"
del "build\EFW Automation\lib\PySide2\QtQuickWidgets.pyd"
del "build\EFW Automation\lib\PySide2\QtRemoteObjects.pyd"
del "build\EFW Automation\lib\PySide2\QtScript.pyd"
del "build\EFW Automation\lib\PySide2\QtScriptTools.pyd"
del "build\EFW Automation\lib\PySide2\QtScxml.pyd"
del "build\EFW Automation\lib\PySide2\QtSensors.pyd"
del "build\EFW Automation\lib\PySide2\QtSerialPort.pyd"
del "build\EFW Automation\lib\PySide2\QtSql.pyd"
del "build\EFW Automation\lib\PySide2\QtSvg.pyd"
del "build\EFW Automation\lib\PySide2\QtTest.pyd"
del "build\EFW Automation\lib\PySide2\QtTextToSpeech.pyd"
del "build\EFW Automation\lib\PySide2\QtWebChannel.pyd"
del "build\EFW Automation\lib\PySide2\QtWebEngine.pyd"
del "build\EFW Automation\lib\PySide2\QtWebEngineCore.pyd"
del "build\EFW Automation\lib\PySide2\QtWebEngineWidgets.pyd"
del "build\EFW Automation\lib\PySide2\QtWebSockets.pyd"
del "build\EFW Automation\lib\PySide2\QtWinExtras.pyd"
del "build\EFW Automation\lib\PySide2\QtXmlPatterns.pyd"
del "build\EFW Automation\lib\PySide2\ucrtbase.dll"
del "build\EFW Automation\lib\PySide2\vcamp140.dll"
del "build\EFW Automation\lib\PySide2\vccorlib140.dll"
del "build\EFW Automation\lib\PySide2\vcomp140.dll"
del "build\EFW Automation\lib\PySide2\vcruntime140_1.dll"
del "build\EFW Automation\lib\PySide2\vcruntime140.dll"

@RD /S /Q "build\EFW Automation\lib\PySide2\examples"
@RD /S /Q "build\EFW Automation\lib\PySide2\glue"
@RD /S /Q "build\EFW Automation\lib\PySide2\include"
@RD /S /Q "build\EFW Automation\lib\PySide2\qml"
@RD /S /Q "build\EFW Automation\lib\PySide2\resources"
@RD /S /Q "build\EFW Automation\lib\PySide2\scripts"
@RD /S /Q "build\EFW Automation\lib\PySide2\support"
@RD /S /Q "build\EFW Automation\lib\PySide2\translations"
@RD /S /Q "build\EFW Automation\lib\PySide2\typesystems"
@RD /S /Q "build\EFW Automation\lib\PySide2\qml"
@RD /S /Q "build\EFW Automation\lib\PySide2\resources"

@RD /S /Q "build\EFW Automation\lib\PySide2\plugins\assetimporters"
@RD /S /Q "build\EFW Automation\lib\PySide2\plugins\audio"
@RD /S /Q "build\EFW Automation\lib\PySide2\plugins\bearer"
@RD /S /Q "build\EFW Automation\lib\PySide2\plugins\canbus"
@RD /S /Q "build\EFW Automation\lib\PySide2\plugins\gamepads"
@RD /S /Q "build\EFW Automation\lib\PySide2\plugins\generic"
@RD /S /Q "build\EFW Automation\lib\PySide2\plugins\geometryloaders"
@RD /S /Q "build\EFW Automation\lib\PySide2\plugins\geoservices"
@RD /S /Q "build\EFW Automation\lib\PySide2\plugins\iconengines"
@RD /S /Q "build\EFW Automation\lib\PySide2\plugins\mediaservice"
@RD /S /Q "build\EFW Automation\lib\PySide2\plugins\platforminputcontexts"
@RD /S /Q "build\EFW Automation\lib\PySide2\plugins\platformthemes"
@RD /S /Q "build\EFW Automation\lib\PySide2\plugins\playlistformats"
@RD /S /Q "build\EFW Automation\lib\PySide2\plugins\position"
@RD /S /Q "build\EFW Automation\lib\PySide2\plugins\printsupport"
@RD /S /Q "build\EFW Automation\lib\PySide2\plugins\qmltooling"
@RD /S /Q "build\EFW Automation\lib\PySide2\plugins\renderers"
@RD /S /Q "build\EFW Automation\lib\PySide2\plugins\renderplugins"
@RD /S /Q "build\EFW Automation\lib\PySide2\plugins\scenegraph"
@RD /S /Q "build\EFW Automation\lib\PySide2\plugins\sceneparsers"
@RD /S /Q "build\EFW Automation\lib\PySide2\plugins\sensorgestures"
@RD /S /Q "build\EFW Automation\lib\PySide2\plugins\sensors"
@RD /S /Q "build\EFW Automation\lib\PySide2\plugins\sqldrivers"
@RD /S /Q "build\EFW Automation\lib\PySide2\plugins\texttospeech"
@RD /S /Q "build\EFW Automation\lib\PySide2\plugins\virtualkeyboard"
@RD /S /Q "build\EFW Automation\lib\PySide2\plugins\webview"

del "build\EFW Automation\lib\PySide2\Qt5WebEngineCore.dll"
del "build\EFW Automation\lib\PySide2\opengl32sw.dll"
del "build\EFW Automation\lib\PySide2\QtOpenGLFunctions.pyd"
del "build\EFW Automation\lib\PySide2\d3dcompiler_47.dll"
del "build\EFW Automation\lib\PySide2\Qt5Pdf.dll"

del "build\EFW Automation\lib\PySide2\Qt5Designer.dll"
del "build\EFW Automation\lib\PySide2\Qt5Quick.dll"
del "build\EFW Automation\lib\PySide2\Qt53DRender.dll"
del "build\EFW Automation\lib\PySide2\Qt5DesignerComponents.dll"
del "build\EFW Automation\lib\PySide2\Qt5XmlPatterns.dll"

del /q /f build\EFW Automation\lib\*.pyd
del /q /f build\EFW Automation\lib\*.dll

del /s /q /f build\EFW Automation\lib\PySide2\*.exe
del /s /q /f build\EFW Automation\lib\PySide2\*.pyi

FOR /d /r . %%d IN (*.dist-info) DO @IF EXIST "%%d" rd /s /q "%%d"
@RD /S /Q build\EFW Automation\lib\multiprocessing

:: Copy adt folder to crested EFW Automation\lib folder
robocopy adt\ "build\EFW Automation\lib" /E

:: Copy res folder to crested EFW Automation folder
robocopy res "build\EFW Automation\res" /E


:: Finished
echo Finished, exiting in 5 seconds ...
timeout /T 5 /NOBREAK