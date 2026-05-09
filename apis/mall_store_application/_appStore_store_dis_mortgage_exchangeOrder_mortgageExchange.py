import os

from util.client import client

data = {
    "exchangeType": 0,  # 换货类型 1先退后换 2秒换 3只换不退 4先换后退
    "files": [],  # 换货单附件，支持3个
    "productList": [],  # TODO: 添加参数说明
    "reasonFirst": "",  # 一级原因
    "reasonFirstId": 0,  # 一级原因id
    "reasonFirstRemark": "",  # 一级原因备注
    "reasonSecond": "",  # 二级原因
    "reasonSecondId": 0,  # 二级原因id
    "reasonSecondRemark": "",  # 二级原因备注
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_dis_mortgage_exchangeOrder_mortgageExchange(data=data, headers=headers):
    """
    押货换货下单
    /appStore/store/dis/mortgage/exchangeOrder/mortgageExchange

    参数说明:
    - exchangeType: 换货类型 1先退后换 2秒换 3只换不退 4先换后退
    - files: 换货单附件，支持3个
    - reasonFirst: 一级原因
    - reasonFirstId: 一级原因id
    - reasonFirstRemark: 一级原因备注
    - reasonSecond: 二级原因
    - reasonSecondId: 二级原因id
    - reasonSecondRemark: 二级原因备注
    - storeCode: 服务中心编号
    """

    url = "/appStore/store/dis/mortgage/exchangeOrder/mortgageExchange"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
