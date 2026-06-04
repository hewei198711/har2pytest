import os

from util.client import client

data = {
    "applyRange": "",  # 适用范围，1：云商, 2：微店，4.26.5版本需求：YC853。增加字号和位置可调整，前端默认送：1
    "fontSizeLocationConfig": {
        "issueDateFontSize": 0,
        "issueDateHeight": 0.0,
        "issueDateWidth": 0.0,
        "issueDateX": 0.0,
        "issueDateY": 0.0,
        "ratio": 0.0,
        "storeNmFontSize": 0,
        "storeNmHeight": 0.0,
        "storeNmWidth": 0.0,
        "storeNmX": 0.0,
        "storeNmY": 0.0,
        "storeNoFontSize": 0,
        "storeNoHeight": 0.0,
        "storeNoWidth": 0.0,
        "storeNoX": 0.0,
        "storeNoY": 0.0,
        "validDateFontSize": 0,
        "validDateHeight": 0.0,
        "validDateWidth": 0.0,
        "validDateX": 0.0,
        "validDateY": 0.0,
    },  # 字体大小位置配置
    "id": 0,  # id
    "templateName": "",  # 授权书模板名称
    "url": "",  # 底图链接
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_store_authorization_createAuthorizationTemplate(data=data, headers=headers):
    """
    新增授权书模板
    /mgmt/store/authorization/createAuthorizationTemplate

    参数说明:
    - applyRange: 适用范围，1：云商, 2：微店，4.26.5版本需求：YC853。增加字号和位置可调整，前端默认送：1
    - fontSizeLocationConfig: 字体大小位置配置
    - fontSizeLocationConfig.issueDateFontSize: 签发日期字号
    - fontSizeLocationConfig.issueDateHeight: 签发日期高度
    - fontSizeLocationConfig.issueDateWidth: 签发日期宽度
    - fontSizeLocationConfig.issueDateX: 签发日期X坐标
    - fontSizeLocationConfig.issueDateY: 签发日期Y坐标
    - fontSizeLocationConfig.ratio: 比例
    - fontSizeLocationConfig.storeNmFontSize: 店名字号
    - fontSizeLocationConfig.storeNmHeight: 店名高度
    - fontSizeLocationConfig.storeNmWidth: 店名宽度
    - fontSizeLocationConfig.storeNmX: 店名X坐标
    - fontSizeLocationConfig.storeNmY: 店名Y坐标
    - fontSizeLocationConfig.storeNoFontSize: 店号字号
    - fontSizeLocationConfig.storeNoHeight: 店号高度
    - fontSizeLocationConfig.storeNoWidth: 店号宽度
    - fontSizeLocationConfig.storeNoX: 店号X坐标
    - fontSizeLocationConfig.storeNoY: 店号Y坐标
    - fontSizeLocationConfig.validDateFontSize: 授权有效日期字号
    - fontSizeLocationConfig.validDateHeight: 授权有效日期高度
    - fontSizeLocationConfig.validDateWidth: 授权有效日期宽度
    - fontSizeLocationConfig.validDateX: 授权有效日期X坐标
    - fontSizeLocationConfig.validDateY: 授权有效日期Y坐标
    - id: id
    - templateName: 授权书模板名称
    - url: 底图链接
    """

    url = "/mgmt/store/authorization/createAuthorizationTemplate"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
