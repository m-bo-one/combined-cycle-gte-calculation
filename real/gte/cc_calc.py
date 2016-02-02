# -*- coding: utf-8 -*-
# FILE='cc_calc/real/gte/cc_calc.py'
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


from wspru_api import WspRuAPI
from helpers import lazyproperty


wspru_api = WspRuAPI()


class CCCalcR(object):

    @lazyproperty
    def h3cp(self):
        """Ентальпія продуктів згорання перед ГТ (Дж/кгг).
        """
        return wspru_api.wspg('HGST', self.gs0, self.T3gte)

    @lazyproperty
    def h3iair(self):
        """Ентальпія повітря при температурі перед турбіною (Дж/кгг).
        """
        return wspru_api.wspg('HGST', self.gsiair, self.T3gte)

    @lazyproperty
    def h1gte_lh(self):
        """Ентальпія перед ГК при ізоентропному стиску до температури
        визначення Ql_h (Дж/кгг).
        """
        return self.h1gte - wspru_api.wspg('HGST', self.gsiair, self.Tl_h)

    @lazyproperty
    def h2gte_r_lh(self):
        """Ентальпія після ГК при ізоентропному стиску до температури
        визначення Ql_h (Дж/кгг).
        """
        return self.h2gte_r - wspru_api.wspg('HGST', self.gsiair, self.Tl_h)

    @lazyproperty
    def h3cp_lh(self):
        """Ентальпія продуктів згорання перед ГТ до температури
        визначення Ql_h (Дж/кгг).
        """
        return self.h3cp - wspru_api.wspg('HGST', self.gs0, self.Tl_h)

    @lazyproperty
    def h3iair_lh(self):
        """Ентальпія повітря при температурі перед турбіною до температури
        визначення Ql_h (Дж/кгг).
        """
        return self.h3iair - wspru_api.wspg('HGST', self.gsiair, self.Tl_h)

    @lazyproperty
    def giair_over(self):
        """Надлишкова витрата повітря в розрахунку 1 кг палива.
        """
        return (self.h2gte_r_lh * self.L0 - (self.L0 + 1) * self.h3cp_lh + \
            self.Ql_h * self.ETAc_c) / float(self.h3iair_lh - self.h2gte_r_lh)
