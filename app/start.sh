#!/bin/bash
# Instalar dependências
apt-get update && apt-get install -y wget unzip
# Instalar Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get install -y ./google-chrome-stable_current_amd64.deb
# Instalar ChromeDriver
wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
unzip chromedriver_linux64.zip -d /usr/bin/
# Rodar o servidor
gunicorn app:app
