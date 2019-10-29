#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
from tkinter import filedialog
from tkinter import Tk
from ciso8601 import parse_datetime as to_date
import requests
from bs4 import BeautifulSoup
from time import time, sleep
from openpyxl import Workbook
import os


# In[ ]:


def get_lines():
    lines = []
    root = Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    for file in filedialog.askopenfilenames():
        with open(file) as txt:
            for line in txt.readlines():
                yield line


# In[ ]:


def get_ramos(entcodigo, ano):
    ramos = []
    try:
        request = requests.get(
            "https://www2.susep.gov.br/menuestatistica/SES/premiosesinistros.aspx?id=54")
        sopa = BeautifulSoup(request.text, "html.parser")

        params = (('id', '54'))
        data = {
            '__VIEWSTATE': sopa.find("input", {"name": "__VIEWSTATE"})["value"],
            '__VIEWSTATEGENERATOR': sopa.find("input", {"name": "__VIEWSTATEGENERATOR"})["value"],
            '__EVENTVALIDATION': sopa.find("input", {"name": "__EVENTVALIDATION"})["value"],
            'ctl00$ContentPlaceHolder1$edEmpresas': entcodigo.ljust(10, " "),
            'ctl00$ContentPlaceHolder1$edInicioPer': str(ano)+"01",
            'ctl00$ContentPlaceHolder1$edFimPer': str(ano)+"12",
            'ctl00$ContentPlaceHolder1$optAgrupamento': 'RAM',
            'ctl00$ContentPlaceHolder1$btnProcessao': 'Processar'}

        request = requests.post(
            'https://www2.susep.gov.br/menuestatistica/SES/premiosesinistros.aspx', params=params, data=data)
        sopa = BeautifulSoup(request.text, "html.parser")
        elements = sopa.find_all("td", {"align": "left"})
        for element in elements[3:]:
            ramos.append(element.text[:4])
        return ramos
    except:
        return False


# In[ ]:


columns = ["1026", "1027", "1028", "1029", "1030",
          "1031", "1032", "1033", "1034", "1035", "1036", "1037"]
os.system("cls")
entcodigo = input("Digite um ENTCODIGO: \n")
ano = input("\nDigite um ano (Formato aaaa): \n")

ramos = get_ramos(entcodigo, ano)
len_ramos = len(ramos)
index = [[7]*len_ramos+[8]*len_ramos+[9]*len_ramos+[10]*len_ramos,ramos*4]

df_ppng = pd.DataFrame(index=index,columns=columns)
df_ppng.fillna(0.0,inplace = True)

df_rvne = pd.DataFrame(index=index,columns=columns)
df_rvne.fillna(0.0,inplace = True)


# In[ ]:


def run():
    total = 0
    print("\nSelecione os arquivos: \n")
    for line in get_lines():
        tpmoid = int(line[23:27])                          # TPMOID          #
        cmpid = line[27:31]                                # CMPID           #
        ramo = line[31:35]                                 # RAMCODIGO       #
        inicio_ro = to_date(line[35:43])                   # ESPDATAINICIORO #
        fim_ro = to_date(line[43:51])                      # ESPDATAFIMRO    #
        emiss_ro = to_date(line[51:59])                    # ESPDATAEMISSRO  #
        inicio_rd = to_date(line[72:80])                   # ESPDATAINICIORD #
        fim_rd = to_date(line[80:88])                      # ESPDATAFIMRD    #
        emiss_rd = to_date(line[88:96])                    # ESPDATAEMISSRD  #
        valor_ro = float(line[59:72].replace(",", "."))    # ESPVALORMOVRO   #
        valor_rd = float(line[96:109].replace(",", "."))   # ESPVALORMOVRD   #

        valor = 0

        if emiss_rd <= data_calc < inicio_rd:
            valor = valor_rd 
        elif inicio_rd <= data_calc < fim_rd:
            valor = valor_rd*((fim_rd-data_calc).days/((fim_rd-inicio_rd).days+1))
            
        df_ppng.loc[(tpmoid, ramo),cmpid] += valor 
        
        if data_calc < emiss_rd:
            df_rvne.loc[(tpmoid, ramo),cmpid] += valor
            
        total += 1
    return total


# In[ ]:


data_calc = to_date(input("\nDigite a data de cálculo: (Formato aaaammdd) \n"))
start = time()
linhas = run()
end = time()
os.system("cls")
sleep(2)
print(f"\nVelocidade: {round(end-start,2)}s\nMédia: {round(linhas/(end-start),2)} linha/s\n")


# In[ ]:


df_rve = df_ppng - df_rvne


# In[ ]:


print("Exportando para Excel...\n\n")
with pd.ExcelWriter('Provisões.xlsx') as writer:  # doctest: +SKIP
    df_ppng.to_excel(writer, sheet_name='PPNG')
    df_rvne.to_excel(writer, sheet_name='RVNE')
    df_rve.to_excel(writer, sheet_name='RVE')
print("Sucesso!")
sleep(2)
quit()


# In[ ]:


df_ppng["PPNG"] = df_ppng["1026"] + df_ppng["1027"] - df_ppng["1027"]
df_ppng["PPNG"] -= (df_ppng["1030"] + df_ppng["1031"] - df_ppng["1032"])
df_ppng["PPNG"] -= (df_ppng["1034"] + df_ppng["1035"] - df_ppng["1036"])

