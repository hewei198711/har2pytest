import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_getImportCertErrorExcel(headers=headers):
    """
    获取导入失败的电子印章认证信息
    /mgmt/store/getImportCertErrorExcel
    """

    url = "/mgmt/store/getImportCertErrorExcel"
    with client.get(url=url, headers=headers) as r:
        return r
