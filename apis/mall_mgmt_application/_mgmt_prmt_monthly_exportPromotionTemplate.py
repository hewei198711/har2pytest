import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_monthly_exportPromotionTemplate(headers=headers):
    """
    下载活动导入模板
    /mgmt/prmt/monthly/exportPromotionTemplate
    """

    url = "/mgmt/prmt/monthly/exportPromotionTemplate"
    with client.get(url=url, headers=headers) as r:
        return r
