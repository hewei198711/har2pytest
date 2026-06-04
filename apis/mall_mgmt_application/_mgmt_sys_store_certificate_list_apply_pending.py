import os

from util.client import client

params = {
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 页码
    "storeCode": "",  # 服务中心编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_store_certificate_list_apply_pending(params=params, headers=headers):
    """
    查询待导入证件的服务中心集合
    /mgmt/sys/store/certificate/list/apply/pending

    参数说明:
    - pageNum: 当前页
    - pageSize: 页码
    - storeCode: 服务中心编码
    """

    url = "/mgmt/sys/store/certificate/list/apply/pending"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
