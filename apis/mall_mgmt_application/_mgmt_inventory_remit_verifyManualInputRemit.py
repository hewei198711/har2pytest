import os
from urllib.parse import urlencode

from util.client import client

data = {
    "verifyRemark": "",  # verifyRemark
    "verifyResult": 0,  # verifyResult
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_inventory_remit_verifyManualInputRemit(data=data, headers=headers):
    """
    手工录入流水审核
    /mgmt/inventory/remit/verifyManualInputRemit

    参数说明:
    - verifyRemark: verifyRemark
    - verifyResult: verifyResult
    """

    url = "/mgmt/inventory/remit/verifyManualInputRemit"
    data = urlencode(data)  # application/x-www-form-urlencoded传参需要特殊处理

    with client.post(url=url, data=data, headers=headers) as r:
        return r
