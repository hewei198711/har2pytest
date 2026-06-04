import os

from util.client import client

data = {
    "attachmentsList": [{"name": "", "url": ""}],  # 附件
    "content": "",  # 内容
    "defType": 0,  # 模板类型: 0 系统模板 1自由编辑模板
    "id": 0,  # TODO: 添加参数说明
    "letterSendType": 0,  # 站内信消息对象 1:个人,2:服务中心
    "msgType": 0,  # 消息类型，与数据词典中消息类型绑定
    "msgTypeName": "",  # 消息类型，与数据词典中消息类型绑定
    "operator": "",  # 创建人
    "pageType": 0,  # 消息跳转页面类型：1-直销员学习，2-直销员考试，3-直销员自主退出申请，4-直销员填写资料，5-直销员签署合同
    "planSceneId": 0,  # 业务主题主键Id(手工消息用到)
    "planSceneTitle": "",  # 业务主题名称
    "remark": "",  # 模版备注
    "sendMall": 0,  # (手工消息用到) 消息平台-商城 0:否, 1:是
    "sendStore": 0,  # (手工消息用到) 消息平台-服务中心 0:否 , 1:是
    "status": 0,  # 状态  :  0 否 ,1 : 是 ,2 :删除状态
    "templateCode": "",  # 模版code
    "templateName": "",  # 模板名称
    "templateType": 0,  # 1 : 邮箱  2 : 短信 3: APP  4: 微信小程序 5:微信公众号 6:站内信
    "title": "",  # 标题
    "updateTime": "",  # TODO: 添加参数说明
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_manageTemplate_update(data=data, headers=headers):
    """
    更新站内信模板
    /mgmt/msgadmin/manageTemplate/update

    参数说明:
    - attachmentsList: 附件
    - content: 内容
    - defType: 模板类型: 0 系统模板 1自由编辑模板
    - letterSendType: 站内信消息对象 1:个人,2:服务中心
    - msgType: 消息类型，与数据词典中消息类型绑定
    - msgTypeName: 消息类型，与数据词典中消息类型绑定
    - operator: 创建人
    - pageType: 消息跳转页面类型：1-直销员学习，2-直销员考试，3-直销员自主退出申请，4-直销员填写资料，5-直销员签署合同
    - planSceneId: 业务主题主键Id(手工消息用到)
    - planSceneTitle: 业务主题名称
    - remark: 模版备注
    - sendMall: (手工消息用到) 消息平台-商城 0:否, 1:是
    - sendStore: (手工消息用到) 消息平台-服务中心 0:否 , 1:是
    - status: 状态  :  0 否 ,1 : 是 ,2 :删除状态
    - templateCode: 模版code
    - templateName: 模板名称
    - templateType: 1 : 邮箱  2 : 短信 3: APP  4: 微信小程序 5:微信公众号 6:站内信
    - title: 标题
    """

    url = "/mgmt/msgadmin/manageTemplate/update"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
