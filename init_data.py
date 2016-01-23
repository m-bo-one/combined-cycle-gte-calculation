# -*- coding: utf-8 -*-
from constants import *

# third party
from pyXSteam.XSteam import XSteam
steamTable = XSteam(XSteam.UNIT_SYSTEM_MKS)


PIk = 5 # степень повышения давления в компрессоре
NtGTE = 6.3 # выходная мощность турбинны в ГТУ, МВт
T1 = 30 + KELVIN_CONST # температура на входе в компрессор, К
T4 = 300 + KELVIN_CONST # температура на выходе из турбинны, К
p1 = 0.1 # давление на входе в компрессор, МПа
p6 = 30 # давление на входе в паровую турбинну, МПа
T6 = 300 + KELVIN_CONST # температура на входе в паровую турбинну, К
deltaTc = 200 + KELVIN_CONST # разница температуры для подбора котла
m = 0.5 # массовой расход, кг/с
T5 = T4 - deltaTc # температура газа на выходе из котла-утилизатора, К
Tcr = 17


INIT_DATA = {
    "PIk": PIk,
    "NtGTE": NtGTE,
    "T1": T1,
    "T4": T4,
    "p1": p1,
    "p6": p6,
    "T6": T6,
    "m": m,
    "T5": T5,
    "Tcr": Tcr
}
