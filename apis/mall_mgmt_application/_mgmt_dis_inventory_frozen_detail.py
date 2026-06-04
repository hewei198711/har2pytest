import os

from util.client import client

params = {
    "beginMonth": 0,  # 月份，格式为：yyyyMM
    "endMonth": 0,  # 月份，格式为：yyyyMM
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "productCode": "",  # 产品编号
    "storeCode": "",  # 服务中心编号
    "type": 0,  # 类型：1冻结 2解冻
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dis_inventory_frozen_detail(params=params, headers=headers):
    """
    查询库存冻结明细
    /mgmt/dis-inventory/frozen-detail

    参数说明:
    - beginMonth: 月份，格式为：yyyyMM
    - endMonth: 月份，格式为：yyyyMM
    - pageNum: 页数
    - pageSize: 页大小
    - productCode: 产品编号
    - storeCode: 服务中心编号
    - type: 类型：1冻结 2解冻
    """

    url = "/mgmt/dis-inventory/frozen-detail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
