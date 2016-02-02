# -*- coding: utf-8 -*-
# FILE='cc_calc/real/gte/gt_calc.py'
from os import sys, path
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


from wspru_api import WspRuAPI
from helpers import lazyproperty


wspru_api = WspRuAPI()


class GTCalcR(object):

    @lazyproperty
    def p3gte(self):
        """Тиск до ГТ (Па).
        """
        return self.p2gte * (1 - self.sigmapb)

    @lazyproperty
    def s3gte(self):
        """Ентропія суміші продуктів згорання і повітря при температурі
        перед ГТ (Дж/кгп*К).
        """
        return wspru_api.wspg('SGSPT', self.gsiair, self.p3gte, self.T3gte)

    @lazyproperty
    def T3gte(self):
        """Температура після КС при ізоентропному розширенні (K).
        """
        return wspru_api.wspg('TGSPS', self.gsiair, self.p3gte, self.s4gte)

    @lazyproperty
    def s4gte(self):
        """Ентропія робочого тіла за ГТ при реальному розширенні (Дж/кгп*К).
        """
        return wspru_api.wspg('SGSPT', self.gsg, self.p4gte, self.T4gte)

    @lazyproperty
    def p4gte(self):
        """Тиск газів за ГТ (Па).
        """
        return self.piair * (1 - self.sigmacc)

    @lazyproperty
    def lgtgte(self):
        """Теплоперепад в ГТ при ізоентропному розширенні (Дж/кгг).
        """
        return self.h3gte - self.h4gte

    @lazyproperty
    def lgtgte_r(self):
        """Теплоперепад в ГТ при реальному розширенні (Дж/кгг).
        """
        return self.lgtgte * self.ETAoi_gt

    @lazyproperty
    def h3gte(self):
        """Ентальпія продуктів зорання при температурі перед ГТ (Дж/кгг).
        """
        return wspru_api.wspg('HGST', self.gsg, self.T3gte)

    @lazyproperty
    def h4gte(self):
        """Ентальпія робочого тіла за ГТ при ізоентропному розширенні (Дж/кгг).
        """
        return wspru_api.wspg('HGST', self.gsg, self.T4gte)

    @lazyproperty
    def h4gte_r(self):
        """Ентальпія робочого тіла за ГТ при реальному розширенні (Дж/кгг).
        """
        return self.h3gte - self.lgtgte_r

    @lazyproperty
    def T4gte_r(self):
        """Температура робочого тіла за ГТ при реальному розширенні (K).
        """
        return wspru_api.wspg('TGSH', self.gsiair, self.h4gte_r)

    @lazyproperty
    def NgtGTE(self):
        """Потужність ГТ (Вт).
        """
        return self.lgtgte_r * self.Ggt * self.ETAm_gte
