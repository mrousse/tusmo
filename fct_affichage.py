# JEU MO MO MO MOTUS V1 - MRousse 11/22
import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
import numpy as np
from fct_jeu import *
from fct_dico import *


# Gestion des boutons
def com_but_up(mot, d, button):
    """
    Fonction du bouton up level
    :param mot: mot concerné
    :param d: dictionnaire utilisé
    :param button: bouton à désactiver
    :return:
    """
    up_lvl(mot, d)
    button['state'] = 'disabled'

    return


def com_but_down(mot, d, button):
    """
    Fonction du bouton down level
    :param mot: mot concerné
    :param d: dictionnaire utilisé
    :param button: bouton à désactiver
    :return:
    """
    down_lvl(mot, d)
    button['state'] = 'disabled'

    return


class GUI:
    def __init__(self, Wind, d, x=900, y=400):
        self.d = d
        self.anti_d = d.copy()
        self.lvl_d = 0
        self.cur_d = {}

        # self.x = x  # larg
        # self.y = y  # hauteur
        self.Wind = Wind
        # Wind.geometry(str(x) + 'x' + str(y))
        Wind.title('Jeu de la TI')

        self.nbr_mots = 0
        self.score = 0
        self.mot_l = ['' for i in range(9)]
        self.l_mot = len(self.mot_l)

        dico_adapt(self.anti_d, self.cur_d, self.nbr_mots, self.lvl_d)      # Mise a niveau du dico

        self.ind_essai = 0
        self.col = 0
        self.aide_af = np.zeros([1, 26])
        self.list_rep = [' . ' for _ in range(self.l_mot)]
        self.list_af = np.zeros([1, self.l_mot])

        # Init les boutons (nouvelle partie, save, nbr de point, nbr de mots)
        panneau = ttk.LabelFrame(Wind, width=100)
        panneau.grid(column=0, row=0, padx=5, pady=5)

        # Nouvelle partie
        self.new_game = ttk.Button(panneau, text='New game', command=self.com_new_game)
        self.new_game.pack(anchor='center')

        # Load game
        self.load = ttk.Button(panneau, text='Load game', command=self.com_load_game)
        self.load.pack(anchor='center')

        try:                                    # Si pas de partie sauvegardee
            f = open('load_game', 'r')
        except FileNotFoundError:
            self.load.configure(state='disabled')

        # Save
        self.save = ttk.Button(panneau, text='Save', command=self.com_save_game)
        self.save.pack(anchor='center')

        if self.mot_l == ['' for i in range(9)] or self.ind_essai != 1:
            self.save.configure(state='disabled')

        # Nbr de mots
        txt_nbr_mots = ttk.Label(panneau, text='Nombre de mots : ')
        txt_nbr_mots.pack()
        self.lbl_nbr_mots = ttk.Label(panneau, text=str(self.nbr_mots))
        self.lbl_nbr_mots.pack()

        # Nbr de point
        txt_nbr_pts = ttk.Label(panneau, text='Score : ')
        txt_nbr_pts.pack()
        self.lbl_nbr_pts = ttk.Label(panneau, text=str(self.score))
        self.lbl_nbr_pts.pack()

        # Give up
        give_up = ttk.Button(panneau, text='Give up', command=self.end_game)
        give_up.pack()

        self.init_grille_jeu()
        self.init_grille_aide()

        self.Wind.bind('<KeyPress>', self.ecr_lettre)

        self.Wind.mainloop()

    # Creation des grilles
    def init_grille_jeu(self):
        # Creation du LabelFrame
        self.grille_jeu = ttk.LabelFrame(self.Wind, width=450, text=' Plateau de jeu ')
        self.grille_jeu.grid(column=1, row=0, padx=5, pady=5)
        # Creation de la grille vide
        for i in range(6):
            for j in range(self.l_mot):
                ttk.Label(self.grille_jeu, text=' . ').grid(column=j, row=i)

        return

    def init_grille_aide(self):
        alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                 'U', 'V', 'W', 'X', 'Y', 'Z']
        # Creation du LabelFrame
        self.grille_aide = ttk.LabelFrame(self.Wind, width=350, text=' Aide ')
        self.grille_aide.grid(column=2, row=0, padx=5, pady=5)
        # Creation de la grille vide
        ind = 0
        for i in range(4):
            for j in range(7):
                ttk.Label(self.grille_aide, text=alpha[ind]).grid(column=j, row=i)
                ind += 1
                if ind >= 25: break

        return

    # Modification des grilles
    def modif_row_jeu(self):
        for i in range(self.l_mot):
            if self.list_af[0][i] == 1:
                couleur = 'red'
            elif self.list_af[0][i] == 2:
                couleur = 'orange'
            else:
                couleur = ''
            ttk.Label(self.grille_jeu, text=self.list_rep[i], background=couleur).grid(column=i, row=self.ind_essai)

        for j in range(9 - self.l_mot):
            ttk.Label(self.grille_jeu, text='  ').grid(column=self.l_mot + j, row=self.ind_essai)

        return

    def modif_aide(self):
        alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                 'U', 'V', 'W', 'X', 'Y', 'Z']
        ind = 0
        for i in range(4):
            for j in range(7):
                if self.aide_af[0][ind] == 1:
                    couleur = 'red'
                elif self.aide_af[0][ind] == 2:
                    couleur = 'orange'
                elif self.aide_af[0][ind] == 3:
                    couleur = 'grey'
                else:
                    couleur = ''
                ttk.Label(self.grille_aide, text=alpha[ind], background=couleur).grid(column=j, row=i)
                ind += 1
                if ind >= 26: break

        return

    # Ecriture
    def ecr_lettre(self, lettre):
        alpha = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                 'U', 'V', 'W', 'X', 'Y', 'Z']
        alpha_min = {"a": 'A', "b": 'B', "c": 'C', "d": 'D', "e": 'E', "f": 'F', "g": 'G', "h": 'H',
                     "i": 'I', "j": 'J', "k": 'J', "l": 'L', "m": 'M', "n": 'N', "o": 'O', "p": 'P',
                     "q": 'Q', "r": 'R', "s": 'S', "t": 'T', "u": 'U', "v": 'V', "w": 'W', "x": 'X',
                     "y": 'Y', "z": 'Z'}

        if lettre.keysym in alpha and self.col < self.l_mot:
            ttk.Label(self.grille_jeu, text=lettre.keysym).grid(column=self.col, row=self.ind_essai)
            self.list_rep[self.col] = lettre.keysym
            self.col += 1
        elif lettre.keysym in alpha_min.keys() and self.col < self.l_mot:
            ttk.Label(self.grille_jeu, text=alpha_min[lettre.keysym]).grid(column=self.col, row=self.ind_essai)
            self.list_rep[self.col] = alpha_min[lettre.keysym]
            self.col += 1
        elif lettre.keysym == 'BackSpace' and self.col > 0 :
            ttk.Label(self.grille_jeu, text=' . ').grid(column=self.col - 1, row=self.ind_essai)
            self.list_rep[self.col - 1] = ' . '
            self.col -= 1
        elif lettre.keysym == 'Return' and self.col == len(self.list_rep):
            mot = ''
            for i in range(self.l_mot):
                mot += self.list_rep[i]
            if mot in self.d.keys():
                nxt_rep = test_rep(self.mot_l, self.list_rep, self.list_af)
                if self.list_rep == self.mot_l :
                    self.win_mot()
                else :
                    test = self.new_try()
                    self.list_rep = nxt_rep
                    if not(test):
                        self.end_game()
            else :
                messagebox.showerror(" Erreur dans la reponse ", "Eh tu essayes de me gruger là ! Ton mot il existe "
                                                                 "pas ! ")
        else:
            if self.col > self.l_mot:
                messagebox.showerror(" Erreur dans la reponse ", "Certes c'est pas la taille qui compte mais fait un "
                                                                 "effort stp... ")
            else :
                messagebox.showerror(" Erreur dans la reponse ", " Concentre toi enfin... ")

        return

    # Gain de manche
    def win_mot(self):
        self.grille_jeu.destroy()
        self.init_grille_jeu()
        self.init_grille_aide()
        self.list_rep = [' . ' for _ in range(self.l_mot)]

        self.mot_l = new_mot(self.cur_d)
        self.l_mot = len(self.mot_l)

        self.list_rep = [' . ' for _ in range(self.l_mot)]
        self.list_rep[0] = self.mot_l[0]
        self.col = 1
        self.ind_essai = 0

        self.list_af = np.zeros([1, self.l_mot])
        self.list_af[0][0] = 1
        self.aide_af = np.zeros([1, 26])

        mot = ''
        for i in range(self.l_mot):
            mot += self.mot_l[i]
        self.score = val_score(self.score, mot, self.ind_essai, self.d)
        self.lbl_nbr_pts.configure(text=str(self.score))
        self.nbr_mots += 1
        self.lbl_nbr_mots.configure(text=str(self.nbr_mots))

        self.modif_row_jeu()

        return

    # Nouvel essai
    def new_try(self):
        self.modif_row_jeu()
        list_aide(self.list_rep, self.list_af, self.aide_af)
        self.modif_aide()

        self.ind_essai += 1
        if self.ind_essai >= 6:
            return False

        self.col = 1
        while self.list_af[0][self.col] == 1:
            self.col += 1

        for i in range(len(self.list_rep)):
            if self.list_af[0][i] == 1:
                self.list_rep[i] = self.mot_l[i]
            else :
                self.list_rep[i] = ' . '

        for i in range(self.l_mot):
            if self.list_af[0][i] != 1:
                self.list_af[0][i] = 0

        self.modif_row_jeu()

        return True

    # Fin de partie
    def end_game(self):
        loser = ttk.LabelFrame(self.Wind)
        loser.grid(column=1, row=2)
        mot = ''
        for i in range(self.l_mot): mot += self.mot_l[i]
        txt = 'Le mot était : ' + mot + '\n Ton mot était trop dur ? '
        ttk.Label(loser, text=txt).grid(column=1, row=0)
        dur = tk.Button(loser, text="Oui t'abuses", command=lambda: com_but_up(mot, self.d, dur))
        dur.grid(column=0, row=1)
        facile = tk.Button(loser, text='Nan je suis \n juste nul.le', command=lambda: com_but_down(mot, self.d, facile))
        facile.grid(column=2, row=1)

        return

    # Commandes
    def com_new_game(self):
        # nouveau mot, modif affichage ligne 1, score et nbr de mot à 0, reset listes af
        self.grille_jeu.destroy()
        self.init_grille_jeu()

        self.mot_l = new_mot(self.cur_d)
        self.l_mot = len(self.mot_l)

        self.list_rep = [' . ' for _ in range(self.l_mot)]
        self.list_rep[0] = self.mot_l[0]
        self.col = 1
        self.ind_essai = 0

        self.list_af = np.zeros([1, self.l_mot])
        self.list_af[0][0] = 1
        self.aide_af = np.zeros([1, 26])

        self.modif_row_jeu()

        self.score = 0
        self.nbr_mots = 0

        self.save.configure(state='enable')

        return


    def com_save_game(self):
        """
        Contient score, nbr mots, mot courant, liste d'aide, ind essai
        :return:
        """
        f = open('load_game.txt', 'w')
        contenu = ['' for i in range(5)]
        contenu[0] = 'score ' + str(self.score)
        contenu[1] = '\nnbr_mots ' + str(self.nbr_mots)
        contenu[2] = '\nmot ' + str(self.mot_l)
        contenu[3] = '\naide ' + str(self.aide_af)
        contenu[4] = '\nessai ' + str(self.ind_essai)
        print(contenu)
        f.writelines(contenu)

        messagebox.showinfo(" Sauvegarde ", " Sauvegarde effectuée ")
        f.close()
        return

    def com_load_game(self):
        """
        Charge score, nbr mots, mot courant, liste d'aide, ind essai
        :return:
        """
        f = open('load_game', 'r')

        score = f.readline()
        self.score = score.split(' ')[1]

        nbr_mots = f.readline()
        self.nbr_mots = nbr_mots.split(' ')[1]

        mot = f.readline()
        self.mot_l = mot.split(' ')[1]

        aide = f.readline()
        aide_val = aide.split(' ')
        aide_val.remove(aide_val[0])
        aide_val[0] = aide_val[0][2]
        aide_val[23] = aide_val[23][0]
        aide = f.readline()
        aide_val += aide.split(' ')
        aide_val.remove('')
        aide_val.remove('')
        aide_val[25] = aide_val[25][0]
        self.aide_af = [int(x[0]) for x in aide_val]

        essai = f.readline()
        self.ind_essai = essai.split(' ')[1]
        f.close()

        self.modif_row_jeu()
        self.modif_aide()
        return


