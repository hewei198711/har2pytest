import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_downloadContractExcelTemplate(headers=headers):
    """
    服务中心批量合同excel模板下载
    /mgmt/store/downloadContractExcelTemplate
    """

    url = "/mgmt/store/downloadContractExcelTemplate"
    with client.get(url=url, headers=headers) as r:
        return r
