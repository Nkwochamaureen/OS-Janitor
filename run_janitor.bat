@echo off
:: 1. Move to the project folder
cd /d "C:\Users\Maureennkwocha\OneDrive - Federal University of Technology, Owerri\Documents\OS-Janitor"

:: 2. Run the script silently and save the log
:: Note: I used 'janitor.py' because that is what showed in your error message.
python janitor.py --path "C:\Users\Maureennkwocha\Downloads" --silent > janitor.log 2>&1S