import json
import random
import requests

class ProxyPool:
    def __init__(self, json_path):
        self.proxy_list = self._load_proxy_list(json_path)  # 所有 IP 列表
        self.proxy_pool = self._generate_proxy_pool()  # 有效 IP 池

    def _load_proxy_list(self, json_path):
        with open(json_path, 'r', encoding='utf-8') as f:
            json_data = json.load(f)
            proxy_list = [f"{item['ip']}:{item['port']}" for item in json_data['data']]

        return proxy_list

    def _generate_proxy_pool(self):
        test_url = 'http://httpbin.org/ip'
        proxy_pool = []
        
        print("开始刷新代理池...")
        for proxy in self.proxy_list:
            try:
                response = requests.get(test_url, proxies={
                    'http': f'http://{proxy}',
                    'https': f'http://{proxy}'}, 
                    timeout=3
                )
                if response.status_code == 200:
                    proxy_pool.append(proxy)
            except Exception as e:
                continue
                
        print(f"验证完成，有效代理数：{len(proxy_pool)}/{len(self.proxy_list)}")
        return proxy_pool

    def get_random_proxy(self):
        """从代理池中返回随机代理"""
        if not self.proxy_pool:  # 代理池中没有有效代理的话，刷新代理池
            self._generate_proxy_pool()
        return random.choice(self.proxy_pool) if self.proxy_pool else None

# if __name__ == '__main__':
#     proxy_pool = ProxyPool('proxy_list.json')
#     print("随机有效代理:", proxy_pool.get_random_proxy())