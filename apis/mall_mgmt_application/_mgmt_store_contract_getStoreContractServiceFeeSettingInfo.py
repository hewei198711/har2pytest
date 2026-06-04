import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_contract_getStoreContractServiceFeeSettingInfo(headers=headers):
    """
    获取服务费申请公司签署人信息
    /mgmt/store/contract/getStoreContractServiceFeeSettingInfo
    """

    url = "/mgmt/store/contract/getStoreContractServiceFeeSettingInfo"
    with client.get(url=url, headers=headers) as r:
        return r
