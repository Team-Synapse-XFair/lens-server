@echo off
python -m venv flask
flask\Scripts\activate

pip install -r requirements.txt

echo Server setup complete. You can now run the server using RunServer.bat