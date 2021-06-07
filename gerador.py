#IMPORTA DEPENDENCIAS NECESSARIAS
import os
import subprocess as sb
import json
from jproperties import Properties
import traceback
import shutil
import PySimpleGUI as sg
from tqdm import tqdm
from time import sleep
from xml.dom import minidom
import logging

#diretorios
#gpos 700 sitef
gpos700SitefConfig = 'Projetos Build/SITEF/odhenPOS/config.xml'
gpos700SitefScriptBat = r'buildsitef.bat'

#gpos 700 rede
gpos700RedeConfig = 'Projetos Build/REDE/odhenPOS/config.xml'
gpos700RedeScriptBat = r'buildrede.bat'

#playstore
playStoreConfig = 'Projetos Build/playstore/odhenPOS/config.xml'
playStoreScriptBat = r'buildplaystore.bat'

#pagseguro
pagSeguroConfig = 'Projetos Build/PAGSEGURO/odhenPOS/config.xml'
pagSeguroScriptBat = r'buildpagseguro.bat'

#getnet
getnetConfig = 'Projetos Build/GETNET/odhenPOS/config.xml'
getnetScriptBat = r'buildgetnet.bat'

#cielo
#cieloConfig = 'Projetos Build/LIO/odhenPOS/build.properties'
cieloPropDir = 'Projetos Build/LIO/odhenPOS/'
cieloScriptBat = r'buildlio.bat'

#diretorios build e copia
prodDir = 'projeto/'
prodDirOdhen = 'projeto/odhenPOS/'

apkDir = 'Aplicativos/cordova/'


class Util:
    #construtor
    def __init__(self):
        print('init Util')

    def dirIsEmpty(self, path):
        if len(os.listdir(path)) == 0:
            return True
        else:
            return False

    #altera valores das tags passadas para a funcao
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

    #renderiza a barra de carregamento. funciona apenas em desenvolvimento
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

    #retira pontos de numeros com ponto
    def tiraPontoNmr(self, nmr):
        strN = str(nmr).replace('.', '')
        nmr = int(strN)
        return nmr

    #abre json e coloca as informaçoes em variavel
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

    #ao final do build, gera uma mensagem
    def generatedMessage(self, cieloLio, cieloLio_teste, gpos700Sitef, gpos700Rede, gpos700Rede_giraffas,
                                   gpos700Rede_react_saas, playStore, pagseguro, getnet):
        if cieloLio == True:
            aux = apkDir + 'cielo lio'
        if cieloLio_teste == True:
            aux = apkDir + 'cielo lio teste'
        if gpos700Sitef == True:
            aux = apkDir + 'sitef'
        if gpos700Rede == True:
            aux = apkDir + 'rede'
        if gpos700Rede_giraffas == True:
            aux = apkDir + 'rede giraffas'
        if gpos700Rede_react_saas == True:
            aux = apkDir + 'rede saas'
        if playStore == True:
            aux = apkDir + 'playstore'
        if pagseguro == True:
            aux = apkDir + 'pagseguro'
        if getnet == True:
            aux = apkDir + 'getnet'
        sg.Print(f'APK gerado!{os.linesep}'
                 f'Verifique diretóriode build. Apk: ', aux, 'gerado!.'
                 f'{os.linesep}')

    #pega o log do argumento passado
    def getBatLog(self, e):
        logger = logging.getLogger('mylogger')
        logger.setLevel(logging.DEBUG)
        #temos também:
        #logging.INFO
        handler = logging.FileHandler('genApkLog.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        logger.info(e)

    #pega dados de arquivo ".properties" e coloca em variavel
    def parseDotProperties(self, dotPropPath):
        p = Properties()
        with open(dotPropPath, "rb") as f:
            p.load(f, "utf-8")
            return p

    #altera arquivos ".properties"
    def changeDotProperties(self, dotPropPath, prop, value):
        p = Properties()
        p[prop] = value
        with open(dotPropPath, "w") as f:
            p.store(f, encoding="utf-8")

    #cria arquivo ".txt"
    def createTXTFile(self, filePath, txt):
        with open(filePath, "w") as f:
            f.write(txt)

    #cria ".txt", deleta ".properties" e altera para ".txt" para ""
    def treatDotProperties(self):
        # conteudo a ser posto no arquivo ".properties"
        txt = f'ext.set("APK_NAME", "odhenPOS"){os.linesep}' \
              f'ext.set("APP_NAME", "Odhen POS"){os.linesep}' \
              f'ext.set("ASSETS_DIR", ["bower_components/assets", "bower_components/templates", "mobile"]){os.linesep}' \
              f'ext.set("WEBVIEW_URL", "mobile/index.html"){os.linesep}' \
              f'ext.set("VERSION_CODE", {self.util.tiraPontoNmr(self.version)}){os.linesep}' \
              f'ext.set("VERSION_NAME", "{self.version}"){os.linesep}' \
              f'ext.set("APPLICATION_ID", "{self.packageName}"){os.linesep}' \
              f'ext.set("APP_ICON", "mobile/images/favicon.png"){os.linesep}' \
              f'ext.set("STORE_FILE", "playStoreKey"){os.linesep}' \
              f'ext.set("STORE_PASSWORD", "teknisa"){os.linesep}' \
              f'ext.set("KEY_ALIAS", "odhen"){os.linesep}' \
              f'ext.set("KEY_PASSWORD", "teknisa"){os.linesep}'
        try:
            # trata ".properties"
            auxPath = cieloPropDir + 'build.txt'
            self.util.createTXTFile(auxPath, txt)
            # deleta arquivo
            os.remove(cieloPropDir + 'build.properties')
            # remove extensão ".txt" para mudar para ".properties"
            base = os.path.splitext(auxPath)[0]
            # adiciona extensao
            os.rename(auxPath, base + ".properties")
        except Exception as e:
            self.util.getBatLog(e)
            sg.popup_error('treatDotProperties ERROR: ', e)
#class Util

class geradorDeApps:
    def __init__(self, cieloLio, cieloLio_teste, gpos700Sitef, gpos700Rede, gpos700Rede_giraffas, gpos700Rede_react_saas, playStore, pagseguro, getnet, packageName, version, mobileFolderPath):
        self.util = Util()
        self.cieloLio = cieloLio
        self.cieloLio_teste = cieloLio_teste
        self.gpos700Sitef = gpos700Sitef
        self.gpos700Rede = gpos700Rede
        self.gpos700Rede_giraffas = gpos700Rede_giraffas
        self.gpos700Rede_react_saas = gpos700Rede_react_saas
        self.playStore = playStore
        self.pagseguro = pagseguro
        self.getnet = getnet
        self.packageName = packageName
        self.version = version
        self.mobileFolderPath = mobileFolderPath + '/'

        self.geraApp()
    #__init__

    #gera o apk
    def geraApp(self):
        #verifica se diretorio existe e se esta vazio
        if os.path.isdir(prodDir) == False:
            self.util.createDir(prodDir, 0o777)
        elif self.util.dirIsEmpty(prodDir) == False:
            self.util.deleteDir(prodDir)
            self.util.createDir(prodDir, 0o777)

        #completa diretorio
        auxPath = prodDirOdhen + 'mobile/'
        self.util.deleteDir(prodDir)
        try:
            sg.Print(f'Copiando diretorio:', self.mobileFolderPath, '; para:', auxPath, f';{os.linesep}'
                     f'Aguarde...')
            sleep(0.5)
            #copia arquivos de "self.mobileFolderPath" para "auxPath"
            shutil.copytree(self.mobileFolderPath, auxPath)
        except Exception as e:
            self.util.getBatLog(e)
            sg.popup_error('Erro na etapa de copiar diretório: ', e)

        #valida quais projetos devem ser gerados e chama ".bat"
        ###
        if self.cieloLio == True:
            if self.packageName:
                self.packageName = self.packageName
            else:
                self.packageName = 'com.odhen.POS'
            try:
                #trata ".properties"
                self.util.treatDotProperties()
                #chama ".bat"
                sb.call([cieloScriptBat])
            except Exception as e:
                self.util.getBatLog(e)
                sg.popup_error('GENERATE LIO APP ERROR!   ', e)
        if self.cieloLio_teste == True:
            if self.packageName:
                self.packageName = self.packageName
            else:
                self.packageName = 'com.odhen.waiterEnterprise'
            try:
                # trata ".properties"
                self.util.treatDotProperties()
                sb.call([cieloScriptBat])
            except Exception as e:
                self.util.getBatLog(e)
                sg.popup_error('GENERATE LIO TESTE APP ERROR!   ', e)
        if self.gpos700Sitef == True:
            if self.packageName:
                self.packageName = self.packageName
            else:
                self.packageName = 'com.odhen.POS'
            try:
                #altera valores das tags passadas do xml
                self.util.mudaXml(gpos700SitefConfig, 'widget', 'android-versionCode', self.util.tiraPontoNmr(self.version))
                self.util.mudaXml(gpos700SitefConfig, 'widget', 'id', self.packageName)
                self.util.mudaXml(gpos700SitefConfig, 'widget', 'version', self.version)
                sb.call([gpos700SitefScriptBat])
            except Exception as e:
                self.util.getBatLog(e)
                sg.popup_error('GENERATE SITEF APP ERROR!   ', e)
        if self.gpos700Rede == True:
            if self.packageName:
                self.packageName = self.packageName
            else:
                self.packageName = 'com.odhen.POS'
            try:
                # altera valores das tags passadas do xml
                self.util.mudaXml(gpos700RedeConfig, 'widget', 'android-versionCode', self.util.tiraPontoNmr(self.version))
                self.util.mudaXml(gpos700RedeConfig, 'widget', 'id', self.packageName)
                self.util.mudaXml(gpos700RedeConfig, 'widget', 'version', self.version)
                sb.call([gpos700RedeScriptBat])
            except Exception as e:
                self.util.getBatLog(e)
                sg.popup_error('GENERATE REDE APP ERROR!   ', e)
        if self.gpos700Rede_giraffas == True:
            if self.packageName:
                self.packageName = self.packageName
            else:
                self.packageName = 'com.odhen.POSat'
            try:
                # altera valores das tags passadas do xml
                self.util.mudaXml(gpos700RedeConfig, 'widget', 'android-versionCode', self.util.tiraPontoNmr(self.version))
                self.util.mudaXml(gpos700RedeConfig, 'widget', 'id', 'com.odhen.POSat')
                self.util.mudaXml(gpos700RedeConfig, 'widget', 'version', self.version)
                sb.call([gpos700RedeScriptBat])
            except Exception as e:
                self.util.getBatLog(e)
                sg.popup_error('GENERATE REDE APP ERROR!   ', e)
        if self.gpos700Rede_react_saas == True:
            if self.packageName:
                self.packageName = self.packageName
            else:
                self.packageName = 'com.odhenpos'
            try:
                # altera valores das tags passadas do xml
                self.util.mudaXml(gpos700RedeConfig, 'widget', 'android-versionCode', self.util.tiraPontoNmr(self.version))
                self.util.mudaXml(gpos700RedeConfig, 'widget', 'id', 'com.odhenpos')
                self.util.mudaXml(gpos700RedeConfig, 'widget', 'version', self.version)
                sb.call([gpos700RedeScriptBat])
            except Exception as e:
                self.util.getBatLog(e)
                sg.popup_error('GENERATE REDE APP ERROR!   ', e)
        if self.playStore == True:
            if self.packageName:
                self.packageName = self.packageName
            else:
                self.packageName = 'com.odhen.POS'
            try:
                # altera valores das tags passadas do xml
                self.util.mudaXml(playStoreConfig, 'widget', 'android-versionCode', self.util.tiraPontoNmr(self.version))
                self.util.mudaXml(playStoreConfig, 'widget', 'id', self.packageName)
                self.util.mudaXml(playStoreConfig, 'widget', 'version', self.version)
                sb.call([playStoreScriptBat])
            except Exception as e:
                self.util.getBatLog(e)
                sg.popup_error('GENERATE PLAYSTORE APP ERROR!   ', e)
        if self.pagseguro == True:
            if self.packageName:
                self.packageName = self.packageName
            else:
                self.packageName = 'com.odhen.POS'
            try:
                # altera valores das tags passadas do xml
                self.util.mudaXml(pagSeguroConfig, 'widget', 'android-versionCode', self.util.tiraPontoNmr(self.version))
                self.util.mudaXml(pagSeguroConfig, 'widget', 'id', self.packageName)
                self.util.mudaXml(pagSeguroConfig, 'widget', 'version', self.version)
                sb.call([pagSeguroScriptBat])
            except Exception as e:
                self.util.getBatLog(e)
                sg.popup_error('GENERATE PLAYSTORE APP ERROR!   ', e)
        if self.getnet == True:
            if self.packageName:
                self.packageName = self.packageName
            else:
                self.packageName = 'com.odhen.POS'
            try:
                # altera valores das tags passadas do xml
                self.util.mudaXml(getnetConfig, 'widget', 'android-versionCode', self.util.tiraPontoNmr(self.version))
                self.util.mudaXml(getnetConfig, 'widget', 'id', self.packageName)
                self.util.mudaXml(getnetConfig, 'widget', 'version', self.version)
                sb.call([getnetScriptBat])
            except Exception as e:
                self.util.getBatLog(e)
                sg.popup_error('GENERATE PLAYSTORE APP ERROR!   ', e)

        #gera mensagem ao final do build
        self.util.generatedMessage(self.cieloLio, self.cieloLio_teste, self.gpos700Sitef, self.gpos700Rede, self.gpos700Rede_giraffas,
                                   self.gpos700Rede_react_saas, self.playStore, self.pagseguro, self.getnet)
    #geraApp
#class geradorDeApps

class TelaPython:
    #CONSTRUTOR
    def __init__(self):
        self.utilTela = Util()
        layout = [
            #CRIA ELEMENTO NA TELA COM UM INPUT PARA RECEBER DADOS
            [sg.Submit('Help', size=(3, 0), key='help')],
            [sg.Text('', size=(60, 1))],
            [sg.Text('Selecione o diretório "mobile/": '),
             sg.InputText('caminho...', size=(40, 5), key='mobileFolderPath'),
             sg.FolderBrowse(target='mobileFolderPath'),
             sg.Stretch()],
            [sg.Text('', size=(60, 1))],
            [sg.Checkbox('Cielo Lio', default=False, key='cieloLio')],
            [sg.Checkbox('Cielo Lio (OdhenPOS_Teste)', default=False, key='cieloLio_teste')],
            [sg.Checkbox('Gpos 700 - Sitef', default=False, key='gpos700Sitef')],
            [sg.Checkbox('Gpos 700 - Rede (Versão padrão)', default=False, key='gpos700Rede')],
            [sg.Checkbox('Gpos 700 - Rede (OdhenPOS Beta - Utilizado no Giraffas, Produção, etc.)', default=False, key='gpos700Rede_giraffas')],
            [sg.Checkbox('Gpos 700 - Rede (React - Utilizado no SAAS - odhenpos.teknisa.cloud)', default=False, key='gpos700Rede_react_saas')],
            [sg.Checkbox('Play Store', default=False, key='playStore')],
            [sg.Checkbox('PagSeguro', default=False, key='pagseguro')],
            [sg.Checkbox('Getnet', default=False, key='getnet')],
            [sg.Text('', size=(60, 1))],
            [sg.Text('Nome do pacote: ', size=(10, 0)),
             sg.Input(size=(30, 0), key='packageName')],
            [sg.Text('Versão: ', size=(10, 0)), sg.Input(size=(30, 0), key='version')],
            [sg.Submit('Gerar', size=(30, 0), key='generateAppBtn')]
        ]
        #CRIA A TELA E COLOCA OS ELEMENTOS DE LAYOUT NELA
        self.janela = sg.Window('Gerador de Aplicativos OdhenPOS').layout(layout)
    #FECHA __init__

    def Iniciar(self):
        try:
            while True:
                # EXTRAIR DADOS DA TELA
                self.event, self.values = self.janela.Read()
                cieloLio = self.values['cieloLio']
                cieloLio_teste = self.values['cieloLio_teste']
                gpos700Sitef = self.values['gpos700Sitef']
                gpos700Rede = self.values['gpos700Rede']
                gpos700Rede_giraffas = self.values['gpos700Rede_giraffas']
                gpos700Rede_react_saas = self.values['gpos700Rede_react_saas']
                playStore = self.values['playStore']
                pagseguro = self.values['pagseguro']
                getnet = self.values['getnet']
                packageName = self.values['packageName']
                version = self.values['version']
                mobileFolderPath = self.values['mobileFolderPath']
                #valida qual botao foi pressionado
                if self.event == 'generateAppBtn':
                    #verifica se algum projeto foi selecionado e se a versão foi digitada
                    if cieloLio or cieloLio_teste or gpos700Sitef or gpos700Rede or gpos700Rede_giraffas or gpos700Rede_react_saas or playStore or pagseguro or getnet and version:
                        #verifica se a string foi alterada
                        if mobileFolderPath == 'caminho...' or mobileFolderPath == '':
                            sg.popup_error(f'Selecione o caminho da "mobile/"!')
                        #se a versao é menor q 5 ou maior q 10
                        elif len(str(self.utilTela.tiraPontoNmr(version))) < 5 or len(str(self.utilTela.tiraPontoNmr(version))) >  10:
                            sg.popup_error(f'ERRO: Versão digitada inválida! Min: 5 {os.linesep}Max; 10')
                        #se tem 4 pontos
                        elif self.utilTela.contaPontosVersao(version) != 4:
                            sg.popup_error(f'ERRO: Digite a versão com pontos (.) !')
                        else:
                            #chama gerador com as opções passadas da tela
                            #gera o apk
                            gerador = geradorDeApps(cieloLio, cieloLio_teste, gpos700Sitef, gpos700Rede, gpos700Rede_giraffas, gpos700Rede_react_saas, playStore, pagseguro, getnet, packageName, version, mobileFolderPath)
                    else:
                        sg.popup_error(f'Algumas opções ou campos não foram preenchidos!')
                elif self.event == 'help':
                    #tutorial de uso
                    sg.Print(f'Olá! Esse é o tutorial de uso do sistema.{os.linesep}'
                             f'Para gerar um apk, selecione o caminho do diretótio "mobile/" que fica dentro do "odhenPOS/".{os.linesep}'
                             f'Após selecionar o caminho do diretório, marque as caixinhas dos apks que deseja gerar. '
                             f'Podem ser marcadas várias de uma vez...{os.linesep}'
                             f'Depois de selecionar o caminho as caixinhas, clique no botão "Gerar" e o sistema irá iniciar o processo de geração.'
                             f'Caso ocorra algum erro, esse provavelmente aparecerá na tela. '
                             f'Também temos um log para registrar falhas: "genApkLog.log", que fica na "buildapk/".{os.linesep}{os.linesep}'
                             f'Agradecido com a preferência!{os.linesep}{os.linesep}'
                             f'Precisando de mais ajuda, me chama: 31 99818-1708')
            #FECHA while
        except Exception as e:
            #pega erros
            self.utilTela.getBatLog(e)
            tb = traceback.format_exc()
            sg.Print(f'Um erro aconteceu.  Aqui está a informação:', e, tb, f'{os.linesep}')
            sg.popup_error(f'ERROR: AN EXCEPTION OCCURRED!', e, tb)
    # FECHA Iniciar
#class TelaPython

#instancia e chama funcai iniciar
tela = TelaPython()
tela.Iniciar()