# -*- coding: utf-8 -*-
from constants import *


# GTE
gte_INIT = dict(
    PIk=13.9,
    NtGTE=6.3,
    T1=18 + KELVIN_CONST,
    T4=428 + KELVIN_CONST,
    p1=0.5
)

# STEAM
pte_INIT = dict(
    NtPTE=8,
    p6=1,
    T6=400 + KELVIN_CONST,
    h6=3264.39,
)
pte_INIT.update(dict(
    T7=pte_INIT['T6'] - Tcr,
    p7=2,
    h7=2270.91
))
pte_INIT.update(dict(
    T8=pte_INIT['T7'],
    p8=pte_INIT['p7'],
    h8=134.11
))

# COMBINED
combined_INIT = {}
combined_INIT.update(**gte_INIT)
combined_INIT.update(**pte_INIT)
