import os

from util.client import client

params = {
    "addEndTime": "",  # 添加结束时间
    "addStartTime": "",  # 添加开始时间
    "applyRange": "",  # 适用范围，1：云商, 2：微店
    "pageNum": 0,  # pageNum
    "pageSize": 0,  # pageSize
    "status": 0,  # 状态，0：已失效，1：生效中
    "templateName": "",  # 授权书模板名称
    "templateNo": "",  # 授权书模板编号
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_authorization_getAuthorizationTemplateList(params=params, headers=headers):
    """
    获取授权书模板列表
    /mgmt/store/authorization/getAuthorizationTemplateList

    参数说明:
    - addEndTime: 添加结束时间
    - addStartTime: 添加开始时间
    - applyRange: 适用范围，1：云商, 2：微店
    - pageNum: pageNum
    - pageSize: pageSize
    - status: 状态，0：已失效，1：生效中
    - templateName: 授权书模板名称
    - templateNo: 授权书模板编号
    """

    url = "/mgmt/store/authorization/getAuthorizationTemplateList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
