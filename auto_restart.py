import requests

client = requests.session()
url = 'https://control.bot-hosting.net/api/client/servers/723d4729/power'
client.get(url)  # sets cookie

url = 'https://control.bot-hosting.net/api/client/servers/723d4729/power'
headers = {
    "Authorization": "Bearer ptlc_XXfLM4wlfgG6GvZ35VjdhLpvAy2Fs5lrgj839DsIsSZ",
    "Accept": "application/json",
    "Content-Type": "application/json",
    "cookie": "eyJpdiI6ImRCejZqZU1ZYUwzRnVNQXl3c213bUE9PSIsInZhbHVlIjoiMy9rODRHV3V5MGsrenQrNTY0UEI0NSt4dVBHczBtZlV3YXo4Zk5FKytRWk0xbnRpcjdWME1mdG1tQ2s0ajVPdGwvaCs0UXNhSnU5S2grVjNadkgyaWpjZE1jQ3lFaUFBdVI5bThtVzNGbmREbDdZam9vMVVRS1VmbDExM0lZN3AiLCJtYWMiOiJkZTdmMzQ5OWU2Zjk4YjhkYzhhYzkzYzFhODYzOTU0MTIwMzEyNGFhZGNjNGI5ZmQ0N2FiZDBjN2Q1ZWVhOGZhIiwidGFnIjoiIn0%3D"
}
payload = '{"signal": "restart"}'
response = client.request('POST', url, data=payload, headers=headers)
print(response.text)
