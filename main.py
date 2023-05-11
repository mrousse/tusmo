# JEU MO MO MO MOTUS V1 - MRousse 02/11/22

import numpy as np
from fct_dico import *
from fct_affichage import *

# Ouverture du dictionnaire :
d = op_dict('dico_new.csv')

# Ouverture de l'affichage
Wind = tk.Tk()
Main_GUI = GUI(Wind, d)
