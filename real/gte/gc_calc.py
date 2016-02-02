# -*- coding: utf-8 -*-
# FILE='cc_calc/real/gte_r/gc_calc.py'
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


from wspru_api import WspRuAPI
from init_data import INIT_DATA


wspru_api = WspRuAPI()


class GCCalcR(object):

    @property
    def p2gte(self):
        """Тиск після ГК (Па).
        """
        return self.PIk * self.p1gte

    @property
    def pbiair(self):
        """Граничний тиск води при температурі навколишнього середовища (Па).
        """
        if self.Tiair > 273.15:
            _p = wspru_api.wsp('PST', self.Tiair)
        else:
            _p = wspru_api.wsp('PSUBT', self.Tiair)
        return _p / float(10**6)

    @property
    def xiair(self):
        """Молярний вміст води.
        """
        return self.phiiair * self.pbiair \
            / float(self.piair - self.phiiair * self.pbiair)

    @property
    def diair(self):
        """Масовий вміст води (кгп/кгсв).
        """
        return self.xiair * wspru_api.wspg('MMGS', 'H2O') \
            / float(wspru_api.wspg('MMGS', 'AirMix'))

    @property
    def gsiair(self):
        """Створення розрахункової суміші вологого повітря.
        """
        return "AirMix:1;H2O:" + str(self.xiair)

    @property
    def h1gte(self):
        """Ентальпія вологого повітря при атмосферних умовах (Дж/кгп).
        """
        return wspru_api.wspg('HGST', self.gsiair, self.Tiair)

    @property
    def h2gte(self):
        """Ентальпія повітря за К при ізоентропному стиску (Дж/кгп).
        """
        return wspru_api.wspg('HGST', self.gsiair, self.T2gte)

    @property
    def s1gte(self):
        """Ентропія повітря перед К (Дж/кгп*К).
        """
        return wspru_api.wspg('SGSPT', self.gsiair, self.piair, self.Tiair)

    @property
    def T2gte(self):
        """Температура повітря за К при ізоентропному стиску (К).
        """
        return wspru_api.wspg('TGSPS', self.gsiair, self.p2gte, self.s1gte)

    @property
    def T2gte_r(self):
        """Температура повітря за К при реальному стиску (К).
        """
        return wspru_api.wspg('TGSH', self.gsiair, self.h2gte_r)

    @property
    def lcgte(self):
        """Теплоперепад в К при ізоентропному стиску  (Дж/кгг).
        """
        return self.h2gte - self.h1gte

    @property
    def lcgte_r(self):
        """Теплоперепад в К при реальному стиску (Дж/кгг).
        """
        return self.lcgte / float(self.ETAoi_c)

    @property
    def h2gte_r(self):
        """Ентальпія повітря за К при реальному стиску (Дж/кгп).
        """
        return self.h1gte + self.lcgte_r

    @property
    def s2gte_r(self):
        """Ентропія повітря за К при реальному стиску (Дж/кгп*К).
        """
        return wspru_api.wspg('SGSPT', self.gsiair, self.p2gte, self.T2gte_r)

    @property
    def NgcGTE(self):
        """Потужність компресора (Вт).
        """
        return self.lcgte_r * self.Giair / float(self.ETAm_gte)
