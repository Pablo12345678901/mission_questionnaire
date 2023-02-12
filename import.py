import requests
import json
import unicodedata
import sys # gestion de la récupération du nom de fichier json entrée depuis la command line (terminal)
import os, json # gestion de la récupération des noms de fichiers json du répertoire

from questionnaire import Questionnaire, Question

# ====> REMARQUE : Les Url ci-dessous sont différentes que celles affichées dans la vidéo.
# C'est normal, continuez bien avec les url de ce fichier

# Liste des questionnaires
open_quizz_db_data = (
    ("Animaux", "Les chats", "https://www.codeavecjonathan.com/res/mission/openquizzdb_50.json"),
    ("Arts", "Musée du Louvre", "https://www.codeavecjonathan.com/res/mission/openquizzdb_86.json"),
    # DEBUG adapté le lien
    ("Bande dessinnée", "Tintin", "https://www.kiwime.com/oqdb/files/2124242395/OpenQuizzDB_124/openquizzdb_124.json"),
    ("Cinéma", "Alien", "https://www.codeavecjonathan.com/res/mission/openquizzdb_241.json"),
    ("Cinéma", "Star wars", "https://www.codeavecjonathan.com/res/mission/openquizzdb_90.json"),
    ("Insectes", "Abeilles", "https://www.kiwime.com/oqdb/files/3237399872/OpenQuizzDB_237/openquizzdb_237.json"),
    )

# FONCTION QUI REMPLACE LES ACCENTS PAR DES CARACTERES SANS ACCENTS
def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')

# FONCTION DE CREATION DU NOM DE FICHIER JSON
def get_quizz_filename(categorie, titre, difficulte):
    return strip_accents(categorie).lower().replace(" ", "") + "_" + strip_accents(titre).lower().replace(" ", "") + "_" + strip_accents(difficulte).lower().replace(" ", "") + ".json"


# CREATION DU FICHIER JSON UTILISE EN TANT QUE QUESTIONNAIRE A PARTIR DE L'URL CONTENANT DU JSON
def generate_json_file(categorie, titre, url):
    out_questionnaire_data = {"categorie": categorie, "titre": titre, "questions": []} # CREATION DU DICTIONNAIRE CONTENANT LE QUESTIONNAIRE
    out_questions_data = []
    try: # Gestion du cas d'erreur de requête
        response = requests.get(url) # récupération du contenu de la page au format binaire
    except: # Gestion du cas d'erreur de requête
        print("Exception pour la requête d'url :", url)
    else: # Exécution de la suite du code
        try: # Gestion du cas d'erreur de data
            data = json.loads(response.text) # désérialisation
            all_quizz = data["quizz"]["fr"] # Récupération des données à utilisées > stockée dans le quizz français
            for quizz_title, quizz_data in all_quizz.items():
                out_filename = get_quizz_filename(categorie, titre, quizz_title) # Création du titre du quizz - quizz title correspond à la difficulté
                #DEBUG print(out_filename)
                out_questionnaire_data["difficulte"] = quizz_title # ajout de la difficulté au clef du dictionnaire

                for question in quizz_data: # pour chaque question création d'un dictionnaire qui contiendra les questions et réponses proposées
                    question_dict = {} 
                    question_dict["titre"] = question["question"]
                    question_dict["choix"] = []

                    for ch in question["propositions"]: 
                        question_dict["choix"].append((ch, ch==question["réponse"])) # pour chaque proposition, création et ajout d'un tuple qui contient la proposition et si elle est juste

                    out_questions_data.append(question_dict) # ajout de la question et réponse dans la data vide
                out_questionnaire_data["questions"] = out_questions_data # ajout de la question au questionnaire
                out_json = json.dumps(out_questionnaire_data) # sérialisation
                # Rédaction du fichier json
                file = open(out_filename, "w")
                file.write(out_json)
                file.close()
                #DEBUG print("end")
        except: # Gestion du cas d'erreur de data
            print("Exception data pour l'url :", url, "correspondant au questionnaire :", titre) # affichage de l'url et le questionnaire qui provoquent une erreur

# FONCTION POUR OBTENIR LA DATA DU QUESTIONNAIRE
def get_quizz_data_from_json_file(filename):
    file = open(filename, "r") # ouverture du fichier en mode lecture
    data = file.read() # les datas sont au format JSON
    file.close()
    quizz = json.loads(data)
    return quizz # pour désérialiser les data

    data = fil
    quizz = json.loads(name)
    print(quizz)

# Affichage des informations du questionnaire
def show_quizz_info(quizz_dictionary):
    print() # esthétique pour la console
    print("Vous avez choisi le questionnaire suivant : ")
    print() # esthétique pour la console
    print("Titre : "+ quizz_dictionary["titre"])
    print("Catégorie : "+ quizz_dictionary["categorie"])
    print("Difficulté : "+ quizz_dictionary["difficulte"])
    print("Nombre total de questions : " + str(len(quizz_dictionary["questions"])))
    print() # esthétique pour la console

# Création du quizz à partir de la data
def quizz_creation_and_format(quizz_dictionary):
    quizz = []
    for i in range(0, len(quizz_dictionary["questions"])):
        title = quizz_dictionary["questions"][i]["titre"]
        choice_list = []
        answer = ""
        # récupération des choix proposés
        for j in range(0, len(quizz_dictionary["questions"][i]["choix"])):
            choice_list.append(quizz_dictionary["questions"][i]["choix"][j][0])
            if quizz_dictionary["questions"][i]["choix"][j][1]: # si le choix est le bon
                answer = quizz_dictionary["questions"][i]["choix"][j][0] # il deviendra la réponse
        quizz.append(Question(title, choice_list, answer))
    return quizz

# Fonction pour montrer à l'utilisateur les fichiers json disponibles dans le répertoire
def show_json_files_in_directory(path_to_json):
    json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
    print("Voici la liste des questionnaire disponibles : ")
    for i in range(0, len(json_files)):
        print(str(i+1), json_files[i])
    return json_files

# Fonction pour demande le choix du questionnaire à l'utilisateur
def ask_which_quizz_to_do(min, max):
    print("Quel questionnaire souhaiteriez-vous effectuer ?")
    quizz_nb_choice_str = input("Veuillez choisir son numéro entre " + str(min) + " et " + str(max) + ") : ")
    try:
        quizz_nb_choice_int = int(quizz_nb_choice_str)
        if min <= quizz_nb_choice_int <= max:
            return quizz_nb_choice_int
        print("ERREUR : Vous devez rentrer un nombre entre", min, "et", max)
    except:
        print("ERREUR : Veuillez rentrer uniquement des chiffres")
    return ask_which_quizz_to_do(min, max) # fonction récursive tant que l'utilisateur n'a pas fait un choix correct


if __name__ == "__main__":
    # PROGRAMME DU QUESTIONNAIRE
    # Pour chaque questionnaire dans la liste
    for quizz_data in open_quizz_db_data:
        generate_json_file(quizz_data[0], quizz_data[1], quizz_data[2]) # création du fichier json correspond au dictionnaire
    # Gestion du titre des questionnaire passés depuis la console
    try:
        filename = sys.argv[1]
    except: # et sinon, proposition et choix parmi les questionnaires disponibles
        path_to_json = os.getcwd() # récupération du répertoire actuel
        json_files = show_json_files_in_directory(path_to_json)
        quizz_nb = ask_which_quizz_to_do(1, len(json_files))
        filename = json_files[quizz_nb-1]
        print(filename)
    quizz_dictionary = get_quizz_data_from_json_file(filename) # récupération du dictionnaire du quizz
    show_quizz_info(quizz_dictionary) # montrer les informations sur le quizz sélectionné
    quizz = quizz_creation_and_format(quizz_dictionary) # récupération du questionnaire formaté dans l'ordre pour le lancer
    Questionnaire(quizz).lancer() # Lancement du questionnaire