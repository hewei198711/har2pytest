import os

from util.client import client

params = {
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
    "storeCode": "",  # storeCode
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_distribution_listDistributionInfo(params=params, headers=headers):
    """
    查询分配量详情
    /mgmt/inventory/distribution/listDistributionInfo

    参数说明:
    - pageNum: pageNum
    - pageSize: pageSize
    - storeCode: storeCode
    """

    url = "/mgmt/inventory/distribution/listDistributionInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
