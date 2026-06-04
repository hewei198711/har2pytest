import os

from util.client import client

data = {
    "approveEndTime": "",  # 审核开始时间  yyyy-MM-dd
    "approveStartTime": "",  # 审核开始时间  yyyy-MM-dd
    "companyCode": [],  # 分公司code
    "controlType": 0,  # 控制类型 1顾客自购单退货 2云商下单退货
    "createEndTime": "",  # 创建结束时间  yyyy-MM-dd
    "createStartTime": "",  # 创建开始时间  yyyy-MM-dd
    "endReturnRatio": 0.0,  # 退货比例结束值(0.00-1.00)
    "isOver": 0,  # 是否超额  0  否 1 是
    "leaderNo": "",  # 负责人卡号
    "pageNum": 0,  # 第几页
    "pageSize": 0,  # 每页显示页数
    "startReturnRatio": 0.0,  # 退货比例起始值(0.00-1.00)
    "state": 0,  # 记录状态 0:失效 1:生效
    "storeCode": "",  # 服务中心编号
    "verifyStatus": 0,  # 审核状态 1审核通过 2审核不通过 3待审核
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_return_config_pageList(data=data, headers=headers):
    """
    退货额度分页搜索列表
    /mgmt/inventory/return/config/pageList

    参数说明:
    - approveEndTime: 审核开始时间  yyyy-MM-dd
    - approveStartTime: 审核开始时间  yyyy-MM-dd
    - companyCode: 分公司code
    - controlType: 控制类型 1顾客自购单退货 2云商下单退货
    - createEndTime: 创建结束时间  yyyy-MM-dd
    - createStartTime: 创建开始时间  yyyy-MM-dd
    - endReturnRatio: 退货比例结束值(0.00-1.00)
    - isOver: 是否超额  0  否 1 是
    - leaderNo: 负责人卡号
    - pageNum: 第几页
    - pageSize: 每页显示页数
    - startReturnRatio: 退货比例起始值(0.00-1.00)
    - state: 记录状态 0:失效 1:生效
    - storeCode: 服务中心编号
    - verifyStatus: 审核状态 1审核通过 2审核不通过 3待审核
    """

    url = "/mgmt/inventory/return/config/pageList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
