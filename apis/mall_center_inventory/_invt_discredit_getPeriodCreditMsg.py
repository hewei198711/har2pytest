from util.client import client

params = {
    "storeCode": "914008",  # storeCode
}

headers = {"channel": "pc", "client": "store", "authorization": "请输入认证令牌"}


def _invt_discredit_getPeriodCreditMsg(params=params, headers=headers):
    """
    获取进行中的分期信用额设置
    /invt/discredit/getPeriodCreditMsg

    参数说明:
    - storeCode: storeCode
    """

    url = "/invt/discredit/getPeriodCreditMsg"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
