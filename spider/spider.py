import requests
import os
from lxml import etree
from bs4 import BeautifulSoup
import re
import time
import random
import json
from state_logger import *
# from deepl_translate import translate_text_deepl
from proxy_pool import ProxyPool

class Spider:
    def __init__(self):
        # self.browser = self._init_browser()

        # 初始化代理池
        self.proxy_pool = ProxyPool('proxy_list.json')

        self.url = "https://sh.5i5j.com/ershoufang/"
        self.cookies = {
            'SECKEY_ABVK': 'u/tTJNif2iYZ6hNp9pzyWnRCNlBczmqqAHrQtNWyTwI%3D',
            'BMAP_SECKEY': 'hqNqhvAjUam_yWrrahaCl7axbAo1DDcmF9fIVVWQCHjXDIj9dGyKfdxuhxshwDUmRbyNV9yzgCc37ydFg0BVDkAyhe1ZEfbkMCr24dVSAao-9j7kBQjTWfEE8HsUTJJFxLMQdp-YD9OZjOcCvi1wFC6t3VoKQmwMR6Ayhb2RTxnAhiUL_lTkcEqez2uKnINC',
            'ser_cookie_id': 'A53CC0BC-3598-216C-548E-65F9514BB84B',
            'sensorsdata2015jssdkchannel': '%7B%22prop%22%3A%7B%22_sa_channel_landing_url%22%3A%22%22%7D%7D',
            'smidV2': '2025012316020288ac7b9c44e79062312e87d37c08416e00d1ea797b1370ec0',
            'gr_user_id': '92d160ed-db39-4152-a026-92a071404e2e',
            'sensorsdata2015jssdkcross': '%7B%22distinct_id%22%3A%22194922e698f6fc-0ee02f325b71908-4c657b58-2764800-194922e6990f9d%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22_latest_wx_ad_click_id%22%3A%22%22%2C%22_latest_wx_ad_hash_key%22%3A%22%22%2C%22_latest_wx_ad_callbacks%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk0OTIyZTY5OGY2ZmMtMGVlMDJmMzI1YjcxOTA4LTRjNjU3YjU4LTI3NjQ4MDAtMTk0OTIyZTY5OTBmOWQifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%22194922e698f6fc-0ee02f325b71908-4c657b58-2764800-194922e6990f9d%22%7D',
            'ershoufang_BROWSES': '825090979%2C824673028%2C501273599%2C825098628',
            'PHPSESSID': 'evqq8tv42j6fna0ku99i10kkl6',
            'Hm_lvt_94ed3d23572054a86ed341d64b267ec6': '1737619324,1739093266,1739864416',
            'HMF_CI': '9c27b4825d1cf597e342ae0610ed51c22db9e880a3421037a9102303f9e0ac6267517adae53579999b482bc73e41e4413481c34302b40e46b072e0a86d0a91cd80',
            'HMACCOUNT': 'D8D5D3657EA1B9FA',
            'Hm_lvt_cf8004879455b04c74d33aa164379a1d': '1737619303,1739093266,1739864442',
            'domain': 'sh',
            'HMY_JC': '460ce0f8a5cb4fd5a8cc33f2693112330f81d6bf15908497101586417d806eaefe,',
            '8fcfcf2bd7c58141_gr_session_id': '1965859f-9a9b-483f-880d-11336928d5a9',
            'Hm_lpvt_94ed3d23572054a86ed341d64b267ec6': '1740145199',
            'Hm_lpvt_cf8004879455b04c74d33aa164379a1d': '1740145199',
            'C3VK': '049571',
        }  # self._get_cookies(True)  # 通过浏览器自动获取 Cookies
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0',
        }
        self.proxies = {  # Clash Verge
            "http": "http://127.0.0.1:7890",
            "https": "http://127.0.0.1:7890",
        }
        
        from data_handler import get_handler
        self.data_handler = get_handler(
            'mysql',
            repo_name='sh_resale_house',
            url='mysql://root:root@localhost/scraping_db'
        )  # MySQL 处理器
        # columns = [
        #     "标题",
        #     "房型",
        #     "方向",
        #     "总价",
        #     "单价",
        #     "面积",
        #     "楼层",
        #     "建造年份",
        #     "建筑类型",
        #     "行政区",
        #     "街道",
        #     "小区",
        #     "地址",
        #     "图片",
        #     "标签",
        #     "网址"
        # ]
        # self.data_handler = get_handler(
        #     'excel',
        #     repo_name='sh_resale_house',
        #     columns=columns
        # )  # Excel 处理器
    
    def _init_browser(self):
        """
        初始化自动化浏览器
        """

        """ DrissionPage 版"""
        from DrissionPage import ChromiumOptions, ChromiumPage

        co = ChromiumOptions()
        co.set_browser_path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
        co.use_system_user_path()
        browser = ChromiumPage(co)

        """ Selenium 版"""
        from selenium import webdriver

        service = webdriver.EdgeService('C:\\Users\\11627\\OneDrive\\CS\\PL\\Python\\Scraping\\drivers\\msedgedriver.exe')
        options = webdriver.EdgeOptions()
        # 无头浏览器设置
        # options.add_argument('--headless')
        # options.add_argument('--disable-gpu')
        # 反反selenium爬虫设置
        # options.add_experimental_option('excludeSwitches', ['enable-automation'])
        # options.add_experimental_option('useAutomationExtension', False)
        # options.add_experimental_option('detach', True)  # 运行结束不关闭浏览器进程

        browser = webdriver.Edge(options=options, service=service)
        browser.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
            "source": "Object.defineProperty(navigator, 'webdriver', {get:()=>undefined})"
        })

        return browser

    # def _get_cookies(self, is_init=False):
    #     if not is_init:
    #         print("Cookie 已过期，正在等待新 Cookie 加载...")
    #         time.sleep(60)

    #     tab = self.browser.new_tab("https://www.taobao.com")
    #     cookies = tab.cookies().as_dict()
    #     # print("cookies", cookies)
    #     tab.close()
    #     self.browser.set.window.mini()

    #     if not is_init:
    #         print("Cookie 已更新，重新尝试...")

    #     return cookies

    def _get_processed_data(self, raw_data):
        """
        向 express 发送原始数据，获取加密值
        :param raw_data: 原始数据
        :return: 加密值
        """
        response = requests.post(
            "http://127.0.0.1:3000",
            json={
                "rawData": raw_data,
            }
        )
        processed_data = response.text
        return processed_data

    def _request(self, url, method='get', headers=None, params=None, data=None):  # todo: 一边爬取一边判断
        """
        根据动态代理池，重写request方法
        随机获取一个代理，尝试请求，避免同一IP频发发起请求遭到风控
        如果失败则移除该代理，继续尝试下一个代理，直到代理池为空
        代理池为空之后，get_random_proxy()会自动刷新代理池，继续尝试
        :param url: 请求的URL
        :param method: 请求方法，默认为GET
        :param headers: 请求头
        """
        while len(self.proxy_pool.proxy_pool) > 0:
            proxy = self.proxy_pool.get_random_proxy()
            proxies = {'http': f'http://{proxy}', 'https': f'http://{proxy}'}
            
            try:
                if method == 'get':
                    response = requests.get(url, headers=headers, params=params,
                                          proxies=proxies, timeout=15)
                else:
                    response = requests.post(url, headers=headers, data=data,
                                           proxies=proxies, timeout=15)
                
                if response.status_code == 200:
                    return response
                
                # 非200响应处理
                print(f"请求失败，状态码：{response.status_code}，移除代理 {proxy}")
                self.proxy_pool.proxy_pool.remove(proxy)
                
            except Exception as e:
                print(f"请求异常：{str(e)}，移除代理 {proxy}")
                self.proxy_pool.proxy_pool.remove(proxy)
        
        raise Exception("代理池已耗尽，所有代理均尝试失败")

    def crawl_list_page(self, page, index):
        """
        爬取二手房列表页
        :param page: 页码
        :param index: 起始索引
        """
        
        response = self._request(
            url=self.url + f"n{page}/",
            method='get',
            headers=self.headers
        )

        # print(response.text)

        if "oopopdwskl" in response.text:
            sleep_time = 3600
            print(f"触发风控，等待 {sleep_time} 秒后继续")
            time.sleep(sleep_time)

        # 使用 Xpath 解析 HTML
        tree = etree.HTML(response.text)
        detail_url_list = tree.xpath('/html/body/div[7]/div[1]/div[2]/ul/li/div[2]/h3/a/@href')[:30]
        for detail_url_index, detail_url in enumerate(detail_url_list):
            if detail_url_index < index:
                continue

            house_id = detail_url.split("/")[-1].split(".")[0]
            tag = tree.xpath(f'/html/body/div[7]/div[1]/div[2]/ul/li[{index + 1}]/div[2]/div[2]/span/text()')  # 房源标签
            data = [*self.crawl_detail_page(house_id), ', '.join(tag), self.url + detail_url.split("/")[-1] + "/"]
            print(data)

            self.data_handler.append_data(data)
            self.data_handler.save_data()
            print("detail_url_index", detail_url_index, "next_index", detail_url_index + 1)

            save_state(page, detail_url_index + 1)
            sleep_time = random.randint(0, 1)
            print(f"已爬取 {detail_url} 并保存数据，等待 {sleep_time} 秒后继续")
            time.sleep(sleep_time)

    def crawl_detail_page(self, house_id):
        """
        爬取二手房详情页
        :param house_id: 二手房ID
        :return: 二手房信息
        """
        response = self._request(
            url="https://appapi.5i5j.com/vr/9/houseinfo",
            method='post',
            headers=self.headers,
            data={
                'cityid': '9',
                'houseid': house_id,
                'type': '1',
                'brokerId': '',
                # 'bid': '565924',
                'equipment': '',
                'from': '',
                'platform': '1',
                'vrcomplanyid': '4',
            }
        )
        house_info = response.json()['data']["houseInfoNew"]

        title = house_info["title"]  # 标题
        layout = house_info["layout"]  # 户型
        head_ing = house_info["heading"]  # 朝向
        price = house_info["price"]  # 总价
        unit_price = house_info["unitprice"]  # 单价
        area = house_info["area"]  # 面积
        floor = house_info["floor"]  # 楼层
        build_year = house_info["buildyear"]  # 建造年份
        building_type = house_info["buildingtype"]  # 建筑类型
        sq = house_info["sq"]  # 街道
        community_name = house_info["communityName"]  # 小区
        address = house_info["address"]  # 地址
        imgs_url = house_info["imgs"]  # 图片链接

        lat = house_info["lat"]  # 纬度
        lng = house_info["lng"]  # 经度

        # 二手房详情json信息中并没有所在行政区信息，但页面上有地图显示行政区信息
        # 因此考虑获取经纬度，再模拟发送请求获取行政区信息
        url = "https://sh.5i5j.com/periphery"
        params = {
            'query': '地铁站',
            'location': f'{lat}, {lng}',
            'radius': '3000',
            'scope': '2',
            'page_num': '0',
        }
        response = self._request(
            url=url,
            method='get',
            params=params,
            headers={
                **self.headers,
                "referer":f"{self.url}/{house_id}.html"
            }
        )
        # print(response.json())
        distinct = response.json()['data'][0]['area']  # 根据地图信息获取房源所在的行政区

        return title, layout, head_ing, price, unit_price, area, floor, build_year, building_type, distinct, sq, community_name, address, ', '.join(imgs_url)
            # try:
            #     # 使用新的重试机制
            # except Exception as e:
            #     attempt += 1
            #     print(f"第 {attempt} 次尝试失败: {e}")
            #     if attempt >= max_retries:
            #         # print(url)
            #         print("所有重试均失败。")
            #         raise e
                
            #     sleep_time = random.randint(10, 20)
            #     print(f"等待 {sleep_time} 秒后进行第 {attempt + 1} 次重试...")
            #     time.sleep(sleep_time)
            # todo: 上面待删除
            
    def save_issued_page_and_exit(self, response_text):
        with open("issued_page.html", "w", encoding="utf-8") as f:
            f.write(response_text)
        exit(0)

if __name__ == "__main__":
    spider = Spider()
    
    try:
        page_origin = 1  # 记录起始页码是 0 还是 1，起始页码为 0 的话后续操作要自动 -1

        # 使用 JSON 获取及保存爬取进度
        state = load_state()
        if state:
            start_page = state["next_page"]
            start_index = state["next_index"]
        else:
            start_page = page_origin
            start_index = 0
        
        page = start_page
        end_page = 177
        if not page_origin:
            end_page -= 1
        
        while True:
            if page > end_page:
                break
            spider.crawl_list_page(page, start_index)

            sleep_time = random.randint(0, 1)
            print(f"已爬取第 {page if page_origin else page + 1} 页并保存数据，等待 {sleep_time} 秒后继续")
            if page == 4:
                exit(0)
            page += 1
            save_state(page, 0)
            time.sleep(sleep_time)
        
        clear_state()
        print("爬取完成~~~！")

    finally:
        spider.data_handler.close_repository()
        # 运行结束后关闭数据仓库（Openxyl 或 数据库连接）