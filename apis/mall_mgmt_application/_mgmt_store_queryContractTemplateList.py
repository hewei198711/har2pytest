import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_queryContractTemplateList(headers=headers):
    """
    合同模板下拉列表
    /mgmt/store/queryContractTemplateList
    """

    url = "/mgmt/store/queryContractTemplateList"
    with client.get(url=url, headers=headers) as r:
        return r
