import os

from util.client import client

data = {
    "disableTime": 0,  # 定时禁用时间
    "enableConfig": 0,  # 上下架配置: 1.立即启用; 2.定时禁用启用
    "enableTime": 0,  # 定时启用时间
    "location": "",  # 显示位置(可多选): 1.APP; 2.小程序;(多选使用逗号分隔)
    "popUpContent": "",  # 弹窗内容
    "popUpTitle": "",  # 弹窗标题
    "popUpType": 0,  # 弹窗类型: 1:系统升级提醒
    "sort": 0,  # 排序
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_savePopUpSetting(data=data, headers=headers):
    """
    新增弹窗配置
    /mgmt/cms/savePopUpSetting

    参数说明:
    - disableTime: 定时禁用时间
    - enableConfig: 上下架配置: 1.立即启用; 2.定时禁用启用
    - enableTime: 定时启用时间
    - location: 显示位置(可多选): 1.APP; 2.小程序;(多选使用逗号分隔)
    - popUpContent: 弹窗内容
    - popUpTitle: 弹窗标题
    - popUpType: 弹窗类型: 1:系统升级提醒
    - sort: 排序
    """

    url = "/mgmt/cms/savePopUpSetting"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
