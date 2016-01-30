from wspru_api import WspRuAPI
from init_data import INIT_DATA


wspru_api = WspRuAPI()


class GTECalcR(object):

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        self.p1gte = self.piair
        self.T1gte = self.Tiair

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
        return self.phiiair * self.pbiair \
            / float(self.piair - self.phiiair * self.pbiair)

    @property
    def diair(self):
        """The mass water content (kg of steam/kg of dry air).
        """
        return self.xiair * wspru_api.wspg('MMGS', 'H2O') \
            / float(wspru_api.wspg('MMGS', 'AirMix'))

    @property
    def gsiair(self):
        """Estimated mixture of moist air (unitless).
        """
        return "AirMix:1;H2O:" + str(self.xiair)

    @property
    def h1gte(self):
        """Enthalpy of moisture air at atmospheric conditions (J/kga).
        """
        return wspru_api.wspg('HGST', self.gsiair, self.Tiair)

    @property
    def h2gte(self):
        """Enthalpy of air after compressor at isoenthropic pressure (J/kga).
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
        """Enthalpy of combusted products at the temperature before GT (J/kgg).
        """
        return wspru_api.wspg('HGST', self.gsg, self.T3gte)

    @property
    def h4gte(self):
        """Enthalpy of working body after GT at isoentropic expansion (J/kgg).
        """
        return wspru_api.wspg('HGST', self.gsg, self.T4gte)

    @property
    def p3gte(self):
        """Pressure before GT (MPa).
        """
        return self.p2gte * (1 - self.sigmapb)

    @property
    def s4gte(self):
        """Enthropy after GT (kJ/kgg*K).
        """
        return wspru_api.wspg('SGSPT', self.gsg, self.p4gte, self.T4gte)

    @property
    def p4gte(self):
        """Pressure after GT (MPa).
        """
        return self.piair * (1 - self.sigmapp)

    @property
    def T3gte(self):
        """Temperature of air after CC at isoenthropic pressure (K).
        """
        return wspru_api.wspg('TGSPS', self.gsiair, self.p3gte, self.s4gte)

    @property
    def lgtgte(self):
        """Heat drop in GT at isoenthropic expansion (J/kgg).
        """
        return self.h3gte - self.h4gte

    @property
    def lgtgte_r(self):
        """Heat drop in GT at real expansion (J/kgg).
        """
        return self.lgtgte * self.ETAoi_gt

    @property
    def NgtGTE(self):
        """Power of GT (W).
        """
        return self.lgtgte_r * self.Gr * self.ETAm_gte

    @property
    def lcgte(self):
        """Heat drop in C at isoenthropic expansion (J/kgg).
        """
        return self.h2gte - self.h1gte

    @property
    def lcgte_r(self):
        """Heat drop in C at real expansion (J/kgg).
        """
        return self.lcgte / float(self.ETAoi_c)

    @property
    def NcGTE(self):
        """Power of C (W).
        """
        return self.lcgte_r * self.Bf / float(self.ETAm_gte)

    @property
    def Gr(self):
        """Gas consumption through GT (kg of gas / sec).
        """
        return self.Giair + self.Bf

    @property
    def NelGTE(self):
        """Power of GTE electric generator (W).
        """
        return self.ETAg_gte * (self.NgtGTE - self.NcGTE)

    @property
    def Q1_gte(self):
        """Amount of heat given for CC (W)
        """
        return self.Ql_h * self.ETAc_c * self.Bf

    @property
    def ETAelGTE(self):
        """Electrical efficiency of GT.
        """
        return self.NelGTE / float(self.Q1_gte)


if __name__ == '__main__':
    real_calc = GTECalcR(**INIT_DATA)
    with open('test_r.txt', 'w') as writer:
        for x in xrange(1, 5):
            pressure = getattr(real_calc, 'p%sgte' % x)
            temperature = getattr(real_calc, 'T%sgte' % x)
            enthropy = wspru_api.wspg('SGSPT', 'AirMix', pressure, temperature)
            writer.write('Point %s\n' % x)
            writer.write("pressure: %s" % pressure)
            writer.write('\n')
            writer.write("temp: %s" % temperature)
            writer.write('\n')
            writer.write("enthropy: %s" % enthropy)
            writer.write('\n' + "-" * 10 + '\n')
