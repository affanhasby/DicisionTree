#!/usr/bin/env python
# coding: utf-8

# In[37]:


# #Ini buat mounting ya pokoknya mah
# from google.colab import drive
# drive.mount('/content/drive')


# In[38]:


import pandas as pd
import numpy as np
path = "C:/Users/User/Downloads/TUPRO 2 AI/"
columns = ["Suhu", "Waktu", "Langit", "Lembab","Output"]
dataset = pd.read_csv(path+"datatest.csv", sep=",", header=None)
dataset.columns = columns
dataset


#%%

# In[ ]:


class Rule:
  def __init__(self,suhu, waktu, langit, lembab, output):
    try:
      self.suhu = suhu.tolist()
    except:
      self.suhu = suhu
    try:
      self.waktu = waktu.tolist()
    except:
      self.waktu = waktu
    try:
      self.langit = langit.tolist()
    except:
      self.langit = langit
    try:
      self.lembab = lembab.tolist()
    except:
      self.lembab = lembab
    self.output = output
  def check(self, suhu, waktu, langit, lembab):
      if (self.suhu == [1,1,1] or (self.suhu[0] == 1 and suhu == "Rendah")  or (self.suhu[1] == 1 and suhu == "Normal")  or (self.suhu[2] == 1 and suhu == "Tinggi")):
        if (self.waktu == [1,1,1,1] or (self.waktu[0] == 1 and waktu == "Pagi") or (self.waktu[1] == 1 and waktu == "Siang") or (self.waktu[2] == 1 and waktu == "Sore") or (self.waktu[3] == 1 and waktu == "Malam")):
          if (self.langit == [1,1,1,1] or (self.langit[0] == 1 and langit == "Berawan") or (self.langit[1] == 1 and langit == "Cerah")  or (self.langit[2] == 1 and langit == "Hujan")  or (self.langit[3] == 1 and langit == "Rintik") ):
            if (self.lembab == [1,1,1] or (self.lembab[0] == 1 and lembab == "Rendah") or (self.lembab[1] == 1 and lembab == "Normal")  or (self.lembab[2] == 1 and lembab == "Tinggi")):
              return True
      return False


# In[ ]:



def decodeKromosom(kromosom):
  suhu = kromosom[0:3]
  waktu = kromosom[3:7]
  langit = kromosom[7:11]
  lembab = kromosom[11:14]
  output = kromosom[14]
  #return suhu, waktu, langit, lembab, output
  return Rule(suhu, waktu, langit, lembab, output)


def generateOutput(dataset,kromosom):
  groupKromosom = groupingKromosom(kromosom)
  rules = [decodeKromosom(kromosom) for kromosom in groupKromosom]
  data = dataset.values
  data_count = 0
  data_true = 0
  outputs = []
  for row in data:
    suhu, waktu, langit, lembab, output = row[0], row[1], row[2], row[3], row[4] == "Ya"
    result = checkResult(rules,suhu,waktu,langit,lembab)
    if (votingResult(result)):
      outputs.append("Ya")
    else:
      outputs.append("Tidak")
  return outputs


def divide_chunks(l): 
    n = 15
    for i in range(0, len(l), n):  
        yield l[i:i + n] 

def groupingKromosom(kromosom):
  return list(divide_chunks(kromosom))


def checkResult(rules, suhu, waktu, langit, lembab):
  return [rule.check(suhu,waktu,langit,lembab) for rule in rules]

def votingResult(result):
  if (True in result):
    return True
  return False


# In[ ]:


kromosom = np.loadtxt(path+"best_kromosom.txt")
pd.DataFrame(generateOutput(dataset,kromosom)).to_csv(path+"output.csv",header=None, index=None)

