# -*- coding: utf-8 -*-
from constants import *
from init_data import gte_INIT


class GTECalc(object):

    def __init__(self, **kwargs):
        self.PIk = kwargs['PIk']
        self.NtGTE = kwargs['NtGTE']
        self.NelGTE = self.NtGTE * 0.8
        self.T1 = kwargs['T1']
        self.T4 = kwargs['T4']
        self.p1 = kwargs['p1']
        self.p2 = self.PIk * self.p1
        self.p4 = self.p1
        self.p3 = self.p2
        self._recalc_temp_at_other_points()

    def _recalc_temp_at_other_points(self):
        self.T3 = self.T4 * (self.PIk ** ((k - 1) / float(k)))
        self.T2 = self.T1 * (self.PIk ** ((k - 1) / float(k)))

    def calc_enthalpy(self):
        def __enthalpy_forml(T):
            return cp * T
        self.h1 = __enthalpy_forml(self.T1)
        self.h2 = __enthalpy_forml(self.T2)
        self.h3 = __enthalpy_forml(self.T3)
        self.h4 = __enthalpy_forml(self.T4)

    def calc_specific_volume_at_point(self, number):
        def _calc_of_volume(p, T):
            return R * T / float(p * 10**6)
        if number == 1:
            self.v1 = _calc_of_volume(self.p1, self.T1)
        elif number == 2:
            self.v2 = _calc_of_volume(self.p2, self.T2)
        elif number == 3:
            self.v3 = _calc_of_volume(self.p3, self.T3)
        elif number == 4:
            self.v4 = _calc_of_volume(self.p4, self.T4)

    def calc_specific_amount_of_heat(self):
        # inlet
        self.q1 = cp * (self.T3 - self.T2)
        # outlet
        self.q2 = cp * (self.T4 - self.T1)

    def calc_therethical_work(self):
        self.l0GTE = self.q1 - self.q2

    def calc_thermal_efficiency(self):
        self.ETAtGTE = self.l0GTE / float(self.q1)

    def calc_electrical_efficiency(self):
        self.ETAelGTE = self.ETAtGTE * ETAoi * ETAem

    def calc_mean_molar_isobaric_heat_capacity(self):
        temp3_100 = self.T3 / 100
        temp1_100 = self.T1 / 100
        temp_singl = temp3_100 - temp1_100
        temp_square = (temp3_100 ** 2) - (temp1_100 ** 2)
        temp_cube = (temp3_100 ** 3) - (temp1_100 ** 3)
        self.Cmupm = (
            1 / (temp3_100 - temp1_100)) * \
            (a * temp_singl + (b / 20) * temp_square + (d / 300) * temp_cube)

    def calc_mean_mass_isobaric_heat_capacity(self):
        self.Cpm = self.Cmupm / float(mu)

    def calc_specific_entropy(self):
        pass

    def main(self):
        self.calc_specific_volume_at_point(1)
        self.calc_specific_volume_at_point(2)
        self.calc_specific_volume_at_point(3)
        self.calc_specific_volume_at_point(4)
        self.calc_specific_amount_of_heat()
        self.calc_enthalpy()
        self.calc_therethical_work()
        self.calc_thermal_efficiency()
        self.calc_electrical_efficiency()
        self.calc_mean_molar_isobaric_heat_capacity()
        self.calc_mean_mass_isobaric_heat_capacity()

    def _save_points_calc(self, gte_result):
        formated_point_string = '{0:35} |{1:20} |{2:20} |{3:20} |{4:20} |\n'
        gte_result.write(formated_point_string.format(
            'Points', 1, 2, 3, 4))
        gte_result.write('-' * 125)
        gte_result.write(formated_point_string.format(
            'Specific volume (m^2/kg)',
            self.v1, self.v2, self.v3, self.v4))
        gte_result.write(formated_point_string.format(
            'Presure (MPa)',
            self.p1, self.p2, self.p3, self.p4))
        gte_result.write(formated_point_string.format(
            'Enthalpy (kJ/kgg)',
            self.h1, self.h2, self.h3, self.h4))
        gte_result.write(formated_point_string.format(
            'Temperature (oC)',
            (self.T1 - KELVIN_CONST),
            (self.T2 - KELVIN_CONST),
            (self.T3 - KELVIN_CONST),
            (self.T4 - KELVIN_CONST)))

    def _save_work_params(self, gte_result):
        format_work_params = "{0}: {1} \n"
        gte_result.write(format_work_params.format(
            "Thermal efficiency (percents)", (self.ETAtGTE * 100)))
        gte_result.write(format_work_params.format(
            "Electrical efficiency (percents)", (self.ETAelGTE * 100)))
        gte_result.write(format_work_params.format(
            "Electric power (MW)", self.NelGTE))

    def save_results(self, file_name='gte_result.txt', mode='w'):
        new_line_f = '{0}{1}'.format('-' * 125, '\n')
        with open(file_name, mode) as gte_result:
            gte_result.write('{0:50}{1}\n'.format('', 'GTE'))
            gte_result.write(new_line_f)
            self._save_points_calc(gte_result)
            gte_result.write(new_line_f)
            self._save_work_params(gte_result)
            gte_result.write(new_line_f)


if __name__ == '__main__':
    gte_calc = GTECalc(**gte_INIT)
    gte_calc.main()
    gte_calc.save_results()
