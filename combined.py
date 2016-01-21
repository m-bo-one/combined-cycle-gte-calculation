# -*- coding: utf-8 -*-
from constants import *
from gte_calc import GTECalc
from pte_calc import PTECalc
from init_data import combined_INIT


class CombinedCalc(GTECalc, PTECalc):

    def __init__(self, **kwargs):
        GTECalc.__init__(self, **kwargs)
        PTECalc.__init__(self, **kwargs)

    def main(self):
        GTECalc.main(self)
        PTECalc.main(self)

    def save_results(self, file_name='combined.txt', mode='a'):
        try:
            import os
            os.remove(file_name)
        except:
            pass
        GTECalc.save_results(self, file_name, mode)
        PTECalc.save_results(self, file_name, mode)


if __name__ == '__main__':
    combined_calc = CombinedCalc(**combined_INIT)
    combined_calc.main()
    combined_calc.save_results()
