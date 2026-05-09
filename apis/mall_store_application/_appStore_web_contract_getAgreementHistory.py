import os

from util.client import client

params = {
    "customerNos": "",  # 客户编码（服务中心/服务公司编码）编码多个用英文逗号分隔(前端不用传)
    "isSigned": 0,  # 是否已签署，1/已签署,2/未签署
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页页数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_web_contract_getAgreementHistory(params=params, headers=headers):
    """
    获取签署协议历史记录
    /appStore/web/contract/getAgreementHistory

    参数说明:
    - customerNos: 客户编码（服务中心/服务公司编码）编码多个用英文逗号分隔(前端不用传)
    - isSigned: 是否已签署，1/已签署,2/未签署
    - pageNum: 页码
    - pageSize: 每页页数
    """

    url = "/appStore/web/contract/getAgreementHistory"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
