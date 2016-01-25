# -*- coding: utf-8 -*-
from constants import *
from init_data import INIT_DATA, steamTable


class SPECalc(object):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self._set_params_at_points()

    def _set_params_at_points(self):
        # -------------------------------------------------------------------
        # POINT ==> 6
        # Entalpy as a function of pressure and temperature.
        self.h6 = steamTable.h_pt(self.p6, self.T6 - KELVIN_CONST)
        # Specific entropy as a function of pressure and temperature
        # (Returns saturated vapour entalpy if mixture.)
        self.s6 = steamTable.s_pt(self.p6, self.T6 - KELVIN_CONST)
        # -------------------------------------------------------------------
        # POINT ==> 7
        self.T7 = self.T1 + self.Tcr
        # Saturation pressure
        self.p7 = steamTable.psat_t(self.T7 - KELVIN_CONST)
        self.s7 = self.s6
        # Vapour fraction as a function of pressure and entropy
        self.x7 = steamTable.x_ps(self.p7, self.s7)
        # Entalpy as a function of temperature and vapour fraction
        self.h7 = steamTable.h_tx(self.T7 - KELVIN_CONST, self.x7)
        # -------------------------------------------------------------------
        # POINT ==> 8
        self.T8 = self.T7
        # Saturated liquid enthalpy
        self.h8 = steamTable.hL_t(self.T8 - KELVIN_CONST)
        self.s8 = steamTable.sL_t(self.T8 - KELVIN_CONST)
        # -------------------------------------------------------------------
        # POINT ==> 9
        self.p9 = self.p6
        self.s9 = self.s8
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
        """Work of steam turbine. (kJ/kgg)
        """
        return self.h6 - self.h7

    @property
    def lsp(self):
        """Work of steam pump. (kJ/kgg)
        """
        return self.h9 - self.h8

    @property
    def qboiler(self):
        """Heat of steam boiler. (kJ/kgg)
        """
        return self.h6 - self.h9

    @property
    def ETAtSPE(self):
        """Thermal efficiency of SPE (dimensionless).
        """
        return (self.lst - self.lsp) / float(self.qboiler)

    @property
    def ETAelSPE(self):
        """Absolute electrical efficiency of SPE (dimensionless).
        """
        return self.ETAtSPE * ETAoi * ETAem

    def save_work_param_of_SPE(self, writer, text, param):
        writer.write(format_work_params.format(text.encode('utf-8'), param))

    def save_results(self, writer):
        writer.write(
            '{0:50}{1}\n'.format(
                u'', u'Паротурбінна установка'.encode('utf-8')))
        writer.write(new_line_f)
        self.save_work_param_of_SPE(
            writer, u"Робота турбінни (кДж/кг водяної пари)", self.lst)
        self.save_work_param_of_SPE(
            writer, u"Робота насоса(кДж/кг водяної пари)", self.lsp)
        self.save_work_param_of_SPE(
            writer, u"Температура КУ (кДж/кг водяної пари)", self.qboiler)
        self.save_work_param_of_SPE(
            writer, u"Термічний ККД (відсотки)", (self.ETAtSPE * 100))
        self.save_work_param_of_SPE(
            writer, u"Електричний ККД (відсотки)", (self.ETAelSPE * 100))


if __name__ == '__main__':
    spe_calc = SPECalc(**INIT_DATA)
    with open(RESULTS_ROOT + 'spe_result.txt', 'w') as writer:
        spe_calc.save_results(writer)
