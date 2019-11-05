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


# Regra |Descrição| Impeditiva
# :-------|:-----------|:-----------
# 7396.1|Verifica se não há linhas em branco.|Sim
# 7396.2|Verifica o tamanho padrão da linha (146 caracteres).|Sim
# 7396.3|Verifica se o campo sequencial EBRSEQ é uma sequência válida, que se inicia em 0000001.|Sim
# 7396.4 |Verifica se o campo ENTCODIGO corresponde à sociedade que está enviando o FIP/SUSEP.|Sim
# 7396.5|Verifica se o campo MRFMESANO corresponde, respectivamente, ao ano, mês e último dia do mês de referência do FIP/SUSEP.|Sim
# 7396.6|Verifica se o campo QUAID corresponde ao quadro 380.|Sim
# 7396.7|Verifica se o campo CMPID corresponde a um tipo de operação válida (conforme tabela “Bib_DefCampos”).|Sim
# 7396.8|Verifica se o PLNCODIGO pertence ao Cadastro de Planos da entidade.|Sim
# 7396.9|Verifica se o CPF do participante (EBRCPFPART) e do beneficiário (EBRCPFBENF) são inteiros e válidos, exceto para preenchimento com zeros.|Sim
# 7396.10|Verifica se os campos EBRDATAINICIO, EBRDATAFIM, EBRDATAOCORR e EBRDATAREG correspondem a uma data válida e se estão compreendidos entre os anos de 1901 e 2099.|Sim
# 7396.11|Verifica se o campo EBRVALORMOV é float.|Sim

# In[3]:


ENTCODIGO_input = input("Digite o código da entidade: ")
CMPID_valid = [str(i) for i in range(1053, 1064)]
date_i = to_datetime("19010101")
date_f = to_datetime("20991231")

index = ["7396.1", "7396.2", "7396.3",
         "7396.4", "7396.5", "7396.6",
         "7396.7", "7396.8", "7396.9",
         "7396.10", "7396.11"]

df_criticas = DF(index=index, columns=["Linhas afetadas"])
df_criticas.fillna(0.0, inplace=True)
lines = 0

for n, line in tqdm(get_lines()):
    line = line.strip().replace(",", ".")
    EBRSEQ = int(line[0:7])
    ENTCODIGO = line[7:12]
    MRFMESANO = line[12:20]
    QUAID = line[20:23]
    CMPID = line[23:27]
    PLNCODIGO = line[27:33]
    EBRCPFPART = line[54:65]
    EBRDATAINICIO = line[76:84]
    EBRVALORMOV = line[108:121]
    EBRCPFBENF = line[65:76]
    EBRDATAFIM = line[84:92]
    EBRDATAOCORR = line[92:100]
    EBRDATAREG = line[100:108]

    # 7396.1 -> Verifica se não há linhas em branco.
    if line == "" or line == None:
        df_criticas.loc["7396.1", "Linhas afetadas"] += 1
    # 7396.2 -> Verifica o tamanho padrão da linha (146 caracteres).
    if len(line) != 146:
        df_criticas.loc["7396.2", "Linhas afetadas"] += 1
    # 7396.3 -> Verifica se o campo sequencial EBRSEQ é uma sequência
    # válida, que se inicia em 0000001.
    if n != EBRSEQ:
        df_criticas.loc["7396.3", "Linhas afetadas"] += 1
    # 7396.4 -> Verifica se o campo ENTCODIGO corresponde à sociedade
    # que está enviando o FIP/SUSEP.
    if ENTCODIGO_input != ENTCODIGO:
        df_criticas.loc["7396.4", "Linhas afetadas"] += 1
    # 7396.5 -> Verifica se o campo MRFMESANO corresponde, respectivamente,
    # ao ano, mês e último dia do mês de referência do FIP/SUSEP.
    try:
        if MRFMESANO[-2:].strip() not in ["28", "30", "31"]:
            df_criticas.loc["7396.5", "Linhas afetadas"] += 1                  
    except:
        df_criticas.loc["7396.5", "Linhas afetadas"] += 1        
    # 7396.6 -> Verifica se o campo QUAID corresponde ao quadro 380.
    if QUAID != "380":
        df_criticas.loc["7396.6", "Linhas afetadas"] += 1
    # 7396.7 -> Verifica se o campo CMPID corresponde a um tipo de operação
    # válida (conforme tabela “Bib_DefCampos”).
    if ENTCODIGO_input != ENTCODIGO:
        df_criticas.loc["7396.7", "Linhas afetadas"] += 1
    # 7396.8 -> Verifica se o PLNCODIGO pertence
    # ao Cadastro de Planos da entidade.
    pass
    # 7396.9 -> Verifica se o CPF do participante (EBRCPFPART)
    # e do beneficiário (EBRCPFBENF) são inteiros e válidos,
    # exceto para preenchimento com zeros.
    if not (valicpf(EBRCPFPART) == valicpf(EBRCPFBENF)):
        df_criticas.loc["7396.9", "Linhas afetadas"] += 1
    """
    HÁ CPFs COM O VALOR 11111111111.
    O QUE FAZER? É VÁLIDO OU INVÁLIDO?
    """
    # 7396.10 -> Verifica se os campos EBRDATAINICIO, EBRDATAFIM,
    # EBRDATAOCORR e EBRDATAREG correspondem a uma data válida
    # e se estão compreendidos entre os anos de 1901 e 2099.
    try:
        tests = [date_i <= to_datetime(EBRDATAINICIO) <= date_f,
                 date_i <= to_datetime(EBRDATAFIM) <= date_f,
                 date_i <= to_datetime(EBRDATAOCORR) <= date_f,
                 date_i <= to_datetime(EBRDATAREG) <= date_f]
        if not all(tests):
            df_criticas.loc["7396.10", "Linhas afetadas"] += 1
    except:
        df_criticas.loc["7396.10", "Linhas afetadas"] += 1
    # 7396.11 -> Verifica se o campo EBRVALORMOV é float.
    try:
        float(EBRVALORMOV)
    except:
        df_criticas.loc["7396.11", "Linhas afetadas"] += 1

    lines += 1


# In[4]:


df_criticas["Linhas Analizadas"] = lines
df_criticas


# In[5]:


df_criticas.to_excel("380.xlsx", sheet_name="Críticas 390")

