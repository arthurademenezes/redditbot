# Project Imports
import requests
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup


class TelegramBot:
    def init(self):
        token = 'XXXXX'
        self.url_base = f'https://api.telegram.org/bot{token}/'

    def Iniciar(self):
        update_id = None
        while True:
            atualizacao = self.novasMensagens(update_id)
            dados = atualizacao["result"]
            if dados:
                for dado in dados:
                    update_id = dado['update_id']
                    mensagem = str(dado["message"]["text"])
                    chat_id = dado["message"]["from"]["id"]
                    primeira = int(
                        dado["message"]["message_id"]) == 1
                    resposta = self.resposta(
                        mensagem, primeira)
                    self.responder(resposta, chat_id)

    def novasMensagens(self, update_id):
        link_requisicao = f'{self.url_base}getUpdates?timeout=100'
        if update_id:
            link_requisicao = f'{link_requisicao}&offset={update_id + 1}'
        resultado = requests.get(link_requisicao)
        return json.loads(resultado.content)

    def resposta(self, mensagem, primeira):
        if primeira == True:
            return f'''Olá bem vindo! digite um subreddit'''

        if primeira == False and mensagem.count("link") != 0:
            html = urlopen('https://www.reddit.com/r/' + mensagem.split()[0])
            soup = BeautifulSoup(html, 'html.parser')
            
            
            lista = []
            linhas = soup.find_all('h3')
            for i in linhas:
                lista.append(i.text)


            links_with_text = []
            for a in soup.find_all('a', {"class": "SQnoC3ObvgnGjWt90zD9Z _2INHSNB8V5eaWp4P0rY_mE"}, href=True): 
                if a.text:
                    links_with_text.append('https://www.reddit.com' + a['href'])

            return lista[0:4] + links_with_text[0:4]

    def responder(self, resposta, chat_id):
        tamanho = len(resposta)
        for i in range(4):
            link_requisicao = f'{self.url_base}sendMessage?chat_id={chat_id}&text={resposta[i]}+{resposta[i+4]}'
            requests.get(link_requisicao)


bot = TelegramBot()
bot.Iniciar()
