import os

from util.client import client

data = {
    "cardNo": "",  # 会员卡号
    "creditAdjustBatchId": 0,  # 信用额调整批次ID
    "creditDiffOption": 0,  # 信用额差值，1：等于0；2：其他
    "from": 0,  # TODO: 添加参数说明
    "instalment": 0,  # 是否分期还款
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_fin_wallet_credit_exportAdjustBatchDetail(data=data, headers=headers):
    """
    信用额调整批次详情-导出
    /mgmt/fin/wallet/credit/exportAdjustBatchDetail

    参数说明:
    - cardNo: 会员卡号
    - creditAdjustBatchId: 信用额调整批次ID
    - creditDiffOption: 信用额差值，1：等于0；2：其他
    - instalment: 是否分期还款
    - pageNum: 页数
    - pageSize: 每页显示数
    """

    url = "/mgmt/fin/wallet/credit/exportAdjustBatchDetail"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
