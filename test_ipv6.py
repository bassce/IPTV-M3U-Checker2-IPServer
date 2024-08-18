import requests

def 获取IPv6地址():
    try:
        response = requests.get('https://v6.ip.zxinc.org/getip', timeout=10)
        if response.status_code == 200:
            ipv6_address = response.text.strip()
            return ipv6_address
        else:
            print(f"获取IPv6地址失败，状态码: {response.status_code}")
            return None
    except requests.RequestException as e:
        print(f"请求时发生错误: {e}")
        return None

if __name__ == "__main__":
    ipv6_address = 获取IPv6地址()
    if ipv6_address:
        print(f"您的IPv6地址是: {ipv6_address}")
    else:
        print("无法获取IPv6地址。")