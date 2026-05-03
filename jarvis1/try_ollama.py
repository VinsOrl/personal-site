from ollama import Client

# Connect to your DGX server's exposed Ollama API
client = Client(host='http://192.168.60.194:11434')

# Send a prompt to the model
response = client.chat(model='gpt-oss:20b', messages=[
  {
    'role': 'user',
    'content': 'Explain quantum computing in one sentence.',
  },
])

print(response['message']['content'])