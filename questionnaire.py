

class Question:
    def __init__(self, titre, choix, bonne_reponse):
        self.titre = titre
        self.choix = choix
        self.bonne_reponse = bonne_reponse

    def FromData(data):
        q = Question(data[2], data[0], data[1]) # data[2] = bonne réponse / data[0] = question / data[1] = liste des choix
        return q

    def poser(self, question_number, total_questions):
        print(f"Question n°{question_number}/{total_questions}")
        print("  " + self.titre)
        for i in range(len(self.choix)):
            print("  ", i+1, "-", self.choix[i])

        print()
        resultat_response_correcte = False
        reponse_int = Question.demander_reponse_numerique_utlisateur(1, len(self.choix))
        if self.choix[reponse_int-1].lower() == self.bonne_reponse.lower():
            print("Bonne réponse")
            resultat_response_correcte = True
        else:
            print("Mauvaise réponse")
            
        print()
        return resultat_response_correcte

    def demander_reponse_numerique_utlisateur(min, max):
        reponse_str = input("Votre réponse (entre " + str(min) + " et " + str(max) + ") : ")
        try:
            reponse_int = int(reponse_str)
            if min <= reponse_int <= max:
                return reponse_int

            print("ERREUR : Vous devez rentrer un nombre entre", min, "et", max)
        except:
            print("ERREUR : Veuillez rentrer uniquement des chiffres")
        return Question.demander_reponse_numerique_utlisateur(min, max)
    
class Questionnaire:
    def __init__(self, questions): # La liste de questions est composées de tuple de question = QUESTION / CHOIX / REPONSE
        self.questions = questions

    def lancer(self):
        score = 0
        total_questions = len(self.questions)
        for i in range(0, total_questions):
            if self.questions[i].poser(i+1, total_questions): # passage du numéro de la question et du nombre total de question à la fonction poser pour affichage
                score += 1
        print("Score final :", score, "sur", len(self.questions))
        return score


