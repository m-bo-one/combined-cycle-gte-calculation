# -*- coding: utf-8 -*-
# FILE='cc_calc/selection/init_data.py'
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


from ideal.constants import *


INIT_DATA = {
    "Tb_out": 300 + KELVIN_CONST, # температура на виході з КУ в циклі, К
    "T1gte": 15 + KELVIN_CONST, # температура навк. середовища, К
    "pb_out": 6 * 10**6, # тиск на виході з КУ в циклі, Па
    "Tc_r": 15, # різниця температур в конденсаторі
    "ETAg_spe": 99.8 / P_100, # ККД електрогенератора ПТУ, %
    "ETAm_spe": 99.8 / P_100, # ККД мех. ПТУ, %
    "sigmapp": 1 / P_100, # втрати тиску між КУ та ПТ, %
}

GTES = {
    "SGT-100": {
        "constructor": "Siemens",
        "NelGTE": 5.05 * 10**6,
        "ETAelGTE": 0.302,
        "PIk": 14,
        "T4gte": 531 + KELVIN_CONST,
        "Ggt": 20.6
    },
    "UGT-5000": {
        "constructor": "Zorya-Mashproekt",
        "NelGTE": 5.25 * 10**6,
        "ETAelGTE": 0.315,
        "Ggt": 21.5,
        "PIk": 14,
        "T4gte": 480 + KELVIN_CONST,
    },
    "Centaur-50": {
        "constructor": "Solar Turbines",
        "NelGTE": 4.6 * 10**6,
        "ETAelGTE": 0.293,
        "Ggt": 19.078,
        "PIk": 14,
        "T4gte": 510 + KELVIN_CONST,
    },
}
for key in GTES.iterkeys():
    GTES[key].update(**INIT_DATA)

INIT_DATA = GTES.copy()
