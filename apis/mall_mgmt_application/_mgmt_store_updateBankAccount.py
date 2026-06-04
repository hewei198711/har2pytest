import os

from util.client import client

data = {
    "account": "",  # 账号
    "accountBank": "",  # 开户银行
    "accountName": "",  # 账户名称
    "accountType": 0,  # 账户性质 1一般帐户 2专用帐户 3临时账户 4基本账户
    "branch": "",  # 开户支行
    "cityName": "",  # 市名称
    "id": 0,  # TODO: 添加参数说明
    "isDeduction": 0,  # 是否扣款账户 1是 2否
    "isUsed": 0,  # 作废标示 1生效 2作废
    "permissionUrl": "",  # 开户许可证
    "provinceName": "",  # 省名称
    "storeCode": "",  # 服务中心编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_updateBankAccount(data=data, headers=headers):
    """
    更新银行账号
    /mgmt/store/updateBankAccount

    参数说明:
    - account: 账号
    - accountBank: 开户银行
    - accountName: 账户名称
    - accountType: 账户性质 1一般帐户 2专用帐户 3临时账户 4基本账户
    - branch: 开户支行
    - cityName: 市名称
    - isDeduction: 是否扣款账户 1是 2否
    - isUsed: 作废标示 1生效 2作废
    - permissionUrl: 开户许可证
    - provinceName: 省名称
    - storeCode: 服务中心编号
    """

    url = "/mgmt/store/updateBankAccount"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
