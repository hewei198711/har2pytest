import os

from util.client import client

data = {
    "businessInfo": "",  # 营业执照信息
    "foodInfo": "",  # 食品经营许可证信息
    "taxInfo": "",  # 税务登记证信息
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_profile_applyCredentialChange(data=data, headers=headers):
    """
    申请服务中心证件信息变更
    /appStore/store/profile/applyCredentialChange

    参数说明:
    - businessInfo: 营业执照信息
    - foodInfo: 食品经营许可证信息
    - taxInfo: 税务登记证信息
    """

    url = "/appStore/store/profile/applyCredentialChange"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
