import os

from util.client import client

params = {
    "applyEndDate": "",  # 提交时间结束 yyyy-MM-dd
    "applyStartDate": "",  # 提交时间开始 yyyy-MM-dd
    "applyType": 0,  # 提交方式 1门店提交 2后台提交
    "auditStatus": 0,  # 状态
    "companyCode": [],  # 分公司code
    "discountLevel": 0,  # 折扣系数等级  1-65%,2-70%,3-75%,4-85%
    "leaderName": "",  # 负责人姓名
    "leaderNo": "",  # 负责人卡号
    "pageNum": 0,  # 当前页,默认第1页
    "pageSize": 0,  # 每页显示数,默认10条
    "shopType": 0,  # 网点类型
    "storeCode": "",  # 服务中心编号
    "storeName": "",  # 服务中心名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_disManageModelChange_exportList(params=params, headers=headers):
    """
    导出搜索列表
    /mgmt/inventory/disManageModelChange/exportList

    参数说明:
    - applyEndDate: 提交时间结束 yyyy-MM-dd
    - applyStartDate: 提交时间开始 yyyy-MM-dd
    - applyType: 提交方式 1门店提交 2后台提交
    - auditStatus: 状态
    - companyCode: 分公司code
    - discountLevel: 折扣系数等级  1-65%,2-70%,3-75%,4-85%
    - leaderName: 负责人姓名
    - leaderNo: 负责人卡号
    - pageNum: 当前页,默认第1页
    - pageSize: 每页显示数,默认10条
    - shopType: 网点类型
    - storeCode: 服务中心编号
    - storeName: 服务中心名称
    """

    url = "/mgmt/inventory/disManageModelChange/exportList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
