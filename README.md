# Tubes3_HR_Magang

## RUN

1. python -m venv venv
2. venv\Scripts\activate
3. pip install -r requirements.txt
4. python .\src\main.py

## MAKE GUI

1.  & '.\Qt Designer Setup.exe'
2.  Install and open file window.ui or make new file for other window (Only once, after install just open normally with search bar)
3.  To build, enter this : pyuic5 src/ui/window.ui -o src/ui/window.py (replace window with your file)
4.  pyuic5 src/ui/home.ui -o src/ui/home.py
5.  pyuic5 src/ui/summary.ui -o src/ui/summary.py

## IF do any pip install

1. in root dir, enter : pip freeze > requirement.txt

## DATABASE

WIP
