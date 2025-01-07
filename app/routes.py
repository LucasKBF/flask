from app import app
from flask import render_template
from flask import Flask, request, jsonify
from markupsafe import Markup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import chromedriver_autoinstaller
import time
import re
import os
@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route("/autenticar")
def login():
    return render_template("login.html")


@app.route("/dashboard", methods=['POST'])
def autenticar():
    usuario= request.form.get("usuario")
    senha= request.form.get("senha")
    notas1 = login (usuario, senha)
    notas2 = Markup(notas1)
    erro1="<br><br><strong style='color:red; font-size: medium;'>Erro ao logar:<br>Verifique se o usuario e senha estão corretos e se o Sigaa está online.</strong>"
    erro = Markup(erro1)
    if notas2=="erro":
      
        return render_template("login.html", erro=erro)
    else:
        return render_template("dashboard.html", notas=notas2)

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/contato")
def contato():
    return render_template("contato.html")

@app.route("/atualizacoes")
def atualizacoes():
    return render_template("atualizacoes.html")
def login(usuario, senha):
    chromedriver_autoinstaller.install()
    app = Flask(__name__)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Ativar modo headless
    chrome_options.add_argument("--disable-gpu")  # Desativar uso de GPU (recomendado no modo headless)
    chrome_options.add_argument("--window-size=1920x1080")  # Definir resolução
    chrome_options.add_argument("--no-sandbox")  # Necessário em alguns sistemas
    chrome_options.add_argument("--disable-dev-shm-usage")  # Prevenir problemas de memória
    navegador = webdriver.Chrome(options=chrome_options)
    def separar_data_horario(data_envio):
        # Expressão regular para capturar a data e o horário no formato dd/mm/aaaaHH:MM
        match = re.match(r"(\d{2}/\d{2}/\d{4})(\d{2}:\d{2})", data_envio)
        if match:
            data = match.group(1)  # A data
            horario = match.group(2)  # O horário
            return data, horario
        else:
            # Caso não encontre o formato esperado, retorna a data e horário vazio
            return data_envio, ""

    # Função para tratar alertas
    def handle_alert():
        try:
            # Verifica se há um alerta na página
            alert = WebDriverWait(navegador, 5).until(EC.alert_is_present())
            alert_text = alert.text
            print(f"Alerta encontrado: {alert_text}")
            
            # Verifica se o alerta é de sessão expirada
            if "Sua sessão foi expirada" in alert_text:
                print("Sessão expirada! Tentando reiniciar...")
                alert.accept()  # Aceita o alerta e tenta fazer login novamente
                # Realizar novamente o login ou redirecionar para a página de login.
                navegador.get("https://sigaa.ifsc.edu.br/sigaa/verTelaLogin.do")
            else:
                alert.accept()  # Aceitar o alerta caso não seja o de sessão expirada
        except:
            pass  # Caso não haja alerta, continua sem problemas

    # Configurações do WebDriver (rodar sem abrir janela do navegador)


    # Inicializar o WebDriver

    # Acessar a página de login
    navegador.get("https://sigaa.ifsc.edu.br/sigaa/verTelaLogin.do")
    username = usuario
    password = senha

    # Acessar a página de login
    navegador.get("https://sigaa.ifsc.edu.br/sigaa/verTelaLogin.do")

    # Esperar até o campo de login aparecer
    WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.NAME, "user.login")))

    # Encontrar os campos de login
    username_field = navegador.find_element(By.NAME, "user.login")
    password_field = navegador.find_element(By.NAME, "user.senha")

    # Preencher os campos de login e submeter
    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)

    # Esperar a página carregar após o login
    WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.XPATH, "//table/tbody/tr")))

    # Tratar alertas, caso ocorram
    handle_alert()

    erros = []
    resultados = []
    nomes_turmas = []
    html_notas = []
    try:
        WebDriverWait(navegador, 5).until(EC.presence_of_element_located((By.ID, "form_acessarTurmaVirtual:turmaVirtual")))
        print(f"Acessando turma: BIOLOGIA")
        botao = navegador.find_element(By.ID, f"form_acessarTurmaVirtual:turmaVirtual")  # Altere para o método de localização correto (ID, Nome, XPath, etc.)
        botao.click()
        botao = navegador.find_element(By.CLASS_NAME, "itemMenuHeaderAlunos")  # Altere para o método de localização correto (ID, Nome, XPath, etc.)
        botao.click()
        botao = navegador.find_element(By.XPATH, "//div[text()='Ver Notas']")  # Altere para o método de localização correto (ID, Nome, XPath, etc.)
        botao.click()
        nomes_turmas.append("BIOLOGIA")
        html_notas.append(navegador.page_source)
    except:
        return "erro"
    # URL da página inicial
    url_inicial = "https://sigaa.ifsc.edu.br/sigaa/portais/discente/discente.jsf"
    navegador.get(url_inicial)

    # Loop para percorrer os IDs dinâmicos
    for x in range(1, 10):  # Ajuste o range conforme necessário
        try:
            # Gerar o seletor de ID dinâmico
            id_selector = f"form_acessarTurmaVirtualj_id_{x}:turmaVirtual"

            # Esperar o elemento com o ID dinâmico estar presente
            WebDriverWait(navegador, 5).until(EC.presence_of_element_located((By.ID, id_selector)))

            # Encontrar o elemento e obter o nome da turma
            elemento_turma = navegador.find_element(By.ID, id_selector)
            nome_turma = elemento_turma.text.strip()
            if nome_turma:  
                nomes_turmas.append(nome_turma)
                print(f"Acessando turma: {nome_turma}")
                elemento_turma.click()
                WebDriverWait(navegador, 10).until(
                    EC.element_to_be_clickable((By.XPATH, "//div[text()='Ver Notas']"))
                )
                botao_notas = navegador.find_element(By.XPATH, "//div[text()='Ver Notas']")
                botao_notas.click()
                
                html_notas.append(navegador.page_source)

                navegador.get(url_inicial)


        except Exception as e:
            erro_msg = f"Erro ao processar o ID {id_selector}: {str(e)}"
            erros.append(erro_msg)
            navegador.get(url_inicial)  # Retorna à página inicial em caso de erro
            continue


    x=0
    resultado2=[]
            
    for html in html_notas:
        soup = BeautifulSoup(html, 'html.parser')
        
        # Remove todas as ocorrências de "Alunos Matriculados"
        for element in soup.find_all(string=lambda text: "Alunos Matriculados" in text):
            element.replace_with(element.replace("Alunos Matriculados", ""))  # Remove o texto

        # Encontra a div com a classe 'notas'
        notas_div = soup.find('div', class_='notas')
        if notas_div:
            resultados.append(notas_div)  # Adiciona a div ao resultado
            resultados = [str(item) for item in resultados]  # Converte todos os itens para string

            # Combina os resultados com os nomes das turmas
            resultado2.append("<strong>" + nomes_turmas[x] + "</strong>" + resultados[x] + "<br><br>")
            resultado = " ".join(resultado2)
            
            print(nomes_turmas[x])  # Imprime o nome da turma
            x += 1  # Incrementa x
  
    # Diretório específicoa
    log_dir = r"C:\Users\lucas\OneDrive\Área de Trabalho\sigab\arquivos"
    os.makedirs(log_dir, exist_ok=True)  # Cria o diretório se não existir

    log_file = os.path.join(log_dir, "erros_log.txt")
    with open(log_file, "w", encoding="utf-8") as arquivo:
        arquivo.write("\n".join(erros))
    print("Logs armazenados")

    # Exibir os nomes coletados
    print("Nomes das turmas coletados:", nomes_turmas)
    navegador.close
    return resultado