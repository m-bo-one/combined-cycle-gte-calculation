# -*- coding: utf-8 -*-
from constants import *
from gte_calc import GTECalc
from init_data import INIT_DATA, steamTable


class CombinedCalc(GTECalc):

    def __init__(self, **kwargs):
        GTECalc.__init__(self, **kwargs)
        self._set_params_at_points()
        self.h5 = cp * self.T5

    def _set_params_at_points(self):
        # -------------------------------------------------------------------
        # POINT ==> 6
        # Ентальпія як функції тиску і температури.
        self.h6 = steamTable.h_pt(self.p6, self.T6 - KELVIN_CONST)
        # Питома ентропія як функція тиску і температури
        # (Повертає насичений пар ентальпії якщо це суміш.)
        self.s6 = steamTable.s_pt(self.p6, self.T6 - KELVIN_CONST)
        # -------------------------------------------------------------------
        # POINT ==> 7
        self.T7 = self.T1 + self.Tcr
        # Насичений тиск
        self.p7 = steamTable.psat_t(self.T7 - KELVIN_CONST)
        self.s7 = self.s6
        # Пари фракції як функції тиску і ентропії
        self.x7 = steamTable.x_ps(self.p7, self.s7)
        # Ентальпія в залежності від температури і парової фракції
        self.h7 = steamTable.h_tx(self.T7 - KELVIN_CONST, self.x7)
        # -------------------------------------------------------------------
        # POINT ==> 8
        self.T8 = self.T7
        # Ентальпія насиченої рідини.
        self.h8 = steamTable.hL_t(self.T8 - KELVIN_CONST)
        # Ентропія насиченої рідини.
        self.s8 = steamTable.sL_t(self.T8 - KELVIN_CONST)
        # -------------------------------------------------------------------
        # POINT ==> 9
        self.p9 = self.p6
        self.s9 = self.s8
        # Ентальпія як функції тиску і ентропії.
        self.h9 = steamTable.h_ps(self.p9, self.s9)
        # -------------------------------------------------------------------
        self._show_errors()

    def _show_errors(self):
        errors = []
        for key, value in self.__dict__.iteritems():
            if str(value) == 'nan':
                errors.append('Param {0} has {1} value'.format(key, value))
        if errors:
            print errors

    @property
    def lst(self):
        """Работа парової турбіни (кДж/кгг).
        """
        return self.h6 - self.h7

    @property
    def lsp(self):
        """Работа насоса (кДж/кгг).
        """
        return self.h9 - self.h8

    @property
    def lspe(self):
        """Работа ПТУ (кДж/кгг).
        """
        return self.lst - self.lsp

    @property
    def qboiler(self):
        """Теплота КУ (кДж/кгг).
        """
        return self.h6 - self.h9

    @property
    def ETAtSPE(self):
        """Термічний ККД ПТУ.
        """
        return (self.lst - self.lsp) / float(self.qboiler)

    @property
    def m_boiler(self):
        """Відношення витрати газу до витрат води і водяної пари (кгг/кгвп)
        """
        return (self.h6 - self.h9) / float(self.h4 - self.h5)

    @property
    def qCC(self):
        """Підвод теплоти в ПГУ (кДж/кгг).
        """
        return self.m_boiler * self.qinGTE

    @property
    def ETAtCC(self):
        """Термічний ККД ПГУ.
        """
        return (self.m_boiler * self.lgte + self.lspe) / float(self.qCC)

    def _table_format_4(self, label, value1, value2, value3):
        writer.write(
            '{0:18}|{1:19}|{2:19}|{3:19}|\n'
            .format(label, value1, value2, value3))
        writer.write('{0}\n'.format('-' * 79))

    def save_results(self, file_name, writer):
        writer.write('{0:35}{1}\n'.format('', 'Combined cycle'))
        writer.write('{0}\n'.format('-' * 79))
        self._table_format_4(
            'Param name',
            'GTE', 'SPE', 'Combined')
        self._table_format_4(
            'Thermal efficiency',
            self.ETAtGTE, self.ETAtSPE, self.ETAtCC)


if __name__ == '__main__':
    combined_calc = CombinedCalc(**INIT_DATA)
    file_name = RESULTS_ROOT + 'combined_result.txt'
    print combined_calc.m_boiler, combined_calc.ETAtCC
    with open(file_name, 'w') as writer:
        combined_calc.save_results(file_name, writer)
