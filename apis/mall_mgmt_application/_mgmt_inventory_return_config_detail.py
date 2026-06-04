import os

from util.client import client

params = {
    "controlType": 0,  # 控制类型 1顾客自购单退货 2云商下单退货
    "endReturnRatio": 0.0,  # 退货比例结束值(0.00-1.00)
    "overEndTime": "",  # 超额结束时间  yyyy-MM-dd
    "overStartTime": "",  # 超额开始时间  yyyy-MM-dd
    "pageNum": 0,  # 第几页
    "pageSize": 0,  # 每页显示页数
    "returnAmountEnd": 0.0,  # 押货余额极限值结束值
    "returnAmountStart": 0.0,  # 押货余额极限值开始值
    "startReturnRatio": 0.0,  # 退货比例起始值(0.00-1.00)
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_return_config_detail(params=params, headers=headers):
    """
    配置额度详情/超额记录
    /mgmt/inventory/return/config/detail

    参数说明:
    - controlType: 控制类型 1顾客自购单退货 2云商下单退货
    - endReturnRatio: 退货比例结束值(0.00-1.00)
    - overEndTime: 超额结束时间  yyyy-MM-dd
    - overStartTime: 超额开始时间  yyyy-MM-dd
    - pageNum: 第几页
    - pageSize: 每页显示页数
    - returnAmountEnd: 押货余额极限值结束值
    - returnAmountStart: 押货余额极限值开始值
    - startReturnRatio: 退货比例起始值(0.00-1.00)
    - storeCode: 服务中心编号
    """

    url = "/mgmt/inventory/return/config/detail"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
