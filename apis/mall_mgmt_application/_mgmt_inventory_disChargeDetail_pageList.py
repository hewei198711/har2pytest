import os

from util.client import client

data = {
    "companyCode": [],  # 分公司code
    "month": 0,  # 所属月份 yyyyMM
    "pageNum": 0,  # 当前页,默认第1页
    "pageSize": 0,  # 每页显示数,默认10条
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_disChargeDetail_pageList(data=data, headers=headers):
    """
    分页列表
    /mgmt/inventory/disChargeDetail/pageList

    参数说明:
    - companyCode: 分公司code
    - month: 所属月份 yyyyMM
    - pageNum: 当前页,默认第1页
    - pageSize: 每页显示数,默认10条
    - storeCode: 服务中心编号
    """

    url = "/mgmt/inventory/disChargeDetail/pageList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
