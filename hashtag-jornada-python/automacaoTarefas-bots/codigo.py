#bibliotecas = pacotes de código
import pyautogui
import time
import pandas
#pyautogui.click -> clica
#pyautogui.write -> escreve um texto
#pyautogui.press -> aperta uma tecla
#pyautogui.hotkey -> aperta um atalho (hotkey)
pyautogui.PAUSE = 0.5
link = "https://dlp.hashtagtreinamentos.com/python/intensivao/login"
email = "pythonimpressionador@gmail.com"    

senha = "1234"
# Passo a Passo do Programa
# Passo 1: Entrar no Sistema da Empresa
##abrir navegador
pyautogui.press("win")
pyautogui.write("chrome")
pyautogui.press("enter")

# Passo 2: Fazer Login
pyautogui.write(link)
pyautogui.press("enter")
#fazer uma pausa maior pro site carregar
time.sleep(3)
pyautogui.click(x=750, y=412)
pyautogui.write(email)
pyautogui.press("tab")
pyautogui.write(senha)
pyautogui.press("enter")
#fazer uma pausa maior pro site carregar
time.sleep(3)

# Passo 3: Abrir a Base de Dados (importar o arquivo)
tabela = pandas.read_csv("produtos.csv")

# Passo 5: Repetir o passo 4 até acabar a lista de produtos
for linha in tabela.index:
# Passo 4: Cadastrar 1 produto
    pyautogui.click(x=708, y= 290)

    codigo = str(tabela.loc[linha, "codigo"])
    pyautogui.write(codigo)
    pyautogui.press("tab")

    marca = str(tabela.loc[linha, "marca"])
    pyautogui.write(marca)
    pyautogui.press("tab")

    tipo = str(tabela.loc[linha, "tipo"])
    pyautogui.write(tipo)
    pyautogui.press("tab")

    categoria = str(tabela.loc[linha, "categoria"])
    pyautogui.write(categoria)
    pyautogui.press("tab")

    preco = str(tabela.loc[linha, "preco_unitario"])
    pyautogui.write(preco)
    pyautogui.press("tab")

    custo = str(tabela.loc[linha, "custo"])
    pyautogui.write(custo)
    pyautogui.press("tab")

    obs = str(tabela.loc[linha, "obs"])
    pyautogui.write(obs)
    pyautogui.press("tab")

    pyautogui.press("enter")
    pyautogui.scroll(5000)