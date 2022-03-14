import os
import random
import time
import urllib.parse
import urllib.request
from os.path import join

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import traceback
from PyPDF2 import PdfFileReader

# 创建一个agent池
agentPools = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.2; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0"
]

headers = {'User-Agent': agentPools[random.randint(0, 2)]}

click_xpath = '//*[contains(concat( " ", @class, " " ), concat( " ", "btn-default", " " ))]'


def fetch_magazines(key_word):
    req = urllib.request.Request('http://scientificmagazines.top/?s=' + key_word, None, headers)
    response = urllib.request.urlopen(req)
    the_page = response.read()
    # print(the_page.decode("utf8"))

    # 创建一个BeautifulSoup解析对象
    soup = BeautifulSoup(the_page, "html.parser", from_encoding="utf-8")
    links = soup.select('.entry')
    for link in links:
        get_pdf_download(key_word, link.text.split("Download")[1])


def get_pdf_download(key_word, url):
    if url.find("pdf") == -1:
        return
    else:
        print("缓存 os.path.dirname(__file__) 地址 : " + os.path.dirname(__file__))
        cd = join(os.path.dirname(__file__), "magazines", key_word)
        print("缓存 地址 : " + cd)

        print("获取地址 :" + url)
        req = urllib.request.Request(url, None, headers)
        response = urllib.request.urlopen(req)
        the_page = response.read()
        soup = BeautifulSoup(the_page, "html.parser", from_encoding="utf-8")
        list = soup.select('.btn-default')
        if list.count == 0:
            return
        wait_url = url + soup.select('.btn-default')[0]['href']
        print("正式下载等待网页地址 : " + wait_url)

        option = webdriver.ChromeOptions()
        option.add_argument('--headless')
        option.add_argument('--disable-popup-blocking')
        option.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
        option.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        option.add_argument('disable-infobars')  # 隐藏"Chrome正在受到自动软件的控制"
        option.add_argument("--user-data-dir=" + r"D:/chrome/")

        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': cd}
        option.add_experimental_option('prefs', prefs)

        driver = webdriver.Chrome(chrome_options=option)

        pdf_name = os.path.basename(url)
        pdf = cd + "\\" + pdf_name

        print(pdf_name + " 是否存在 pdf " + str(os.path.exists(pdf)))
        print(pdf_name + " 是否是有效 pdf " + str(isValidPDF_pathfile(pdf)))
        if os.path.exists(pdf) and isValidPDF_pathfile(pdf):
            print(pdf_name + " 已经存在且有效")
            driver.quit()
        else:
            if os.path.exists(pdf):
                print(pdf_name + " 已经存在 , 进行删除")
                os.remove(pdf)
            try:
                driver.get(url + wait_url)
                # driver.implicitly_wait(40)
                wait = WebDriverWait(driver, 40)
                wait.until(EC.visibility_of_any_elements_located((By.XPATH, click_xpath)))

                html = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
                soup = BeautifulSoup(html, "html.parser", from_encoding="utf-8")
                link = soup.select('.btn-default')[0]['href']
                print("真实下载地址 : " + link)

                driver.find_element_by_xpath(click_xpath).click()

                downloads_done(pdf)

                # 下载后重命名
                os.chdir(cd)
                files = filter(os.path.isfile, os.listdir(cd))
                files = [os.path.join(cd, f) for f in files]  # add path to each file
                files.sort(key=lambda x: os.path.getmtime(x))
                newest_file = files[-1]
                os.rename(newest_file, pdf_name)

                if os.path.exists(pdf) and isValidPDF_pathfile(pdf):
                    print(pdf + " 下载完成 !!!")
                else:
                    print(pdf_name + " 是否存在 pdf " + str(os.path.exists(pdf)))
                    print(pdf_name + " 是否是有效 pdf " + str(isValidPDF_pathfile(pdf)))
                    print(pdf + " 下载失败 正在进行重试 !!!")
                    driver.quit()
                    get_pdf_download(key_word, url)
            except Exception as e:
                print(e)
            finally:
                driver.quit()


def downloads_done(path):
    if not os.path.exists(path):
        time.sleep(0.5)
        downloads_done(path)


def isValidPDF_pathfile(pathfile):
    bValid = True
    try:
        reader = PdfFileReader(pathfile)
        if reader.getNumPages() < 1:  # 进一步通过页数判断。
            bValid = False
    except:
        bValid = False
        print("*" + traceback.format_exc())
    return bValid
