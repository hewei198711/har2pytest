import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_order_riskctrl_exportAddrKeywordsTemplate(headers=headers):
    """
    导入模板下载
    /mgmt/order/riskctrl/exportAddrKeywordsTemplate
    """

    url = "/mgmt/order/riskctrl/exportAddrKeywordsTemplate"
    with client.get(url=url, headers=headers) as r:
        return r
