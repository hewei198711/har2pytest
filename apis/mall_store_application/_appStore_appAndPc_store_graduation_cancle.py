import os

from util.client import client

data = {
    "cancelApplication": "",  # 撤销申请书
    "cancelReason": "",  # 撤销原因
    "id": 0,  # 主键id
    "port": 0,  # 请求端 0后台 1APP 2PC
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_appAndPc_store_graduation_cancle(data=data, headers=headers):
    """
    撤销--后台,app,pc
    /appStore/appAndPc/store/graduation/cancle

    参数说明:
    - cancelApplication: 撤销申请书
    - cancelReason: 撤销原因
    - id: 主键id
    - port: 请求端 0后台 1APP 2PC
    """

    url = "/appStore/appAndPc/store/graduation/cancle"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
