import time
from datetime import datetime as dt
from helpers.excp import Excp
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request, make_response, url_for, redirect
import requests, json
import urllib.request
import socket
from threading import Thread
from datetime import datetime, time as datetime_time, timedelta

app = Flask(__name__)
socket.setdefaulttimeout(5)
working_proxies = []


class ProxyProvider:

    @staticmethod
    def get_from_prov0():
        proxy_list = []

        import base64

        def base64_to_string(b):
            return base64.b64decode(b).decode('utf-8')

        try:
            for i in range(6):
                pagination = "/{0}".format(i) if i > 0 else ""
                url = (f"http://free-proxy.cz/en/proxylist/country"
                       f"/all/all/ping/all{pagination}")
                headers = {
                    "User-Agent":
                        (
                            "Mozilla/5.0 (Macintosh; Intel Mac "
                            "OS X 10_10_1) AppleWebKit/537.36 "
                            "(KHTML, like Gecko) Chrome/37.0.2062.124 "
                            "Safari/537.36"
                        )
                }
                req = requests.post(url=url, headers=headers)
                soup = BeautifulSoup(req.text, 'html.parser')
                trs = soup.find_all("tr")
                for tr in trs:
                    try:
                        tds = tr.find_all("td")
                        ip = base64_to_string(
                            tds[0].get_text().replace(
                                'document.write(Base64.decode("', "").replace(
                                '"))', ""))
                        port = tds[1].find("span").get_text().strip()
                        proxy = "{0}:{1}".format(ip, port)
                    except Exception:
                        pass
                    else:
                        proxy_list.append(proxy)
        except Exception as exp:
            print(Excp.tcb(error=exp))
            return []
        else:
            return proxy_list
            # dictToSend = {'proxyList': proxy_list}
            # res = requests.post(api_url + 'working_proxies', json=dictToSend)
            # res = json.loads(res.text)
            # return res["proxies"]

    @staticmethod
    def get_from_prov1():
        try:
            urls = [
                ("https://api.proxyscrape.com?request=getproxies"
                 "&proxytype=http&timeout=3000&country=all"
                 "&ssl=all&anonymity=all"),
                ("https://api.proxyscrape.com?request=getproxies"
                 "&proxytype=socks4&timeout=3000&country=all"),
                ("https://api.proxyscrape.com?request=getproxies"
                 "&proxytype=socks5&timeout=3000&country=all"),
            ]
            proc = []
            for i in urls:
                soup = BeautifulSoup(requests.get(i).text, 'html.parser')
                proc += [i.strip() for i in soup.get_text().split("\n")[:-1]]
        except Exception as exp:
            print(Excp.tcb(error=exp))
            return []
        else:
            return proc
            # dictToSend = {'proxyList': proc}
            # res = requests.post(api_url + 'working_proxies', json=dictToSend)
            # res = json.loads(res.text)
            # return res["proxies"]

    @staticmethod
    def get_from_prov2():
        from lxml.html import fromstring
        proc = []
        try:
            url = 'https://free-proxy-list.net/'
            response = requests.get(url)
            parser = fromstring(response.text)
            proxies = set()
            for i in parser.xpath('//tbody/tr')[:80]:
                if i.xpath('.//td[7][contains(text(),"yes")]'):
                    proxy = ":".join([i.xpath('.//td[1]/text()')[0],
                                      i.xpath('.//td[2]/text()')[0]])
                    proxies.add(proxy)
            proc += list(proxies)
        except Exception as exp:
            print(Excp.tcb(error=exp))
            return []
        else:
            return proc
            # dictToSend = {'proxyList': proc}
            # res = requests.post(api_url + 'working_proxies', json=dictToSend)
            # res = json.loads(res.text)
            # return res["proxies"]

    @staticmethod
    def get_from_prov3():
        try:
            url = "https://proxy-daily.com/"
            headers = {
                "User-Agent":
                    (
                        "Mozilla/5.0 (Macintosh; Intel Mac "
                        "OS X 10_10_1) AppleWebKit/537.36 (KHTML, "
                        "like Gecko) Chrome/37.0.2062.124 Safari/537.36"
                    )
            }
            req = requests.post(url=url, headers=headers)
            soup = BeautifulSoup(req.text, 'html.parser')
            ips = []
            d = {
                "class": "centeredProxyList freeProxyStyle"
            }
            for i in soup.find_all("div", d):
                ips += i.get_text().strip().split()
        except Exception as exp:
            print(Excp.tcb(error=exp))
            return []
        else:
            return ips
            # dictToSend = {'proxyList': ips}
            # res = requests.post(api_url + 'working_proxies', json=dictToSend)
            # res = json.loads(res.text)
            # return res["proxies"]

    @staticmethod
    def get_from_prov4():
        try:
            import json

            url = "https://www.cool-proxy.net/proxies.json"
            headers = {
                "User-Agent":
                    (
                        "Mozilla/5.0 (Macintosh; Intel "
                        "Mac OS X 10_10_1) AppleWebKit/537.36 "
                        "(KHTML, like Gecko) Chrome/37.0.2062.124 "
                        "Safari/537.36"
                    )
            }
            req = requests.post(url=url, headers=headers)
            soup = BeautifulSoup(req.text, 'html.parser')
            js = json.loads(soup.get_text())
            ips = [":".join([i["ip"], str(i["port"])]) for i in js]
        except Exception as exp:
            print(Excp.tcb(error=exp))
            return []
        else:
            return ips
            # dictToSend = {'proxyList': ips}
            # res = requests.post(api_url + 'working_proxies', json=dictToSend)
            # res = json.loads(res.text)
            # return res["proxies"]

    @staticmethod
    def get_from_prov5():
        proc = []
        try:
            url_spys = "http://spys.me/proxy.txt"
            soup = requests.get(url_spys).text
            for i in soup.split("\n"):
                for j in i.split():
                    if len(j) - len(j.replace(":", "").replace(".", "")) == 4:
                        proc.append(j.strip())
        except Exception as exp:
            print(Excp.tcb(error=exp))
            return []
        else:
            return proc
            # dictToSend = {'proxyList': proc}
            # res = requests.post(api_url + 'working_proxies', json=dictToSend)
            # res = json.loads(res.text)
            # return res["proxies"]

    @staticmethod
    def get_from_prov6():
        try:
            urls = [
                'https://www.proxynova.com/proxy-server-list/'
            ]
            proc = []
            ips = []
            for i in urls:
                soup = BeautifulSoup(requests.get(i).text, "lxml")
                port = soup.select('td:nth-child(2)')
                ip = soup.select('td:nth-child(1) abbr script')
                for i in ip:
                    i = i.text.replace("document.write('", "")
                    i = i.replace(");", "").replace("'", "").replace("+", "").replace(" ", "").strip()
                    ips.append(i)
                for index, address in enumerate(port):
                    proc.append(str(ips[index]) + ":" + address.text.strip())
        except Exception as exp:
            print(exp)
            return []
        else:
            return proc
            # dictToSend = {'proxyList': proc}
            # res = requests.post(api_url + 'working_proxies', json=dictToSend)
            # res = json.loads(res.text)
            # return res["proxies"]

    @staticmethod
    def get_from_prov7():
        try:
            urls = [
                'https://www.proxy-list.download/api/v2/get?l=en&t=http'
            ]
            proc = []
            for i in urls:
                response = json.loads(requests.get(i).text)
                ips = response['LISTA']
                for ip in ips:
                    proc.append(ip['IP'] + ':' + ip['PORT'])

        except Exception as exp:
            print(exp)
            return []
        else:
            return proc
            # dictToSend = {'proxyList': proc}
            # res = requests.post(api_url + 'working_proxies', json=dictToSend)
            # res = json.loads(res.text)
            # return res["proxies"]

    @staticmethod
    def get_from_prov8():
        try:
            urls = [
                'https://api.openproxy.space/lists/http'
            ]
            proc = []
            for i in urls:
                response = json.loads(requests.get(i).text)
                ips = response['data']
                for ip in ips:
                    for i in ip['items']:
                        proc.append(i)

        except Exception as exp:
            print(exp)
            return []
        else:
            return proc
            # dictToSend = {'proxyList': proc}
            # res = requests.post(api_url + 'working_proxies', json=dictToSend)
            # res = json.loads(res.text)
            # return res["proxies"]

    def get_proxies(self):
        return list(set(self.get_from_prov2()
                        + self.get_from_prov3()
                        + self.get_from_prov4()
                        + self.get_from_prov5()
                        + self.get_from_prov6()
                        + self.get_from_prov7()
                        + self.get_from_prov8()))



def time_diff(start, end):
    if isinstance(start, datetime_time):  # convert to datetime
        assert isinstance(end, datetime_time)
        start, end = [datetime.combine(datetime.min, t) for t in [start, end]]
    if start <= end:
        return end - start
    else:
        end += timedelta(1)  # +day
        assert end > start
        return end - start


def check_proxy(proxy):
    try:
        proxy_handler = urllib.request.ProxyHandler({'http': proxy})
        opener = urllib.request.build_opener(proxy_handler)
        opener.addheaders = [
            ('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.7.10) Gecko/20050811 Firefox/1.0.6')]
        urllib.request.install_opener(opener)
        sock = urllib.request.urlopen('https://www.quoka.de/')
        working_proxies.append(proxy)
        print('working : {}'.format(proxy))
    except urllib.error.HTTPError as e:
        print('failed: {}'.format(proxy))
        return e
    except Exception as detail:
        print('failed: {}'.format(proxy))
        return detail
    return 0


@app.route('/', methods=['GET'])
def response():
    return 'Hello World'


@app.route('/working_proxies', methods=['GET'])
def create_row_in_gs():
    pp = ProxyProvider()
    try:
        with open('last scraped time.txt', 'r') as timefile:
            last_scrape_time = datetime.strptime(timefile.readline().strip(), '%y-%m-%d %H:%M:%S')
            current_time = dt.now().strftime('%y-%m-%d %H:%M:%S')
            difference = abs(time_diff(last_scrape_time, current_time).total_seconds())
            if difference > 900:
                if request.method == 'GET':
                    proxies = pp.get_proxies()
                    threads = []

                    for proxy in proxies:
                        thread = Thread(target=check_proxy, args=(proxy.strip(),))
                        thread.start()
                        threads.append(thread)

                    for thread in threads:
                        thread.join()
                    time.sleep(1)
                    response = {'proxies': working_proxies}
                    with open('filtered_proxies.txt', 'w') as proxyfile:
                        proxyfile.writelines(response)
                    with open('last scraped time.txt', 'w') as timefile:
                        timefile.write(str(dt.now().strftime('%y-%m-%d %H:%M:%S')))
                    return jsonify(response)
            else:
                with open('filtered_proxies.txt', 'r') as proxyfile:
                    filtered_list = json.loads(''.join(proxyfile.readlines()))
                    return jsonify(filtered_list)

    except:
        if request.method == 'GET':
            proxies = pp.get_proxies()
            threads = []

            for proxy in proxies:
                thread = Thread(target=check_proxy, args=(proxy.strip(),))
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()
            time.sleep(1)
            response = {'proxies': working_proxies}
            with open('filtered_proxies.txt', 'w') as proxyfile:
                proxyfile.writelines(response)
            with open('last scraped time.txt', 'w') as timefile:
                timefile.write(str(dt.now().strftime('%y-%m-%d %H:%M:%S')))
            return jsonify(response)


if __name__ == '__main__':
    app.run(debug=False, use_reloader=True, host='0.0.0.0', port=3000)
