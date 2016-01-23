# -*- coding: utf-8 -*-
from constants import *
from init_data import INIT_DATA
from combined import CombinedCalc


# third party
import matplotlib.pyplot as plt
from numpy import *


GTES = {
    "SGT-100": {
        "constructor": "Siemens",
        "fuel": "gas",
        "N": 5.05, # MW
        "frequency": 50, # Hrz
        "ETAel": 0.302,
        "rpm": 17384,
        "PIk": 14,
        "T4": 531 + KELVIN_CONST, # oC
        "g4": 20.6 # kg/s,
    },
    "UGT-5000": {
        "constructor": "Zorya-Mashproekt",
        "N": 5.25, # MW
        "ETAel": 0.315,
        "g4": 21.5, # kg/s
        "PIk": 14,
        "T4": 480 + KELVIN_CONST,
        "rpm": 12840,
    },
    "GE4.5MW": {
        "constructor": "General Electric",
        "N": 4.57, # MW
        "T4": 565 + KELVIN_CONST,
        "g4": 16.3, # kg/s
        "PIk": 14.5,
        "rpm": 7000,
    }
}


class GTEAnalysisResult(object):

    def __init__(self, **kwargs):
        self.recal_engines = self.recalculated_data_of_engines(kwargs)
        self.engine_count = len(kwargs.keys())
        self.index = arange(self.engine_count)
        self.bar_width = 0.35

    @staticmethod
    def autolabel(ax, rects):
        # attach some text labels
        for rect in rects:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                    '%s' % round(height, 4),
                    ha='center', va='bottom')

    @staticmethod
    def recalculated_data_of_engines(GTES):
        recal_engines = {
            "ETAts": {
                "GTE": [],
                "SPE": [],
                "CC": []
            },
            "T4s": [],
            "PIks": [],
            "Ns": [],
            "names": [],
        }
        for key in GTES.keys():
            INIT_DATA.update({
                "T4": GTES[key]['T4'],
                "PIk": GTES[key]['PIk']
            })
            recal_engines['names'].append(key)
            recal_engines['T4s'].append(GTES[key]['T4'])
            recal_engines['PIks'].append(GTES[key]['PIk'])
            recal_engines['Ns'].append(GTES[key]['N'])
            combined_calc = CombinedCalc(**INIT_DATA)
            recal_engines["ETAts"]["GTE"].append(
                combined_calc.ETAtGTE
            )
            recal_engines["ETAts"]["SPE"].append(
                combined_calc.ETAtSPE
            )
            recal_engines["ETAts"]["CC"].append(
                combined_calc.ETAtCombined
            )
        return recal_engines

    def plot_ETAt(self):
        fig, ax = plt.subplots()
        rects1 = plt.bar(
            self.index,
            self.recal_engines["ETAts"]["GTE"],
            self.bar_width,
            color="b")
        rects2 = plt.bar(
            self.index + self.bar_width,
            self.recal_engines["ETAts"]["SPE"],
            self.bar_width,
            color="g")
        rects3 = plt.bar(
            self.index + 2 * self.bar_width,
            self.recal_engines["ETAts"]["CC"],
            self.bar_width,
            color="r")
        plt.xticks(self.index + 1.5 * self.bar_width, self.recal_engines['names'])
        self.autolabel(ax, rects1)
        self.autolabel(ax, rects2)
        self.autolabel(ax, rects3)
        ax.legend(
            (rects1[0], rects2[0], rects3[0]), ('GTE', 'SPE', 'CC'), loc=4)
        ax.set_ylabel('Thermal efficiency')
        plt.savefig(MEDIA_ROOT + 'engines_thermal_efficiency.png', dpi=400)
        plt.clf()

    def plot_T4(self):
        fig, ax = plt.subplots()
        rects1 = plt.bar(
            self.index,
            self.recal_engines["T4s"],
            self.bar_width,
            color="b")
        plt.xticks(self.index + 0.5 * self.bar_width, self.recal_engines['names'])
        self.autolabel(ax, rects1)
        ax.set_ylabel('Temperature of exhasted gases (K)')
        plt.savefig(MEDIA_ROOT + 'engines_exhaust.png', dpi=400)
        plt.clf()

    def plot_PIk(self):
        fig, ax = plt.subplots()
        rects1 = plt.bar(
            self.index,
            self.recal_engines["PIks"],
            self.bar_width,
            color="r")
        plt.xticks(self.index + 0.5 * self.bar_width, self.recal_engines['names'])
        self.autolabel(ax, rects1)
        ax.set_ylabel('Pressure ratio')
        plt.savefig(MEDIA_ROOT + 'engines_pressure_ration.png', dpi=400)
        plt.clf()

    def plot_N(self):
        fig, ax = plt.subplots()
        rects1 = plt.bar(
            self.index,
            self.recal_engines["Ns"],
            self.bar_width,
            color="g")
        plt.xticks(self.index + 0.5 * self.bar_width, self.recal_engines['names'])
        self.autolabel(ax, rects1)
        ax.set_ylabel('Power (MW)')
        plt.savefig(MEDIA_ROOT + 'engines_power.png', dpi=400)
        plt.clf()

    def plot_gist_of_engines(self):
        self.plot_ETAt()
        self.plot_T4()
        self.plot_PIk()
        self.plot_N()

if __name__ == '__main__':
    analysis = GTEAnalysisResult(**GTES)
    analysis.plot_gist_of_engines()
