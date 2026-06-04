import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_contract_getYangzhouServiceFeeSettingInfo(headers=headers):
    """
    获取服务费申请扬州公司签署人信息
    /mgmt/store/contract/getYangzhouServiceFeeSettingInfo
    """

    url = "/mgmt/store/contract/getYangzhouServiceFeeSettingInfo"
    with client.get(url=url, headers=headers) as r:
        return r
