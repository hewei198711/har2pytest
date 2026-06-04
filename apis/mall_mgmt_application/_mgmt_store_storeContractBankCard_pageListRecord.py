import os

from util.client import client

data = {
    "createEndDate": "",  # 操作时间结束 yyyy-MM-dd
    "createStartDate": "",  # 操作时间开始 yyyy-MM-dd
    "mainTableId": 0,  # 对公签约银行卡管理表id
    "operator": "",  # 操作人
    "operatorNo": "",  # 操作人工号
    "pageNum": 0,  # 当前页,默认第1页
    "pageSize": 0,  # 每页显示数,默认10条
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_storeContractBankCard_pageListRecord(data=data, headers=headers):
    """
    操作日志列表
    /mgmt/store/storeContractBankCard/pageListRecord

    参数说明:
    - createEndDate: 操作时间结束 yyyy-MM-dd
    - createStartDate: 操作时间开始 yyyy-MM-dd
    - mainTableId: 对公签约银行卡管理表id
    - operator: 操作人
    - operatorNo: 操作人工号
    - pageNum: 当前页,默认第1页
    - pageSize: 每页显示数,默认10条
    """

    url = "/mgmt/store/storeContractBankCard/pageListRecord"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
