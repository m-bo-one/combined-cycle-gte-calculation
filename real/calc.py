from wspru_api import WspRuAPI
from init_data import INIT_DATA


wspru_api = WspRuAPI()


class RealCalc(object):

    def __init__(self, **kwargs):
        self.p1gte = self.piair = kwargs['piair']
        self.PIk = kwargs['PIk']
        self.T1gte = self.Tiair = kwargs['Tiair']
        self.T3gte= kwargs['T3']
        self.phiiair = kwargs['phiiair']
        self.gsg = kwargs['gsg']
        self.gs0 = kwargs['gs0']
        self.sigmapb = kwargs['sigmapb']
        self.sigmapp = kwargs['sigmapp']

    @property
    def p2gte(self):
        """Pressure after gas compressor (MPa).
        """
        return self.PIk * self.p1gte

    @property
    def pbiair(self):
        """Boundary pressure of water at the temperature of environment (MPa).
        """
        if self.Tiair > 273.15:
            _p = wspru_api.wsp('PST', self.Tiair)
        else:
            _p = wspru_api.wsp('PSUBT', self.Tiair)
        return _p / float(10**6)

    @property
    def xiair(self):
        """The molar water content (unitless).
        """
        return self.phiiair * self.pbiair / float(self.piair - self.phiiair * self.pbiair)

    @property
    def diair(self):
        """The mass water content (kg of steam/kg of dry air).
        """
        return self.xiair * wspru_api.wspg('MMGS', 'H2O') / float(wspru_api.wspg('MMGS', 'AirMix'))

    @property
    def gsiair(self):
        """Estimated mixture of moist air (unitless).
        """
        return "AirMix:1;H2O:" + str(self.xiair)

    @property
    def h1gte(self):
        """Enthalpy of moisture air at atmospheric conditions (kJ/kga).
        """
        return wspru_api.wspg('HGST', self.gsiair, self.Tiair)

    @property
    def h2gte(self):
        """Enthalpy of air after compressor at isoenthropic pressure (kJ/kga).
        """
        return wspru_api.wspg('HGST', self.gsiair, self.T2gte)

    @property
    def s1gte(self):
        """Enthropy of inlet air (kj/kga*K).
        """
        return wspru_api.wspg('SGSPT', self.gsiair, self.piair, self.Tiair)

    @property
    def T2gte(self):
        """Temperature of air after compressor at isoenthropic pressure (K).
        """
        return wspru_api.wspg('TGSPS', self.gsiair, self.p2gte, self.s1gte)

    @property
    def h3gte(self):
        """Enthalpy of combusted products at the temperature before GT (kJ/kgg).
        """
        return wspru_api.wspg('HGST', self.gsg, self.T3gte)

    @property
    def h4gte(self):
        """Enthalpy of working body after GT at isoentropic expansion (kJ/kgg).
        """
        return wspru_api.wspg('HGST', self.gsg, self.T4gte)

    @property
    def p3gte(self):
        """Pressure before GT (MPa).
        """
        return self.p2gte * (1 - self.sigmapb)

    @property
    def s3gte(self):
        """Enthropy before GT (kJ/kgg*K).
        """
        return wspru_api.wspg('SGSPT', self.gsg, self.p3gte, self.T3gte)

    @property
    def p4gte(self):
        """Pressure after GT (MPa).
        """
        return self.piair * (1 - self.sigmapp)

    @property
    def T4gte(self):
        """Temperature of air after GT at isoenthropic pressure (K).
        """
        return wspru_api.wspg('TGSPS', self.gsiair, self.p4gte, self.s3gte)


if __name__ == '__main__':
    real_calc = RealCalc(**INIT_DATA)
