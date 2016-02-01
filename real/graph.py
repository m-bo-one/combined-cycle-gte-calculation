# -*- coding: utf-8 -*-
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


from spe_r import SPECalcR
from init_data import *

# third party
import matplotlib.pyplot as plt
from matplotlib import rc
from numpy import linspace, random

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})
font = {'family': 'Droid Sans',
        'weight': 'normal'}
rc('font', **font)


def plot_Nel_ETAel(param_to_change, title, from_p, to_p, count, f_name):
    _r_dict = {}

    params = linspace(
        from_p,
        to_p,
        count
    )
    for p in params:
        INIT_DATA[param_to_change] = p
        real_calc = SPECalcR(**INIT_DATA)
        _r_dict[p] = (
            (real_calc.NelCC / float(10**6), ),
            (real_calc.ETAelCC * 100, )
        )

        plt.plot(
            _r_dict[p][1], _r_dict[p][0],
            'o',
            color=random.rand(3, 1),
        )
        plt.text(
            _r_dict[p][1][0], _r_dict[p][0][0],
            round(p, 3),
            size=10, ha='center', va='bottom')
    plt.xlabel(u"ККДелПГУ (%)")
    plt.ylabel(u"NелПГУ (МВт)")
    plt.title(title, ha='center', va='center')
    plt.grid(True)
    plt.savefig('pictures/' + f_name, dpi=450)
    plt.clf()


def plot_graph(
    x_name, y_name, x_label, y_label, x_1, x_2, title, f_name, count
):
    x_list = linspace(x_1, x_2, count)
    y_list = {
        "GTE": [],
        "CC": []
    }
    for x in xrange(count):
        INIT_DATA[x_name] = x_list[x]
        real_calc = SPECalcR(**INIT_DATA)
        y_list["GTE"].append(getattr(real_calc, y_name + "GTE"))
        y_list["CC"].append(getattr(real_calc, y_name + "CC"))

    plt.plot(
        x_list, y_list["GTE"],
        'g-',
        label=u'ГТУ'
    )
    plt.plot(
        x_list, y_list["CC"],
        'r-',
        label=u'ПГУ'
    )
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    # plt.title(title, ha='center', va='center')
    plt.legend(loc=7)
    plt.grid(True)
    plt.savefig('pictures/' + f_name, dpi=150)
    plt.clf()


if __name__ == '__main__':
    # plot_graph(
    #     x_name='T2spe',
    #     y_name='Nel',
    #     x_label=u'Температура за паровою турбіною, (К)',
    #     y_label=u'Потужність елекрогенератора (Вт)',
    #     x_1=25 + KELVIN_CONST,
    #     x_2=100 + KELVIN_CONST,
    #     title=u'Залежність між температурою за паровою турбіною та потужністю електрогенератора',
    #     f_name='T2spe-Nel.png',
    #     count=10
    # )
    # plot_graph(
    #     x_name='T2spe',
    #     y_name='ETAel',
    #     x_label=u'Температура за паровою турбіною, (К)',
    #     y_label=u'Електричний ККД',
    #     x_1=25 + KELVIN_CONST,
    #     x_2=100 + KELVIN_CONST,
    #     title=u'Залежність між температурою за паровою турбіною та електричним ККД',
    #     f_name='T2spe-ETAel.png',
    #     count=10
    # )
    # plot_graph(
    #     x_name='Tb_out',
    #     y_name='ETAel',
    #     x_label=u'Температура на виході з КУ в циклі, (К)',
    #     y_label=u'Електричний ККД',
    #     x_1=300 + KELVIN_CONST,
    #     x_2=500 + KELVIN_CONST,
    #     title=u'Залежність між температурою на виході з КУ в циклі та електричним ККД',
    #     f_name='Tb_out-ETAel.png',
    #     count=20
    # )
    plot_graph(
        x_name='T4gte',
        y_name='ETAel',
        x_label=u'Температура за ГТ, (К)',
        y_label=u'Електричний ККД',
        x_1=400 + KELVIN_CONST,
        x_2=600 + KELVIN_CONST,
        title=u'Залежність між температурою за ГТ та електричним ККД',
        f_name='T4gte-ETAel.png',
        count=10
    )
    plot_graph(
        x_name='T4gte',
        y_name='Nel',
        x_label=u'Температура за ГТ, (К)',
        y_label=u'Електрична потужність (Вт)',
        x_1=400 + KELVIN_CONST,
        x_2=600 + KELVIN_CONST,
        title=u'Залежність між температурою за ГТ та електричною потужністю (Вт)',
        f_name='T4gte-Nel.png',
        count=10
    )
    plot_graph(
        x_name='PIk',
        y_name='ETAel',
        x_label=u'Ступінь підвищення тиску в компресорі',
        y_label=u'Електричний ККД',
        x_1=10,
        x_2=15,
        title=u'Залежність між степенем підвищення тиску та електричним ККД',
        f_name='PIk-ETAel.png',
        count=10
    )
    plot_graph(
        x_name='PIk',
        y_name='Nel',
        x_label=u'Ступінь підвищення тиску в компресорі',
        y_label=u'Електрична потужність (Вт)',
        x_1=10,
        x_2=15,
        title=u'Залежність між степенем підвищення тиску та електричною потужністю (Вт)',
        f_name='PIk-Nel.png',
        count=10
    )
    # plot_Nel_ETAel(
    #     'T3gte',
    #     u'Зміна теператури перед ГТ',
    #     1100 + KELVIN_CONST,
    #     1300 + KELVIN_CONST,
    #     10, 'T3gte-Nel-ETAel.png')
    # plot_Nel_ETAel(
    #     'Tb_out',
    #     u'Зміна температури на виході з КУ',
    #     300 + KELVIN_CONST,
    #     540 + KELVIN_CONST,
    #     10, 'Tb_out-Nel-ETAel.png')
