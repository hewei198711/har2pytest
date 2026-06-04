import os

from util.client import client

params = {
    "auditEndTime": "",  # 审批结束时间 yyyy-MM-dd
    "auditStartTime": "",  # 审批开始时间 yyyy-MM-dd
    "bizMode": 0,  # 经营模式 1->1:3押货 2->85折押货
    "companyCode": "",  # 分公司编号
    "companyCodes": [],  # 分公司编号列表
    "endTime": "",  # 结束时间 yyyy-MM-dd
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "startTime": "",  # 开始时间 yyyy-MM-dd
    "status": 0,  # 状态 1待审核 2审核通过 3已驳回 4已取消
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_dis_mortgage_order_apply_page(params=params, headers=headers):
    """
    分页查询
    /mgmt/inventory/dis/mortgage/order/apply/page

    参数说明:
    - auditEndTime: 审批结束时间 yyyy-MM-dd
    - auditStartTime: 审批开始时间 yyyy-MM-dd
    - bizMode: 经营模式 1->1:3押货 2->85折押货
    - companyCode: 分公司编号
    - companyCodes: 分公司编号列表
    - endTime: 结束时间 yyyy-MM-dd
    - pageNum: 页数
    - pageSize: 页大小
    - startTime: 开始时间 yyyy-MM-dd
    - status: 状态 1待审核 2审核通过 3已驳回 4已取消
    - storeCode: 服务中心编号
    """

    url = "/mgmt/inventory/dis/mortgage/order/apply/page"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
