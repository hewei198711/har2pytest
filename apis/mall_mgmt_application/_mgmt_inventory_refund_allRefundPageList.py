import os

from util.client import client

data = {
    "applyEndTime": "",  # 申请结束时间  yyyy-MM-dd
    "applyStartTime": "",  # 申请开始时间  yyyy-MM-dd
    "companyCode": "",  # 分公司code
    "companyCodes": [],  # 分公司编号列表
    "pageNum": 0,  # 第几页
    "pageSize": 0,  # 页数
    "refundType": [],  # 款项类型
    "storeCenter": "",  # 服务中心
    "storeCode": "",  # 服务中心Code
    "verifyStatus": 0,  #  审核状态  0-> 待审核  1->审核通过  2->已驳回  3-> 已取消 4 -> 已退款
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_refund_allRefundPageList(data=data, headers=headers):
    """
    所有服务中心退款搜索分页列表
    /mgmt/inventory/refund/allRefundPageList

    参数说明:
    - applyEndTime: 申请结束时间  yyyy-MM-dd
    - applyStartTime: 申请开始时间  yyyy-MM-dd
    - companyCode: 分公司code
    - companyCodes: 分公司编号列表
    - pageNum: 第几页
    - pageSize: 页数
    - refundType: 款项类型
    - storeCenter: 服务中心
    - storeCode: 服务中心Code
    - verifyStatus:  审核状态  0-> 待审核  1->审核通过  2->已驳回  3-> 已取消 4 -> 已退款
    """

    url = "/mgmt/inventory/refund/allRefundPageList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
