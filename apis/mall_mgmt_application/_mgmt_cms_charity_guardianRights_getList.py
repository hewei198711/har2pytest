import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _mgmt_cms_charity_guardianRights_getList(headers=headers):
    """
    公益购守护者权益列表查询(下拉框)
    /mgmt/cms/charity/guardianRights/getList
    """

    url = "/mgmt/cms/charity/guardianRights/getList"
    with client.post(url=url, headers=headers) as r:
        return r
