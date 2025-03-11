import requests
#记得修改登录密码和路由器登录地址
# 登录路由器的 URL
login_url = "http://192.168.0.1/" #修改登录ip

# 登录请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:135.0) Gecko/20100101 Firefox/135.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate",
    "Content-Type": "application/json; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": "http://192.168.0.1",#修改登录ip
    "Connection": "keep-alive",
    "Referer": "http://192.168.0.1/",#修改登录ip
    "Priority": "u=0",
}

# 登录请求体
login_data = {
    "method": "do",
    "login": {
        "password": "自己的登录密码浏览器f12登录一遍获取"  # 登录密码
    }
}

# 第一步：登录路由器，获取 stok
try:
    # 发送登录请求
    login_response = requests.post(login_url, headers=headers, json=login_data)
    login_response.raise_for_status()  # 检查请求是否成功
    # print("登录响应状态码:", login_response.status_code)

    # 解析登录响应
    login_json = login_response.json()
    # print("登录响应内容:", login_json)

    # 提取 stok
    stok = login_json.get("stok")
    if not stok:
        print("登录失败：未找到 stok")
        exit()

    # print("提取的 stok:", stok)

except requests.exceptions.RequestException as e:
    print("登录请求失败:", e)
    exit()

# 第二步：使用 stok 构造新的 URL，获取 ipv4 地址
# 构造新的 URL
ipv4_url = f"http://192.168.0.1/stok={stok}/ds" #修改登录ip

# 获取 ipv4 地址的请求体
ipv4_data = {
    "network": {
        "name": "wan_status"
    },
    "method": "get"
}

try:
    # 发送获取 ipv4 地址的请求
    ipv4_response = requests.post(ipv4_url, headers=headers, json=ipv4_data)
    ipv4_response.raise_for_status()  # 检查请求是否成功
    # print("获取 ipv4 地址响应状态码:", ipv4_response.status_code)

    # 解析获取 ipv4 地址的响应
    ipv4_json = ipv4_response.json()
    # print("获取 ipv4 地址响应内容:", ipv4_json)

    # 提取 ipv4 地址
    ipaddr = ipv4_json.get("network", {}).get("wan_status", {}).get("ipaddr")
    if ipaddr:
        print("提取的 ipv4 地址:", ipaddr)
    else:
        print("未找到 ipv4 地址")

except requests.exceptions.RequestException as e:
    print("获取 ipv4 地址请求失败:", e)