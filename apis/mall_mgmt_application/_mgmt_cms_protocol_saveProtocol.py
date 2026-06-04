import os

from util.client import client

data = {
    "applyChannelType": 0,  # 适用渠道类型,0：全部（默认）1:h5端 2:app端 3:miniapp小程序端 4:pc端
    "id": 0,  # 协议ID
    "protocol": "",  # 协议内容
    "protocolType": 0,  # 协议类型 1:商城注册及开卡协议 2:油葱商城隐私协议政策 3:油葱商城用户协议 4:完美VIP卡使用规则
    "protocolTypeDesc": "",  # 协议类型说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_cms_protocol_saveProtocol(data=data, headers=headers):
    """
    保存商城协议配置
    /mgmt/cms/protocol/saveProtocol

    参数说明:
    - applyChannelType: 适用渠道类型,0：全部（默认）1:h5端 2:app端 3:miniapp小程序端 4:pc端
    - id: 协议ID
    - protocol: 协议内容
    - protocolType: 协议类型 1:商城注册及开卡协议 2:油葱商城隐私协议政策 3:油葱商城用户协议 4:完美VIP卡使用规则
    - protocolTypeDesc: 协议类型说明
    """

    url = "/mgmt/cms/protocol/saveProtocol"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
