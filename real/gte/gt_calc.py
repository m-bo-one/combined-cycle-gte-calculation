# -*- coding: utf-8 -*-
# FILE='cc_calc/real/gte_r/gt_calc.py'
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


from wspru_api import WspRuAPI
from init_data import INIT_DATA


wspru_api = WspRuAPI()


class GTCalcR(object):

    @property
    def p3gte(self):
        """Тиск до ГТ (Па).
        """
        return self.p2gte * (1 - self.sigmapb)

    @property
    def s3gte(self):
        """Ентропія суміші продуктів згорання і повітря при температурі перед ГТ (Дж/кгп*К).
        """
        return wspru_api.wspg('SGSPT', self.gsiair, self.p3gte, self.T3gte)

    @property
    def T3gte(self):
        """Температура після КС при ізоентропному розширенні (K).
        """
        return wspru_api.wspg('TGSPS', self.gsiair, self.p3gte, self.s4gte)

    @property
    def s4gte(self):
        """Ентропія робочого тіла за ГТ при реальному розширенні (Дж/кгп*К).
        """
        return wspru_api.wspg('SGSPT', self.gsg, self.p4gte, self.T4gte)

    @property
    def p4gte(self):
        """Тиск газів за ГТ (Па).
        """
        return self.piair * (1 - self.sigmapp)

    @property
    def lgtgte(self):
        """Теплоперепад в ГТ при ізоентропному розширенні (Дж/кгг).
        """
        return self.h3gte - self.h4gte

    @property
    def lgtgte_r(self):
        """Теплоперепад в ГТ при реальному розширенні (Дж/кгг).
        """
        return self.lgtgte * self.ETAoi_gt

    @property
    def h3gte(self):
        """Ентальпія продуктів зорання при температурі перед ГТ (Дж/кгг).
        """
        return wspru_api.wspg('HGST', self.gsg, self.T3gte)

    @property
    def h4gte(self):
        """Ентальпія робочого тіла за ГТ при ізоентропному розширенні (Дж/кгг).
        """
        return wspru_api.wspg('HGST', self.gsg, self.T4gte)

    @property
    def h4gte_r(self):
        """Ентальпія робочого тіла за ГТ при реальному розширенні (Дж/кгг).
        """
        return self.h3gte - self.lgtgte_r

    @property
    def T4gte_r(self):
        """Температура робочого тіла за ГТ при реальному розширенні (K).
        """
        return wspru_api.wspg('TGSH', self.gsiair, self.h4gte_r)

    @property
    def NgtGTE(self):
        """Потужність ГТ (Вт).
        """
        return self.lgtgte_r * self.Ggt * self.ETAm_gte
