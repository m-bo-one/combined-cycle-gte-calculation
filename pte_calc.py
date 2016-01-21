# -*- coding: utf-8 -*-
from constants import *
from init_data import pte_INIT

# third party
from pyXSteam.XSteam import XSteam
steamTable = XSteam(XSteam.UNIT_SYSTEM_MKS)


class PTECalc(object):

    def __init__(self, **kwargs):
        self.m_flow = kwargs['m']
        self.T1 = kwargs['T1']
        self.T6 = kwargs['T6']
        self.p6 = kwargs['p6']
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
        self.T7 = self.T1 + Tcr
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

    def calc_power_of_stem_turbine_and_gen(self):
        self.NtPTE = (self.m_flow * self.lt) / float(10**3)
        self.NelPTE = self.NtPTE * 0.8

    def calc_work_of_adiabatic_steam_expansion(self):
        self.lt = self.h6 - self.h7

    def calc_work_of_adiabatic_compression_of_water_in_pump(self):
        self.ln = self.h9 - self.h8

    def calc_heat_in_boiler(self):
        self.qb = self.h6 - self.h9

    def calc_thermal_efficiency(self):
        self.ETAtPTE = (self.lt - self.ln) / float(self.qb)

    def calc_electrical_efficiency(self):
        self.ETAelPTE = self.ETAtPTE * ETAoi * ETAem

    def calc_specific_steam_consumption(self):
        self.d0PTE = 3600 / float(self.lt - self.ln)

    def calc_specific_steam_consumption_real(self):
        self.dPTE = self.d0PTE / float(ETAoi * ETAem)

    def calc_steam_consumption_of_power_plant(self):
        self.DPTE = self.NtPTE * 10**3 * self.dPTE

    def calc_effective_efficiency(self):
        self.ETAePTE = ETAk * ETApp * ETAi * ETAm * ETAg

    def calc_specific_cond_fuel_consumption(self):
        self.bc = 0.123 / float(self.ETAePTE)

    def calc_cond_fuel_consumption(self):
        self.Bc = self.bc * self.NelPTE * 10**3

    def main(self):
        self.calc_work_of_adiabatic_steam_expansion()
        self.calc_work_of_adiabatic_compression_of_water_in_pump()
        self.calc_heat_in_boiler()
        self.calc_power_of_stem_turbine_and_gen()
        self.calc_thermal_efficiency()
        self.calc_electrical_efficiency()
        self.calc_specific_steam_consumption()
        self.calc_specific_steam_consumption_real()
        self.calc_steam_consumption_of_power_plant()
        self.calc_effective_efficiency()
        self.calc_specific_cond_fuel_consumption()
        self.calc_cond_fuel_consumption()

    def _save_work_params(self, pte_result):
        format_work_params = "{0}: {1} \n"
        pte_result.write(format_work_params.format(
            "Turbine work (kJ/kgws)", self.lt))
        pte_result.write(format_work_params.format(
            "Pump work (kJ/kgws)", self.ln))
        pte_result.write(format_work_params.format(
            "Boiler heat (kJ/kgws)", self.qb))
        pte_result.write(format_work_params.format(
            "Thermal efficiency (percents)", (self.ETAtPTE * 100)))
        pte_result.write(format_work_params.format(
            "Electrical efficiency (percents)", (self.ETAelPTE * 100)))
        pte_result.write(format_work_params.format(
            "Electric power (MW)", self.NelPTE))
        pte_result.write(format_work_params.format(
            "Real specific steam consumption (kg/kW*h)", self.dPTE))
        pte_result.write(format_work_params.format(
            "Steam consumption of power plant (kg/h)", self.DPTE))
        pte_result.write(format_work_params.format(
            "Specific fuel conditional consumption (kg/kW*h)", self.bc))
        pte_result.write(format_work_params.format(
            "Fuel conditional consumption (kg/h)", self.Bc))

    def save_results(self, file_name='pte_result.txt', mode='w'):
        new_line_f = '{0}{1}'.format('-' * 79, '\n')
        with open(file_name, mode) as pte_result:
            pte_result.write('{0:30}{1} \n'.format('', 'Steam power plant'))
            pte_result.write(new_line_f)
            self._save_work_params(pte_result)


if __name__ == '__main__':
    pte_calc = PTECalc(**pte_INIT)
    pte_calc.main()
    pte_calc.save_results()
