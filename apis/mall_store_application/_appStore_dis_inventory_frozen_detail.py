import os

from util.client import client

params = {
    "bizNo": "",  # 来源的 业务编号
    "createBegin": "",  # 出/入库开始时间
    "createEnd": "",  # 出/入库结束时间
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "type": 0,  # 类型：1冻结 2解冻
    "产品编码": "",  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_dis_inventory_frozen_detail(params=params, headers=headers):
    """
    库存冻结明细
    /appStore/dis-inventory/frozen-detail

    参数说明:
    - bizNo: 来源的 业务编号
    - createBegin: 出/入库开始时间
    - createEnd: 出/入库结束时间
    - pageNum: 页数
    - pageSize: 页大小
    - type: 类型：1冻结 2解冻
    """

    url = "/appStore/dis-inventory/frozen-detail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
