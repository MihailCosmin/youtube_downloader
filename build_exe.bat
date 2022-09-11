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
echo executables = [Executable("main.py", base=base, icon="icons/yt_dlp_gui.png")]>> setup.py
echo, >> setup.py
echo packages = ["ctypes","imp", "PySide2", "yt_dlp"]>> setup.py
echo excludes = ["PyQt5", "PyQt4", "reportlab", "matplotlib", "numba", "scipy", "sqlalchemy", "sqlite3", "soupsieve", "llvmlite", "black", "bs4", "jupyter", "tornado", "pygments"]>> setup.py
echo options = {>> setup.py
echo     'build_exe': {>> setup.py
echo         'packages': packages,>> setup.py
echo         'excludes': excludes,>> setup.py 
echo     },>> setup.py
echo }>> setup.py
echo setup(>> setup.py
echo     name="<yt_dlp_gui>",>> setup.py
echo     options=options,>> setup.py
echo     version="0.0.0.1",>> setup.py
echo     description='^<yt_dlp_gui is a standalone application for '>> setup.py
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
@REM del setup.py

:: Create ALTHOM-Publisher folder
if not exist "build\yt_dlp_gui" mkdir "build\yt_dlp_gui"
robocopy "build\exe.win-amd64-3.9" "build\yt_dlp_gui" /E /MOVE

@REM @RD /S /Q "build\yt_dlp_gui\lib\res"
@REM @RD /S /Q "build\yt_dlp_gui\lib\Test"

@RD /S /Q "build\yt_dlp_gui\lib\pytz"
@RD /S /Q "build\yt_dlp_gui\lib\numpy"
@RD /S /Q "build\yt_dlp_gui\lib\Cryptodome"
@RD /S /Q "build\yt_dlp_gui\lib\distutils"
@RD /S /Q "build\yt_dlp_gui\lib\test"
@RD /S /Q "build\yt_dlp_gui\lib\tkinter"

del "build\yt_dlp_gui\lib\PySide2\Qt3DExtras.pyd"

@REM :: PySide2 folder imported with too many files and folders. Deleting unnecessary ones.
@REM del "build\yt_dlp_gui\lib\PySide2\Qt3DExtras.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt53DExtras.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5Bluetooth.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5Multimedia.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5Quick3D.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5QuickParticles.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5RemoteObjects.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5ScriptTools.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\QtLocation.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\QtQuick.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\QtSensors.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\concrt140.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\libEGL.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\libGLESv2.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\msvcp140_1.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\msvcp140_2.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\msvcp140_codecvt_ids.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\msvcp140.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\py.typed"
@REM del "build\yt_dlp_gui\lib\PySide2\pyside2.abi3.lib"
@REM del "build\yt_dlp_gui\lib\PySide2\qt.conf"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt3DAnimation.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt3DCore.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt3DExtras.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt3DInput.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt3DLogic.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt3DRender.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt53DAnimation.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt53DCore.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt53DExtras.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt53DInput.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt53DLogic.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt53DQuick.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt53DQuickAnimation.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt53DQuickExtras.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt53DQuickInput.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt53DQuickRender.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt53DQuickScene2D.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5Bluetooth.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5Bodymovin.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5Charts.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5Concurrent.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5DataVisualization.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5DBus.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5Gamepad.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5Help.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5Location.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5Multimedia.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5MultimediaQuick.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5MultimediaWidgets.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5NetworkAuth.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5Nfc.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5OpenGL.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5PdfWidgets.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5Positioning.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5PositioningQuick.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5PrintSupport.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5Purchasing.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5QmlModels.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5QmlWorkerScript.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5Quick3D.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5Quick3DAssetImport.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5Quick3DRender.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5Quick3DRuntimeRender.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5Quick3DUtils.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5QuickControls2.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5QuickParticles.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5QuickShapes.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5QuickTemplates2.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5QuickTest.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5QuickWidgets.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5RemoteObjects.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5Script.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5ScriptTools.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5Scxml.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5Sensors.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5SerialBus.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5SerialPort.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5Sql.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5Svg.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5Test.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5TextToSpeech.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5VirtualKeyboard.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5WinExtras.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\QtAxContainer.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\QtCharts.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\QtConcurrent.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\QtDataVisualization.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\QtHelp.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\QtLocation.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\QtMultimedia.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\QtMultimediaWidgets.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\QtNetwork.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\QtOpenGL.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\QtPositioning.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\QtPrintSupport.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\QtQml.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\QtQuick.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\QtQuickControls2.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\QtQuickWidgets.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\QtRemoteObjects.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\QtScript.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\QtScriptTools.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\QtScxml.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\QtSensors.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\QtSerialPort.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\QtSql.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\QtSvg.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\QtTest.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\QtTextToSpeech.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\QtWinExtras.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\QtXmlPatterns.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\ucrtbase.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\vcamp140.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\vccorlib140.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\vcomp140.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\vcruntime140_1.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\vcruntime140.dll"

@REM @RD /S /Q "build\yt_dlp_gui\lib\PySide2\examples"
@REM @RD /S /Q "build\yt_dlp_gui\lib\PySide2\glue"
@REM @RD /S /Q "build\yt_dlp_gui\lib\PySide2\include"
@REM @RD /S /Q "build\yt_dlp_gui\lib\PySide2\qml"
@REM @RD /S /Q "build\yt_dlp_gui\lib\PySide2\resources"
@REM @RD /S /Q "build\yt_dlp_gui\lib\PySide2\scripts"
@REM @RD /S /Q "build\yt_dlp_gui\lib\PySide2\support"
@REM @RD /S /Q "build\yt_dlp_gui\lib\PySide2\translations"
@REM @RD /S /Q "build\yt_dlp_gui\lib\PySide2\typesystems"
@REM @RD /S /Q "build\yt_dlp_gui\lib\PySide2\qml"
@REM @RD /S /Q "build\yt_dlp_gui\lib\PySide2\resources"

@REM @RD /S /Q "build\yt_dlp_gui\lib\PySide2\plugins\assetimporters"
@REM @RD /S /Q "build\yt_dlp_gui\lib\PySide2\plugins\audio"
@REM @RD /S /Q "build\yt_dlp_gui\lib\PySide2\plugins\bearer"
@REM @RD /S /Q "build\yt_dlp_gui\lib\PySide2\plugins\canbus"
@REM @RD /S /Q "build\yt_dlp_gui\lib\PySide2\plugins\gamepads"
@REM @RD /S /Q "build\yt_dlp_gui\lib\PySide2\plugins\generic"
@REM @RD /S /Q "build\yt_dlp_gui\lib\PySide2\plugins\geometryloaders"
@REM @RD /S /Q "build\yt_dlp_gui\lib\PySide2\plugins\geoservices"
@REM @RD /S /Q "build\yt_dlp_gui\lib\PySide2\plugins\iconengines"
@REM @RD /S /Q "build\yt_dlp_gui\lib\PySide2\plugins\mediaservice"
@REM @RD /S /Q "build\yt_dlp_gui\lib\PySide2\plugins\platforminputcontexts"
@REM @RD /S /Q "build\yt_dlp_gui\lib\PySide2\plugins\platformthemes"
@REM @RD /S /Q "build\yt_dlp_gui\lib\PySide2\plugins\playlistformats"
@REM @RD /S /Q "build\yt_dlp_gui\lib\PySide2\plugins\position"
@REM @RD /S /Q "build\yt_dlp_gui\lib\PySide2\plugins\printsupport"
@REM @RD /S /Q "build\yt_dlp_gui\lib\PySide2\plugins\qmltooling"
@REM @RD /S /Q "build\yt_dlp_gui\lib\PySide2\plugins\renderers"
@REM @RD /S /Q "build\yt_dlp_gui\lib\PySide2\plugins\renderplugins"
@REM @RD /S /Q "build\yt_dlp_gui\lib\PySide2\plugins\scenegraph"
@REM @RD /S /Q "build\yt_dlp_gui\lib\PySide2\plugins\sceneparsers"
@REM @RD /S /Q "build\yt_dlp_gui\lib\PySide2\plugins\sensorgestures"
@REM @RD /S /Q "build\yt_dlp_gui\lib\PySide2\plugins\sensors"
@REM @RD /S /Q "build\yt_dlp_gui\lib\PySide2\plugins\sqldrivers"
@REM @RD /S /Q "build\yt_dlp_gui\lib\PySide2\plugins\texttospeech"
@REM @RD /S /Q "build\yt_dlp_gui\lib\PySide2\plugins\virtualkeyboard"

@REM del "build\yt_dlp_gui\lib\PySide2\opengl32sw.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\QtOpenGLFunctions.pyd"
@REM del "build\yt_dlp_gui\lib\PySide2\d3dcompiler_47.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5Pdf.dll"

@REM del "build\yt_dlp_gui\lib\PySide2\Qt5Designer.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5Quick.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt53DRender.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5DesignerComponents.dll"
@REM del "build\yt_dlp_gui\lib\PySide2\Qt5XmlPatterns.dll"

@REM del /q /f build\yt_dlp_gui\lib\*.pyd
@REM del /q /f build\yt_dlp_gui\lib\*.dll

@REM del /s /q /f build\yt_dlp_gui\lib\PySide2\*.exe
@REM del /s /q /f build\yt_dlp_gui\lib\PySide2\*.pyi

@REM FOR /d /r . %%d IN (*.dist-info) DO @IF EXIST "%%d" rd /s /q "%%d"
@REM @RD /S /Q build\yt_dlp_gui\lib\multiprocessing

:: Copy adt folder to crested yt_dlp_gui\lib folder
robocopy adt\ "build\yt_dlp_gui\lib" /E

:: Copy res folder to crested yt_dlp_gui folder
robocopy res "build\yt_dlp_gui\res" /E


:: Finished
echo Finished, exiting in 5 seconds ...
timeout /T 5 /NOBREAK