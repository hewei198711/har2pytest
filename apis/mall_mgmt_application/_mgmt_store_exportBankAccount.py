import os

from util.client import client

data = {
    "companyCode": "",  # 分公司编号
    "isSigned": 0,  # 是否已签约，1/是，2/否
    "isUsed": 0,  # 作废标示 1生效 2作废
    "leaderCardNo": "",  # 总店负责人卡号
    "opType": 0,  # 操作类型 1新增 2修改 3作废
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 页大小
    "storeCode": "",  # 服务中心编号
    "verifyStatus": 0,  # 审核状态 3待审核, 不选则是全部
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_exportBankAccount(data=data, headers=headers):
    """
    导出银行卡账号excel
    /mgmt/store/exportBankAccount

    参数说明:
    - companyCode: 分公司编号
    - isSigned: 是否已签约，1/是，2/否
    - isUsed: 作废标示 1生效 2作废
    - leaderCardNo: 总店负责人卡号
    - opType: 操作类型 1新增 2修改 3作废
    - pageNum: 页数
    - pageSize: 页大小
    - storeCode: 服务中心编号
    - verifyStatus: 审核状态 3待审核, 不选则是全部
    """

    url = "/mgmt/store/exportBankAccount"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
