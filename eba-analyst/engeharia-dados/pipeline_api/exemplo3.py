import requests

url = "https://jsonplaceholder.typicode.com/comments"
params = {"postId": 8}

response = requests.get(url, params=params)
comentarios = response.json()

print(f"Total de {len(comentarios)} comentários encontrados!!")
print(f"Erro: {response.status_code} - {response.text}")
