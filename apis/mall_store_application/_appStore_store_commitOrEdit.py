import os

from util.client import client

data = {
    "cardVOs": [],  # 身份证年审pojo
    "companyCode": "",  # 分公司code
    "id": 0,  # 主键id(编辑时需要)
    "licenseVOs": [],  # 证件年审pojo
    "personImageVO": "",  # 个人形象年审pojo
    "reviewModelName": "",  # 年审类型(模块)名称 身份证年审、证件年审、店铺形象年审、个人形象年审
    "reviewModelType": 0,  # 年审类型(模块) 1-身份证年审、2-证件年审、3-店铺形象年审、4-个人形象年审
    "reviewTitle": "",  # 身份证年审、证件年审、店铺形象年审、个人形象年审
    "storeCode": "",  # 服务中心编号
    "storeImageVO": "",  # 店铺信息年审pojo
    "storeName": "",  # 服务中心名称
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _appStore_store_commitOrEdit(data=data, headers=headers):
    """
    年审申请提交
    /appStore/store/commitOrEdit

    参数说明:
    - cardVOs: 身份证年审pojo
    - companyCode: 分公司code
    - id: 主键id(编辑时需要)
    - licenseVOs: 证件年审pojo
    - personImageVO: 个人形象年审pojo
    - reviewModelName: 年审类型(模块)名称 身份证年审、证件年审、店铺形象年审、个人形象年审
    - reviewModelType: 年审类型(模块) 1-身份证年审、2-证件年审、3-店铺形象年审、4-个人形象年审
    - reviewTitle: 身份证年审、证件年审、店铺形象年审、个人形象年审
    - storeCode: 服务中心编号
    - storeImageVO: 店铺信息年审pojo
    - storeName: 服务中心名称
    """

    url = "/appStore/store/commitOrEdit"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
