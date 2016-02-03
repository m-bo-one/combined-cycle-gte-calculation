# -*- coding: utf-8 -*-
# FILE='cc_calc/selection/graph.py'
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


from init_data import INIT_DATA
from selection import SelectionCalcR
from real.helpers import lazyproperty
from real.wspru_api import WspRuAPI


# third party
import matplotlib.pyplot as plt
from numpy import *
from matplotlib import rc


_graph_class = SelectionCalcR
engines_keys = {
    0: "GTE",
    1: "CC"
}


class SelectionAnalysisResult(object):

    def __init__(self, **kwargs):
        self.recal_engines = self.recalculated_data_of_engines(kwargs)
        self.__ccc = len(engines_keys.keys())
        self.engine_count = len(kwargs.keys())
        self.index = arange(self.engine_count)
        self.bar_width = 0.35

    @staticmethod
    def autolabel(ax, rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width() / 2., 1.05 * height,
                    '%s' % round(height, 4),
                    ha='center', va='bottom')

    @staticmethod
    def recalculated_data_of_engines(GTES):
        recal_engines = {
            "ETAels": {
                0: [],
                1: []
            },
            "Nels": {
                0: [],
                1: []
            },
            "Q1s": [],
            "T4s": [],
            "PIks": [],
            "names": [],
        }
        for key in GTES.keys():
            recal_engines['names'].append(key)
            recal_engines['T4s'].append(GTES[key]['T4gte'])
            recal_engines['PIks'].append(GTES[key]['PIk'])
            combined_calc = _graph_class(**GTES[key])
            recal_engines['Q1s'].append(
                round(combined_calc.Q1_gte / 10**6, 3))
            for x in (0, 1):
                recal_engines["ETAels"][x].append(
                    round(
                        getattr(
                            combined_calc, 'ETAel' + engines_keys[x])
                        * 100, 3)
                )
                recal_engines["Nels"][x].append(
                    round(
                        getattr(
                            combined_calc, 'Nel' + engines_keys[x]) / 10**6, 3)
                )
        return recal_engines

    def plot_gist(self, params, label, file_name, compare=True):
        font = {'family': 'Droid Sans',
                'weight': 'normal'}
        rc('font', **font)
        fig, ax = plt.subplots()
        _col = ('g', 'b')
        _ar_range = (0, 1)
        _bar_width = self.bar_width
        _add_m = 0
        if not compare:
            _ar_range = (0, )
            _bar_width = self.bar_width * 2
            _add_m = 0.35
        _bar_widthes = (0, _bar_width)
        _rects = []
        for x in _ar_range:
            _get_param_x = self.recal_engines[params][x]
            if not compare:
                _get_param_x = self.recal_engines[params]
            rects = plt.bar(
                self.index + _bar_widthes[x],
                _get_param_x,
                _bar_width,
                color=_col[x])
            _rects.append(rects)
            plt.xticks(
                _add_m + self.index + _ar_range[x] * _bar_width,
                self.recal_engines['names'])
            self.autolabel(ax, rects)
        if compare:
            ax.legend(
                (_rects[0][0], _rects[1][0]), (u'ГТУ', u'ПГУ'), loc=4)
        else:
            ax.legend(
                (_rects[0][0], ), (u'ГТУ', ), loc=4)
        ax.set_ylabel(label)
        plt.savefig('pictures/' + file_name, dpi=400)
        plt.clf()

    def main(self):
        self.plot_gist(
            'ETAels',
            u'Електричний ККД, (%)',
            'engines_electrical_efficiency.png')
        self.plot_gist(
            'Nels',
            u'Електрична потужність, (МВт)',
            'engines_electrical_power.png')
        self.plot_gist(
            'Q1s',
            u'Підведена теплота, (МВт)',
            'engines_elevated_heat.png',
            compare=False)
        self.plot_gist(
            'T4s',
            u'Температура вихідних газів за ГТ, (К)',
            'engines_exhaust_gt.png',
            compare=False)


if __name__ == '__main__':
    real = SelectionAnalysisResult(**INIT_DATA)
    real.main()
