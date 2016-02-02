# -*- coding: utf-8 -*-
# FILE='cc_calc/real/gte_r.py'
from wspru_api import WspRuAPI
from init_data import INIT_DATA


wspru_api = WspRuAPI()


class GTECalcR(object):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.p1gte = self.piair
        self.T1gte = self.Tiair

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
        """Ентальпія вологого повітря при атмосферних умовах (Дж/кгв).
        """
        return wspru_api.wspg('HGST', self.gsiair, self.Tiair)

    @property
    def h2gte(self):
        """Ентальпія повітря за К при ізоентропному стиску (Дж/кгв).
        """
        return wspru_api.wspg('HGST', self.gsiair, self.T2gte)

    @property
    def s1gte(self):
        """Ентропія повітря перед К (Дж/кгв*К).
        """
        return wspru_api.wspg('SGSPT', self.gsiair, self.piair, self.Tiair)

    @property
    def T2gte(self):
        """Температура повітря за К при ізоентропному стиску (К).
        """
        return wspru_api.wspg('TGSPS', self.gsiair, self.p2gte, self.s1gte)

    @property
    def h3gte(self):
        """Ентальпія продуктів зорання при температурі перед ГТ (Дж/кгг).
        """
        return wspru_api.wspg('HGST', self.gsg, self.T3gte)

    @property
    def h4gte(self):
        """Ентальпія робочого тіла за ГТ при ізоентропному розширенні (Дж/кгг).
        """
        return wspru_api.wspg('HGST', self.gsg, self.T4gte)

    @property
    def p3gte(self):
        """Тиск до ГТ (Па).
        """
        return self.p2gte * (1 - self.sigmapb)

    @property
    def s4gte(self):
        """Ентропя після ГТ (Дж/кгв*К).
        """
        return wspru_api.wspg('SGSPT', self.gsg, self.p4gte, self.T4gte)

    @property
    def p4gte(self):
        """Тиск після ГТ (Па).
        """
        return self.piair * (1 - self.sigmapp)

    @property
    def T3gte(self):
        """Температура після КС при ізоентропному розширенні (K).
        """
        return wspru_api.wspg('TGSPS', self.gsiair, self.p3gte, self.s4gte)

    @property
    def lgtgte(self):
        """Теплоперепад в ГТ при ізоентропному розширенні (Дж/кгг).
        """
        return self.h3gte - self.h4gte

    @property
    def lgtgte_r(self):
        """Теплоперепад в ГТ при реальному розширенні (Дж/кгг).
        """
        return self.lgtgte * self.ETAoi_gt

    @property
    def NgtGTE(self):
        """Потужність ГТ (Вт).
        """
        return self.lgtgte_r * self.Gr * self.ETAm_gte

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
    def NcGTE(self):
        """Потужність компресора (Вт).
        """
        return self.lcgte_r * self.Bf / float(self.ETAm_gte)

    @property
    def Gr(self):
        """Витрата газу через ГТ (кгг/с).
        """
        return self.Giair + self.Bf

    @property
    def NelGTE(self):
        """Потужність електрогенератора ГТУ (Вт).
        """
        return self.ETAg_gte * (self.NgtGTE - self.NcGTE)

    @property
    def Q1_gte(self):
        """Теплота, підведена в ГТУ (Вт)
        """
        return self.Ql_h * self.ETAc_c * self.Bf

    @property
    def ETAelGTE(self):
        """Електричний ККД ГТУ.
        """
        return self.NelGTE / float(self.Q1_gte)


if __name__ == '__main__':
    real_calc = GTECalcR(**INIT_DATA)
    print real_calc.s1gte
    with open('test_r.txt', 'w') as writer:
        for x in xrange(1, 5):
            pressure = getattr(real_calc, 'p%sgte' % x)
            temperature = getattr(real_calc, 'T%sgte' % x)
            enthropy = wspru_api.wspg('SGSPT', 'AirMix', pressure, temperature)
            writer.write('Point %s\n' % x)
            writer.write("pressure: %s" % pressure)
            writer.write('\n')
            writer.write("temp: %s" % temperature)
            writer.write('\n')
            writer.write("enthropy: %s" % enthropy)
            writer.write('\n' + "-" * 10 + '\n')
