import os

from util.client import client

params = {
    "id": 0,  # id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_appAndPc_store_graduation_queryGraduationInfoById(params=params, headers=headers):
    """
    根据id查询结业申请详情
    /appStore/appAndPc/store/graduation/queryGraduationInfoById

    参数说明:
    - id: id
    """

    url = "/appStore/appAndPc/store/graduation/queryGraduationInfoById"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
