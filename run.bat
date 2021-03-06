pushd %~dp0

if exist "C:\ProgramData\Anaconda3\_conda.exe" (
    call echo "Anaconda Already Installed at C:\ProgramData\Anaconda3"
) else (
    call echo "Downloading Anaconda..."
    call curl https://repo.anaconda.com/archive/Anaconda3-2020.11-Windows-x86_64.exe -o Anaconda3-Windows-x86_64.exe
    call echo "Installing Anaconda at C:\ProgramData\Anaconda3..."
    call start /wait "" Anaconda3-Windows-x86_64.exe /InstallationType=AllUsers /AddToPath=1 /RegisterPython=1 /S /D=C:\ProgramData\Anaconda3
    call del Anaconda3-Windows-x86_64.exe
    call conda update -n base -c defaults conda
)

call "C:\ProgramData\Anaconda3\Scripts\activate.bat"
call conda env create -f environment.yml
call conda activate crossoutML
call python main.py
