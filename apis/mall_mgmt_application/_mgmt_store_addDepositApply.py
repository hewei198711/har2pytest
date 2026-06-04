import os

from util.client import client

data = {
    "depositType": 0,  # 保证金类型 1开店保证金 2超额保证金
    "id": 0,  # 主键ID
    "money": 0.0,  # 保证金额
    "payAccount": "",  # 付款账户
    "payBankName": "",  # 付款银行名称
    "payType": 0,  # 转账类型 1 委托扣款; 2 银行收款; 3 手工退款; 4 无法识别款
    "storeCode": "",  # 店铺编号
    "submitRemark": "",  # 提交备注
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_addDepositApply(data=data, headers=headers):
    """
    保证金添加/调整申请
    /mgmt/store/addDepositApply

    参数说明:
    - depositType: 保证金类型 1开店保证金 2超额保证金
    - id: 主键ID
    - money: 保证金额
    - payAccount: 付款账户
    - payBankName: 付款银行名称
    - payType: 转账类型 1 委托扣款; 2 银行收款; 3 手工退款; 4 无法识别款
    - storeCode: 店铺编号
    - submitRemark: 提交备注
    """

    url = "/mgmt/store/addDepositApply"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
