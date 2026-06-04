import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_getInvoiceContent(headers=headers):
    """
    获取发票采集内容
    /mgmt/sys/getInvoiceContent
    """

    url = "/mgmt/sys/getInvoiceContent"
    with client.get(url=url, headers=headers) as r:
        return r
