from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time
from datetime import datetime
import os
import numpy as np
import glob
import os.path
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from sys import exit
import gspread
from selenium.webdriver.common.action_chains import ActionChains
from gspread_dataframe import get_as_dataframe


#link1 = "http://192.168.3.141/"
link1 = 'http://devcemag.innovaro.com.br:81/sistema'
nav = webdriver.Chrome()
time.sleep(2)
nav.get(link1)

########### LOGIN ###########

#logando 
WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="username"]'))).send_keys("luan araujo")
WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]'))).send_keys("luanaraujo")

time.sleep(2)

WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]'))).send_keys(Keys.ENTER)

time.sleep(2)

#abrindo menu

WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="bt_1892603865"]/table/tbody/tr/td[2]'))).click()

time.sleep(2)

#clicando em produção
WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[8]/div[2]/div[7]/span[2]'))).click()

time.sleep(2)

#clicando em SFC
WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[8]/div[2]/div[12]/span[2]'))).click()

time.sleep(2)

#clicando em apontamento
WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[8]/div[2]/div[14]/span[2]'))).click()

time.sleep(3)

r = 0

while r < 3:
    
    r = r + 1

    ########### ACESSANDO PLANILHAS ###########

    sheet = 'Apontamento automático'
    worksheet1 = 'Serra'
    #worksheet2 = 'Estamparia'
    #worksheet3 = 'Apontadas'

    filename = "service_account.json"

    sa = gspread.service_account(filename)
    sh = sa.open(sheet)

    wks1 = sh.worksheet(worksheet1)
    #wks2 = sh.worksheet(worksheet2)
    #wks3 = sh.worksheet(worksheet3)

    serra = wks1.get_all_records()
    #estamparia = wks2.get_all_records()
    #apontadas = wks3.get_all_records()

    serra = pd.DataFrame(serra)
    #estamparia = pd.DataFrame(estamparia)
    #apontadas = pd.DataFrame(apontadas)

    ########### Tratando planilhas ###########

    #ajustando datas
    for i in range(len(serra)):
        try:
            if serra['Data'][i] == "":
                serra['Data'][i] = serra['Data'][i-1]
        except:
            pass

    i = None

    #filtrando pecas que não foram apontadas
    serra_filter = serra.loc[(serra.Status) != "Apontada!"]

    #inserindo 0 antes do código da peca
    serra_filter['Peca'] = serra_filter['Peca'].astype(str)

    for i in range(len(serra)):
        try:
            if len(serra_filter['Peca'][i]) == 5:
                serra_filter['Peca'][i] = "0" + serra_filter['Peca'][i] 
        except:
            pass

    i = None

    #data de hoje
    data_realizado = datetime.now()
    ts = pd.Timestamp(data_realizado)
    data_realizado = data_realizado.strftime('%d/%m/%Y')

    ########### PREENCHIMENTO ###########

    c = 1

    i = 0

    for i in range(len(serra)):

        try:
            peca = serra_filter['Peca'][i]
            qtde = str(serra_filter['Qtde'][i])
            data = serra_filter['Data'][i]
            pessoa = '4054'
            c = c+2

            try:
                nav.switch_to.default_content()
            except:
                pass

            #mudando iframe
            iframe1 = WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div[2]/iframe')))
            nav.switch_to.frame(iframe1)
            time.sleep(3)

            #Insert
            WebDriverWait(nav, 2).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[1]/td/div/form/table/thead/tr[1]/td[1]/table/tbody/tr/td[2]/table/tbody/tr/td[2]/div'))).click()
            time.sleep(2)

            #classe
            try:
                WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/table/tbody/tr[1]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[" + str(c) + "]/td[3]/div/div"))).click()
            except:
                pass
            
            try:
                WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/table/tbody/tr[1]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[" + str(c) + "]/td[3]/div/input"))).send_keys("Produção por máquina")
                time.sleep(2)
            except:
                pass
            
            #data
            WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/table/tbody/tr[1]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[" + str(c) + "]/td[5]/div/div"))).click()
            time.sleep(2)
            WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/table/tbody/tr[1]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[" + str(c) + "]/td[5]/div/input"))).send_keys(data)

            #pessoa
            WebDriverWait(nav, 2).until(EC.element_to_be_clickable((By.XPATH, "/html/body/table/tbody/tr[1]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[" + str(c) + "]/td[8]/div/div"))).click()
            time.sleep(2)
            WebDriverWait(nav, 2).until(EC.element_to_be_clickable((By.XPATH, "/html/body/table/tbody/tr[1]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[" + str(c) + "]/td[8]/div/input"))).send_keys(pessoa)

            #peça
            WebDriverWait(nav, 2).until(EC.element_to_be_clickable((By.XPATH, "/html/body/table/tbody/tr[1]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[" + str(c) + "]/td[10]/div/div"))).click()
            time.sleep(2)
            WebDriverWait(nav, 2).until(EC.element_to_be_clickable((By.XPATH, "/html/body/table/tbody/tr[1]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[" + str(c) + "]/td[10]/div/input"))).send_keys(peca)
            
            WebDriverWait(nav, 2).until(EC.element_to_be_clickable((By.XPATH, "/html/body/table/tbody/tr[1]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[" + str(c) + "]/td[12]/div/div"))).click()
            time.sleep(5)

            #processo
            WebDriverWait(nav, 2).until(EC.element_to_be_clickable((By.XPATH, "/html/body/table/tbody/tr[1]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[" + str(c) + "]/td[12]/div/input"))).send_keys('S C Serras')
            WebDriverWait(nav, 2).until(EC.element_to_be_clickable((By.XPATH, "/html/body/table/tbody/tr[1]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[" + str(c) + "]/td[18]/div/div"))).click()
            time.sleep(2)

            #quantidade
            WebDriverWait(nav, 2).until(EC.element_to_be_clickable((By.XPATH, "/html/body/table/tbody/tr[1]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[" + str(c) + "]/td[18]/div/div"))).click()
            time.sleep(2)
            WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, "/html/body/table/tbody/tr[1]/td/div/form/table/tbody/tr[1]/td[1]/table/tbody/tr[" + str(c) + "]/td[18]/div/input"))).send_keys(qtde)
            time.sleep(5)

            #insert
            ActionChains(nav).key_down(Keys.CONTROL).send_keys('m').key_up(Keys.CONTROL).perform()
            time.sleep(3)
            ActionChains(nav).key_down(Keys.CONTROL).send_keys('m').key_up(Keys.CONTROL).perform()
            time.sleep(3)

            try:
                nav.find_element("xpath", '/html/body/div[10]/div[2]/table/tbody/tr[2]/td/div/button').click()
            except:
                pass            

            #innovaro real
            #WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/table/tbody/tr[1]/td/div/form/table/thead/tr[1]/td[1]/table/tbody/tr/td[2]/table/tbody/tr/td[4]/div'))).click()
            #time.sleep(2)

            time.sleep(6)

            try:

                # volta p janela principal (fora do iframe)
                nav.switch_to.default_content()
                texto_erro = nav.find_element("xpath", '/html/body/div[10]/div[2]/table/tbody/tr[1]/td[2]/div/div/span[1]').text
                WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="confirm"]'))).click()
                wks1.update('D' + str(i+2), texto_erro)
                
                WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="bt_1892603865"]/table/tbody/tr/td[2]'))).click()
                time.sleep(5)
                WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[8]/div[2]/div[14]/span[2]'))).click()
                time.sleep(5)
                WebDriverWait(nav, 10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/div/table/tbody/tr/td[1]/table/tbody/tr/td[4]/span/div'))).click()
                time.sleep(5)

                c = 1

            except:
                wks1.update('D' + str(i+2), 'Apontada!')

        except:
            c = 1