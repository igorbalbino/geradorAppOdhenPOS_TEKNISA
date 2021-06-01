#IMPORTA DEPENDENCIAS NECESSARIAS
import os
import subprocess as sb
import json
import traceback
import shutil
import PySimpleGUI as sg
from tqdm import tqdm
from time import sleep
from xml.dom import minidom
import logging

gpos700SitefConfig = 'Projetos Build/SITEF/odhenPOS/config.xml'
gpos700SitefScriptBat = r'buildsitef.bat'

gpos700RedeConfig = 'Projetos Build/REDE/odhenPOS/config.xml'
gpos700RedeScriptBat = r'buildrede.bat'

playStoreConfig = 'Projetos Build/playstore/odhenPOS/config.xml'
playStoreScriptBat = r'buildplaystore.bat'

pagSeguroConfig = 'Projetos Build/PAGSEGURO/odhenPOS/config.xml'
pagSeguroScriptBat = r'buildpagseguro.bat'

getnetConfig = 'Projetos Build/GETNET/odhenPOS/config.xml'
getnetScriptBat = r'buildgetnet.bat'

#cieloConfig = 'Projetos Build/LIO/odhenPOS/odhen-webview/config.xml'
cieloScriptBat = r'buildlio.bat'

prodDir = 'projeto/'
prodDirOdhen = 'projeto/odhenPOS/'

apkDir = 'Aplicativos/cordova/'

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
        sg.Print('Conteudo de', path, f'deletado!{os.linesep}')
        try:
            shutil.rmtree(path)
        except Exception as e:
            sg.popup_error(f'DELETE DIR ERROR!   ', e)

    def createDir(self, path, permission):
        sg.Print('Diretorio ', path, f' criado!{os.linesep}')
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

    def retornaJson(self, dataJson):
        try:
            emailInfo = open(dataJson)
            wjson = emailInfo.read()
            wjdata = json.loads(wjson)
            return wjdata
        except Exception as e:
            sg.popup_error(f'JSON ERROR!', e)

    def contaPontosVersao(self, version):
        strV = str(version)
        qtdPontos = 0
        for dot in strV:
            if '.' in dot:
                qtdPontos = qtdPontos + 1
        return qtdPontos

    def generatedMessage(self, cieloLio, gpos700Sitef, gpos700Rede, playStore):
        if cieloLio == True:
            aux = apkDir + 'cielo lio'
        if gpos700Sitef == True:
            aux = apkDir + 'sitef/'
        if gpos700Rede == True:
            aux = apkDir + 'rede/'
        if playStore == True:
            aux = apkDir + 'playstore/'
        sg.Print(f'APK gerado!{os.linesep}'
                 f'Verifique diretório: ', aux, 'para pegar arquivo APK.'
                 f'{os.linesep}')

    def getBatLog(self, func):
        logger = logging.getLogger('mylogger')
        logger.setLevel(logging.DEBUG)
        #temos também:
        #logging.INFO
        handler = logging.FileHandler('genApkLog.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        logger.info(func)
#class Util

class geradorDeApps:
    def __init__(self, cieloLio, gpos700Sitef, gpos700Rede, playStore, pagseguro, getnet, packageName, version, mobileFolderPath):
        self.util = Util()
        self.cieloLio = cieloLio
        self.gpos700Sitef = gpos700Sitef
        self.gpos700Rede = gpos700Rede
        self.playStore = playStore
        self.pagseguro = pagseguro
        self.getnet = getnet
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
            sg.Print(f'Copiando diretorio:', self.mobileFolderPath, '; para:', auxPath, f';{os.linesep}'
                     f'Aguarde...')
            sleep(0.5)
            shutil.copytree(self.mobileFolderPath, auxPath)
            #self.util.barraDeCarregamentoDIR(self.mobileFolderPath, auxPath)
        except Exception as e:
            sg.popup_error('Erro na etapa de copiar diretório: ', e)

        if self.cieloLio == True:
            try:
                #self.util.mudaXml(cieloConfig, 'widget', 'android-versionCode',self.util.tiraPontoNmr(self.version))
                #self.util.mudaXml(cieloConfig, 'widget', 'id', self.packageName)
                #self.util.mudaXml(cieloConfig, 'widget', 'version', self.version)
                sb.call([cieloScriptBat])
            except Exception as e:
                error = f'Script build error{os.linesep}' + e
                self.util.getBatLog(error)
                sg.popup_error('GENERATE LIO APP ERROR!   ', e)
        if self.gpos700Sitef == True:
            try:
                self.util.mudaXml(gpos700SitefConfig, 'widget', 'android-versionCode', self.util.tiraPontoNmr(self.version))
                self.util.mudaXml(gpos700SitefConfig, 'widget', 'id', self.packageName)
                self.util.mudaXml(gpos700SitefConfig, 'widget', 'version', self.version)
                sb.call([gpos700SitefScriptBat])
            except Exception as e:
                error = f'Script build error{os.linesep}' + e
                self.util.getBatLog(error)
                sg.popup_error('GENERATE SITEF APP ERROR!   ', e)
        if self.gpos700Rede == True:
            try:
                self.util.mudaXml(gpos700RedeConfig, 'widget', 'android-versionCode', self.util.tiraPontoNmr(self.version))
                self.util.mudaXml(gpos700RedeConfig, 'widget', 'id', self.packageName)
                self.util.mudaXml(gpos700RedeConfig, 'widget', 'version', self.version)
                sb.call([gpos700RedeScriptBat])
            except Exception as e:
                error = f'Script build error{os.linesep}' + e
                self.util.getBatLog(error)
                sg.popup_error('GENERATE REDE APP ERROR!   ', e)
        if self.playStore == True:
            try:
                self.util.mudaXml(playStoreConfig, 'widget', 'android-versionCode', self.util.tiraPontoNmr(self.version))
                self.util.mudaXml(playStoreConfig, 'widget', 'id', self.packageName)
                self.util.mudaXml(playStoreConfig, 'widget', 'version', self.version)
                sb.call([playStoreScriptBat])
            except Exception as e:
                error = f'Script build error{os.linesep}' + e
                self.util.getBatLog(error)
                sg.popup_error('GENERATE PLAYSTORE APP ERROR!   ', e)
        if self.pagseguro == True:
            try:
                self.util.mudaXml(pagSeguroConfig, 'widget', 'android-versionCode', self.util.tiraPontoNmr(self.version))
                self.util.mudaXml(pagSeguroConfig, 'widget', 'id', self.packageName)
                self.util.mudaXml(pagSeguroConfig, 'widget', 'version', self.version)
                sb.call([pagSeguroScriptBat])
            except Exception as e:
                error = f'Script build error{os.linesep}' + e
                self.util.getBatLog(error)
                sg.popup_error('GENERATE PLAYSTORE APP ERROR!   ', e)
        if self.getnet == True:
            try:
                self.util.mudaXml(getnetConfig, 'widget', 'android-versionCode', self.util.tiraPontoNmr(self.version))
                self.util.mudaXml(getnetConfig, 'widget', 'id', self.packageName)
                self.util.mudaXml(getnetConfig, 'widget', 'version', self.version)
                sb.call([getnetScriptBat])
            except Exception as e:
                error = f'Script build error{os.linesep}' + e
                self.util.getBatLog(error)
                sg.popup_error('GENERATE PLAYSTORE APP ERROR!   ', e)

        self.util.generatedMessage(self.cieloLio, self.gpos700Sitef, self.gpos700Rede, self.playStore)
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
            [sg.Checkbox('PagSeguro', default=False, key='pagseguro')],
            [sg.Checkbox('Getnet', default=False, key='getnet')],
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
                pagseguro = self.values['pagseguro']
                getnet = self.values['getnet']
                packageName = self.values['packageName']
                version = self.values['version']
                mobileFolderPath = self.values['mobileFolderPath']
                #progBar = self.values['progBar']
                if self.event == 'generateAppBtn':
                    if cieloLio or gpos700Sitef or gpos700Rede or playStore and packageName and pagseguro and getnet and version:
                        if mobileFolderPath == 'caminho...' or mobileFolderPath == '':
                            sg.popup_error(f'Selecione o caminho da "mobile/"!')
                        elif len(str(self.utilTela.tiraPontoNmr(version))) < 5 or len(str(self.utilTela.tiraPontoNmr(version))) >  10:
                            sg.popup_error(f'ERRO: Versão digitada inválida! Min: 5 {os.linesep}Max; 10')
                        elif self.utilTela.contaPontosVersao(version) != 4:
                            sg.popup_error(f'ERRO: Digite a versão com pontos (.) !')
                        else:
                            gerador = geradorDeApps(cieloLio, gpos700Sitef, gpos700Rede, playStore, pagseguro, getnet, packageName, version, mobileFolderPath)
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