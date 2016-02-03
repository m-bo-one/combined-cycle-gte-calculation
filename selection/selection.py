# -*- coding: utf-8 -*-
# FILE='cc_calc/selection/selection.py'
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


from init_data import INIT_DATA
from real.helpers import lazyproperty
from real.wspru_api import WspRuAPI


wspru_api = WspRuAPI()


class SelectionCalcR(object):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @lazyproperty
    def Q1_gte(self):
        """Теплота, підведена в ГТУ (Вт)
        """
        return self.NelGTE / float(self.ETAelGTE)

    @lazyproperty
    def hb_in(self):
        """Ентальпія пару на вході в КУ (Дж/кгвп).
        """
        return wspru_api.wspg('HGST', 'AirMix', self.T4gte)

    @lazyproperty
    def hb_out(self):
        """Ентальпія пару на виході з КУ в циклі (Дж/кгвп).
        """
        return wspru_api.wsp('HPT', self.pb_out, self.Tb_out)

    @lazyproperty
    def Db(self):
        """Витрата пару котра генеруеться КУ (кгвп/с).
        """
        return self.Ggt * self.hb_in / float(self.hb_out)

    @lazyproperty
    def hst_in(self):
        """Ентальпія пару на вході в ПТ (Дж/кгвп).
        """
        return wspru_api.wsp('HPT', self.pst_in, self.Tb_out)

    @lazyproperty
    def pst_in(self):
        """Тиск пару на вході в ПТ (Па).
        """
        return self.pb_out * (1 - self.sigmapp)

    @lazyproperty
    def Tst_out(self):
        """Температура пару на виході із ПТ (К).
        """
        return self.T1gte + self.Tc_r

    @lazyproperty
    def pst_out(self):
        """Тиск пару на виході в ПТ (Дж/кгвп).
        """
        return wspru_api.wsp('PST', self.Tst_out)

    @lazyproperty
    def hst_out(self):
        """Ентальпія пару на виході в ПТ (Дж/кгвп).
        """
        return wspru_api.wsp('HPT', self.pst_out, self.Tst_out)

    @lazyproperty
    def Pst(self):
        """Внутрішня потужність ПТ (Вт).
        """
        return self.Db * (self.hst_in - self.hst_out)

    @lazyproperty
    def NelSPE(self):
        """Електрична потужність ПТУ (Вт).
        """
        return (self.Pst - 1 * 10**3) * self.ETAm_spe * self.ETAg_spe

    @lazyproperty
    def NelCC(self):
        """Електрична потужність ПГУ (Вт).
        """
        return self.NelGTE + self.NelSPE

    @lazyproperty
    def ETAelCC(self):
        """Електрична потужність ПГУ.
        """
        return self.NelCC / float(self.Q1_gte)


if __name__ == '__main__':
    for key in INIT_DATA.iterkeys():
        calc = SelectionCalcR(**INIT_DATA[key])
        print key
        print calc.ETAelGTE
        print calc.ETAelCC
        print "-" * 10
