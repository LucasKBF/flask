import os
from dotenv import load_dotenv
email = 'sigaav2@gmail.com'
load_dotenv()  # Carrega as variáveis do arquivo .env
senha = os.getenv('APP_PASSWORD')
print(senha)