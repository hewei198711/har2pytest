import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_qrcode_exportBatchQrCodeTemplate(headers=headers):
    """
    服务中心活码批量导入模板下载
    /mgmt/store/qrcode/exportBatchQrCodeTemplate
    """

    url = "/mgmt/store/qrcode/exportBatchQrCodeTemplate"
    with client.get(url=url, headers=headers) as r:
        return r
