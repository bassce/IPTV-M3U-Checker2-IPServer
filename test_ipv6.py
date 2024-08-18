import requests

# 测试的 IPv6 URL
url = "http://[2409:8087:1a01:df::4077]:80/ottrrs.hl.chinamobile.com/PLTV/88888888/224/3221226010/index.m3u8"

try:
    # 发起GET请求
    response = requests.get(url, timeout=10)

    # 检查响应状态码
    if response.status_code == 200:
        print("请求成功！")
        print("响应内容：")
        print(response.text)  # 或者 response.content 对于二进制内容
    else:
        print(f"请求失败，状态码：{response.status_code}")

except requests.exceptions.RequestException as e:
    print(f"请求出现错误：{e}")
