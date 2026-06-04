import os

from util.client import client

params = {
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_product_quota_getDetail(params=params, headers=headers):
    """
    查询服务中心分配详情
    /mgmt/product/quota/getDetail

    参数说明:
    - pageNum: pageNum
    - pageSize: pageSize
    - storeCode: 服务中心编号
    """

    url = "/mgmt/product/quota/getDetail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
