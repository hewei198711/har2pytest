import os

from util.client import client

data = {
    "accountName": "",  # 账户名称
    "accountNo": "",  # 签约银行账号
    "contractStatus": 0,  # 签约状态 1已签约 2已解约
    "credentialNo": "",  # 证件号码
    "credentialType": 0,  # 证件类型 1身份证 2其他
    "expireTime": "",  # 签约截止时间 yyyyMMdd
    "identificNo": "",  # 客户标识号/客户编号
    "openBank": 0,  # 开户银行 1中国工商银行ICBC 2中国建设银行CBC
    "phone": "",  # 手机号
    "remark": "",  # 备注
    "resource": 0,  # TODO: 添加参数说明
    "singleQuota": 0.0,  # 代收单笔限额
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_storeContractBankCard_updateOrSave(data=data, headers=headers):
    """
    编辑/新增
    /mgmt/store/storeContractBankCard/updateOrSave

    参数说明:
    - accountName: 账户名称
    - accountNo: 签约银行账号
    - contractStatus: 签约状态 1已签约 2已解约
    - credentialNo: 证件号码
    - credentialType: 证件类型 1身份证 2其他
    - expireTime: 签约截止时间 yyyyMMdd
    - identificNo: 客户标识号/客户编号
    - openBank: 开户银行 1中国工商银行ICBC 2中国建设银行CBC
    - phone: 手机号
    - remark: 备注
    - singleQuota: 代收单笔限额
    """

    url = "/mgmt/store/storeContractBankCard/updateOrSave"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
