# -*- coding: utf-8 -*-
from constants import *

# third party
from pyXSteam.XSteam import XSteam
steamTable = XSteam(XSteam.UNIT_SYSTEM_MKS)


INIT_DATA = {
    "PIk": 13, # ступінь підвищення тиску в компресорі
    "T1": 15 + KELVIN_CONST, # температурі на вході в компресорі, К,
    "T4": 420 + KELVIN_CONST, # температура на виході з турбіни, К,
    "p1": 0.1, # тиск на вході в компресор, МПа,
    "p6": 15, # тиск на вході в парову турбіну, МПа,
    "T6": 300 + KELVIN_CONST, # температура на вході в парову турбіну, К,
    "T5": 150 + KELVIN_CONST, # температура газу на виході з КУ, К
    "Tcr": 17, # різниця температур в конденсаторі
}
