import os

from util.client import client

params = {
    "parentReasonId": "",  # 配置时间
    "returnType": "",  # 退换货类型
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_getReturnReasons(params=params, headers=headers):
    """
    查找退换货原因
    /mgmt/sys/getReturnReasons

    参数说明:
    - parentReasonId: 配置时间
    - returnType: 退换货类型
    """

    url = "/mgmt/sys/getReturnReasons"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
