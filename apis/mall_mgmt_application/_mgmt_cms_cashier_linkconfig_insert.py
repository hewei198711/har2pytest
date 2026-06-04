import os

from util.client import client

data = {
    "cashierAppid": "",  # 小程序的原始id
    "cashierPageUrl": "",  # 落地页链接地址
    "cashierTitle": "",  # 收银台链接配置标题
    "disclaimer": "",  # 免责声明
    "id": 0,  # 收银台链接id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_cashier_linkconfig_insert(data=data, headers=headers):
    """
    收银台链接配置保存信息
    /mgmt/cms/cashier/linkconfig/insert

    参数说明:
    - cashierAppid: 小程序的原始id
    - cashierPageUrl: 落地页链接地址
    - cashierTitle: 收银台链接配置标题
    - disclaimer: 免责声明
    - id: 收银台链接id
    """

    url = "/mgmt/cms/cashier/linkconfig/insert"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
