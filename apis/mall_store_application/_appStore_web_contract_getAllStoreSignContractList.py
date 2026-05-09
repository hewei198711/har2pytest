import os

from util.client import client

params = {
    "signTypes": [],  # 对账单签署类型，1/1:3库存对账单，2/85%库存对账单，3/85%账款对账单
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_web_contract_getAllStoreSignContractList(params=params, headers=headers):
    """
    获取待店铺签署的所有电子合同
    /appStore/web/contract/getAllStoreSignContractList

    参数说明:
    - signTypes: 对账单签署类型，1/1:3库存对账单，2/85%库存对账单，3/85%账款对账单
    - storeCode: 服务中心编号
    """

    url = "/appStore/web/contract/getAllStoreSignContractList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
