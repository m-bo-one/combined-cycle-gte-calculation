# -*- coding: utf-8 -*-
from constants import *
from init_data import INIT_DATA


class GTECalc(object):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.p4 = self.p1
        self.p3 = self.p2

    @property
    def p2(self):
        """Тиск після компресора (МПа).
        """
        return self.PIk * self.p1

    @property
    def T2(self):
        """Температура після компресора (К).
        """
        return self.T1 * (self.PIk ** ((k - 1) / float(k)))

    @property
    def T3(self):
        """Температура після ГТ (К).
        """
        return self.T4 * (self.PIk ** ((k - 1) / float(k)))

    @property
    def h1(self):
        """Ентальпія до компресора (кДж/кгг).
        """
        return cp * self.T1

    @property
    def h2(self):
        """Ентальпія після компресора (кДж/кгг).
        """
        return cp * self.T2

    @property
    def h3(self):
        """Ентальпія після камери згоряння (кДж/кгг).
        """
        return cp * self.T3

    @property
    def h4(self):
        """Ентальпія після ГТ (кДж/кгг).
        """
        return cp * self.T4

    @property
    def v1(self):
        """Питомий об'ем перед компресором (м^2/кгг).
        """
        return R * self.T1 / float(self.p1 * 10**6)

    @property
    def v2(self):
        """Питомий об'ем після компресора (м^2/кгг).
        """
        return R * self.T2 / float(self.p2 * 10**6)

    @property
    def v3(self):
        """Питомий об'ем після камери згоряння (м^2/кгг).
        """
        return R * self.T3 / float(self.p3 * 10**6)

    @property
    def v4(self):
        """Питомий об'ем після ГТ (м^2/кгг).
        """
        return R * self.T4 / float(self.p4 * 10**6)

    @property
    def lgt(self):
        """Работа ГТ (кДж/кгг).
        """
        return self.h3 - self.h4

    @property
    def lgc(self):
        """Работа компресора (кДж/кгг).
        """
        return self.h2 - self.h1

    @property
    def lgte(self):
        """Работа ГТУ (кДж/кгг).
        """
        return self.lgt - self.lgc

    @property
    def qinGTE(self):
        """Кількість підведеної теплоти до камери згоряння (кДж/кгг).
        """
        return self.h3 - self.h2

    @property
    def qoutGTE(self):
        """Кількість відведеної теплоти (кДж/кгг).
        """
        return self.h4 - self.h1

    @property
    def l0GTE(self):
        """Питома теоретична робота 1 кг газу (кДж/кгг).
        """
        return self.qinGTE - self.qoutGTE

    @property
    def ETAtGTE(self):
        """Термічний ККД ГТУ.
        """
        return (self.lgt - self.lgc) / float(self.qinGTE)

    def save_points_calc(self, gte_result):
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

    def save_work_params_of_GTE(self, gte_result):
        gte_result.write(format_work_params.format(
            "Thermal efficiency (percents)", (self.ETAtGTE * 100)))

    def save_results(self, writer):
        writer.write('{0:50}{1}\n'.format('', 'GTE'))
        writer.write(new_line_f)
        self.save_points_calc(writer)
        writer.write(new_line_f)
        self.save_work_params_of_GTE(writer)
        writer.write(new_line_f)


if __name__ == '__main__':
    gte_calc = GTECalc(**INIT_DATA)
    with open(RESULTS_ROOT + 'gte_result.txt', 'w') as writer:
        gte_calc.save_results(writer)
