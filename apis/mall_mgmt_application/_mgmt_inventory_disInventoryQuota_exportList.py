import os

from util.client import client

params = {
    "auditEndDate": "",  # 审核时间结束 yyyy-MM-dd
    "auditStartDate": "",  # 审核时间开始 yyyy-MM-dd
    "auditStatus": 0,  # 状态 1审核通过  2审核不通过 3待审核
    "auditType": 0,  # 审核类型 1新增/编辑审核 2删除审核
    "companyCode": [],  # 分公司code
    "createEndDate": "",  # 创建时间结束 yyyy-MM-dd
    "createStartDate": "",  # 创建时间开始 yyyy-MM-dd
    "leaderNo": "",  # 负责人卡号
    "pageNum": 0,  # 当前页,默认第1页
    "pageSize": 0,  # 每页显示数,默认10条
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_disInventoryQuota_exportList(params=params, headers=headers):
    """
    批量导出列表
    /mgmt/inventory/disInventoryQuota/exportList

    参数说明:
    - auditEndDate: 审核时间结束 yyyy-MM-dd
    - auditStartDate: 审核时间开始 yyyy-MM-dd
    - auditStatus: 状态 1审核通过  2审核不通过 3待审核
    - auditType: 审核类型 1新增/编辑审核 2删除审核
    - companyCode: 分公司code
    - createEndDate: 创建时间结束 yyyy-MM-dd
    - createStartDate: 创建时间开始 yyyy-MM-dd
    - leaderNo: 负责人卡号
    - pageNum: 当前页,默认第1页
    - pageSize: 每页显示数,默认10条
    - storeCode: 服务中心编号
    """

    url = "/mgmt/inventory/disInventoryQuota/exportList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
