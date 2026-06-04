import os

from util.client import client

data = {
    "adjustMonth": "",  # 录入月份
    "adjustNo": "",  # 调整单号
    "adjustStatus": 0,  # 审批状态：1：待审核；2：已通过；3：已驳回，6：已撤回
    "cardNo": "",  # 会员卡号
    "companyCode": "",  # 分公司编号
    "from": 0,  # TODO: 添加参数说明
    "memberId": 0,  # 顾客编号
    "mobile": "",  # 普通过客手机号
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_getAdjustList(data=data, headers=headers):
    """
    手工录入款项审核-列表
    /mgmt/fin/wallet/getAdjustList

    参数说明:
    - adjustMonth: 录入月份
    - adjustNo: 调整单号
    - adjustStatus: 审批状态：1：待审核；2：已通过；3：已驳回，6：已撤回
    - cardNo: 会员卡号
    - companyCode: 分公司编号
    - memberId: 顾客编号
    - mobile: 普通过客手机号
    - pageNum: 页数
    - pageSize: 每页显示数
    """

    url = "/mgmt/fin/wallet/getAdjustList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
