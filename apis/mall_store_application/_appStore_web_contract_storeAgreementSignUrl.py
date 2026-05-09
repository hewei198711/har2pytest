import os

from util.client import client

params = {
    "customerNo": "",  # 客户编号，服务中心编码/服务公司编码
    "partyAType": "",  # 签署单位，01000/完美（中国）有限公司，Y0000/扬州完美有限公司
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_web_contract_storeAgreementSignUrl(params=params, headers=headers):
    """
    获取协议签署链接
    /appStore/web/contract/storeAgreementSignUrl

    参数说明:
    - customerNo: 客户编号，服务中心编码/服务公司编码
    - partyAType: 签署单位，01000/完美（中国）有限公司，Y0000/扬州完美有限公司
    """

    url = "/appStore/web/contract/storeAgreementSignUrl"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
