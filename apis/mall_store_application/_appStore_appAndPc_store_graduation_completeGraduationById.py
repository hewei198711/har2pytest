import os

from util.client import client

data = {
    "decoratePic": "",  # 装修拆除照片
    "id": 0,  # 主键id
    "port": 0,  # 请求端 0后台 1APP 2PC
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_appAndPc_store_graduation_completeGraduationById(data=data, headers=headers):
    """
    完成结业--后台,app,pc
    /appStore/appAndPc/store/graduation/completeGraduationById

    参数说明:
    - decoratePic: 装修拆除照片
    - id: 主键id
    - port: 请求端 0后台 1APP 2PC
    """

    url = "/appStore/appAndPc/store/graduation/completeGraduationById"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
