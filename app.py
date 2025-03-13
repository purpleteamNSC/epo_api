# TODO:
# PEGAR LOGS DO EPO

# IMPORTANDO AS BIBLIOTECAS
import os
import requests
from dotenv import load_dotenv
import logging
from logging.handlers import SysLogHandler
import socket
import json


# INICIA AS VARIAVEIS DE AMBIENTE
load_dotenv()


# VARIAVEIS DE AMBIENTE
client_id = os.getenv("CLIENT_ID")
secret = os.getenv("SECRET")
trelix_api = os.getenv("TRELLIX_API")


# DEFINIR SCOPE CONFORME NECESSIDADE DO ENDPOINT A SER CONSUMIDO
scopes = "epo.evt.r epo.device.r"
base_url = "https://api.manage.trellix.com"


# FUNÇOES


# PEGA O TOKEN (PRECISA DEFINIR O SCOPE NECESSARIO PARA O ENDPOINT ESPECIFICO)
def get_token():
    url = "https://auth.trellix.com/auth/realms/IAM/protocol/openid-connect/token"

    header = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    data = {
        "grant_type": "client_credentials",
        "scope": scopes,
    }

    auth = (client_id, secret)

    res = requests.post(url, headers=header, auth=auth, data=data)

    # token = res.json().get('access_token',[])
    token = res.json()["access_token"]

    return token


# BUSCA TODOS OS DEVICES NO EPO
def get_devices():
    resource = "/epo/v2/devices"
    url = base_url + resource

    header = {
        "Content-Type": "application/vnd.api+json",
        "Authorization": f"Bearer {get_token()}",
        "x-api-key": f"{trelix_api}",
    }

    res = requests.get(url, headers=header)

    print(res.json())


# BUSCA OS LOGS NO EPO
def get_events():
    qtd = "10"
    resource = f"/epo/v2/events?page%5Blimit%5D={qtd}"
    url = base_url + resource

    header = {
        "Content-Type": "application/vnd.api+json",
        "Authorization": f"Bearer {get_token()}",
        "x-api-key": f"{trelix_api}",
    }

    res = requests.get(url, headers=header)

    data = res.json()["data"]

    return data


# MANDAR PARA SYSLOG VIA SOCKET
def send_to_syslog(msg):
    # ip do servidor syslog
    ip = "127.0.0.1"
    # Porta do servidor syslog
    port = int(514)

    syslog_message = f"{json.dumps(msg)}"
    adress = (ip, port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.sendto(syslog_message.encode("utf-8"), adress)
    sock.close()


# EXECUÇÃO
events = get_events()

for event in events:
    send_to_syslog(event)
