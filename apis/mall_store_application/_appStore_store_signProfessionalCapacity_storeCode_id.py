import os

from util.client import client

params = {
    "storeCode": "",  # 服务中心编号
    "id": "",  # 门店专业技能id
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_signProfessionalCapacity_storeCode_id(params=params, headers=headers):
    """
    门店勾选仪器
    /appStore/store/signProfessionalCapacity/{storeCode}/{id}

    参数说明:
    - sign: 勾选类型不为空 0：未勾选；1：已勾选
    - id: 门店专业技能id
    - storeCode: 服务中心编号
    """

    url = f"/appStore/store/signProfessionalCapacity/{params['storeCode']}/{params['id']}"
    with client.get(url=url, headers=headers) as r:
        return r
