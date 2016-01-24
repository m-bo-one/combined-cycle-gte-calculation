import inspect


# third party
import requests
from bs4 import BeautifulSoup


class WspRuAPI(object):

    url_format = 'http://www.wsp.ru/ru/test/%s.asp'

    def _gen_data(self, wspg, *args):
        """
        params
        @gas_specification - type of gas;
        @p - pressure (Pa);
        @t - temperature (K);
        @s - enthropy (J/(kg*K))
        """
        if wspg == 'SGSPT':
            data = dict(
                gas_specification=args[0], p=args[1], t=args[2])
        elif wspg == 'HGST':
            data = dict(
                gas_specification=args[0], t=args[1])
        elif wspg == 'TGSPS':
            data = dict(
                gas_specification=args[0], p=args[1], s=args[2])
        elif wspg in ('PST', 'PSUBT'):
            data = dict(t=args[0])
        return "&".join("%s=%s" % (k, v) for k, v in data.items())

    def _get_result(self, url, wspg, *args):
        data = self._gen_data(wspg, *args)
        response = requests.get(url, params=data)
        html_doc = response.content.decode('cp1251').encode('utf-8')
        soup = BeautifulSoup(html_doc, "lxml")
        return float(soup.find('strong').text.replace(',', '.'))

    def wspg(self, wspg, *args):
        f_name = inspect.stack()[0][3]
        url = self.url_format % (f_name + wspg)
        return self._get_result(url, wspg, *args)

    def wsp(self, wspg, *args):
        f_name = inspect.stack()[0][3]
        url = self.url_format % (f_name + wspg)
        return self._get_result(url, wspg, *args)


if __name__ == '__main__':
    api = WspRuAPI()
    print api.wspg('TGSPS', 'N2', 100000, 7000.234)
