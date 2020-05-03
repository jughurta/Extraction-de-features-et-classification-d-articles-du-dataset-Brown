import nltk
from nltk.corpus import brown
import my_toolsv2 as mt
import json

def ex_constitution_corpus():
  themes = {"news":["news", "reviews", "editorial"], 
            "literature":["science_fiction", "romance", "fiction", "mystery"], 
            "sciences":["learned"]}
  nb_instances = 0
  corpus = {}
  for category in themes:
    print(category, ":")
    nb_doc = len(brown.fileids(categories=themes[category]))
    print("  ",nb_doc, "documents")
    nb_instances += nb_doc
    corpus[category] = brown.fileids(categories=themes[category])
  print("NB instances :", nb_instances)
  return corpus

def get_train_test_corpus(corpus):
  import random
  train = {}
  test = {}
  for category, fileids in corpus.items():
    x = int(20*len(fileids)/100)#nb instances pour le train set
    test[category] = []
    print("On prend %s éléments sur %s pour le test"%(str(x),str(len(fileids))))
    for i in range(x):
      id_doc = random.randint(0,len(fileids)-1)#prend un index au hasard
      test[category].append(fileids[id_doc])#stocke le document dans test
      fileids.remove(fileids[id_doc])
    train[category] = fileids #le reste va dans le train set
  dataset = {"train": train, "test":test}
  return dataset

###Corpus complet
corpus = ex_constitution_corpus()

###Séparation train/test
test_train = get_train_test_corpus(corpus)

###Stockage du résultat
test_train_json = json.dumps(test_train, indent =2)
chemin = "train_test.json"
mt.ecrire(test_train_json, chemin)
print("Dataset stocké dans %s"%chemin)
