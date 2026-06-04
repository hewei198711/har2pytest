import os

from util.client import client

data = {
    "companyCode": "",  # 分公司code
    "currentDiscountLevel": [],  # 当前折扣系数等级  1-65%,2-70%,3-75%,4-85%
    "leaderName": "",  # 负责人姓名
    "leaderNo": "",  # 负责人卡号
    "moneyType": 0,  # 可用结余为负  0->是  1 ->否
    "month": 0,  # TODO: 添加参数说明
    "pageNum": 0,  # 第几页
    "pageSize": 0,  # 每页显示页数
    "searchIsAll": False,  # 是否查询全部 标识 true 是   其他 否
    "storeCode": "",  # 服务中心编号
    "storeCodes": [],  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_deposit_pageList(data=data, headers=headers):
    """
    85折账款管理 -- 押货保证金分页查询列表
    /mgmt/inventory/deposit/pageList

    参数说明:
    - companyCode: 分公司code
    - currentDiscountLevel: 当前折扣系数等级  1-65%,2-70%,3-75%,4-85%
    - leaderName: 负责人姓名
    - leaderNo: 负责人卡号
    - moneyType: 可用结余为负  0->是  1 ->否
    - pageNum: 第几页
    - pageSize: 每页显示页数
    - searchIsAll: 是否查询全部 标识 true 是   其他 否
    - storeCode: 服务中心编号
    """

    url = "/mgmt/inventory/deposit/pageList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
