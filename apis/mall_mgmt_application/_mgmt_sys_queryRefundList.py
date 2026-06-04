import os

from util.client import client

params = {
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_queryRefundList(params=params, headers=headers):
    """
    查询退款阈值修改记录
    /mgmt/sys/queryRefundList

    参数说明:
    - pageNum: pageNum
    - pageSize: pageSize
    """

    url = "/mgmt/sys/queryRefundList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
