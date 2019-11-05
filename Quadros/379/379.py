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
# 7395.1|Verifica se não há linhas em branco.|Sim
# 7395.2|Verifica o tamanho padrão da linha (205 caracteres).|Sim
# 7395.3|Verifica se o campo sequencial EBISEQ é uma sequência válida, que se inicia em 0000001.|Sim
# 7395.4|Verifica se o campo ENTCODIGO corresponde à sociedade que está enviando o FIP/SUSEP.|Sim
# 7395.5|Verifica se o campo MRFMESANO corresponde, respectivamente, ao ano, mês e último dia do mês de referência do FIP/SUSEP.|Sim
# 7395.6|Verifica se o campo QUAID corresponde ao quadro 379.|Sim
# 7395.7|Verifica se o campo TPMOID corresponde a um tipo de movimento valido|Sim
# 7395.8|Verifica se o campo TPMOPREV corresponde a um tipo de movimento de previdência valido.|Sim
# 7395.9| Verifica se o campo CMPID corresponde a um tipo de operação válida.|Sim
# 7395.10|Verifica se o PLNCODIGO pertence ao Cadastro de Planos da entidade.|Sim
# 7395.11|Verifica se o CPF do participante (EBICPFPART) e do beneficiário (EBICPFBENF) são inteiros e válidos, exceto para preenchimento com zeros.|Sim
# 7395.12| Verifica se os campos EBIDATAINICIO, EBIDATAFIM, EBIDATAOCORR, EBIDATAREG e EBIDATACOMUNICA correspondem a uma data válida e se estão compreendidos entre os anos de 1901 e 2099.|Sim
# 7395.13| Verifica se as datas relacionadas ao evento (EBIDATAOCORR, EBIDATAREG e EBIDATARCOMUNICA), para a combinação de TPMOID 0001 e TPMOPREV 0001, estão entre os limites de trinta anos para mais ou menos em relação ao mês de referência |Sim
# 7395.14| Verifica se o campo EBIBENVEN é inteiro e maior ou igual a zero.|Sim
# 7395.15|Verifica se os campos EBIVALORPBAC, EBIVALORPBC, EBIVALORMOV e EBIVALORMON são float.|Sim
# 7395.18| Valida a correspondência entre os campos CMPID e TPMOID.|Sim
# 

# In[3]:


ENTCODIGO_input = input("Digite o código da entidade: ")
CMPID_valid = [str(i) for i in range(1038, 1053)]
date_i = to_datetime("19010101")
date_f = to_datetime("20991231")

index = ["7395.1", "7395.2", "7395.3", "7395.4",
         "7395.5", "7395.6", "7395.7", "7395.8",
         "7395.9", "7395.10", "7395.11", "7395.12",
         "7395.13", "7395.14", "7395.15", "7395.18"]

df_criticas = DF(index=index, columns=["Linhas afetadas"])
df_criticas.fillna(0.0, inplace=True)
lines = 0

for n, line in tqdm(get_lines()):
    line = line.strip().replace(",", ".")
    EBISEQ = int(line[:7])
    ENTCODIGO = line[7:12]
    MRFMESANO = line[12:20]
    QUAID = line[20:23]
    TPMOID = line[23:27]
    TPMOPREV = line[27:31]
    CMPID = line[31:35]
    PLNCODIGO = line[35:41]
    EBICPFPART = line[62:73]
    EBICPFBENF = line[73:84]
    EBIDATAINICIO = line[84:92]
    EBIDATAFIM = line[92:100]
    EBIDATAOCORR = line[100:108]
    EBIDATAREG = line[108:116]
    EBIDATACOMUNICA = line[116:124]
    EBIBENVEN = line[124:128]
    EBIVALORPBAC = line[128:141]
    EBIVALORPBC = line[141:154]
    EBIVALORMOV = line[154:167]
    EBIVALORMON = line[167:180]

    # 7395.1 -> Verifica se não há linhas em branco.
    if line == "" or line == None:
        df_criticas.loc["7395.1", "Linhas afetadas"] += 1
    # 7395.2 -> Verifica o tamanho padrão da linha (205 caracteres).
    if len(line) != 205:
        df_criticas.loc["7395.2", "Linhas afetadas"] += 1
    # 7395.3 -> Verifica se o campo sequencial EBISEQ é uma sequência
    # válida, que se inicia em 0000001.
    if EBISEQ != n:
        df_criticas.loc["7395.3", "Linhas afetadas"] += 1
    # 7395.4 -> Verifica se o campo ENTCODIGO corresponde à sociedade
    # que está enviando o FIP/SUSEP.
    if ENTCODIGO_input != ENTCODIGO:
        df_criticas.loc["7395.4", "Linhas afetadas"] += 1
    # 7395.5 -> Verifica se o campo MRFMESANO corresponde,
    # respectivamente, ao ano, mês e último dia do mês de referência
    # do FIP/SUSEP.
    try:
        if MRFMESANO[-2:].strip() not in ["28", "30", "31"]:
            df_criticas.loc["7395.5", "Linhas afetadas"] += 1                  
    except:
        df_criticas.loc["7395.5", "Linhas afetadas"] += 1        
    # 7395.6 -> Verifica se o campo QUAID corresponde ao quadro 379.
    if QUAID != "379":
        df_criticas.loc["7395.6", "Linhas afetadas"] += 1
    # 7395.7 -> Verifica se o campo TPMOID corresponde a um tipo de
    # movimento valido
    if TPMOID not in ["0001", "0002", "0003",
                      "0004", "0005", "0006", "0014"]:
        df_criticas.loc["7395.7", "Linhas afetadas"] += 1
    # 7395.8 -> Verifica se o campo TPMOPREV corresponde a um tipo de
    # movimento de previdência valido.
    if TPMOPREV not in ["0001", "0002", "0003"]:
        df_criticas.loc["7395.8", "Linhas afetadas"] += 1
    # 7395.9 -> Verifica se o campo CMPID corresponde a um tipo
    # de operação válida.
    if CMPID not in CMPID_valid:
        df_criticas.loc["7395.9", "Linhas afetadas"] += 1
    # 7395.10 -> Verifica se o PLNCODIGO pertence ao Cadastro de
    # Planos da entidade.
    pass
    # 7395.11 -> Verifica se o CPF do participante (EBICPFPART)
    # e do beneficiário (EBICPFBENF) são inteiros e válidos,
    # exceto para preenchimento com zeros.
    if not (valicpf(EBICPFPART) == valicpf(EBICPFBENF)):
        df_criticas.loc["7395.11", "Linhas afetadas"] += 1
    """
        HÁ CPFs COM O VALOR 11111111111.
        O QUE FAZER? É VÁLIDO OU INVÁLIDO?
    """
    # 7395.12 Verifica se os campos EBIDATAINICIO, EBIDATAFIM,
    # EBIDATAOCORR, EBIDATAREG e EBIDATACOMUNICA correspondem a uma
    # data válida e se estão compreendidos entre os anos de 1901 e 2099.
    try:
        tests = [date_i <= to_datetime(EBIDATAINICIO) <= date_f,
                 date_i <= to_datetime(EBIDATAFIM) <= date_f,
                 date_i <= to_datetime(EBIDATAOCORR) <= date_f,
                 date_i <= to_datetime(EBIDATAREG) <= date_f,
                 date_i <= to_datetime(EBIDATACOMUNICA) <= date_f]
        if not all(tests):
            df_criticas.loc["7395.12", "Linhas afetadas"] += 1
    except:
        df_criticas.loc["7395.12", "Linhas afetadas"] += 1
    # 7395.13 -> Verifica se as datas relacionadas ao evento (EBIDATAOCORR,
    # EBIDATAREG e EBIDATARCOMUNICA), para a combinação de TPMOID 0001 e
    # TPMOPREV 0001, estão entre os limites de trinta anos para mais ou
    # menos em relação ao mês de referência
    pass
    # 7395.14 -> Verifica se o campo EBIBENVEN
    # é inteiro e maior ou igual a zero.
    try:
        if not int(EBIBENVEN) >= 0:
            df_criticas.loc["7395.14", "Linhas afetadas"] += 1
    except:
        df_criticas.loc["7395.14", "Linhas afetadas"] += 1
    # 7395.15 -> Verifica se os campos EBIVALORPBAC, EBIVALORPBC,
    # EBIVALORMOV e EBIVALORMON são float.
    try:
        float(EBIVALORPBAC)
        float(EBIVALORPBC)
        float(EBIVALORMOV)
        float(EBIVALORMON)
    except:
        df_criticas.loc["7395.15", "Linhas afetadas"] += 1
    # 7395.18 -> Valida a correspondência entre os campos CMPID e TPMOID.
    if TPMOID == "0014" and CMPID not in ["1049", "1052"]:
        df_criticas.loc["7395.18", "Linhas afetadas"] += 1

    lines += 1


# In[4]:


df_criticas["Linhas Analizadas"] = lines
df_criticas


# In[5]:


df_criticas.to_excel("379.xlsx",sheet_name="Críticas 379")


# In[ ]:




