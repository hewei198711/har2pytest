import os

from util.client import client

params = {
    "storeCode": "",  # 服务中心编号
    "templateNo": "",  # 模板编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_getTemplateFillKeyValue(params=params, headers=headers):
    """
    根据服务中心及模板编号获取填充字段-对应值
    /mgmt/store/getTemplateFillKeyValue

    参数说明:
    - storeCode: 服务中心编号
    - templateNo: 模板编号
    """

    url = "/mgmt/store/getTemplateFillKeyValue"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
