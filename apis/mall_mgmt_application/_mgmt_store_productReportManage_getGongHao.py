import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_productReportManage_getGongHao(headers=headers):
    """
    获取当前登录者工号
    /mgmt/store/productReportManage/getGongHao
    """

    url = "/mgmt/store/productReportManage/getGongHao"
    with client.get(url=url, headers=headers) as r:
        return r
