import os

from util.client import client

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
    "content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
}


def _mgmt_isensitive_importSensitive(headers=headers):
    """
    导入敏感词
    /mgmt/isensitive/importSensitive
    """

    url = "/mgmt/isensitive/importSensitive"
    with client.post(url=url, headers=headers) as r:
        return r
