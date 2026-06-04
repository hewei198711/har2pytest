import os

from util.client import client

params = {
    "certificateTypeId": 0,  # 证件类型id
    "companyName": "",  # 公司名称
    "expiredStatus": 0,  # 下载状态 0->未失效,1->已失效
    "pageNum": 0,  # 页码
    "pageSize": 0,  # 每页大小
    "storeCode": "",  # 服务中心编码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_store_certificate_passed_list(params=params, headers=headers):
    """
    获取已申请通过的证件列表
    /mgmt/sys/store/certificate/passed/list

    参数说明:
    - certificateTypeId: 证件类型id
    - companyName: 公司名称
    - expiredStatus: 下载状态 0->未失效,1->已失效
    - pageNum: 页码
    - pageSize: 每页大小
    - storeCode: 服务中心编码
    """

    url = "/mgmt/sys/store/certificate/passed/list"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
