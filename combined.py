# -*- coding: utf-8 -*-
from constants import *
from gte_calc import GTECalc
from spe_calc import SPECalc
from init_data import INIT_DATA, steamTable

# third party
import matplotlib.pyplot as plt
from numpy import *


class CombinedCalc(GTECalc, SPECalc):

    def __init__(self, **kwargs):
        GTECalc.__init__(self, **kwargs)
        SPECalc.__init__(self, **kwargs)
        self.h5 = cp * self.T5

    @property
    def m_boiler(self):
        """Relationship between heat in boiler and heat from
        gas turbine and exhausted gases from boiler (kgg/kgws)
        """
        return (self.h6 - self.h9) / float(self.h4 - self.h5)

    @property
    def qCombined(self):
        """Production of heat in combined cycle. (kJ/kgws)
        """
        return self.m_boiler * self.qinGTE

    @property
    def lst(self):
        """Work of steam turbine. (kJ/kgws)
        """
        return self.h6 - self.h7

    @property
    def lsp(self):
        """Work of steam pump. (kJ/kgws)
        """
        return self.h9 - self.h8

    @property
    def lspe(self):
        """Work of steam power engine. (kJ/kgws)
        """
        return self.lgt - self.lgc

    @property
    def ETAtCombined(self):
        """Thermal efficiency of combined cycle. (dimensionless)
        """
        return (self.m_boiler * self.lgte + self.lspe) / float(self.qCombined)

    @property
    def ETAelCombined(self):
        """Absolute electrical efficiency of SPE (dimensionless).
        """
        return self.ETAtCombined * ETAoi * ETAem

    @staticmethod
    def plot_graph_dependency(plot_config):
        list_of_setted_param_x = linspace(
            plot_config['x']['data']['from'],
            plot_config['x']['data']['to'],
            plot_config['x']['data']['count'])
        list_of_recalculated_param_y = {
            "GTE": [],
            "SPE": [],
            "CC": []
        }
        for setted_param in list_of_setted_param_x:
            change_key = plot_config['x']['data']['name']
            INIT_DATA[change_key] = setted_param
            combined_calc = CombinedCalc(**INIT_DATA)
            list_of_recalculated_param_y['GTE'] \
                .append(combined_calc.ETAtGTE)
            list_of_recalculated_param_y['SPE'] \
                .append(combined_calc.ETAtSPE)
            list_of_recalculated_param_y['CC'] \
                .append(combined_calc.ETAtCombined)

        plt.plot(
            # first curve
            list_of_setted_param_x,
            list_of_recalculated_param_y['GTE'],
            plot_config['GTE']['grid'],
            # second curve
            list_of_setted_param_x,
            list_of_recalculated_param_y['SPE'],
            plot_config['SPE']['grid'],
            # third curve
            list_of_setted_param_x,
            list_of_recalculated_param_y['CC'],
            plot_config['CC']['grid'],
        )
        plt.xlabel(plot_config['x']['label'])
        plt.ylabel(plot_config['y']['label'])
        plt.grid(True)
        plt.savefig(plot_config['file_name'], dpi=200)

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
            self.ETAtGTE, self.ETAtSPE, self.ETAtCombined)
        self._table_format_4(
            'Electr. efficiency',
            self.ETAelGTE, self.ETAelSPE, self.ETAelCombined)

    def plot_ETAt_PIk(self):
        plot_config = PLOT_CONFIG.copy()
        plot_config['y']['label'] = "Thermal efficiency"
        plot_config['x']['label'] = "Compressor pressure ratio"
        plot_config['x']['data']['from'] = 10
        plot_config['x']['data']['to'] = 20
        plot_config['x']['data']['count'] = 10
        plot_config['x']['data']['name'] = "PIk"
        plot_config['file_name'] = "ETAt-PIk.png"
        self.plot_graph_dependency(plot_config)

    def plot_graphs(self):
        self.plot_ETAt_PIk()

if __name__ == '__main__':
    combined_calc = CombinedCalc(**INIT_DATA)
    file_name = 'combined_result.txt'
    with open(file_name, 'w') as writer:
        combined_calc.save_results(file_name, writer)
    combined_calc.plot_graphs()
