# -*- coding: utf-8 -*-
from constants import *
from combined import CombinedCalc
from init_data import INIT_DATA

# third party
import matplotlib.pyplot as plt
from matplotlib import rc
from numpy import linspace


class TotalResult(CombinedCalc):

    @staticmethod
    def plot_graph_dependency(plot_config):
        font = {'family': 'Droid Sans',
                'weight': 'normal'}
        rc('font', **font)
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
                        combined_calc,
                        plot_config['y']['data']['names'][key]))
        plt.plot(
            list_of_setted_param_x,
            list_of_recalculated_param_y[0],
            plot_config['GTE']['grid'],
            label=plot_config['GTE']['trs']
        )
        plt.plot(
            list_of_setted_param_x,
            list_of_recalculated_param_y[1],
            plot_config['SPE']['grid'],
            label=plot_config['SPE']['trs']
        )
        plt.plot(
            list_of_setted_param_x,
            list_of_recalculated_param_y[2],
            plot_config['CC']['grid'],
            label=plot_config['CC']['trs']
        )
        plt.xlabel(plot_config['x']['label'])
        plt.ylabel(plot_config['y']['label'])
        plt.title(plot_config['title'])
        plt.grid(True)
        plt.legend()
        plt.savefig(plot_config['file_name'], dpi=400)
        plt.clf()

    def plot_ETAt_PIk(self):
        plot_config = PLOT_CONFIG.copy()
        plot_config['y']['label'] = u"Термічний ККД"
        plot_config['x']['label'] = u"Ступінь стиснення"
        plot_config['x']['data']['from'] = 10
        plot_config['x']['data']['to'] = 20
        plot_config['x']['data']['count'] = 100
        plot_config['x']['data']['name'] = u"Пк"
        plot_config['y']['data']['names'] = [
            "ETAtGTE", "ETAtSPE", "ETAtCombined"]
        plot_config['file_name'] = MEDIA_ROOT + "ETAt-PIk.png"
        plot_config['title'] = u"Залежність між термічним ККД " + \
            u"та ступенем стиснення"
        self.plot_graph_dependency(plot_config)

    def plot_ETAt_T1(self):
        plot_config = PLOT_CONFIG.copy()
        plot_config['y']['label'] = u"Термічний ККД"
        plot_config['x']['label'] = u"Температура перед компресором, (К)"
        plot_config['x']['data']['from'] = 0 + KELVIN_CONST
        plot_config['x']['data']['to'] = 50 + KELVIN_CONST
        plot_config['x']['data']['count'] = 100
        plot_config['x']['data']['name'] = u"T1"
        plot_config['y']['data']['names'] = [
            "ETAtGTE", "ETAtSPE", "ETAtCombined"]
        plot_config['file_name'] = MEDIA_ROOT + "ETAt-T1.png"
        plot_config['title'] = u"Залежність між термічним ККД " + \
            u"та температурою перед компресором"
        self.plot_graph_dependency(plot_config)

    def plot_ETAt_T4(self):
        plot_config = PLOT_CONFIG.copy()
        plot_config['y']['label'] = u"Термічний ККД"
        plot_config['x']['label'] = u"Температура після турбіни, (К)"
        plot_config['x']['data']['from'] = 200 + KELVIN_CONST
        plot_config['x']['data']['to'] = 400 + KELVIN_CONST
        plot_config['x']['data']['count'] = 100
        plot_config['x']['data']['name'] = u"T4"
        plot_config['y']['data']['names'] = [
            "ETAtGTE", "ETAtSPE", "ETAtCombined"]
        plot_config['file_name'] = MEDIA_ROOT + "ETAt-T4.png"
        plot_config['title'] = u"Залежність між термічним ККД " + \
            u"та температурою після турбіни"
        self.plot_graph_dependency(plot_config)

    def plot_ETAt_p6(self):
        plot_config = PLOT_CONFIG.copy()
        plot_config['y']['label'] = u"Термічний ККД"
        plot_config['x']['label'] = u"Тиск на вході в парову турбіну, (МПа)"
        plot_config['x']['data']['from'] = 0.1
        plot_config['x']['data']['to'] = 20
        plot_config['x']['data']['count'] = 100
        plot_config['x']['data']['name'] = u"p6"
        plot_config['y']['data']['names'] = [
            "ETAtGTE", "ETAtSPE", "ETAtCombined"]
        plot_config['file_name'] = MEDIA_ROOT + "ETAt-p6.png"
        plot_config['title'] = u"Залежність між термічним ККД " + \
            u"та тиском на вході в парову турбіну"
        self.plot_graph_dependency(plot_config)

    def plot_ETAt_T6(self):
        plot_config = PLOT_CONFIG.copy()
        plot_config['y']['label'] = u"Термічний ККД"
        plot_config['x']['label'] = u"Температура на вході в парову турбіни, (К)"
        plot_config['x']['data']['from'] = 300 + KELVIN_CONST
        plot_config['x']['data']['to'] = 400 + KELVIN_CONST
        plot_config['x']['data']['count'] = 100
        plot_config['x']['data']['name'] = u"T6"
        plot_config['y']['data']['names'] = [
            "ETAtGTE", "ETAtSPE", "ETAtCombined"]
        plot_config['file_name'] = MEDIA_ROOT + "ETAt-T6.png"
        plot_config['title'] = u"Залежність між термічним ККД " + \
            u"та температурою на вході в парову турбіну"
        self.plot_graph_dependency(plot_config)

    def plot_ETAt_Tcr(self):
        plot_config = PLOT_CONFIG.copy()
        plot_config['y']['label'] = u"Термічний ККД"
        plot_config['x']['label'] = u"Різниця температури в конденсаторі, (К)"
        plot_config['x']['data']['from'] = 0 + KELVIN_CONST
        plot_config['x']['data']['to'] = 20 + KELVIN_CONST
        plot_config['x']['data']['count'] = 100
        plot_config['x']['data']['name'] = u"Tcr"
        plot_config['y']['data']['names'] = [
            "ETAtGTE", "ETAtSPE", "ETAtCombined"]
        plot_config['file_name'] = MEDIA_ROOT + "ETAt-Tcr.png"
        plot_config['title'] = u"Залежність між термічним ККД " + \
            u"та різницею температур в конденсаторі"
        self.plot_graph_dependency(plot_config)

    def plot_ETAt_T5(self):
        plot_config = PLOT_CONFIG.copy()
        plot_config['y']['label'] = u"Термічний ККД"
        plot_config['x']['label'] = u"Температура за котлом-утилізатором, (К)"
        plot_config['x']['data']['from'] = 100 + KELVIN_CONST
        plot_config['x']['data']['to'] = 200 + KELVIN_CONST
        plot_config['x']['data']['count'] = 100
        plot_config['x']['data']['name'] = u"T5"
        plot_config['y']['data']['names'] = [
            "ETAtGTE", "ETAtSPE", "ETAtCombined"]
        plot_config['file_name'] = MEDIA_ROOT + "ETAt-T5.png"
        plot_config['title'] = u"Залежність між термічним ККД " + \
            u"та температурою за котлом-утилізатором"
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
