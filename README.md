# CopyEverything-Desktop

A desktop interface for the Copy Everything project. Ubuntu/Linux, Windows, and Mac are supported.

Dependencies:
	-python3
	-PyQt5
	-Qt5 \w QML
	-[QML Material](https://github.com/papyros/qml-material)
	-[socketIO-client](https://pypi.python.org/pypi/socketIO-client)
    
How to compile:
    - Run:: pyinstaller gui.py --noconsole -F --clean --distpath dist --workpath build --icon=[full path]\favicon.ico -n CopyEverything
    - Copy the qml folder to the dist folder