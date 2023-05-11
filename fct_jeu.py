# JEU MO MO MO MOTUS V1 - MRousse 11/22
import random as rd


def new_mot(d) -> list:
    """
    Tire au sort le mot à deviner
    :param d: dictionnaire
    :return: liste des lettres du mot
    """
    keys = list(d.keys())
    mot = rd.choice(keys)  # mot a deviner
    mot_l = list(mot)  # liste des lettres
    return mot_l


def val_score(score, mot, ind_essai, d):
    """
    Calcule le score obtenu
    :param score: score actuel
    :param mot: mot devine
    :param ind_essai: indice de l'essai gagnant
    :param d: dico utilisé
    :return: nouveau score
    """
    score += d[mot] * 100
    score += (6-ind_essai)*50

    return score


def is_in(lettre, ind, mot, rep) -> int:
    """
    Cherche la résence d'une lettre dans un mot
    :param lettre: lettre etudiee
    :param ind: indice de la lettre dans le mot d'origine
    :param mot: mot de reference
    :param rep: reponse
    :return: 0 si pas dans le mot, 1 si bonne place, 2 si mal placee
    """
    l = len(mot)
    for i in range(l):
        if lettre == mot[i]:
            if i == ind:
                rep[i] = lettre
                mot[i] = '.'
                return 1
            else :
                mot[i] = '.'
                return 2
    return 0


def test_rep(mot, rep, af_jeu):
    """
    Modifie les listes d'affichage
    :param mot: mot de reference
    :param rep: reponse a tester
    :param af_jeu: couleurs de la ligne a afficher
    :return: prochaine rep
    """
    l = len(mot)
    cop_mot = mot.copy()
    nxt_rep = [' . ' for i in range(l)]
    for i in range(l):
        couleur = is_in(rep[i], i, cop_mot, nxt_rep)
        af_jeu[0][i] = couleur
    return nxt_rep


def list_aide(rep, af_jeu, af_aide):
    """
    Modifier l'af_aide en fct de af_jeu
    :param rep: reponse
    :param af_jeu: couleurs des lettres trouvees
    :param af_aide: couleurs des lettres de l'aide
    :return: af_aide
    """
    alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
             'U', 'V', 'W', 'X', 'Y', 'Z']

    for i in range(len(rep)):
        if af_jeu[0][i] == 1:
            for j in range(len(alpha)):
                if rep[i] == alpha[j]: af_aide[0][j] = 1
        elif af_jeu[0][i] == 2:
            for j in range(len(alpha)):
                if rep[i] == alpha[j]: af_aide[0][j] = 2
        else :
            for j in range(len(alpha)):
                if rep[i] == alpha[j] and af_aide[0][j]==0 : af_aide[0][j] = 3
    return