import requests

url = "https://www.google.com/"

reposta = requests.get(url)

print(reposta.text)
