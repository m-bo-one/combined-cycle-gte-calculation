# -*- coding: utf-8 -*-
# FILE='cc_calc/real/gte_r.py'
from wspru_api import WspRuAPI
from init_data import INIT_DATA
from gte import GCCalcR, GTCalcR, CCCalcR
from helpers import lazyproperty


wspru_api = WspRuAPI()


class GTECalcR(GCCalcR, GTCalcR, CCCalcR):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.p1gte = self.piair
        self.T1gte = self.Tiair
        GCCalcR.__init__(self)
        GTCalcR.__init__(self)
        CCCalcR.__init__(self)

    @lazyproperty
    def Ggt(self):
        """Витрата газу через ГТ (кгг/с).
        """
        return (
            (self.giair_over + self.L0 + 1) / float(self.giair_over + self.L0)
        ) * self.Giair

    @lazyproperty
    def Bf(self):
        """Витрата палива (кгп/с).
        """
        return (1 / float(self.giair_over + self.L0)) * self.Giair

    @lazyproperty
    def NelGTE(self):
        """Потужність електрогенератора ГТУ (Вт).
        """
        return self.NgtGTE - self.NgcGTE

    @lazyproperty
    def Q1_gte(self):
        """Теплота, підведена в ГТУ (Вт)
        """
        return self.h1gte_lh * self.Giair + self.Ql_h * self.ETAc_c * self.Bf

    @lazyproperty
    def ETAelGTE(self):
        """Електричний ККД ГТУ.
        """
        return self.NelGTE / float(self.Q1_gte)


if __name__ == '__main__':
    real_calc = GTECalcR(**INIT_DATA)
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
