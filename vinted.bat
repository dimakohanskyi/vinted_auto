@echo off

python -m venv .venv

call .venv\Scripts\activate

pip install -r req.txt

python db/models.py

pause