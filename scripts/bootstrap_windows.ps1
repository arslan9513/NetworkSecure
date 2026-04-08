Param(
  [string]$PythonExe = "py -3.12",
  [string]$VenvDir = ".venv"
)

Write-Host "[1/7] OSGeo/konflikt environment üýtgeýjileri arassalanýar..."
Remove-Item Env:PYTHONHOME -ErrorAction SilentlyContinue
Remove-Item Env:PYTHONPATH -ErrorAction SilentlyContinue

Write-Host "[2/7] Virtual environment döredilýär: $VenvDir"
Invoke-Expression "$PythonExe -m venv $VenvDir"
if ($LASTEXITCODE -ne 0) { throw "venv döredilip bilmedi" }

Write-Host "[3/7] venv aktivleşdirilýär"
& "$VenvDir\Scripts\Activate.ps1"

Write-Host "[4/7] pip täzelenýär"
python -m pip install --upgrade pip setuptools wheel
if ($LASTEXITCODE -ne 0) { throw "pip täzelenmedi" }

Write-Host "[5/7] Dependencies gurnalýar"
pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw "dependencies gurnalyp bilmedi" }

Write-Host "[6/7] Migrations + demo maglumatlar"
python manage.py migrate
python manage.py seed_demo

Write-Host "[7/7] Serwer işe goýberilýär"
python manage.py runserver
