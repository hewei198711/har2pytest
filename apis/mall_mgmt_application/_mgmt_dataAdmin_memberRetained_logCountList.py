import os

from util.client import client

params = {
    "channel": 0,  # 开通渠道：1->H5；2->APP；3->小程序；4->PC；5->填表；6->上海健康；7->油葱极速版
    "clientType": 0,  # 登入客户端: 1,5-> PC; 2->APP; 3->小程序; 7->完美大学
    "endTime": "",  # 结束时间,yyyy-MM-dd
    "pageNum": 0,  # TODO: 添加参数说明
    "pageSize": 0,  # TODO: 添加参数说明
    "startTime": "",  # 开始时间,yyyy-MM-dd
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_dataAdmin_memberRetained_logCountList(params=params, headers=headers):
    """
    用户留存数据-留存统计（登录）人数
    /mgmt/dataAdmin/memberRetained/logCountList

    参数说明:
    - channel: 开通渠道：1->H5；2->APP；3->小程序；4->PC；5->填表；6->上海健康；7->油葱极速版
    - clientType: 登入客户端: 1,5-> PC; 2->APP; 3->小程序; 7->完美大学
    - endTime: 结束时间,yyyy-MM-dd
    - startTime: 开始时间,yyyy-MM-dd
    """

    url = "/mgmt/dataAdmin/memberRetained/logCountList"
    with client.get(url=url, params=params, headers=headers) as r:
        return r
