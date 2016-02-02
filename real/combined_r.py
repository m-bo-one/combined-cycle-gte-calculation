# -*- coding: utf-8 -*-
# FILE='cc_calc/real/combined_r.py'
from wspru_api import WspRuAPI
from init_data import INIT_DATA
from gte_r import GTECalcR
from helpers import lazyproperty


wspru_api = WspRuAPI()


class CombinedCalcR(GTECalcR):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.p1gte = self.piair
        self.T1gte = self.Tiair
        self._check_boiler_temperature()
        self.Q1_cc = self.Q1_gte

    def _check_boiler_temperature(self):
        """Перевірка різниці температур на вході та після КУ (не менше ніж 20 оС).
        """
        _diff = self.T4gte - self.Tb_out
        if _diff < 20:
            raise BaseException("Різниця між вихідними газами з ГТУ ({0}) "
                "та на виході з КУ ({1}) повинна бути більше ніж 20 оС. (Зараз {2})"
                .format(
                    self.T4gte, self.Tb_out, _diff))
        return

    @lazyproperty
    def pd(self):
        """Тиск пару в барабані КУ (Па).
        """
        return self.p4gte + self.deltaps

    @lazyproperty
    def hb_in(self):
        """Ентальпія пару на вході в КУ (Дж/кгвп).
        """
        return wspru_api.wspg('HGST', self.gsg, self.T4gte)

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
    def pst_in(self):
        """Тиск пару на вході в ПТ (Па).
        """
        return self.pb_out * (1 - self.sigmapp)

    @lazyproperty
    def hst_in(self):
        """Ентальпія пару на вході в ПТ (Дж/кгвп).
        """
        return wspru_api.wsp('HPT', self.pst_in, self.Tb_out)

    @lazyproperty
    def h2spe(self):
        """Ентальпія пару після ПТ (Дж/кгвп).
        """
        return wspru_api.wsp('HPT', self.p2spe, self.T2spe)

    @lazyproperty
    def hout(self):
        """Ентальпія пару на виході з КУ (Дж/кгг).
        """
        return self.hb_in - self.ETAb * \
            (self.hb_in - wspru_api.wspg('HGST', self.gsg, self.Tiair))

    @lazyproperty
    def teta_out(self):
        """Температура вихлопних газів з КУ (К).
        """
        return wspru_api.wspg('TGSH', self.gsg, self.hout)

    @lazyproperty
    def Pst(self):
        """Внутрішня потужність ПТ (Вт).
        """
        return self.Db * (self.hst_in - self.h2spe)

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
    def Q1b(self):
        """Кількість теплоти підведена до КУ (Вт).
        """
        return self.Q1_gte * (1 - self.ETAelGTE)

    @lazyproperty
    def Q1_spe(self):
        """Кількість теплоти підведена до ПТУ (Вт).
        """
        return self.Q1b * self.ETAb

    @lazyproperty
    def ETAelSPE(self):
        """Електрична потужність ПТУ.
        """
        return self.NelSPE / float(self.Q1_spe)

    @lazyproperty
    def ETAelCC(self):
        """Електрична потужність ПГУ.
        """
        return self.NelCC / float(self.Q1_cc)


if __name__ == '__main__':
    real_calc = CombinedCalcR(**INIT_DATA)
    print real_calc.ETAelSPE
    print real_calc.ETAelCC
