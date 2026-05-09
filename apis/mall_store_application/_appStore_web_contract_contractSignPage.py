import os

from util.client import client

params = {
    "docNo": "",  # 合同编号
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_web_contract_contractSignPage(params=params, headers=headers):
    """
    手动签署页面
    /appStore/web/contract/contractSignPage

    参数说明:
    - docNo: 合同编号
    - storeCode: 服务中心编号
    """

    url = "/appStore/web/contract/contractSignPage"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
