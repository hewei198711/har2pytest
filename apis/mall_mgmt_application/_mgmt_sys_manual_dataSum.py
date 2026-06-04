import os

from util.client import client

data = {
    "creatAtEnd": 0,  # 下载结束时间(毫秒时间戳)
    "creatAtEnd4LocalDateTime": "",  # TODO: 添加参数说明
    "createAtStart": 0,  # 下载开始时间(毫秒时间戳)
    "createAtStart4LocalDateTime": "",  # TODO: 添加参数说明
    "likeTime": 0,  # 点赞次数
    "storeCode": "",  # 店号
    "sumDownLoadTime": 0,  # 下载次数
    "viewTime": 0,  # 浏览次数
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_sys_manual_dataSum(data=data, headers=headers):
    """
    优秀案例库数据统计
    /mgmt/sys/manual/dataSum

    参数说明:
    - creatAtEnd: 下载结束时间(毫秒时间戳)
    - createAtStart: 下载开始时间(毫秒时间戳)
    - likeTime: 点赞次数
    - storeCode: 店号
    - sumDownLoadTime: 下载次数
    - viewTime: 浏览次数
    """

    url = "/mgmt/sys/manual/dataSum"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
