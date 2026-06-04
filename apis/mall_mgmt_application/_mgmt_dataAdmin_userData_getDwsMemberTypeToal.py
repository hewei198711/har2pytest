import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_dataAdmin_userData_getDwsMemberTypeToal(headers=headers):
    """
    根据日期类型查询用户增长数
    /mgmt/dataAdmin/userData/getDwsMemberTypeToal
    """

    url = "/mgmt/dataAdmin/userData/getDwsMemberTypeToal"
    with client.post(url=url, headers=headers) as r:
        return r
