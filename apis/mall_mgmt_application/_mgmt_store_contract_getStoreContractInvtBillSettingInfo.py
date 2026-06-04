import os

from util.client import client

params = {
    "signType": 0,  # signType
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_contract_getStoreContractInvtBillSettingInfo(params=params, headers=headers):
    """
    获取公司签署人信息
    /mgmt/store/contract/getStoreContractInvtBillSettingInfo

    参数说明:
    - signType: signType
    """

    url = "/mgmt/store/contract/getStoreContractInvtBillSettingInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
