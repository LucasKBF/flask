from app.config import *

with open(r"C:\Users\lucas\OneDrive\Área de Trabalho\SigaaV2\app\manu.txt", "r") as arquivo:
#with open(r"C:\Users\Victor\codes\GitHub\SigaaV2\app\manu.txt", "r") as arquivo:
    manu = arquivo.read()
    em_manutencao = manu


@app.before_request
def verifica_manutencao():
    global em_manutencao
    
    #endregion
#region Ignorar requisições para arquivos estáticos
    if em_manutencao == "True" and not (request.endpoint == 'manutencao' or request.endpoint.startswith('templates/static')):
        return redirect(url_for('manutencao'))

@app.route('/manutencao')
def manutencao():
    if em_manutencao=="False":
        return redirect(url_for('/'))
    else:
        return render_template('manutenção.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('templates/static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/")
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/autenticar")
def login():
    return render_template("login.html")

@app.route("/dashboard", methods=['POST'])
def autenticar():
    usuario= request.form.get("usuario")
    senha= request.form.get("senha")
    notasfaltas = request.form.get("notasfaltas")
    notas1, atividades, resultado_info = login (usuario, senha)
    notas2 = Markup(notas1)
    atividades2 = Markup(atividades)
    resultado_info2 = Markup(resultado_info)
    erro1="<br><br><strong style='color:red; font-size: medium;'>Erro ao logar:<br>Verifique se o usuario e senha estão corretos e se o Sigaa está online.</strong>"
    erro = Markup(erro1)
    if notas2=="erro":

        return render_template("login.html", erro=erro)
    else:
        return render_template("dashboard.html", notas=notas2, atv=atividades2, info=resultado_info2)

@app.route("/sobre")
def sobre():
    return render_template("sobre.html")

@app.route("/creditos")
def creditos():
    return render_template("creditos.html")

@app.route("/segurança")
def segurança():
    return render_template("segurança.html")

@app.route("/termosdeservico")
def termosdeservico():
    return render_template("termosdeservico.html")

@app.route("/politicadeprivacidade")
def politicadeprivacidade():
    return render_template("politicadeprivacidade.html")

@app.route('/LICENSE')
def license():
    return render_template("LICENSE.html")

@app.route('/contato', methods=['GET', 'POST'])
def contato():
    status = ""
    if request.method == 'POST':


        #endregion
#region Captura os dados do formulário
        nome = request.form.get('nome')
        email = request.form.get('email')
        mensagem = request.form.get('mensagem')

        smtp_server = "smtp.gmail.com"
        smtp_port = 587  
        #endregion
#region Usando TLS
        from_email = "sigaav2@gmail.com"  
        #endregion
#region Substitua pelo seu e-mail Gmail
        to_email = "sigaav2@gmail.com"  
        #endregion
#region Substitua pelo e-mail do destinatário
        subject = "Contato"
        body = f"Nome: {nome} \nEmail: {email} \nMensagem: {mensagem}"
        
        msg = MIMEMultipart()
        msg['From'] = from_email
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        try:
            
            #endregion
#region Conectando ao servidor SMTP do Gmail e enviando o e-mail
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  
            #endregion
#region Habilita segurança
            server.login(from_email, senha)  
            #endregion
#region Use a senha de aplicativo, não a senha normal
            text = msg.as_string()
            server.sendmail(from_email, to_email, text)
            print("E-mail enviado com sucesso!")
            status = "<script>alert('Email enviado com sucesso!')</script>"

        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")
        finally:
            if server:
                server.quit()
    status = Markup(status)
    return render_template('contato.html', status=status)


@app.route("/email", methods=['POST'])
def email():
    return render_template("contato.html")

@app.route("/atualizacoes")
def atualizacoes():
    return render_template("atualizacoes.html")


def login(usuario, senha):
    app = Flask(__name__)
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Executar em modo headless
    chrome_options.add_argument("--disable-gpu")  # Necessário em alguns sistemas
    chrome_options.add_argument("--no-sandbox")  # Requerido em alguns ambientes como Docker
    chrome_options.add_argument("--disable-dev-shm-usage")  # Prevenir problemas de memória em ambientes limitados

    #endregion
#region Prevenir problemas de memória
    navegador = webdriver.Chrome(options=chrome_options)
    def separar_data_horario(data_envio):
        
        #endregion
#region Expressão regular para capturar a data e o horário no formato dd/mm/aaaaHH:MM
        match = re.match(r"(\d{2}/\d{2}/\d{4})(\d{2}:\d{2})", data_envio)
        if match:
            data = match.group(1)  
            #endregion
#region A data
            horario = match.group(2)  
            #endregion
#region O horário
            return data, horario
        else:
            
            #endregion
#region Caso não encontre o formato esperado, retorna a data e horário vazio
            return data_envio, ""

    
    #endregion
#region Função para tratar alertas
    def handle_alert():
        try:
            
            #endregion
#region Verifica se há um alerta na página
            alert = WebDriverWait(navegador, 5).until(EC.alert_is_present())
            alert_text = alert.text
            print(f"Alerta encontrado: {alert_text}")
            
            
            #endregion
#region Verifica se o alerta é de sessão expirada
            if "Sua sessão foi expirada" in alert_text:
                print("Sessão expirada! Tentando reiniciar...")
                alert.accept()  
                #endregion
#region Aceita o alerta e tenta fazer login novamente
                
                #endregion
#region Realizar novamente o login ou redirecionar para a página de login.
                navegador.get("https://sigaa.ifsc.edu.br/sigaa/verTelaLogin.do")
            else:
                alert.accept()  
                #endregion
#region Aceitar o alerta caso não seja o de sessão expirada
        except:
            pass  
        #endregion
#region Inicializar o WebDriver

    
    #endregion
#region Acessar a página de login
    navegador.get("https://sigaa.ifsc.edu.br/sigaa/verTelaLogin.do")
    username = usuario
    password = senha

    
    #endregion
#region Acessar a página de login
    navegador.get("https://sigaa.ifsc.edu.br/sigaa/verTelaLogin.do")

    
    #endregion
#region Esperar até o campo de login aparecer
    WebDriverWait(navegador, 10).until(EC.presence_of_element_located((By.NAME, "user.login")))

    
    #endregion
#region Encontrar os campos de login
    username_field = navegador.find_element(By.NAME, "user.login")
    password_field = navegador.find_element(By.NAME, "user.senha")

    
    #endregion
#region Preencher os campos de login e submeter
    username_field.send_keys(username)
    password_field.send_keys(password)
    password_field.send_keys(Keys.RETURN)

#endregion
#region Ver se a senha ta errada
    
    elements = navegador.find_elements(By.XPATH, "//center[@style='color: #922; font-weight: bold;' and text()='Usuário e/ou senha inválidos']")
    
    if elements:
        print("Elemento encontrado!")
    else:
        print("Elemento não encontrado!")



    
    #endregion


    # Aguarda até que pelo menos uma tabela que contenha "Matrícula:" esteja visível
    try: WebDriverWait(navegador, 4).until(
        EC.presence_of_all_elements_located((By.XPATH, "//table[.//td[contains(text(), 'Matrícula:')]]"))
        )
    except:
        return "erro"
    # Captura todas as tabelas que contêm "Matrícula:"
    tabelas = navegador.find_elements(By.XPATH, "//table[.//td[contains(text(), 'Matrícula:')]]")
    
    print(f"Número de tabelas encontradas: {len(tabelas)}")
    
    # Iterar pelas tabelas para processar ou selecionar uma específica
    for index, tabela in enumerate(tabelas):
        print(f"\nTabela {index + 1}:")
        resultado_info = tabela.get_attribute('outerHTML')  # Exibe o HTML da tabela
        # Parsear o HTML com BeautifulSoup
    soup = BeautifulSoup(resultado_info, "html.parser")

    # Localizar e remover o elemento <a>
    link = soup.find("a", text="Detalhar")  # Localiza o elemento <a> pelo texto
    if link:
        link.decompose()  # Remove o elemento do HTML

    # Obter o HTML atualizado
    resultado_info = soup.prettify()
#region Tratar alertas, caso ocorram
    handle_alert()
    rows = navegador.find_elements(By.XPATH, "//table/tbody/tr")
    atividades=[]
    erros = []
    for row in rows:
        try:
            # Capturando os elementos necessários
            data_element = row.find_element(By.CSS_SELECTOR, "td font[color='gray']")
            atividade_element = row.find_element(By.CSS_SELECTOR, "td small font[color='gray']")
            
            # Extraindo informações
            data_envio = data_element.text.strip()
            atividade_info = atividade_element.get_attribute("innerText").split("\n")
            materia = atividade_info[0].strip()
            
            # Filtrando a parte do nome da atividade
            if "Tarefa:" in atividade_info[1]:
                nome_atividade = atividade_info[1].split("Tarefa:")[-1].strip()
            elif "Avaliação:" in atividade_info[1]:
                nome_atividade = atividade_info[1].split("Avaliação:")[-1].strip()
            elif "Questionário:" in atividade_info[1]:
                nome_atividade = atividade_info[1].split("Questionário:")[-1].strip()
            else:
                nome_atividade = "Atividade não especificada"

            # Separando data e horário (ajuste conforme necessário)
            if " " in data_envio:  # Verifica se existe um espaço, o que indica que temos data e horário juntos
                data_envio, horario_envio = data_envio.split(" ", 1)  # Divide a string em data e horário
            else:
                horario_envio = ""  # Caso não tenha horário, deixa em branco

            # Armazenando a atividade no banco de dados
            atividade = {
                'data_envio': data_envio,
                'horario_envio': horario_envio,  # Agora com horário separado
                'materia': materia,
                'nome_atividade': nome_atividade
            }
            atividades.append(atividade)
        except Exception as e:
            erros.append(e)
            continue
    if atividades:
        atv = atividades
    else:
        atv = '<p style="text-align: center;"> Nenhuma atividade encontrada.</p>'
    resultados = []
    nomes_turmas = []
    html_notas = []
    try:
        WebDriverWait(navegador, 5).until(EC.presence_of_element_located((By.ID, "form_acessarTurmaVirtual:turmaVirtual")))
        print(f"Acessando turma: BIOLOGIA")
        botao = navegador.find_element(By.ID, f"form_acessarTurmaVirtual:turmaVirtual")  
        #endregion
#region Altere para o método de localização correto (ID, Nome, XPath, etc.)
        botao.click()
        botao = navegador.find_element(By.CLASS_NAME, "itemMenuHeaderAlunos")  
        #endregion
#region Altere para o método de localização correto (ID, Nome, XPath, etc.)
        botao.click()
        botao = navegador.find_element(By.XPATH, "//div[text()='Ver Notas']")  
        #endregion
#region Altere para o método de localização correto (ID, Nome, XPath, etc.)
        botao.click()
        nomes_turmas.append("BIOLOGIA")
        html_notas.append(navegador.page_source)
    except:
        return "erro"
    
    #endregion
#region URL da página inicial
    url_inicial = "https://sigaa.ifsc.edu.br/sigaa/portais/discente/discente.jsf"
    navegador.get(url_inicial)

    
    #endregion
#region Loop para percorrer os IDs dinâmicos
    for x in range(1, 10):  
        #endregion
#region Ajuste o range conforme necessário
        try:
            
            #endregion
#region Gerar o seletor de ID dinâmico
            id_selector = f"form_acessarTurmaVirtualj_id_{x}:turmaVirtual"

            
            #endregion
#region Esperar o elemento com o ID dinâmico estar presente
            WebDriverWait(navegador, 5).until(EC.presence_of_element_located((By.ID, id_selector)))

            
            #endregion
#region Encontrar o elemento e obter o nome da turma
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
            navegador.get(url_inicial) 
            continue

            #endregion

        


    resultado2 = []
    erros = []
    log_dir = r"app\logs"
    log_file = os.path.join(log_dir, "log.txt")

    try:
        for idx, html in enumerate(html_notas):
            soup = BeautifulSoup(html, 'html.parser')

            # Remove o último <th> na linha com id "trAval"
            tr = soup.find('tr', id='trAval')
            if tr:
                th_elements = tr.find_all('th')
                if th_elements:
                    th_elements[-1].decompose()

            # Remove a última célula de cada linha de todas as tabelas
            for table in soup.find_all('table'):
                for row in table.find_all('tr'):
                    cells = row.find_all(['th', 'td'])
                    if cells:
                        cells[-1].decompose()

            # Remove todas as ocorrências de "Alunos Matriculados"
            for element in soup.find_all(string=lambda text: "Alunos Matriculados" in text):
                element.replace_with(element.replace("Alunos Matriculados", ""))

            # Adiciona a div com a classe 'notas' ao resultado
            notas_div = soup.find('div', class_='notas')
            if notas_div:
                div_str = str(notas_div)
                resultado2.append(f"<strong>{nomes_turmas[idx]}</strong>{div_str}<br><br><br><br>")
        
        # Converte o resultado final para string
        resultado = " ".join(resultado2)
        soup = BeautifulSoup(resultado, 'html.parser')

        # Itera pelas tabelas para remover colunas específicas
        for table in soup.find_all('table'):
            headers = table.find('tr').find_all('th')
            indices_to_remove = [index for index, header in enumerate(headers) if header.text.strip().lower() in ['matrícula', 'nome']]

            for row in table.find_all('tr'):
                cells = row.find_all(['th', 'td'])
                for index in sorted(indices_to_remove, reverse=True):
                    if index < len(cells):
                        cells[index].decompose()

        # Resultado final
        resultado_final = str(soup)

    except Exception as e:
        erros.append(f"Erro ao processar HTML: {e}")

    # Cria o diretório de logs, se necessário, e salva os erros
    os.makedirs(log_dir, exist_ok=True)
    with open(log_file, "w", encoding="utf-8") as arquivo:
        arquivo.write("\n".join(erros))
    if erros:
        print("Erros armazenados:", erros)

    print("Nomes das turmas coletados:", nomes_turmas)
    return resultado_final, atv, resultado_info