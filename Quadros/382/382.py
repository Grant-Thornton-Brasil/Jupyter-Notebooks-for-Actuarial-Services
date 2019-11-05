#!/usr/bin/env python
# coding: utf-8

# In[1]:


from tqdm import tqdm
from tkinter import Tk
from tkinter import filedialog
from pandas import DataFrame as DF
from pycpfcnpj.cpf import validate as valicpf
from ciso8601 import parse_datetime as to_datetime


# In[2]:


def get_lines():
    lines = []
    root = Tk()
    root.attributes("-topmost", True)
    root.withdraw()
    for file in filedialog.askopenfilenames():
        with open(file) as txt:
            for n, line in enumerate(txt.readlines(), 1):
                yield n, line


# Regra| Descrição| Impeditiva
# :------|:-----------|:-----------
# 7398.1| Verifica se não há linhas em branco| Sim
# 7398.2| Verifica o tamanho padrão da linha (188 caracteres) |Sim
# 7398.3| Verifica se o campo sequencial ESCSEQ é uma sequência válida, que se inicia em 0000001 |Sim
# 7398.4| Verifica se o campo ENTCODIGO corresponde à sociedade que está enviando o FIP/SUSEP |Sim
# 7398.5| Verifica se o campo MRFMESANO corresponde, respectivamente, ao ano, mês e último dia do mês de referência do FIP/SUSEP |Sim
# 7398.6| Verifica se o campo QUAID corresponde ao quadro 382 |Sim
# 7398.7| Verifica se o código do tipo de movimento é valido (conforme tabela ‘Tipos Movimentos’ do FIPSUSEP)| Sim
# 7398.8| Verifica se o campo CMPID corresponde a um tipo de operação válida (conforme tabela ‘Bib_DefCamposEstatisticos’ do FIPSUSEP)|Sim
# 7398.9| Verifica se o PLNCODIGO pertence à tabela ‘Planos’ da entidade. |Sim
# 7398.10| Verifica se os campos ESCVALORMOVRO, ESCVALORMOVRD, ESCIMPSEG, ESCVALORCARO, ESCVALORCARD, ESCVALORCIRO e ESCVALORCIRD são float. |Sim
# 7398.13| Valida a correspondência entre os campos TPMOID e CMPID |Sim

# In[3]:


index = ["7398."+str(i) for i in range(1,11)]
index.append("7398.13")
df_criticas = DF(index=index, columns=["Linhas afetadas"])
df_criticas.fillna(0, inplace=True)


# In[4]:


CMPID_valid = [str(i) for i in range(1065,1077)]
ENTCODIGO_input = input("Digite o código da entidade: ")

lines = 0

for n, line in tqdm(get_lines()):
    line = line.strip().replace(",",".")
    ESCSEQ  = line[0:7]
    ENTCODIGO  = line[7:12]
    MRFMESANO  = line[12:20]
    QUAID = line[20:23]
    TPMOID = line[23:27]
    CMPID = line[27:31]
    PLNCODIGO = line[31:37]
    ESCDATAINICIORO = line[37:45]
    ESCDATAFIMRO  = line[45:53]
    ESCDATAEMISSRO = line[53:61]
    ESCVALORMOVRO  = line[61:74]
    ESCDATAINICIORD  = line[74:82]
    ESCDATAFIMRD  = line[82:90]
    ESCDATAEMISSRD  = line[90:98]
    ESCVALORMOVRD  = line[98:111]
    ESCIMPSEG  = line[111:127]
    ESCCODCESS = line[127:132]
    ESCFREQ  = line[132:136]
    ESCVALORCARO = line[136:149]
    ESCVALORCARD = line[149:162]
    ESCVALORCIRO  = line[162:175]
    ESCVALORCIRD  = line[175:188]
    # 7398.1 -> Verifica se não há linhas em branco.
    if line == "" or line == None:
        df_criticas.loc["7398.1", "Linhas afetadas"] += 1
    # 7398.2 -> Verifica o tamanho padrão da linha 
    # (188 caracteres).
    if len(line) != 188:
        df_criticas.loc["7398.1", "Linhas afetadas"] += 1
    # 7398.3 -> Verifica se o campo sequencial ESCSEQ 
    # é uma sequência válida, que se inicia em 0000001.
    if n != int(ESCSEQ):
        df_criticas.loc["7398.3", "Linhas afetadas"] += 1
    # 7398.4 -> Verifica se o campo ENTCODIGO corresponde
    # à sociedade que está enviando o FIP/SUSEP.
    if ENTCODIGO != ENTCODIGO_input:
        df_criticas.loc["7398.4", "Linhas afetadas"] += 1
    # 7398.5 -> Verifica se o campo MRFMESANO corresponde, 
    # respectivamente, ao ano, mês e último dia do mês de 
    # referência do FIP/SUSEP.
    try:
        if MRFMESANO[-2:].strip() not in ["28", "30", "31"]:
            df_criticas.loc["7398.5", "Linhas afetadas"] += 1                  
    except:
        df_criticas.loc["7398.5", "Linhas afetadas"] += 1      
    # 7398.6 -> Verifica se o campo QUAID corresponde 
    # ao quadro 382.
    if QUAID != "382":
        df_criticas.loc["7398.6", "Linhas afetadas"] += 1        
    # 7398.7 -> Verifica se o código do tipo de movimento é
    # valido (conforme tabela ‘Tipos Movimentos’ do FIPSUSEP).
    if TPMOID not in ["0007","0008","0009","0010"]:
        df_criticas.loc["7398.7", "Linhas afetadas"] += 1        
    # 7398.8 -> Verifica se o campo CMPID corresponde a um 
    # tipo de operação válida 
    # (conforme tabela ‘Bib_DefCamposEstatisticos’ do FIPSUSEP).
    if CMPID not in CMPID_valid:
        df_criticas.loc["7398.8", "Linhas afetadas"] += 1        
    # 7398.9 -> Verifica se o PLNCODIGO pertence à 
    # tabela ‘Planos’ da entidade.
    pass
    # 7398.10 -> Verifica se os campos ESCVALORMOVRO, ESCVALORMOVRD, 
    # ESCIMPSEG, ESCVALORCARO, ESCVALORCARD, ESCVALORCIRO e 
    # ESCVALORCIRD são float.
    try:
        float(ESCVALORMOVRO)
        float(ESCVALORMOVRD)
        float(ESCIMPSEG)
        float(ESCVALORCARO)
        float(ESCVALORCARD)
        float(ESCVALORCIRO)
        float(ESCVALORCIRD)
    except:
        df_criticas.loc["7398.10", "Linhas afetadas"] += 1
    # 7398.13 -> Valida a correspondência 
    # entre os campos TPMOID e CMPID.
    try:
        tests = [
            TPMOID in ["0007", "0008"] and CMPID in ["1065", "1066", "1067", "1068"],
            TPMOID == "0009" and CMPID in ["1069", "1070", "1071", "1072"],
            TPMOID == "0010" and CMPID in ["1073", "1074", "1075", "1076"]
        ]
        if not any(tests):
            df_criticas.loc["7398.13", "Linhas afetadas"] += 1                    
    except:
        df_criticas.loc["7398.13", "Linhas afetadas"] += 1       
        
    lines += 1


# In[5]:


df_criticas["Linhas Analizadas"] = lines
df_criticas.to_excel("382.xlsx", sheet_name="Críticas 382")

