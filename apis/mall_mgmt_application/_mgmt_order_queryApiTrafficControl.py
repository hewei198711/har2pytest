import os

from util.client import client

params = {
    "cityCode": "",  # 市编码
    "districtCode": "",  # 区县编码
    "provinceCode": "",  # 省编码
    "streetCode": "",  # 街道编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_queryApiTrafficControl(params=params, headers=headers):
    """
    查询交通管制
    /mgmt/order/queryApiTrafficControl

    参数说明:
    - cityCode: 市编码
    - districtCode: 区县编码
    - provinceCode: 省编码
    - streetCode: 街道编码
    """

    url = "/mgmt/order/queryApiTrafficControl"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
