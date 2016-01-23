# -*- coding: utf-8 -*-
from constants import *
from combined import CombinedCalc
from init_data import INIT_DATA

# third party
import matplotlib.pyplot as plt
from numpy import *


class TotalResult(CombinedCalc):

    @staticmethod
    def plot_graph_dependency(plot_config):
        list_of_setted_param_x = linspace(
            plot_config['x']['data']['from'],
            plot_config['x']['data']['to'],
            plot_config['x']['data']['count'])
        list_of_recalculated_param_y = {
            0: [],
            1: [],
            2: []
        }
        for setted_param in list_of_setted_param_x:
            change_key = plot_config['x']['data']['name']
            INIT_DATA[change_key] = setted_param
            combined_calc = CombinedCalc(**INIT_DATA)
            for key in list_of_recalculated_param_y.keys():
                list_of_recalculated_param_y[key] \
                    .append(getattr(
                        combined_calc, plot_config['y']['data']['names'][key]))
        plt.plot(
            list_of_setted_param_x,
            list_of_recalculated_param_y[0],
            plot_config['GTE']['grid'],
            label=plot_config['GTE']['name']
        )
        plt.plot(
            list_of_setted_param_x,
            list_of_recalculated_param_y[1],
            plot_config['SPE']['grid'],
            label=plot_config['SPE']['name']
        )
        plt.plot(
            list_of_setted_param_x,
            list_of_recalculated_param_y[2],
            plot_config['CC']['grid'],
            label=plot_config['CC']['name']
        )
        plt.xlabel(plot_config['x']['label'])
        plt.ylabel(plot_config['y']['label'])
        plt.title(
            'Dependence between {0} and {1}'.format(
                plot_config['y']['label'].lower(),
                plot_config['x']['label'].lower()))
        plt.grid(True)
        plt.legend()
        plt.savefig(plot_config['file_name'], dpi=400)
        plt.clf()

    def plot_ETAt_PIk(self):
        plot_config = PLOT_CONFIG.copy()
        plot_config['y']['label'] = "Thermal efficiency"
        plot_config['x']['label'] = "Compressor pressure ratio"
        plot_config['x']['data']['from'] = 10
        plot_config['x']['data']['to'] = 20
        plot_config['x']['data']['count'] = 10
        plot_config['x']['data']['name'] = "PIk"
        plot_config['y']['data']['names'] = [
            "ETAtGTE", "ETAtSPE", "ETAtCombined"]
        plot_config['file_name'] = MEDIA_ROOT + "ETAt-PIk.png"
        self.plot_graph_dependency(plot_config)

    def plot_ETAt_T1(self):
        plot_config = PLOT_CONFIG.copy()
        plot_config['y']['label'] = "Thermal efficiency"
        plot_config['x']['label'] = "Temperature before compressor (K)"
        plot_config['x']['data']['from'] = 0 + KELVIN_CONST
        plot_config['x']['data']['to'] = 50 + KELVIN_CONST
        plot_config['x']['data']['count'] = 10
        plot_config['x']['data']['name'] = "T1"
        plot_config['y']['data']['names'] = [
            "ETAtGTE", "ETAtSPE", "ETAtCombined"]
        plot_config['file_name'] = MEDIA_ROOT + "ETAt-T1.png"
        self.plot_graph_dependency(plot_config)

    def plot_ETAt_T4(self):
        plot_config = PLOT_CONFIG.copy()
        plot_config['y']['label'] = "Thermal efficiency"
        plot_config['x']['label'] = "Temperature after gas turbine (K)"
        plot_config['x']['data']['from'] = 200 + KELVIN_CONST
        plot_config['x']['data']['to'] = 400 + KELVIN_CONST
        plot_config['x']['data']['count'] = 10
        plot_config['x']['data']['name'] = "T4"
        plot_config['y']['data']['names'] = [
            "ETAtGTE", "ETAtSPE", "ETAtCombined"]
        plot_config['file_name'] = MEDIA_ROOT + "ETAt-T4.png"
        self.plot_graph_dependency(plot_config)

    def plot_ETAt_p6(self):
        plot_config = PLOT_CONFIG.copy()
        plot_config['y']['label'] = "Thermal efficiency"
        plot_config['x']['label'] = "Pressure before steam turbine (MPa)"
        plot_config['x']['data']['from'] = 0.1
        plot_config['x']['data']['to'] = 20
        plot_config['x']['data']['count'] = 10
        plot_config['x']['data']['name'] = "p6"
        plot_config['y']['data']['names'] = [
            "ETAtGTE", "ETAtSPE", "ETAtCombined"]
        plot_config['file_name'] = MEDIA_ROOT + "ETAt-p6.png"
        self.plot_graph_dependency(plot_config)

    def plot_ETAt_T6(self):
        plot_config = PLOT_CONFIG.copy()
        plot_config['y']['label'] = "Thermal efficiency"
        plot_config['x']['label'] = "Temperature before steam turbine (K)"
        plot_config['x']['data']['from'] = 300 + KELVIN_CONST
        plot_config['x']['data']['to'] = 400 + KELVIN_CONST
        plot_config['x']['data']['count'] = 10
        plot_config['x']['data']['name'] = "T6"
        plot_config['y']['data']['names'] = [
            "ETAtGTE", "ETAtSPE", "ETAtCombined"]
        plot_config['file_name'] = MEDIA_ROOT + "ETAt-T6.png"
        self.plot_graph_dependency(plot_config)

    def plot_ETAt_Tcr(self):
        plot_config = PLOT_CONFIG.copy()
        plot_config['y']['label'] = "Thermal efficiency"
        plot_config['x']['label'] = "Temperature diff in condencator (K)"
        plot_config['x']['data']['from'] = 0 + KELVIN_CONST
        plot_config['x']['data']['to'] = 30 + KELVIN_CONST
        plot_config['x']['data']['count'] = 10
        plot_config['x']['data']['name'] = "Tcr"
        plot_config['y']['data']['names'] = [
            "ETAtGTE", "ETAtSPE", "ETAtCombined"]
        plot_config['file_name'] = MEDIA_ROOT + "ETAt-Tcr.png"
        self.plot_graph_dependency(plot_config)

    def plot_ETAt_T5(self):
        plot_config = PLOT_CONFIG.copy()
        plot_config['y']['label'] = "Thermal efficiency"
        plot_config['x']['label'] = "Temperature after boiler (K)"
        plot_config['x']['data']['from'] = 100 + KELVIN_CONST
        plot_config['x']['data']['to'] = 200 + KELVIN_CONST
        plot_config['x']['data']['count'] = 10
        plot_config['x']['data']['name'] = "T5"
        plot_config['y']['data']['names'] = [
            "ETAtGTE", "ETAtSPE", "ETAtCombined"]
        plot_config['file_name'] = MEDIA_ROOT + "ETAt-T5.png"
        self.plot_graph_dependency(plot_config)

    def plot_graphs(self):
        self.plot_ETAt_PIk()
        self.plot_ETAt_T1()
        self.plot_ETAt_T4()
        self.plot_ETAt_p6()
        self.plot_ETAt_T6()
        self.plot_ETAt_Tcr()
        self.plot_ETAt_T5()

if __name__ == '__main__':
    total = TotalResult(**INIT_DATA)
    total.plot_graphs()
