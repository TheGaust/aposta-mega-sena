from os import system
from random import randint
from time import sleep
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import html5lib
from urllib.request import urlopen

class Loteria:

    def Menu_principal(self):
        system ('cls')
        print('''       Bem Vindo!
        [1] Verificar resultados
        [2] Criar novo jogo aleatório
        [3] Excluir jogo criado
        [4] Sair
        ''')
        acao = input('O que deseja fazer? ')
        return(acao)
    

    
    def Verifica_jogo(self):
        loteria = list()
        lote = list()
        loter = list()
        total = 0
        driver = webdriver.Edge()
        driver.get('https://loterias.caixa.gov.br/Paginas/Mega-Sena.aspx')
        src = driver.page_source
        driver.close()
        soup = BeautifulSoup(src,'html5lib')
        verifica = soup.find('ul', id='ulDezenas')
        numeros = verifica.find_all('li')
        system ('cls')
        for li in numeros:
            lote.append(li.get_text()) 
            loter = [int(elemento) for elemento in lote]
            loteria = [str(elemento) for elemento in loter]
        with open('mega.txt', 'r') as arquivo:
            linhas = arquivo.readlines()
            for linha in linhas:
                linha = linha.strip()
                numeros = [str(num) for num in linha.split()]
                teste = ' '.join(numeros)
                comuns = set(loteria).intersection(numeros)
                numeros_semelhantes = len(comuns)
                if numeros_semelhantes >= 4:
                    total = total + 1
                    print('O jogo: ',teste,' teve ',numeros_semelhantes,' números iguais ao do resultado')
        if total == 0:
            print('Não houve nenhum jogo com 4 acertos ou mais.')
        input('Aperte enter para voltar')
        self.Menu_principal()
            
    
    def Criar_jogo(self):
        numeros = list()
        numero = list()
        num = list()
        teste = list()
        lista = False
        quant = 0
        total = 1
        i = 0
        qua = int(input('Quantos jogos novos deseja criar? '))
        if qua <= 0:
            print('Valor invalido!')
            input('Digite qualquer coisa para voltar.')
            self.Criar_jogo
        else:
            while total <= qua:
                while True:
                    num = randint(1, 60)
                    if num not in numeros:
                        numeros.append(num)
                        quant = quant + 1
                    if quant >= 6:
                        break
                quant = 0
                numeros.sort()
                numero = [str(elemento) for elemento in numeros]
                with open('mega.txt', 'r') as arquivo:
                    for linha in arquivo:
                        num = [str(element) for element in linha.split()]
                        if linha.strip() == numero:
                            lista = True
                            numeros.clear()
                            break
                if not lista:
                    with open('mega.txt', 'a+') as arquivo:
                        arquivo.writelines(' '.join(map(str,numeros)) + '\n')
                    num = [str(elemen) for elemen in numeros]
                    teste = ' '.join(num)
                    print(teste)
                    total = total + 1
                    numeros.clear()
        input()
    
    def Excluir_jogo(self):
        i = 1
        consultas = self.mostrar_lista()
        for consulta in consultas:
            print(f'[{i}] {consulta}')
            i = i+1
        else:
            excluir = input('Qual sequencia deseja deletar?')
            print('para voltar apenas aperte enter')
            self.excluir_sequencia(excluir)
        
    def excluir_sequencia(self, excluir):
        try:
            with open('mega.txt', 'r', ) as arquivo:
                lines = arquivo.readlines()
                ptr = 1
                with open('mega.txt', 'w', ) as arch:
                    for line in lines:
                        if ptr != int(excluir):
                            arch.write(line)
                        ptr += 1
            print('Sequencia ',excluir,' deletada')
            input('Digite qualquer coisa.')
            self.Menu_principal()
        except Exception as error:
            self.Menu_principal()

    def mostrar_lista(self):
        usuarios = []
        try:
            with open('mega.txt', 'r', encoding='latin-1', newline='') as arquivo:
                for linha in arquivo:
                    usuarios.append(linha)
                return usuarios
        except Exception as error:
            return ''

    def run(self):
        acao = self.Menu_principal()

        if acao == '1':
            self.Verifica_jogo()

        elif acao == '2':
            self.Criar_jogo()

        elif acao == '3':
            self.Excluir_jogo()

        else:
            print('Bye')
            input()
            exit()
      
while True:
    Loteria().run()