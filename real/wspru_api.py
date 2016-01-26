# third party
import requests
from bs4 import BeautifulSoup


class WspRuAPI(object):

    url_format = 'http://www.wsp.ru/ru/test/%s.asp'

    def _gen_data(self, f_type, *args):
        """
        params
        @gas_specification - type of gas (Ex.: AirMix, Air, N2 etc.);
        @p - pressure (Pa);
        @t - temperature (K);
        @s - enthropy (J/(kg*K));
        @h - enthalpy (J/kg);
        """
        if f_type == 'SGSPT':
            data = dict(
                gas_specification=args[0], p=args[1], t=args[2])
        elif f_type == 'HPT':
            data = dict(p=args[0], t=args[1])
        elif f_type == 'HGST':
            data = dict(
                gas_specification=args[0], t=args[1])
        elif f_type == 'TGSH':
            data = dict(
                gas_specification=args[0], h=args[1])
        elif f_type == 'TGSPS':
            data = dict(
                gas_specification=args[0], p=args[1], s=args[2])
        elif f_type in ('PST', 'PSUBT'):
            data = dict(t=args[0])
        elif f_type == 'MMGS':
            data = dict(gas_specification=args[0])
        return "&".join("%s=%s" % (k, v) for k, v in data.items())

    def _get_result(self, f_name, f_type, *args):
        url = self.url_format % (f_name + f_type)
        data = self._gen_data(f_type, *args)
        response = requests.get(url, params=data)
        html_doc = response.content.decode('cp1251').encode('utf-8')
        soup = BeautifulSoup(html_doc, "lxml")
        return float(soup.find('strong').text.replace(',', '.'))

    def wspg(self, f_type, *args):
        return self._get_result('wspg', f_type, *args)

    def wsp(self, f_type, *args):
        return self._get_result('wsp', f_type, *args)


if __name__ == '__main__':
    api = WspRuAPI()
    print api.wspg('TGSPS', 'N2', 10000000, 7000.234)
