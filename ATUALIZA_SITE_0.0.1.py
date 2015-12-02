#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 27 10:11:23 2015

@author: papacheco - Pedro Al Pacheco - pedro.pacheco.a@gmail.com
Versao 0.0.1
"""

from datetime import datetime
import shutil
import os
import pysftp

#Pega data e hora
agora = datetime.now()
hoje = str(agora)

#Variavel caminho do sistema

vcs = os.getcwd()
dir_backup = "/ARQ_SITE/backup"
dir_st = "/ARQ_SITE/"
diretoriohist = "historico/"
arqlog = ("pysftp.log")

#Arquivos_Diretorios====================================================
#Move diretorio com data
def dirdata():
    #print "Backup de pasta"
    #Vai para diretorio    
    os.chdir(vcs)
    #Copia log para arq_site
    shutil.copy(arqlog,"ARQ_SITE")
    shutil.move("ARQ_SITE",diretoriohist+"ARQ_SITE"+hoje)
    
    
#Cria diretorio
def cria_dir():
    diretorio = "ARQ_SITE"
    existe = os.path.isdir(diretorio)
    if existe == False:
        os.mkdir("ARQ_SITE")
        os.mkdir("ARQ_SITE/backup")
        print ("Diretorio criado!"+diretorio)
    else:
        print ("Diretorio já existe!"+diretorio)
        
#Cria dir Historico
def cria_dirhist():
    existe = os.path.isdir(diretoriohist)
    if existe == False:
        os.mkdir(diretoriohist)
        print "Diretorio Historico criado!"
    else:
        print "Diretorio Historico já existe!"
        
#Cria arquivo de log
def crialog():
    existe = os.path.isfile(arqlog)
    if existe == False:
        open(arqlog, "wb")
        print "Log criado!"
    else:
        print "Log já existe!"

#=======================================================================
crialog()
cria_dirhist()

print "                                                 "
print "************ COPIA DO SERVIDOR DE HOMOLOGACAO ****************"
print "                                                 "
srv = pysftp.Connection(host="172.21.3.89", username="root",password="senha",log=arqlog)
arq_cop = raw_input("OPERAÇÃO HOMOLOGAÇÃO===>>Digite o caminho e arquivo remoto:")
#Criando diretorio temporario
cria_dir()
#Navega até o diretorio temporario
os.chdir("ARQ_SITE")
#Recebe arquivo remoto
srv.get(arq_cop)
print "                                                 "
print "************ ENVIO PARA PRODUÇÃO ****************"
print "                                                 "
 
#Conecta no servidor produção
srv = pysftp.Connection(host="172.21.3.11", username="root",password="senha",log=arqlog)
arq_cop = raw_input("OPERAÇÃO PRODUÇÃO***>>Digite o nome do arquivo :")
caminho_cop_remoto = raw_input("OPERAÇÃO PRODUÇÃO***>>Digite o caminho do arquivo onde será enviado :")
##salva arquivo original para backup
#Variavel diretorio de backup
cambackup = vcs+dir_backup
#Variavel do arquivo a ser baixado 
comtot = caminho_cop_remoto+arq_cop
#Vai para diretorio de backup
os.chdir(cambackup)
#Baixa arquivo original que será backupeado
arq_bkp = srv.exists(comtot)
if arq_bkp == True:
    srv.get(comtot)
    os.chdir(vcs)
    dirdata()
else:
    print "Arquivo Novo!"
    ##Daqui para baixo faz envio para produção
    #Vai para diretorio de aquivos de troca
    os.chdir(vcs+dir_st)
    #Vai para diretorio remoto
    with srv.cd(caminho_cop_remoto):
        #Envia arquivo ao site
        srv.put(arq_cop)
        diret = os.chdir(vcs)
        #Move "ARQ_SITE" para diretorio com data e hora
        dirdata()
