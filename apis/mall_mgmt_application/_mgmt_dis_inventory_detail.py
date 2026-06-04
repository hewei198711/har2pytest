import os

from util.client import client

params = {
    "beginMonth": 0,  # 月份，格式为：yyyyMM
    "bizType": 0,  # 业务类型：1押货 2押货退回 3交付数量 4交付退回 5库存调整
    "endMonth": 0,  # 月份，格式为：yyyyMM
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "productCode": "",  # 产品编号
    "storeCode": "",  # 服务中心编号
    "type": 0,  # 出入库：1入库 2出库
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dis_inventory_detail(params=params, headers=headers):
    """
    查询库存明细
    /mgmt/dis-inventory/detail

    参数说明:
    - beginMonth: 月份，格式为：yyyyMM
    - bizType: 业务类型：1押货 2押货退回 3交付数量 4交付退回 5库存调整
    - endMonth: 月份，格式为：yyyyMM
    - pageNum: 页数
    - pageSize: 页大小
    - productCode: 产品编号
    - storeCode: 服务中心编号
    - type: 出入库：1入库 2出库
    """

    url = "/mgmt/dis-inventory/detail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
