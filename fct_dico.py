# JEU MO MO MO MOTUS V1 - MRousse 11/22
import csv


def op_dict(namefile) -> dict:
    """
    Ouvre le fichier et créé le dictionary
    :param namefile: nom du fichier
    :return: d
    """
    d = {}
    f = open(namefile, 'r', newline='')
    w = csv.reader(f)

    for row in w:
        # key_val = row.split(',')
        # d[key_val[0]] = key_val[1]
        d[row[0]] = int(row[1])

    f.close()
    return d


def save_dict(d, fichier):
    """
    Sauvegarde le dictionnaire courant et écrase le précédent si besoin
    :param d: dictionnaire courant
    :param fichier: emplacement de la sauvegarde en .csv
    :return:
    """

    f = open(fichier, 'w', newline='')
    w = csv.writer(f)
    keys = d.keys()
    for key in keys:
        w.writerow([key, d[key]])

    f.close()
    return


def up_lvl(mot, d):
    """
    Augmente le niveau du mot
    :param mot: mot étudié
    :param d: dico utilisé
    :return:
    """
    if d[mot] < 5: d[mot] = d[mot] + 1
    save_dict(d, 'dico_new.csv')

    return


def down_lvl(mot, d):
    """
        Diminue le niveau du mot
        :param mot: mot étudié
        :param d: dico utilisé
        :return:
    """
    if d[mot] > 0: d[mot] = d[mot] - 1
    save_dict(d, 'dico_new.csv')

    return


def dico_adapt(d, cur_d, nbr_mots, lvl_d):
    """
    Modifier le dictionnaire courant en fct du niveau actuel
    :param d: d sans les mots de cur_d (ie ceux trop durs)
    :param cur_d: d actuel
    :param nbr_mots: niveau actuel du joueur
    :param lvl_d: niveau actuel de d
    :return:
    """
    lvl = {0: 1, 3:2, 6:3, 10:4, 20: 5}                 # Correspondance entre le nbr de mot (ie lvl joueur)
    mots = list(d.keys()).copy()                        # et le niveau des mots du dico
    if lvl[nbr_mots] > lvl_d:
        for mot in mots:
            if d[mot] <= lvl[nbr_mots]:
                cur_d[mot] = d[mot]
                del d[mot]
        lvl_d = lvl[nbr_mots]

    return
