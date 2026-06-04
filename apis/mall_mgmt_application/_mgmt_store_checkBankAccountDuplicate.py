import os

from util.client import client

params = {
    "account": "",  # 银行账户
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_checkBankAccountDuplicate(params=params, headers=headers):
    """
    检测是否有银行账号重复,重复则返回服务中心编号
    /mgmt/store/checkBankAccountDuplicate

    参数说明:
    - account: 银行账户
    """

    url = "/mgmt/store/checkBankAccountDuplicate"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
