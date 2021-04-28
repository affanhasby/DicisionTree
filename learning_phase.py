#!/usr/bin/env python
# coding: utf-8

# In[56]:


#Ini buat mounting ya pokoknya mah
# from google.colab import drive
# drive.mount('/content/drive')


# In[57]:


import pandas as pd
import numpy as np

path = "C:/Users/User/Downloads/TUPRO 2 AI/"
columns = ["Suhu", "Waktu", "Langit", "Lembab","Output"]
dataset = pd.read_csv(path+"datalatih.csv", sep=";", header=None)
dataset.columns = columns
rulePerPopulation = 25
crossover_rate, mutation_rate = 0.75, 0.025
dataset


# In[58]:


dataset.values[0]


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


def encodeKromosom(suhu=[1,1,1], waktu=[1,1,1,1], langit=[1,1,1,1], lembab=[1,1,1], output=0):
  return np.concatenate([suhu,waktu,langit,lembab,[output]]).tolist()

def decodeKromosom(kromosom):
  suhu = kromosom[0:3]
  waktu = kromosom[3:7]
  langit = kromosom[7:11]
  lembab = kromosom[11:14]
  output = kromosom[14]
  return Rule(suhu, waktu, langit, lembab, output)

def randomKromosom():
  return [np.random.randint(0,2) for i in range(15*rulePerPopulation)]


# In[ ]:


def initialRandomPopulation(population = 10):
  return [randomKromosom() for i in range(population)]

def parentSelection(fitness, kromosom, jumlah_parent = 5):
  sorteddata = [a for a,b in sorted(zip(kromosom,fitness),key=lambda x : x[1], reverse=True)]
  return sorteddata[0:jumlah_parent]

def mutationKromosom(kromosom):
  for i in range(len(kromosom)):
    if (np.random.rand() < mutation_rate):
      if (kromosom[i] == 1):
        kromosom[i] = 0
      else:
        kromosom[i] = 1
  return kromosom
def mutationPopulation(population):
  return [mutationKromosom(kromosom) for kromosom in population]
  
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

def fitnessPerKromosom(dataset,kromosom):
  groupKromosom = groupingKromosom(kromosom)
  rules = [decodeKromosom(kromosom) for kromosom in groupKromosom]
  data = dataset.values
  data_count = 0
  data_true = 0
  for row in data:
    suhu, waktu, langit, lembab, output = row[0], row[1], row[2], row[3], row[4] == "Ya"
    result = checkResult(rules,suhu,waktu,langit,lembab)
    if (votingResult(result) == output):
      data_true += 1
    data_count += 1
  return data_true/data_count

def fitnessPerPopulation(dataset, population):
  return [fitnessPerKromosom(dataset,kromosom) for kromosom in population]

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

def crossOverKromosom(kromosom1, kromosom2):
  half = int(len(kromosom1) / 2)
  k2 = kromosom2[half::].copy()
  k1 = kromosom1[half::].copy()
  kromosom1 = np.concatenate([kromosom1[0:half], k2])
  kromosom2 = np.concatenate([kromosom2[0:half],k1])
  return kromosom1, kromosom2

def crossOverPopulation(population):
  for i in range(len(population)):
    if (np.random.rand() > crossover_rate):
      randomNumber = np.random.randint(0,len(population))
      kromosom1 = population[i]
      kromosom2 = population[randomNumber]
      kromosom1, kromosom2 = crossOverKromosom(kromosom1,kromosom2)
      population[i] = kromosom1
      population[randomNumber] = kromosom2
  return population
  


# In[62]:


parentPopulation = initialRandomPopulation(50)
best_fitness = 0
best_kromosom = parentPopulation[0]

for i in range(50):
  fitness = fitnessPerPopulation(dataset,parentPopulation)
  print("Generasi ke",i+1)
  print("Fitness :",max(fitness))
  if (max(fitness) > best_fitness):
    index_max = fitness.index(max(fitness))
    best_fitness = max(fitness)
    best_kromosom = parentPopulation[index_max]
    print("Best Fitness updated :",best_fitness)
  parentPopulation = parentSelection(fitness,parentPopulation,25)
  offspring = crossOverPopulation(parentPopulation.copy())
  offspring = mutationPopulation(offspring)
  parentPopulation = np.concatenate([parentPopulation,offspring,initialRandomPopulation(50)])
  


# In[ ]:


np.savetxt(path+"best_kromosom.txt",best_kromosom)


# 
