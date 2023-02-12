import requests
import json
import unicodedata

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
)

# MISSION
# Refaire fonctionner le script d'import
# Questionnaire
#   Fonctionne avec les fichiers JSON
#   Pouvoir donner un fichier en entrée, par exemple :
#   python questionnaire.py chats.json
# Affichier aussi
#   Le titre du questionnaire
#   La catégorie, la difficulté
#   Le nombre total de questions
#   Pour chaque question, afficher le numéro de la question. Exemple :  question n°1/20
# Qualité / autres développeurs
#   Soumettre le code dans GIT régulièrement
#       Créer un repo git et faire des commit à chaque ajout de nouvelle fonctionnalité
#   Commenter le code


# A ETUDIER
def strip_accents(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')


# FONCTION D'OBTENTION DU NOM DE FICHIER JSON SUR BASE DE LA CATEGORIE, TITRE ET NIVEAU DIFFICULTE
def get_quizz_filename(categorie, titre, difficulte):
    return strip_accents(categorie).lower().replace(" ", "") + "_" + strip_accents(titre).lower().replace(" ", "") + "_" + strip_accents(difficulte).lower().replace(" ", "") + ".json"


# CREATION DU FICHIER JSON UTILISE EN TANT QUE QUESTIONNAIRE A PARTIR DE L'URL CONTENANT DU JSON
def generate_json_file(categorie, titre, url):
    out_questionnaire_data = {"categorie": categorie, "titre": titre, "questions": []} # CREATION DU DICTIONNAIRE CONTENANT LE QUESTIONNAIRE
    out_questions_data = []
    response = requests.get(url) # récupération du contenu de la page au format binaire
    data = json.loads(response.text) # désérialisation
    all_quizz = data["quizz"]["fr"] # Récupération des données à utilisées > stockée dans le quizz français
    for quizz_title, quizz_data in all_quizz.items():
        out_filename = get_quizz_filename(categorie, titre, quizz_title) # Création du titre du quizz - quizz title correspond à la difficulté
        print(out_filename)
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
        print("end")


# Pour chaque questionnaire dans la liste
for quizz_data in open_quizz_db_data:
    generate_json_file(quizz_data[0], quizz_data[1], quizz_data[2]) # création du fichier json correspond au dictionnaire

