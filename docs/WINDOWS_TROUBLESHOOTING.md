# Windows Troubleshooting (OSGeo4W Python konflikti)

Eger sizde şuňa meňzeş ýalňyşlyk çykýan bolsa:

- `Fatal Python error: init_fs_encoding`
- `ModuleNotFoundError: No module named 'encodings'`
- `program name = 'C:\OSGeo4W\bin\python3.exe'`

onda taslama **OSGeo4W Python** bilen açylýar. Bu taslama üçin aýratyn `venv` ulanyň.

## Gysgaça çözgüt

PowerShell-de:

```powershell
cd <taslama-papkasy>
Remove-Item Env:PYTHONHOME -ErrorAction SilentlyContinue
Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

## Eger `py` ýok bolsa

`python` ýerine doly ýol ulanyň (Microsoft Store ýa-da python.org gurlan interpreter):

```powershell
"C:\Path\To\Python312\python.exe" -m venv .venv
```

## IDE sazlamasy

VS Code: `Python: Select Interpreter` → `.venv\Scripts\python.exe` saýlaň.

