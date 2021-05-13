#IMPORTA DEPENDENCIAS NECESSARIAS
import os
import subprocess as sb
import traceback
import shutil
import PySimpleGUI as sg
from tqdm import tqdm
from time import sleep
from xml.dom import minidom

gpos700SitefConfig = './Projetos Build/SITEF/odhenPOS/config.xml'
gpos700SitefScriptBat = './buildsitef.bat'

gpos700RedeConfig = './Projetos Build/REDE/odhenPOS/config.xml'
gpos700RedeScriptBat = './buildrede.bat'

playStoreConfig = './Projetos Build/playstore/odhenPOS/config.xml'
playStoreScriptBat = './buildplaystore.bat'

prodDir = './projeto/'
prodDirOdhen = './projeto/odhenPOS/'

class Util:
    def __init__(self):
        print('init Util')

    def dirIsEmpty(self, path):
        if len(os.listdir(path)) == 0:
            return True
        else:
            return False

    def mudaXml(self, path, tag, attr, value):
        try:
            xmldoc = minidom.parse(path)
            tags = xmldoc.getElementsByTagName(tag)
            for item in tags:
                strItem = str(item.attributes[attr].value)
                item.attributes[attr].value = strItem.replace(item.attributes[attr].value, str(value))
            with open(path, "w") as f:
                xmldoc.writexml(f, indent='', encoding="utf-8")
        except Exception as e:
            sg.popup_error(f'XML ERROR!   ', e)

    def deleteDir(self, path):
        print('conteudo de', path, f'deletado!{os.linesep}')
        try:
            shutil.rmtree(path)
        except Exception as e:
            sg.popup_error(f'DELETE DIR ERROR!   ', e)

    def createDir(self, path, permission):
        print('diretorio ', path, f' criado!{os.linesep}')
        try:
            os.mkdir(path, mode=permission)
        except Exception as e:
            sg.popup_error(f'CREATE DIR ERROR!   ', e)

    def barraDeCarregamentoDIR(self, path, pathAux):
        srcCount = os.listdir(path)
        dstCount = os.listdir(pathAux)
        qtd = len(srcCount)
        for i in tqdm(range(qtd)):
            for item in srcCount:
                if item in dstCount:
                    #sg.Print(tqdm(range(qtd)))
                    qtd = qtd - 1
                    sleep(0.01)

    def tiraPontoNmr(self, nmr):
        strN = str(nmr).replace('.', '')
        nmr = int(strN)
        return nmr

    def contaPontosVersao(self, version):
        strV = str(version)
        qtdPontos = 0
        for dot in strV:
            if '.' in dot:
                qtdPontos = qtdPontos + 1
        return qtdPontos
#class Util

class geradorDeApps:
    def __init__(self, cieloLio, gpos700Sitef, gpos700Rede, playStore, packageName, version, mobileFolderPath):
        self.util = Util()
        self.cieloLio = cieloLio
        self.gpos700Sitef = gpos700Sitef
        self.gpos700Rede = gpos700Rede
        self.playStore = playStore
        self.packageName = packageName
        self.version = version
        self.mobileFolderPath = mobileFolderPath + '/'

        self.geraApp()
    #__init__

    def geraApp(self):
        if os.path.isdir(prodDir) == False:
            self.util.createDir(prodDir, 0o777)
        elif self.util.dirIsEmpty(prodDir) == False:
            self.util.deleteDir(prodDir)
            self.util.createDir(prodDir, 0o777)

        auxPath = prodDirOdhen + 'mobile/'
        self.util.deleteDir(prodDir)
        try:
            sg.Print('copiando...')
            shutil.copytree(self.mobileFolderPath, auxPath)
            #self.util.barraDeCarregamentoDIR(self.mobileFolderPath, auxPath)
        except Exception as e:
            sg.popup_error('Erro na etapa de copiar diretório: ', e)

        #if self.cieloLio == True:
            #try:
                #print('validiu')
            #except Exception as e:
                #sg.popup_error('GENERATE APP ERROR!   ', e)
        if self.gpos700Sitef == True:
            try:
                self.util.mudaXml(gpos700SitefConfig, 'widget', 'android-versionCode', self.util.tiraPontoNmr(self.version))
                self.util.mudaXml(gpos700SitefConfig, 'widget', 'id', self.packageName)
                self.util.mudaXml(gpos700SitefConfig, 'widget', 'version', self.version)
                sb.call(gpos700SitefScriptBat)
            except Exception as e:
                sg.popup_error('GENERATE APP ERROR!   ', e)
        if self.gpos700Rede == True:
            try:
                self.util.mudaXml(gpos700RedeConfig, 'widget', 'android-versionCode', self.util.tiraPontoNmr(self.version))
                self.util.mudaXml(gpos700RedeConfig, 'widget', 'id', self.packageName)
                self.util.mudaXml(gpos700RedeConfig, 'widget', 'version', self.version)
                sb.call(gpos700RedeScriptBat)
            except Exception as e:
                sg.popup_error('GENERATE APP ERROR!   ', e)
        if self.playStore == True:
            try:
                self.util.mudaXml(playStoreConfig, 'widget', 'android-versionCode', self.util.tiraPontoNmr(self.version))
                self.util.mudaXml(playStoreConfig, 'widget', 'id', self.packageName)
                self.util.mudaXml(playStoreConfig, 'widget', 'version', self.version)
                sb.call(playStoreScriptBat)
            except Exception as e:
                sg.popup_error('GENERATE APP ERROR!   ', e)
    #geraApp
#class geradorDeApps

class TelaPython:
    #CRIA FUNCAO CONSTRUTOR
    def __init__(self):
        self.utilTela = Util()
        layout = [
            #CRIA ELEMENTO NA TELA COM UM INPUT PARA RECEBER DADOS
            [sg.Text('Gerador de Aplicativos OdhenPOS', size=(60, 5))],
            [sg.Text('Selecione o diretório "mobile/": '),
             sg.InputText('caminho...', size=(40, 5), key='mobileFolderPath'),
             sg.FolderBrowse(target='mobileFolderPath'),
             sg.Stretch()],
            #[sg.Checkbox('Cielo Lio', default=False, key='cieloLio')],
            [sg.Checkbox('Gpos 700 - Sitef', default=False, key='gpos700Sitef')],
            [sg.Checkbox('Gpos 700 - Rede', default=False, key='gpos700Rede')],
            [sg.Checkbox('Play Store', default=False, key='playStore')],
            [sg.Text('Nome do pacote: ', size=(10, 0)),
             sg.Input(size=(30, 0), default_text='com.odhen.POS', key='packageName')],
            [sg.Text('Versão: ', size=(10, 0)), sg.Input(size=(30, 0), key='version')],
            [sg.Submit('Gerar', size=(30, 0), key='generateAppBtn')],
            #[sg.ProgressBar(50, orientation='h', size=(30, 10), key='progBar')]
        ]
        #CRIA A TELA E COLOCA OS ELEMENTOS DE LAYOUT NELA
        self.janela = sg.Window('Gerador de Aplicativos OdhenPOS').layout(layout)
    #FECHA __init__

    def Iniciar(self):
        try:
            while True:
                # EXTRAIR DADOS DA TELA
                self.event, self.values = self.janela.Read()
                #cieloLio = self.values['cieloLio']
                cieloLio = False
                gpos700Sitef = self.values['gpos700Sitef']
                gpos700Rede = self.values['gpos700Rede']
                playStore = self.values['playStore']
                packageName = self.values['packageName']
                version = self.values['version']
                mobileFolderPath = self.values['mobileFolderPath']
                #progBar = self.values['progBar']
                if self.event == 'generateAppBtn':
                    if cieloLio or gpos700Sitef or gpos700Rede or playStore and packageName and version:
                        if mobileFolderPath == 'caminho...' or mobileFolderPath == '':
                            sg.popup_error(f'Selecione o caminho da "mobile/"!')
                        elif len(str(self.utilTela.tiraPontoNmr(version))) < 5 or len(str(self.utilTela.tiraPontoNmr(version))) >  10:
                            sg.popup_error(f'ERRO: Versão digitada inválida! Min: 5 {os.linesep}Max; 10')
                        elif self.utilTela.contaPontosVersao(version) != 4:
                            sg.popup_error(f'ERRO: Digite a versão com pontos (.) !')
                        else:
                            gerador = geradorDeApps(cieloLio, gpos700Sitef, gpos700Rede, playStore, packageName, version, mobileFolderPath)
                    else:
                        sg.popup_error(f'Algumas opções ou campos não foram preenchidos!')
                #elif self.event == 'prodSelectBtn':
                    #print('selecionar diretorio')
            #FECHA while
        except Exception as e:
            tb = traceback.format_exc()
            #print(f'Um erro aconteceu.  Aqui está a informação:', e, tb, f'{os.linesep}')
            #print(f'ERROR: AN EXCEPTION OCCURRED!', e, tb)
            sg.Print(f'Um erro aconteceu.  Aqui está a informação:', e, tb, f'{os.linesep}')
            sg.popup_error(f'ERROR: AN EXCEPTION OCCURRED!', e, tb)
    # FECHA Iniciar
#class TelaPython

tela = TelaPython()
tela.Iniciar()