import os

from util.client import client

params = {
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_queryStoreContractRelation(params=params, headers=headers):
    """
    根据服务中心编号查询服务中心合同对接关联信息
    /mgmt/store/queryStoreContractRelation

    参数说明:
    - storeCode: 服务中心编号
    """

    url = "/mgmt/store/queryStoreContractRelation"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
