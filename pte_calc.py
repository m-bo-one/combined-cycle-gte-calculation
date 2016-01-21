# -*- coding: utf-8 -*-
from constants import *
from init_data import pte_INIT

# third party
from thermopy.iapws import Water


class PTECalc(object):

    w = Water()

    def __init__(self, **kwargs):
        self.NtPTE = kwargs['NtPTE']
        self.NelPTE = self.NtPTE * 0.8
        self.T6 = kwargs['T6']
        self.p6 = kwargs['p6']
        # self.h6 = kwargs['h6']
        self.T7 = kwargs['T7']
        self.p7 = self.w.psat(self.T7) / float(10**6)
        self.h7 = kwargs['h7']
        self.T8 = kwargs['T8']
        self.p8 = kwargs['p8']
        self.h8 = kwargs['h8']
        self.T9 = self.T8
        self.p9 = self.p8
        self.h9 = self.h8

    def calc_params_at_point(self, number):
        if number == 6:
            self.h6 = w.h(self.p6 * 10**6, self.T6)
        elif number == 7:
            self.p7 = self.w.psat(self.T7) / float(10**6)


    def calc_work_of_adiabatic_steam_expansion(self):
        self.lt = self.h6 - self.h7

    def calc_work_of_adiabatic_compression_of_water_in_pump(self):
        self.ln = vWater * (self.p6 - self.p7)

    def calc_heat_in_boiler(self):
        self.qb = self.h6 - self.h8

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
        new_line_f = '{0}{1}'.format('\n', '-' * 125)
        with open(file_name, mode) as pte_result:
            pte_result.write('{0:50}{1}'.format('', 'PTE'))
            pte_result.write(new_line_f)
            self._save_work_params(pte_result)


if __name__ == '__main__':
    pte_calc = PTECalc(**pte_INIT)
    pte_calc.main()
    pte_calc.save_results()
