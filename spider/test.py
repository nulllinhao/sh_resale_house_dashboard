import requests

cookies = {
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
    'C3VK': 'e16622',
    'Hm_lpvt_cf8004879455b04c74d33aa164379a1d': '1740145491',
    'Hm_lpvt_94ed3d23572054a86ed341d64b267ec6': '1740145491',
}

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Referer': 'https://sh.5i5j.com/ershoufang/n1/',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-Fetch-User': '?1',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0',
    'sec-ch-ua': '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    # 'Cookie': 'SECKEY_ABVK=u/tTJNif2iYZ6hNp9pzyWnRCNlBczmqqAHrQtNWyTwI%3D; BMAP_SECKEY=hqNqhvAjUam_yWrrahaCl7axbAo1DDcmF9fIVVWQCHjXDIj9dGyKfdxuhxshwDUmRbyNV9yzgCc37ydFg0BVDkAyhe1ZEfbkMCr24dVSAao-9j7kBQjTWfEE8HsUTJJFxLMQdp-YD9OZjOcCvi1wFC6t3VoKQmwMR6Ayhb2RTxnAhiUL_lTkcEqez2uKnINC; ser_cookie_id=A53CC0BC-3598-216C-548E-65F9514BB84B; sensorsdata2015jssdkchannel=%7B%22prop%22%3A%7B%22_sa_channel_landing_url%22%3A%22%22%7D%7D; smidV2=2025012316020288ac7b9c44e79062312e87d37c08416e00d1ea797b1370ec0; gr_user_id=92d160ed-db39-4152-a026-92a071404e2e; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22194922e698f6fc-0ee02f325b71908-4c657b58-2764800-194922e6990f9d%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22_latest_wx_ad_click_id%22%3A%22%22%2C%22_latest_wx_ad_hash_key%22%3A%22%22%2C%22_latest_wx_ad_callbacks%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk0OTIyZTY5OGY2ZmMtMGVlMDJmMzI1YjcxOTA4LTRjNjU3YjU4LTI3NjQ4MDAtMTk0OTIyZTY5OTBmOWQifQ%3D%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%22%2C%22value%22%3A%22%22%7D%2C%22%24device_id%22%3A%22194922e698f6fc-0ee02f325b71908-4c657b58-2764800-194922e6990f9d%22%7D; ershoufang_BROWSES=825090979%2C824673028%2C501273599%2C825098628; PHPSESSID=evqq8tv42j6fna0ku99i10kkl6; Hm_lvt_94ed3d23572054a86ed341d64b267ec6=1737619324,1739093266,1739864416; HMF_CI=9c27b4825d1cf597e342ae0610ed51c22db9e880a3421037a9102303f9e0ac6267517adae53579999b482bc73e41e4413481c34302b40e46b072e0a86d0a91cd80; HMACCOUNT=D8D5D3657EA1B9FA; Hm_lvt_cf8004879455b04c74d33aa164379a1d=1737619303,1739093266,1739864442; domain=sh; HMY_JC=460ce0f8a5cb4fd5a8cc33f2693112330f81d6bf15908497101586417d806eaefe,; 8fcfcf2bd7c58141_gr_session_id=1965859f-9a9b-483f-880d-11336928d5a9; C3VK=e16622; Hm_lpvt_cf8004879455b04c74d33aa164379a1d=1740145491; Hm_lpvt_94ed3d23572054a86ed341d64b267ec6=1740145491',
}

response = requests.get('https://sh.5i5j.com/ershoufang/n1/', cookies=cookies, headers=headers)

print(response.text)