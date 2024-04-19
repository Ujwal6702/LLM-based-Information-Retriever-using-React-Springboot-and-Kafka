import requests

url = "http://localhost:8000/register/"

payload = {
    "email": "ujwalujwalc@gmail.com",
    "name": "John Doe",
    "password": "secure_password"
}

response = requests.post(url, json=payload)

print(response.text)