import os

from util.client import client

params = {
    "asc": False,  # 是否升序:true-升序,false-降序
    "cardNo": "",  # 会员卡号
    "endTime": "",  # 操作时间止区(yyyy-MM-dd)
    "id": 0,  # 登录提醒id
    "mobile": "",  # 手机号
    "pageNum": 0,  # 当前页
    "pageSize": 0,  # 每页数量
    "platform": 0,  # 数据平台:1-APP,2-PC,4-小程序
    "realName": "",  # 会员姓名
    "shareWay": 0,  # 分享方式:1-生成海报,2-转发朋友圈,3-分享到会话
    "sortBy": 0,  # 排序字段:1-操作时间,2-访问次数,3-访问人数
    "startTime": "",  # 操作时间起区(yyyy-MM-dd)
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_prmt_loginGift_exportShare(params=params, headers=headers):
    """
    导出分享明细
    /mgmt/prmt/loginGift/exportShare

    参数说明:
    - asc: 是否升序:true-升序,false-降序
    - cardNo: 会员卡号
    - endTime: 操作时间止区(yyyy-MM-dd)
    - id: 登录提醒id
    - mobile: 手机号
    - pageNum: 当前页
    - pageSize: 每页数量
    - platform: 数据平台:1-APP,2-PC,4-小程序
    - realName: 会员姓名
    - shareWay: 分享方式:1-生成海报,2-转发朋友圈,3-分享到会话
    - sortBy: 排序字段:1-操作时间,2-访问次数,3-访问人数
    - startTime: 操作时间起区(yyyy-MM-dd)
    """

    url = "/mgmt/prmt/loginGift/exportShare"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
