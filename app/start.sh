# Atualizar pacotes
apt-get update && apt-get install -y wget unzip

# Instalar Google Chrome
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
apt-get install -y ./google-chrome-stable_current_amd64.deb

# Baixar ChromeDriver
wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip
unzip chromedriver_linux64.zip -d ./chromedriver_dir

# Configurar PATH para incluir o diretório do ChromeDriver
export PATH=$PATH:$(pwd)/chromedriver_dir

# Iniciar o servidor
gunicorn app:app
