import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_web_contract_queryContractTemplateList(headers=headers):
    """
    合同模板下拉列表
    /appStore/web/contract/queryContractTemplateList
    """

    url = "/appStore/web/contract/queryContractTemplateList"
    with client.get(url=url, headers=headers) as r:
        return r
