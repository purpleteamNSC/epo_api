# Trellix EPO Log Collector

Este repositório contém um script Python para coletar logs e informações de dispositivos do Trellix EPO (ePolicy Orchestrator) via API e enviá-los para um servidor Syslog.

## Funcionalidades

- Autenticação na API do Trellix usando client credentials.
- Recuperação de dispositivos cadastrados no EPO.
- Coleta de eventos (logs) do EPO.
- Envio dos logs para um servidor Syslog via socket UDP.

## Pré-requisitos

- Python 3.8+
- Biblioteca `requests`
- Biblioteca `python-dotenv`

## Configuração

1. Crie um arquivo `.env` na raiz do projeto e defina as variáveis de ambiente:

```
CLIENT_ID=seu_client_id
SECRET=seu_segredo
TRELLIX_API=sua_chave_de_api
```

2. Passos para criar as credenciais:
- Acesse: https://auth.ui.trellix.com/dashboard.html
- Clique no avatar no canto superior direto
- Clique em Clientcredentials
- Clique no botao ADD 
- Escolha todos os scopes com epo.

3. Instale as bibliotecas necessárias:

```bash
pip install requests python-dotenv
```

## Uso

Para executar o codigo e enviar para o syslog.

```python
python app.py
```

## Testando o recebimento com Netcat (simulando um syslog)

Instale o Netcat.

```python
sudo apt update
sudo apt install netcat
```

Coloque em modo de escuta para ver os logs.

```python
sudo nc -vklu 514
```

Para executar o script e enviar para o syslog.

```python
python app.py
```

## Estrutura do Código

- `get_token()`: Obtém o token de autenticação necessário para acessar a API.
- `get_devices()`: Faz uma requisição para obter todos os dispositivos do EPO.
- `get_events()`: Coleta os logs mais recentes do EPO.
- `send_to_syslog()`: Envia mensagens para o servidor Syslog.

## Personalização

- Para mudar a quantidade de logs coletados, ajuste a variável `qtd` na função `get_events()`.
- Configure o IP e porta do servidor Syslog na função `send_to_syslog()`.

## Observações

- Certifique-se de ter as permissões corretas configuradas na API do Trellix.
- O escopo de acesso à API pode ser ajustado conforme a necessidade dos endpoints.

## Licença

Este projeto está sob a licença MIT.

