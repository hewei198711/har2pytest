import os

from util.client import client

data = {
    "applyEndTime": "",  # 申请提现结束时间
    "applyStartTime": "",  # 申请提现开始时间
    "cardNo": "",  # 会员卡号
    "companyCode": "",  # 分公司编号
    "from": 0,  # TODO: 添加参数说明
    "mobile": "",  # 手机号码
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "realname": "",  # 顾客姓名
    "withdrawStatus": 0,  # 提现状态,0:全部，1：待审核；2：待受理；4：汇款成功；5：汇款失败；6：已撤销
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_getWithdrawList(data=data, headers=headers):
    """
    余额提现审批-列表
    /mgmt/fin/wallet/getWithdrawList

    参数说明:
    - applyEndTime: 申请提现结束时间
    - applyStartTime: 申请提现开始时间
    - cardNo: 会员卡号
    - companyCode: 分公司编号
    - mobile: 手机号码
    - pageNum: 页数
    - pageSize: 每页显示数
    - realname: 顾客姓名
    - withdrawStatus: 提现状态,0:全部，1：待审核；2：待受理；4：汇款成功；5：汇款失败；6：已撤销
    """

    url = "/mgmt/fin/wallet/getWithdrawList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
