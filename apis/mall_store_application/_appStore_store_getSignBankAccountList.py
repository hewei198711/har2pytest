from util.client import client

headers = {"channel": "pc", "client": "store", "authorization": "请输入认证令牌"}


def _appStore_store_getSignBankAccountList(headers=headers):
    """
    获取签约银行列表
    /appStore/store/getSignBankAccountList

    参数说明:
    - isSigned: 是否已签约，1/是，2/否
    """

    url = "/appStore/store/getSignBankAccountList"
    with client.get(url=url, headers=headers) as r:
        return r
