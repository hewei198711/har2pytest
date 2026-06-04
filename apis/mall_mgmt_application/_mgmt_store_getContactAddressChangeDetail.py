import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_getContactAddressChangeDetail(params=params, headers=headers):
    """
    获取联系地址资料变更详情
    /mgmt/store/getContactAddressChangeDetail

    参数说明:
    - id: id
    """

    url = "/mgmt/store/getContactAddressChangeDetail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
