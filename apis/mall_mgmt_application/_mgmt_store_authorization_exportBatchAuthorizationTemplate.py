import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_authorization_exportBatchAuthorizationTemplate(headers=headers):
    """
    服务中心授权书批量导入模板下载
    /mgmt/store/authorization/exportBatchAuthorizationTemplate
    """

    url = "/mgmt/store/authorization/exportBatchAuthorizationTemplate"
    with client.get(url=url, headers=headers) as r:
        return r
