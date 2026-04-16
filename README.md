# Simulador de Dispositivos

Threads inicializa varios publishers de uma vez para o mesmo router na mesma key.

Pub conecta no endpoint, abre a sessão e publica 10 mensagens num intervalo aleatório entre 1 e 10 minutos, no formato:
- {Datetime Now} -- {sessao do zenoh id} -- {número da ordem da mensagem}

e escreve num csv para cada thread publicadora

Sub le  a publicacao no topico

# Como Rodar
## MQTT
- Rodar o broker MQTT: 
- -  `C:\Arquivos de Programas\mosquitto >start mosquitto`
- Rodar a thread de [Subscribers](mqtt_sub_threads.py)
- Rodar a thread de [Publishers](mqtt_pub_threads.py)
- Deve gerar um [csv](Thread-0.csv)

## Zenoh
- Rodar o broker Zenoh:
- `C:\Users\mosoa\Downloads\zenoh-router >zenohd.exe`
- Rodar a thread de [Publishers](zenoh_pub_threads.py)
- 