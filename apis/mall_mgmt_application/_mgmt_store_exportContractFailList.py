import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_exportContractFailList(headers=headers):
    """
    服务中心批量合同导入失败记录导出
    /mgmt/store/exportContractFailList
    """

    url = "/mgmt/store/exportContractFailList"
    with client.get(url=url, headers=headers) as r:
        return r
