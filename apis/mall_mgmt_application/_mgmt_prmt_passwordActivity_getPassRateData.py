import os

from util.client import client

params = {
    "activityId": 0,  # activityId
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_passwordActivity_getPassRateData(params=params, headers=headers):
    """
    口令活动人数通过率
    /mgmt/prmt/passwordActivity/getPassRateData

    参数说明:
    - activityId: activityId
    """

    url = "/mgmt/prmt/passwordActivity/getPassRateData"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
