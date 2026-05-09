import os

from util.client import client

data = {
    "account": "",  # 账号
    "accountBank": "",  # 开户银行
    "accountName": "",  # 账户名称
    "accountType": 0,  # 账户性质 1一般帐户 2专用帐户 3临时账户 4基本账户
    "bankAccountId": 0,  # 银行账户ID
    "branch": "",  # 开户支行
    "cityName": "",  # 市名称
    "isDeduction": 0,  # 是否扣款账户 1是 2否
    "opType": 0,  # 操作类型, 1/新增, 2/修改, 3/删除
    "permissionUrl": "",  # 开户许可证
    "provinceName": "",  # 省名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_profile_applyBankAccountChange(data=data, headers=headers):
    """
    申请服务中心银行账号变更
    /appStore/store/profile/applyBankAccountChange

    参数说明:
    - account: 账号
    - accountBank: 开户银行
    - accountName: 账户名称
    - accountType: 账户性质 1一般帐户 2专用帐户 3临时账户 4基本账户
    - bankAccountId: 银行账户ID
    - branch: 开户支行
    - cityName: 市名称
    - isDeduction: 是否扣款账户 1是 2否
    - opType: 操作类型, 1/新增, 2/修改, 3/删除
    - permissionUrl: 开户许可证
    - provinceName: 省名称
    """

    url = "/appStore/store/profile/applyBankAccountChange"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
