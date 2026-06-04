import os

from util.client import client

params = {
    "id": "",  # 记录主键id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_getMemberCustomerLogInfo(params=params, headers=headers):
    """
    获取自定义顾客修改详情
    /mgmt/prmt/getMemberCustomerLogInfo

    参数说明:
    - id: 记录主键id
    """

    url = "/mgmt/prmt/getMemberCustomerLogInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
