import urllib.parse
import urllib.request
from bs4 import BeautifulSoup


def fetch_magazines(key_word):
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}
    req = urllib.request.Request('http://scientificmagazines.top/?s=' + key_word, None, headers)
    response = urllib.request.urlopen(req)
    the_page = response.read()
    print(the_page.decode("utf8"))

    # 创建一个BeautifulSoup解析对象
    soup = BeautifulSoup(the_page, "html.parser", from_encoding="utf-8")
    links = soup.select('.entry-title , .entry')
    print("打印 所有的 item :")
    print(links)
    # for link in links:
    #     print(link.name, link['href'], link.get_text())
