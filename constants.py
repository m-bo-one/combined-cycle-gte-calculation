# -*- coding: utf-8 -*-
# CONSTANTS
KELVIN_CONST = 273.15
R = 287 # J/kg*K
i = 5
cp = 1.0045
cv = 0.717
k = cp / float(cv)
a = 26.879
b = 6.971
d = -0.8206
mu = 28.01
ETAoi = 0.83
ETAem = 0.95
ETAcc = 0.95 # КПД камеры сгорания
EL_P_koef = 0.8

# STEAM
vWater = 1.0002 # Удельный обьем воды
ETAk = 0.89 # 0,86 -:- 0,92 -- КПД, учитывающий потери при сжигании топлива в котлоагрегате;
ETApp = 0.99 # 0,98 -:- 0,995 -- КПД, учитывающий потери в паропроводе при транспортировке водяного пара от парового котла до турбины;
ETAi = 0.41 # 0,37 -:- 0,45 -- внутренний КПД цикла, учитывающий потери из –за необратимости процессов в турбине и насосе;
ETAm = 0.98 # 0,97 -:- 0.995 -- механический КПД, учитывающий потери в подшипниках и на привод масляного насоса турбоагрегата;
ETAg = 0.98 # 0,97 -:- 0,99 -- КПД электрического генератора.
phi = 0.98 # коефициент сохранения теплоты
Qcond = 29330 # теплота сгорания условного топлива, кДж/кг

# FORMATS
format_work_params = "{0}: {1} \n"
new_line_f = '{0}{1}'.format('-' * 125, '\n')
formated_point_string = '{0:35} |{1:20} |{2:20} |{3:20} |{4:20} |\n'

# CONFIG FOR PLOTING
PLOT_CONFIG = {
    "x": {
        "label": None,  # label for x point, @string
        "data": {
            "from": None, # beggining point for ploting, @int
            "to": None, # end point, @int
            "count": None, # how much points to construct, @int
            "name": None, # name of param for changing, @string
        }
    },
    "y": {
        "label": None # label for y point, @string
    },
    "file_name": None,
    "GTE": {
        "grid": "ro-",
        "name": "Gas turbine engine" # default value
    },
    "SPE": {
        "grid": "bo-",
        "name": "Steam power engine" # default value
    },
    "CC": {
        "grid": "go-",
        "name": "Combined engine" # default value
    },
}
