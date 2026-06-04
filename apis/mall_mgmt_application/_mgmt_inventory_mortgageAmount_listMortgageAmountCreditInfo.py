import os

from util.client import client

params = {
    "endDay": "",  # 到期日期(结束)  格式yyyy-MM-dd
    "endTime": "",  # 审核时间 结束时间 yyyy-MM-dd
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "startDay": "",  # 到期日期(开始)  格式yyyy-MM-dd
    "startTime": "",  # 审核时间 开始时间 yyyy-MM—dd
    "storeCode": "",  # 服务中心编号
    "verifyStatus": 0,  # 审核状态
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_inventory_mortgageAmount_listMortgageAmountCreditInfo(params=params, headers=headers):
    """
    信誉额详情
    /mgmt/inventory/mortgageAmount/listMortgageAmountCreditInfo

    参数说明:
    - endDay: 到期日期(结束)  格式yyyy-MM-dd
    - endTime: 审核时间 结束时间 yyyy-MM-dd
    - pageNum: 页数
    - pageSize: 页大小
    - startDay: 到期日期(开始)  格式yyyy-MM-dd
    - startTime: 审核时间 开始时间 yyyy-MM—dd
    - storeCode: 服务中心编号
    - verifyStatus: 审核状态
    """

    url = "/mgmt/inventory/mortgageAmount/listMortgageAmountCreditInfo"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
