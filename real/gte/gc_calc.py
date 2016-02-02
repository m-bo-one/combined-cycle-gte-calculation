# -*- coding: utf-8 -*-
# FILE='cc_calc/real/gte/gc_calc.py'
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


from wspru_api import WspRuAPI
from helpers import lazyproperty


wspru_api = WspRuAPI()


class GCCalcR(object):

    @lazyproperty
    def p2gte(self):
        """Тиск після ГК (Па).
        """
        return self.PIk * self.p1gte

    @lazyproperty
    def pbiair(self):
        """Граничний тиск води при температурі навколишнього середовища (Па).
        """
        if self.Tiair > 273.15:
            _p = wspru_api.wsp('PST', self.Tiair)
        else:
            _p = wspru_api.wsp('PSUBT', self.Tiair)
        return _p / float(10**6)

    @lazyproperty
    def xiair(self):
        """Молярний вміст води.
        """
        return self.phiiair * self.pbiair \
            / float(self.piair - self.phiiair * self.pbiair)

    @lazyproperty
    def diair(self):
        """Масовий вміст води (кгп/кгсв).
        """
        return self.xiair * wspru_api.wspg('MMGS', 'H2O') \
            / float(wspru_api.wspg('MMGS', 'AirMix'))

    @lazyproperty
    def gsiair(self):
        """Створення розрахункової суміші вологого повітря.
        """
        return "AirMix:1;H2O:" + str(self.xiair)

    @lazyproperty
    def h1gte(self):
        """Ентальпія вологого повітря при атмосферних умовах (Дж/кгп).
        """
        return wspru_api.wspg('HGST', self.gsiair, self.Tiair)

    @lazyproperty
    def h2gte(self):
        """Ентальпія повітря за К при ізоентропному стиску (Дж/кгп).
        """
        return wspru_api.wspg('HGST', self.gsiair, self.T2gte)

    @lazyproperty
    def s1gte(self):
        """Ентропія повітря перед К (Дж/кгп*К).
        """
        return wspru_api.wspg('SGSPT', self.gsiair, self.piair, self.Tiair)

    @lazyproperty
    def T2gte(self):
        """Температура повітря за К при ізоентропному стиску (К).
        """
        return wspru_api.wspg('TGSPS', self.gsiair, self.p2gte, self.s1gte)

    @lazyproperty
    def T2gte_r(self):
        """Температура повітря за К при реальному стиску (К).
        """
        return wspru_api.wspg('TGSH', self.gsiair, self.h2gte_r)

    @lazyproperty
    def lcgte(self):
        """Теплоперепад в К при ізоентропному стиску  (Дж/кгг).
        """
        return self.h2gte - self.h1gte

    @lazyproperty
    def lcgte_r(self):
        """Теплоперепад в К при реальному стиску (Дж/кгг).
        """
        return self.lcgte / float(self.ETAoi_c)

    @lazyproperty
    def h2gte_r(self):
        """Ентальпія повітря за К при реальному стиску (Дж/кгп).
        """
        return self.h1gte + self.lcgte_r

    @lazyproperty
    def s2gte_r(self):
        """Ентропія повітря за К при реальному стиску (Дж/кгп*К).
        """
        return wspru_api.wspg('SGSPT', self.gsiair, self.p2gte, self.T2gte_r)

    @lazyproperty
    def NgcGTE(self):
        """Потужність компресора (Вт).
        """
        return self.lcgte_r * self.Giair / float(self.ETAm_gte)
