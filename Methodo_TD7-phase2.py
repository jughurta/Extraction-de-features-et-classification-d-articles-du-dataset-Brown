import nltk
from nltk.corpus import brown
import json
import my_toolsv2 as mt

def get_features_light(liste_fichier):
  features_file = {}
  for fileid in liste_fichier:
    features_file[fileid] = {}
    stats_mots = mt.get_stats_longueur(brown.words(fileid))
    for feature, valeur in stats_mots.items():
      features_file[fileid][feature] = valeur
  print("->Features extraites:", list(features_file[fileid].keys())[:20],"...")
  return features_file

def get_features(liste):
  features_file = {}
  for fileid in liste:
    features_file[fileid] = {}#on initialise les features du fichier
    # Utilisons notre libraire my_tools pour ajouter des stats sur les mots
    words = brown.words(fileid)
    stats_mots = mt.get_stats_longueur(words)
    for feature, valeur in stats_mots.items():
      features_file[fileid][feature] = valeur
    # Puis sur les phrases
    stats_phrases = mt.get_types_phrases(brown.raw(fileid))
    for feature, valeur in stats_phrases.items():
      features_file[fileid][feature] = valeur
    adverbes = mt.get_effectif_adverbes(words)
    for feature, valeur in adverbes.items():
      features_file[fileid][feature] = valeur
    #... l'entrée varie mais la sortie est un dico {"feature_name":valeur,...}
  print("->Features extraites:", list(features_file[fileid].keys())[:20],"...")
  return features_file

###On récupère la liste des fichiers à traiter
train_test = json.load(open("train_test.json"))
print("\nRécupération de la liste des fichiers")
liste_all_files = mt.get_all_files(train_test)
print("-> %s fichiers"%str(len(liste_all_files))) 

###On extrait les features
print("\nExtraction des features")
features_by_file = get_features_light(liste_all_files)

###On écrit la sortie
print("\nEcriture de la sortie JSON")
filename = "features_by_file.json"
mt.sauvegarder(features_by_file, filename)
print("-> %s"%filename)
