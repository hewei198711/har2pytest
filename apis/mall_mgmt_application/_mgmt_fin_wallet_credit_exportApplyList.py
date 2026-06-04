import os

from util.client import client

data = {
    "auditStatus": 0,  # 审核状态：1：待审核；2：已通过；9：不通过；7：待提交
    "cardNo": "",  # 会员卡号
    "companyCode": "",  # TODO: 添加参数说明
    "effectEndTime": "",  # 新增调整结束时间
    "effectStartTime": "",  # 新增调整开始时间
    "effectStatus": 0,  # 生效状态，1：未生效，2：已生效
    "from": 0,  # TODO: 添加参数说明
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_credit_exportApplyList(data=data, headers=headers):
    """
    导出信用额申请列表
    /mgmt/fin/wallet/credit/exportApplyList

    参数说明:
    - auditStatus: 审核状态：1：待审核；2：已通过；9：不通过；7：待提交
    - cardNo: 会员卡号
    - effectEndTime: 新增调整结束时间
    - effectStartTime: 新增调整开始时间
    - effectStatus: 生效状态，1：未生效，2：已生效
    - pageNum: 页数
    - pageSize: 每页显示数
    """

    url = "/mgmt/fin/wallet/credit/exportApplyList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
