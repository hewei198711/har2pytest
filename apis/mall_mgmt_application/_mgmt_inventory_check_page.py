import os

from util.client import client

params = {
    "beginFinishCheckTime": "",  # 开始完成盘点时间
    "beginReadyCheckTime": "",  # 开始马上盘点时间
    "bizMode": 0,  # 经营模式 1->1:3, 2->多折扣
    "companyCodes": [],  # 分公司编号
    "endFinishCheckTime": "",  # 结束完成盘点时间
    "endReadyCheckTime": "",  # 结束马上盘点时间
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "quarter": 0,  # 季度
    "storeCode": "",  # 门店编号
    "year": 0,  # 年份
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_check_page(params=params, headers=headers):
    """
    列表查询
    /mgmt/inventory/check/page

    参数说明:
    - beginFinishCheckTime: 开始完成盘点时间
    - beginReadyCheckTime: 开始马上盘点时间
    - bizMode: 经营模式 1->1:3, 2->多折扣
    - companyCodes: 分公司编号
    - endFinishCheckTime: 结束完成盘点时间
    - endReadyCheckTime: 结束马上盘点时间
    - pageNum: 页数
    - pageSize: 页大小
    - quarter: 季度
    - storeCode: 门店编号
    - year: 年份
    """

    url = "/mgmt/inventory/check/page"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
