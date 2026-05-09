import os

from util.client import client

params = {
    "pageNum": 0,  # 页数
    "pageSize": 0,  # 每页显示数
    "signStatus": 0,  # 签署状态，1.未提交，2.待店铺签署，3.待公司签署，4.已完成，5.已撤销，11.待用户签署
    "templateName": "",  # 合同模板名称
    "templateNo": "",  # 合同模板编号
    "year": "",  # 年度
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_web_contract_querySubmitContractList(params=params, headers=headers):
    """
    合同列表
    /appStore/web/contract/querySubmitContractList

    参数说明:
    - pageNum: 页数
    - pageSize: 每页显示数
    - signStatus: 签署状态，1.未提交，2.待店铺签署，3.待公司签署，4.已完成，5.已撤销，11.待用户签署
    - templateName: 合同模板名称
    - templateNo: 合同模板编号
    - year: 年度
    """

    url = "/appStore/web/contract/querySubmitContractList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
