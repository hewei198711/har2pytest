import os

from util.client import client

data = {
    "accountNo": "",  # 签约银行账号
    "companyCode": [],  # 分公司编号
    "contractStatus": 0,  # 签约状态 1已签约 2已解约
    "createEndDate": "",  # 生成日期结束 yyyy-MM-dd
    "createStartDate": "",  # 生成日期开始 yyyy-MM-dd
    "dataFrom": 0,  # 数据来源 1->运营后台 2->接口返回
    "identifyStatus": 0,  # 识别状态 1已识别 2已待识别 3拒绝通过
    "leaderNo": "",  # 负责人卡号
    "openBank": 0,  # 开户银行 1中国工商银行ICBC 2中国建设银行CBC
    "pageNum": 0,  # 当前页,默认第1页
    "pageSize": 0,  # 每页显示数,默认10条
    "phone": "",  # 手机号
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_storeContractBankCard_pageList(data=data, headers=headers):
    """
    分页列表
    /mgmt/store/storeContractBankCard/pageList

    参数说明:
    - accountNo: 签约银行账号
    - companyCode: 分公司编号
    - contractStatus: 签约状态 1已签约 2已解约
    - createEndDate: 生成日期结束 yyyy-MM-dd
    - createStartDate: 生成日期开始 yyyy-MM-dd
    - dataFrom: 数据来源 1->运营后台 2->接口返回
    - identifyStatus: 识别状态 1已识别 2已待识别 3拒绝通过
    - leaderNo: 负责人卡号
    - openBank: 开户银行 1中国工商银行ICBC 2中国建设银行CBC
    - pageNum: 当前页,默认第1页
    - pageSize: 每页显示数,默认10条
    - phone: 手机号
    - storeCode: 服务中心编号
    """

    url = "/mgmt/store/storeContractBankCard/pageList"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
