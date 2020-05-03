import nltk
from nltk.corpus import brown
import json
import my_toolsv2 as mt
import os

def get_entete_arff(feature_names, classes):
  """On crée l'entête du arff"""
  lignes_arff = ["@relation TRAIN_DATABASE\n"]#nom de la relation
  for name in feature_names:
    lignes_arff.append("@attribute %s numeric\n"%name)#noms des features
  lignes_arff.append("@attribute classes {%s}\n"%",".join(classes))#les classes
  return lignes_arff

def get_lignes_arff(feature_names, classes, features_by_file):
  """Renvoie la liste des lignes nécessaires pour le fichier ARFF"""
  lignes_arff = get_entete_arff(feature_names, classes)
  lignes_arff.append("@data\n\n")#on passe à la partie DATA
  for nom_classe, l_fichier in classes.items():
    for fileid in l_fichier:#Pour chaque fichier
      l_values = [features_by_file[fileid][name] for name in feature_names]
      l_values.append(nom_classe)#pour l'évaluation
      # La liste des features séparées par des virgules :
      ligne_values = ",".join([str(x) for x in l_values])
      lignes_arff.append(ligne_values)
  return lignes_arff

##pour avoir la répartition train_test
train_test =mt.lire_json("train_test.json")

##la liste des fichiers à traiter
all_fileids = mt.get_all_files(train_test)

###récupération des features précédement extraites
features_by_file = mt.lire_json("features_by_file.json")

### récupération de la liste des noms des features extraites
id_hasard = all_fileids[0]
feature_names = features_by_file[id_hasard].keys()

###Définition des combinaisons de features
liste_adverbes = mt.lire_json("liste_adverbes_en.json")
feature_sets = {"all_features" : feature_names,
              "longueur_max_only"   : ["L_max_mots"]}

###Création des ARFF
try:
  os.makedirs("arff_files")#création du dossier pour les ranger
  print("Dossier 'arff_files' créé")
except:
  print("Dossier 'arff_files' déjà créé")
  pass

for feature_set_name, feature_list in feature_sets.items():
  print("\nFeature set : %s"%feature_set_name)
  for dataset, classes in train_test.items():
    print("  Processing %s set"%dataset)
    filename = "arff_files/%s__%s.arff"%(feature_set_name, dataset)
    lignes_arff = get_lignes_arff(feature_list, classes, features_by_file)
    mt.ecrire("\n".join(lignes_arff), filename)
    print("    ->sortie = %s"%filename)
