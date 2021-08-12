import config
from library.client import client as rconClient

client = rconClient(shell_mode=True)
client.connect(use_json=False)
client.start_listen()

while True:
    client.run(input())