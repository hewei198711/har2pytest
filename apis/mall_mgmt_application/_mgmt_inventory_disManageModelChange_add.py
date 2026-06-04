import os

from util.client import client

data = {
    "applyFiles": [],  # 申请表文件
    "applyType": 0,  # 提交方式 1门店提交 2后台提交
    "companyCode": "",  # 分公司code
    "companyName": "",  # 分公司名称
    "discountLevel": 0,  # 折扣系数等级  1-65%,2-70%,3-75%,4-85%
    "id": 0,  # 主键id
    "leaderName": "",  # 负责人姓名
    "leaderNo": "",  # 负责人卡号
    "settleAccount": 0,  # 结清账务 0未结清 1已结清
    "shopType": 0,  # 网点类型
    "storeCode": "",  # 服务中心编号
    "storeName": "",  # 服务中心名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_disManageModelChange_add(data=data, headers=headers):
    """
    新增
    /mgmt/inventory/disManageModelChange/add

    参数说明:
    - applyFiles: 申请表文件
    - applyType: 提交方式 1门店提交 2后台提交
    - companyCode: 分公司code
    - companyName: 分公司名称
    - discountLevel: 折扣系数等级  1-65%,2-70%,3-75%,4-85%
    - id: 主键id
    - leaderName: 负责人姓名
    - leaderNo: 负责人卡号
    - settleAccount: 结清账务 0未结清 1已结清
    - shopType: 网点类型
    - storeCode: 服务中心编号
    - storeName: 服务中心名称
    """

    url = "/mgmt/inventory/disManageModelChange/add"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
