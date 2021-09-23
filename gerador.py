#IMPORTA DEPENDENCIAS NECESSARIAS
import os
from os.path import expanduser
from os.path import exists
import subprocess as sb
import json
from jproperties import Properties
from pathlib import Path
import traceback
import shutil
import PySimpleGUI as sg
from tqdm import tqdm
from time import sleep
from xml.dom import minidom
import logging
#import asyncio

#diretorios
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

#gpos 700 sitef
gpos700SitefConfig = 'Projetos Build/SITEF/odhenPOS/config.xml'
gpos700SitefScriptBat = ROOT_DIR + r'\\Scripts\\buildsitef.bat'
gpos700SitefAPK = 'Aplicativos/cordova/sitef/odhenPOS-SITEF.apk'
gpos700SitefAPKd = 'Aplicativos/cordova/sitef/odhenPOS-SITEF-debug.apk'

#gpos 700 rede
gpos700RedeConfig = 'Projetos Build/REDE/odhenPOS/config.xml'
gpos700RedeScriptBat = ROOT_DIR + r'\\Scripts\\buildrede.bat'
gpos700RedeAPK = 'Aplicativos/cordova/rede/odhenPOS-REDE.apk'
gpos700RedeAPKd = 'Aplicativos/cordova/rede/odhenPOS-REDE-debug.apk'

#playstore
playStoreConfig = 'Projetos Build/playstore/odhenPOS/config.xml'
playStoreScriptBat = ROOT_DIR + r'\\Scripts\\buildplaystore.bat'
playStoreAPK = 'Aplicativos/cordova/playstore/odhenPOS-playstore.apk'
playStoreAPKd = 'Aplicativos/cordova/playstore/odhenPOS-playstore-debug.apk'

#pagseguro
pagSeguroConfig = 'Projetos Build/PAGSEGURO/odhenPOS/config.xml'
pagSeguroScriptBat = ROOT_DIR + r'\\Scripts\\buildpagseguro.bat'
pagSeguroAPK = 'Aplicativos/cordova/pagseguro/odhenPOS-PAGSEGURO.apk'
pagSeguroAPKd = 'Aplicativos/cordova/pagseguro/odhenPOS-PAGSEGURO-debug.apk'

#getnet
getnetConfig = 'Projetos Build/GETNET/odhenPOS/config.xml'
getnetScriptBat = ROOT_DIR + r'\\Scripts\\buildgetnet.bat'
getnetAPK = 'Aplicativos/cordova/getnet/odhenPOS-GETNET.apk'
getnetAPKd = 'Aplicativos/cordova/getnet/odhenPOS-GETNET-debug.apk'

#cielo
#cieloConfig = 'Projetos Build/LIO/odhenPOS/build.properties'
cieloPropDir = 'Projetos Build/LIO/odhenPOS/'
cieloScriptBat = ROOT_DIR + r'/Scripts/buildlio.bat'
cieloAPK = 'Aplicativos/lio/'

dependenciesDir = 'dependencias/'

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
    #dirIsEmpty

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
    #mudaXml

    def deleteDir(self, path):
        sg.Print('Conteudo de', path, f'deletado!{os.linesep}')
        try:
            shutil.rmtree(path)
        except Exception as e:
            sg.popup_ok(f'DELETE DIR ERROR!   ', e)
    #deleteDir

    def createDir(self, path, permission):
        sg.popup_ok('Diretorio ', path, f' criado!{os.linesep}')
        try:
            os.mkdir(path, mode=permission)
        except Exception as e:
            sg.popup_error(f'CREATE DIR ERROR!   ', e)
    #createDir

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
    #barraDeCarregamentoDIR

    #retira pontos de numeros com ponto
    def tiraPontoNmr(self, nmr):
        strN = str(nmr).replace('.', '')
        nmr = int(strN)
        return nmr
    #tiraPontoNmr

    #troca contra-barra por barra e barras duplas por barras
    def trocaBarra(self, txt):
        aux = str(txt).replace('\\', '/')
        if '//' in aux:
            aux = str(aux).replace('//', '/')
        return aux
    #trocaBarra

    #abre json e coloca as informaçoes em variavel
    def retornaJson(self, dataJson):
        try:
            emailInfo = open(dataJson)
            wjson = emailInfo.read()
            wjdata = json.loads(wjson)
            return wjdata
        except Exception as e:
            sg.popup_error(f'JSON ERROR!', e)
    #retornaJson

    def contaPontosVersao(self, version):
        strV = str(version)
        qtdPontos = 0
        for dot in strV:
            if '.' in dot:
                qtdPontos = qtdPontos + 1
        return qtdPontos
    #contaPontosVersao

    #ao final do build, gera uma mensagem
    def generatedMessage(self, txt):
        if txt == 'sitef':
            aux = 'sitef'
        if txt == 'rede':
            aux = 'rede'
        if txt == 'rede giraffas':
            aux = 'rede giraffas'
        if txt == 'rede saas':
            aux = 'rede saas'
        if txt == 'playstore':
            aux = 'playstore'
        if txt == 'pagseguro':
            aux = 'pagseguro'
        if txt == 'getnet':
            aux = 'getnet'
        sg.Print(f'APK gerado!{os.linesep}'
                 f'Verifique diretório de build. Apk: ', aux, ' gerado!.'
                 f'{os.linesep}')
    #generatedMessage

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
    #getBatLog

    #pega dados de arquivo ".properties" e coloca em variavel
    def parseDotProperties(self, dotPropPath):
        p = Properties()
        with open(dotPropPath, "rb") as f:
            p.load(f, "utf-8")
            return p
    #parseDotProperties

    #altera arquivos ".properties"
    def changeDotProperties(self, dotPropPath, prop, value):
        p = Properties()
        p[prop] = value
        with open(dotPropPath, "w") as f:
            p.store(f, encoding="utf-8")
    #changeDotProperties

    #cria arquivo ".txt"
    def createTXTFile(self, filePath, txt):
        with open(filePath, "w") as f:
            f.write(txt)
    #createTXTFileAPK gerado!

    #cria ".txt", deleta ".properties" e altera para ".txt" para ""
    def treatDotProperties(self, version, packageName):
        # conteudo a ser posto no arquivo ".properties"
        content = f'ext.set("APK_NAME", "odhenPOS"){os.linesep}' \
              f'ext.set("APP_NAME", "Odhen POS"){os.linesep}' \
              f'ext.set("ASSETS_DIR", ["bower_components/assets", "bower_components/templates", "mobile"]){os.linesep}' \
              f'ext.set("WEBVIEW_URL", "mobile/index.html"){os.linesep}' \
              f'ext.set("VERSION_CODE", {self.tiraPontoNmr(version)}){os.linesep}' \
              f'ext.set("VERSION_NAME", "{version}"){os.linesep}' \
              f'ext.set("APPLICATION_ID", "{packageName}"){os.linesep}' \
              f'ext.set("APP_ICON", "mobile/images/favicon.png"){os.linesep}' \
              f'ext.set("STORE_FILE", "playStoreKey"){os.linesep}' \
              f'ext.set("STORE_PASSWORD", "teknisa"){os.linesep}' \
              f'ext.set("KEY_ALIAS", "odhen"){os.linesep}' \
              f'ext.set("KEY_PASSWORD", "teknisa"){os.linesep}'
        try:
            # trata ".properties"
            auxPath = dependenciesDir + 'build.txt'
            if exists(auxPath):
                os.remove(auxPath)
            #cria txt
            self.createTXTFile(auxPath, content)
            if exists(dependenciesDir + 'build.properties'):
                #deleta arquivo
                os.remove(dependenciesDir + 'build.properties')
            p = Path(auxPath)
            #renomeia através da lib Path
            p.rename(p.with_suffix('.properties'))
        except Exception as e:
            self.getBatLog(e)
            sg.popup_error('treatDotProperties ERROR: ', e)
    #treatDotProperties

    # cria ".txt", deleta ".properties" e altera para ".txt" para ""
    def treatGradle(self, param):
        ip = '192.168.122.121'
        port = '3128'
        if param:
            # conteudo a ser posto no arquivo ".properties"
            content = f'# Project-wide Gradle settings.{os.linesep}{os.linesep}' \
                        f'# IDE (e.g. Android Studio) users:' \
                        f'# Gradle settings configured through the IDE *will override*{os.linesep}' \
                        f'# any settings specified in this file.{os.linesep}{os.linesep}' \
                        f'# For more details on how to configure your build environment visit{os.linesep}' \
                        f'# http://www.gradle.org/docs/current/userguide/build_environment.html{os.linesep}{os.linesep}' \
                        f'# The setting is particularly useful for tweaking memory settings.{os.linesep}' \
                        f'# Default value: -Xmx10248m -XX:MaxPermSize=256m{os.linesep}' \
                        f'# org.gradle.jvmargs=-Xmx2048m -XX:MaxPermSize=512m -XX:+HeapDumpOnOutOfMemoryError -Dfile.encoding=UTF-8{os.linesep}{os.linesep}' \
                        f'# When configured, Gradle will run in incubating parallel mode.{os.linesep}' \
                        f'# This option should only be used with decoupled projects. More details, visit{os.linesep}' \
                        f'# http://www.gradle.org/docs/current/userguide/multi_project_builds.html#sec:decoupled_projects{os.linesep}' \
                        f'# org.gradle.parallel=true{os.linesep}' \
                        f'systemProp.http.proxyHost={ip}{os.linesep}' \
                        f'systemProp.http.proxyPort={port}{os.linesep}' \
                        f'systemProp.http.proxyUser={os.linesep}' \
                        f'systemProp.http.proxyPassword={os.linesep}' \
                        f'systemProp.http.proxyHost={ip}{os.linesep}' \
                        f'systemProp.http.proxyPort={port}{os.linesep}' \
                        f'systemProp.http.proxyUser={os.linesep}' \
                        f'systemProp.http.proxyPassword={os.linesep}{os.linesep}' \
                        f'org.gradle.parallel=true{os.linesep}' \
                        f'org.gradle.daemon=true'
        else:
            content = f'# Project-wide Gradle settings.{os.linesep}{os.linesep}' \
                      f'# IDE (e.g. Android Studio) users:' \
                      f'# Gradle settings configured through the IDE *will override*{os.linesep}' \
                      f'# any settings specified in this file.{os.linesep}{os.linesep}' \
                      f'# For more details on how to configure your build environment visit{os.linesep}' \
                      f'# http://www.gradle.org/docs/current/userguide/build_environment.html{os.linesep}{os.linesep}' \
                      f'# The setting is particularly useful for tweaking memory settings.{os.linesep}' \
                      f'# Default value: -Xmx10248m -XX:MaxPermSize=256m{os.linesep}' \
                      f'# org.gradle.jvmargs=-Xmx2048m -XX:MaxPermSize=512m -XX:+HeapDumpOnOutOfMemoryError -Dfile.encoding=UTF-8{os.linesep}{os.linesep}' \
                      f'# When configured, Gradle will run in incubating parallel mode.{os.linesep}' \
                      f'# This option should only be used with decoupled projects. More details, visit{os.linesep}' \
                      f'# http://www.gradle.org/docs/current/userguide/multi_project_builds.html#sec:decoupled_projects{os.linesep}' \
                      f'# org.gradle.parallel=true{os.linesep}' \
                      f'systemProp.http.proxyHost={os.linesep}' \
                      f'systemProp.http.proxyPort={os.linesep}' \
                      f'systemProp.http.proxyUser={os.linesep}' \
                      f'systemProp.http.proxyPassword={os.linesep}' \
                      f'systemProp.http.proxyHost={os.linesep}' \
                      f'systemProp.http.proxyPort={os.linesep}' \
                      f'systemProp.http.proxyUser={os.linesep}' \
                      f'systemProp.http.proxyPassword={os.linesep}{os.linesep}' \
                      f'org.gradle.parallel=true{os.linesep}' \
                      f'org.gradle.daemon=true'
        try:
            # trata ".properties"
            auxPath = dependenciesDir + 'gradle.txt'
            if exists(auxPath):
                os.remove(auxPath)
            # cria txt
            self.createTXTFile(auxPath, content)
            if exists(dependenciesDir + 'gradle.properties'):
                # deleta arquivo
                os.remove(dependenciesDir + 'gradle.properties')
            p = Path(auxPath)
            # renomeia através da lib Path
            p.rename(p.with_suffix('.properties'))
        except Exception as e:
            self.getBatLog(e)
            sg.popup_error('treatGradle ERROR: ', e)
    # treatDotProperties

    #verifica se o arquivo existe
    def verifyFile(self, path):
        if exists(path):
            return True
        elif exists(path) == False:
            return False
        else:
            return 'Aconteceu um erro aqui! func: verifyFile'
    #verifyFile

    def countAndConcatenateListDir(self, path):
        try:
            path = Path(path)
            dirItens = os.listdir(path)
            n = 0
            for item in dirItens:
                n = n + 1
            sg.popup_ok(f'Temos "{n}" adquivos e/ou diretorios em {path}.{os.linesep} '
                     f'O de index "0" será usado para o build atual. Caso não funcione, '
                     f'configure a váriavel de ambiente manualmente. {os.linesep}')
            returnItem = os.path.join("C:\Program Files\Java\\", dirItens[0])
            return returnItem
        except Exception as e:
            self.getBatLog(e)
            sg.popup_error('countAndConcatenateListDir ERROR: ', e)
    #countAndConcatenateListDir

#class Util

class geradorDeApps:
    def __init__(self, cieloLio, cieloLio_teste, gpos700Sitef, gpos700Rede, gpos700Rede_giraffas, gpos700Rede_react_saas, playStore,
                 pagseguro, getnet, packageName, version, mobileFolderPath, activeProxy):
        self.util                      = Util()
        self.cieloLio                  = cieloLio
        self.cieloLio_teste            = cieloLio_teste
        self.gpos700Sitef              = gpos700Sitef
        self.gpos700Rede               = gpos700Rede
        self.gpos700Rede_giraffas      = gpos700Rede_giraffas
        self.gpos700Rede_react_saas    = gpos700Rede_react_saas
        self.playStore                 = playStore
        self.pagseguro                 = pagseguro
        self.getnet                    = getnet
        self.packageName               = packageName
        self.version                   = version
        self.mobileFolderPath          = mobileFolderPath + '/'
        self.activeProxy               = activeProxy

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

        #valida se usa proxy
        if self.activeProxy and (self.cieloLio or self.cieloLio_teste):
            self.util.treatGradle(True)
        else:
            self.util.treatGradle(False)

        #cria vars para verificação
        #pega user_dir
        user_dir = expanduser("~")

        #pega variaveis de ambiente
        java_home = os.getenv("JAVA_HOME")
        android_home = os.getenv("ANDROID_HOME")
        android_sdk_root = os.getenv("ANDROID_SDK_ROOT")

        #verifica se a variavel de ambiente JAVA_HOME esta setada e instalada
        if not java_home and os.path.isdir('C:\Program Files\Java') \
                and not self.util.dirIsEmpty('C:\Program Files\Java'):
            sg.PopupOK('Setando JAVA_HOME provisória...')
            dirItens = self.util.countAndConcatenateListDir('C:\Program Files\Java')
            os.environ["JAVA_HOME"] = dirItens
            java_home = os.getenv("JAVA_HOME")
        elif not os.path.isdir('C:\Program Files\Java'):
            sg.PopupError(f'{os.linesep}{os.linesep}'
                          f'Necessário instalar JDK! Link: https://www.oracle.com/java/technologies/javase/javase-jdk8-downloads.html'
                          f'{os.linesep}{os.linesep}')

        #faz a verificacao com o ANDROID_HOME e ANDROID_SDK_ROOT
        if not android_home and os.path.isdir(user_dir+'\\AppData\\Local\\Android\\Sdk') \
                and not self.util.dirIsEmpty(user_dir+'\\AppData\\Local\\Android\\Sdk'):
            sg.PopupOK('Setando ANDROID_HOME e ANDROID_SDK_ROOT provisória...')
            os.environ["ANDROID_HOME"]      = user_dir+'\\AppData\\Local\\Android\\Sdk'
            os.environ["ANDROID_SDK_ROOT"]  = user_dir + '\\AppData\\Local\\Android\\Sdk'
            android_home = os.getenv("ANDROID_HOME")
            android_sdk_root = os.getenv("ANDROID_SDK_ROOT")
        elif not os.path.isdir(user_dir+'\\AppData\\Local\\Android\\Sdk'):
            sg.PopupError(f'{os.linesep}{os.linesep}' \
                          f'Necessário instalar Android SDK!' \
                          f'{os.linesep}{os.linesep}')

        #verifica se a build-tools necessária existe
        if not os.path.isdir(str(android_home)+'\\build-tools\\22.0.1'):
            sg.PopupOK('Copiando 22.0.1/. Aguarde...')
            shutil.copytree(dependenciesDir+"/22.0.1", str(android_home)+'\\build-tools')

        #completa diretorio
        auxPath = prodDirOdhen + 'mobile/'
        self.util.deleteDir(prodDir)
        sg.PopupOK(f'Copiando mobile. Aguarde...')
        try:
            #copia arquivos de "self.mobileFolderPath" para "auxPath"
            shutil.copytree(self.mobileFolderPath, auxPath)
        except Exception as e:
            self.util.getBatLog(e)
            sg.popup_error('Copiar mobile/ ERROR: ', e)

        #valida quais projetos devem ser gerados e chama ".bat"
        ###
        if self.cieloLio == True:
            if self.packageName:
                self.packageName = self.packageName
            else:
                self.packageName = 'com.odhen.POS'
            try:
                #trata ".properties"
                self.util.treatDotProperties(self.version, self.packageName)
                #chama ".bat"
                sb.call([cieloScriptBat])
                if self.util.dirIsEmpty(cieloAPK):
                    sg.Print('Ocorreu um erro!!    APKs cielo não gerados.')
                elif self.util.dirIsEmpty(cieloAPK) == False:
                    sg.Print('APKs cielo gerados!!.')
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
                self.util.treatDotProperties(self.version, self.packageName)
                sb.call([cieloScriptBat])
                if self.util.dirIsEmpty(cieloAPK):
                    sg.Print('Ocorreu um erro!!       APKs cielo teste não gerados.')
                elif self.util.dirIsEmpty(cieloAPK) == False:
                    sg.Print('APKs cielo teste gerados!!')
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
                if self.util.verifyFile(gpos700SitefAPK) and self.util.verifyFile(gpos700SitefAPKd):
                    # gera mensagem ao final do build
                    self.util.generatedMessage('sitef')
                elif self.util.verifyFile(gpos700SitefAPK) or self.util.verifyFile(gpos700SitefAPKd):
                    sg.Print('Apenas 1 apk foi gerado')
                else:
                    sg.Print('Nenhum apk foi gerado.')
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
                if self.util.verifyFile(gpos700RedeAPK) and self.util.verifyFile(gpos700RedeAPKd):
                    # gera mensagem ao final do build
                    self.util.generatedMessage('rede')
                elif self.util.verifyFile(gpos700RedeAPK) or self.util.verifyFile(gpos700RedeAPKd):
                    sg.Print('Apenas 1 apk foi gerado')
                else:
                    sg.Print('Nenhum apk foi gerado.')
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
                if self.util.verifyFile(gpos700RedeAPK) and self.util.verifyFile(gpos700RedeAPKd):
                    # gera mensagem ao final do build
                    self.util.generatedMessage('rede giraffas')
                elif self.util.verifyFile(gpos700RedeAPK) or self.util.verifyFile(gpos700RedeAPKd):
                    sg.Print('Apenas 1 apk foi gerado')
                else:
                    sg.Print('Nenhum apk foi gerado.')
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
                if self.util.verifyFile(gpos700RedeAPK) and self.util.verifyFile(gpos700RedeAPKd):
                    # gera mensagem ao final do build
                    self.util.generatedMessage('rede saas')
                elif self.util.verifyFile(gpos700RedeAPK) or self.util.verifyFile(gpos700RedeAPKd):
                    sg.Print('Apenas 1 apk foi gerado')
                else:
                    sg.Print('Nenhum apk foi gerado.')
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
                if self.util.verifyFile(playStoreAPK) and self.util.verifyFile(playStoreAPKd):
                    #gera mensagem ao final do build
                    self.util.generatedMessage('playstore')
                elif self.util.verifyFile(playStoreAPK) or self.util.verifyFile(playStoreAPKd):
                    sg.Print('Apenas 1 apk foi gerado')
                else:
                    sg.Print('Nenhum apk foi gerado.')
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
                if self.util.verifyFile(pagSeguroAPK) and self.util.verifyFile(pagSeguroAPKd):
                    # gera mensagem ao final do build
                    self.util.generatedMessage('pagseguro')
                elif self.util.verifyFile(pagSeguroAPK) or self.util.verifyFile(pagSeguroAPKd):
                    sg.Print('Apenas 1 apk foi gerado')
                else:
                    sg.Print('Nenhum apk foi gerado.')
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
                sb.call([r'C:\Workspace\buildapk\Scripts'])
                if self.util.verifyFile(getnetAPK) and self.util.verifyFile(getnetAPKd):
                    # gera mensagem ao final do build
                    self.util.generatedMessage('getnet')
                elif self.util.verifyFile(getnetAPK) or self.util.verifyFile(getnetAPKd):
                    sg.Print('Apenas 1 apk foi gerado')
                else:
                    sg.Print('Nenhum apk foi gerado.')
            except Exception as e:
                self.util.getBatLog(e)
                sg.popup_error('GENERATE PLAYSTORE APP ERROR!   ', e)
        ###
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
            [sg.Checkbox('Ativar proxy', default=False, key='activeProxy')],
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
            #[sg.Checkbox('PagSeguro', default=False, key='pagseguro')],
            #[sg.Checkbox('Getnet', default=False, key='getnet')],
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
                activeProxy               = self.values['activeProxy']
                cieloLio                  = self.values['cieloLio']
                cieloLio_teste            = self.values['cieloLio_teste']
                gpos700Sitef              = self.values['gpos700Sitef']
                gpos700Rede               = self.values['gpos700Rede']
                gpos700Rede_giraffas      = self.values['gpos700Rede_giraffas']
                gpos700Rede_react_saas    = self.values['gpos700Rede_react_saas']
                playStore                 = self.values['playStore']
                #pagseguro                 = self.values['pagseguro']
                pagseguro                 = False
                #getnet                    = self.values['getnet']
                getnet                    = False
                packageName               = self.values['packageName']
                version                   = self.values['version']
                mobileFolderPath          = self.values['mobileFolderPath']
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
                            gerador = geradorDeApps(cieloLio, cieloLio_teste, gpos700Sitef, gpos700Rede, gpos700Rede_giraffas,
                                                    gpos700Rede_react_saas, playStore, pagseguro, getnet, packageName, version,
                                                    mobileFolderPath, activeProxy)
                    else:
                        sg.popup_error(f'Algumas opções ou campos não foram preenchidos!')
                elif self.event == 'help':
                    #tutorial de uso
                    sg.Print(f'Olá! Esse é o tutorial de uso do sistema.{os.linesep}'
                             f'Para gerar um apk, selecione o caminho do diretótio "mobile/" que fica dentro do "odhenPOS/".{os.linesep}'
                             f'Após selecionar o caminho do diretório, marque as caixinhas dos apks que deseja gerar. '
                             f'Podem ser marcadas várias de uma vez...{os.linesep}'
                             f'Depois de selecionar o caminho as caixinhas, '
                             f'digite o número da versão com pontos, como no exemplo: 7.0.0.0.0.{os.linesep}{os.linesep}'
                             f'Não é necessário informar o pacote para gerar o apk. '
                             f'Esse fica setado automaticamente de acordo com o padrão de cada projeto.{os.linesep}'
                             f'Caso coloque o pacote, o sistema irá assumir esse pacote para todos os apks que forem gerados.{os.linesep}{os.linesep}'
                             f'Clique no botão "Gerar" e o sistema irá iniciar o processo de geração.{os.linesep}{os.linesep}'
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