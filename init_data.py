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
    # NtPTE=8,
    m=0.5,
    T1=15 + KELVIN_CONST,
    p6=15,
    T6=100 + KELVIN_CONST,
    # h6=3264.39,
)

# COMBINED
combined_INIT = {}
combined_INIT.update(**gte_INIT)
combined_INIT.update(**pte_INIT)
