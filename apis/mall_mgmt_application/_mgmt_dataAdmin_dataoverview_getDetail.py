import os

from util.client import client

params = {
    "queryDate": "",  # queryDate
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_dataoverview_getDetail(params=params, headers=headers):
    """
    根据日期查询数据概览详情
    /mgmt/dataAdmin/dataoverview/getDetail

    参数说明:
    - queryDate: queryDate
    """

    url = "/mgmt/dataAdmin/dataoverview/getDetail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
