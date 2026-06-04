import os

from util.client import client

params = {
    "id": 0,  # 资料变更ID
    "storeCode": "",  # 服务中心编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_getProfileBankAccountChangeDetail(params=params, headers=headers):
    """
    获取服务中心银行账户信息变更详情
    /mgmt/store/getProfileBankAccountChangeDetail

    参数说明:
    - id: 资料变更ID
    - storeCode: 服务中心编码
    """

    url = "/mgmt/store/getProfileBankAccountChangeDetail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
