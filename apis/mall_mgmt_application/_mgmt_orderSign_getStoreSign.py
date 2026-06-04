import os

from util.client import client

params = {
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_orderSign_getStoreSign(params=params, headers=headers):
    """
    批量发送结点信息功能-查询服务中心数据,签约单数量
    /mgmt/orderSign/getStoreSign

    参数说明:
    - storeCode: 服务中心编号
    """

    url = "/mgmt/orderSign/getStoreSign"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
