#!/usr/bin/env python
# coding: utf-8

# In[5]:


import textract
from re import findall


# In[2]:


def run(pdf):
    path = "C:\\Users\\marcelo.franceschini\\OneDrive - GRANT THORNTON BRASIL\\MMF\\Desktop Backup\\PDFs\\"
    text = textract.process(path+pdf).decode(encoding='UTF-8',errors='strict')
    credora_nome = findall(r'Credora\r\n[A-Z .\ ]*\r\n[A-Z .\ ]*',text)[0].replace("\r\n"," ").replace("Credora ","").strip()
    credora_cnpj = findall(r'[0-9]{2}\.?[0-9]{3}\.?[0-9]{3}\/?[0-9]{4}\-?[0-9]{2}',text)[0].strip()
    emitente_nome = findall(r'(Emitente\r\n[A-Z 1-9 \n]*[A-Z 1-9 \n]*[\n A-Z 1-9]*)',text)[0].replace("\r\n"," ").replace("Emitente ","").replace(" CPF ","").strip()
    emitente_doc = findall(r'(\d{3}\.\d{3}\.\d{3}\-\d{2})',text)[0]

    if emitente_nome.strip() in [None, "\n", "",]:
        emitente_nome = findall(r"Emitente\r\n\r\n[A-Z \n \.]*",text)[0].replace("Emitente\r\n\r\n","")

    datas = findall("[0-9]{2}-[0-9]{2}-[0-9]{4}",text)
    emiss = datas[0]
    venc = datas[1]

    valores = list(map(lambda x: x.replace("$ ",""),findall(r"[R$] [0-9]*.[0-9]*,[0-9]*",text)))
    principal = valores[0]
    try:
        parcelas = ";".join([valores[5],valores[8],valores[-1]])
    except IndexError:
        parcelas= ";".join([valores[5],valores[-1],"0"])

    info = [
        pdf,
        credora_nome,
        credora_cnpj,
        emitente_nome,
        emitente_doc,
        emiss,
        venc,
        principal,
        parcelas,
    ]
    write = ";".join(info)
    print(write)
    return write


# In[3]:


lista = []
with open("lista1.txt") as txt:
    lista = txt.read().split("\n")


# In[6]:


with open("export1.txt","a+") as txt:
    headers = [
        "PDF File",
        "Credora_nome",
        "Credora_CNPJ",
        "Emitente_nome",
        "Emitente_DOC",
        "Valor de Principal",
        "Parcela 1",
        "Parcela 2",
        "Parcela 3",
        "Data Emiss",
        "Data Venc"
    ]
    txt.write(";".join(headers)+"\n")
    for i in lista:
        txt.write(run(i)+"\n")

