import os

from util.client import client

data = {
    "mobile": "",  # 手机号
    "type": "",  # 业务类型：1.修改负责人旧手机号, 2.修改负责人新手机号, 3.修改配偶旧手机号, 4.修改配偶新手机号,5结业验证验证码
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
}


def _appStore_appAndPc_store_graduation_sendSmsCode(data=data, headers=headers):
    """
    服务中心结业申请发送短信验证码
    /appStore/appAndPc/store/graduation/sendSmsCode

    参数说明:
    - mobile: 手机号
    - type: 业务类型：1.修改负责人旧手机号, 2.修改负责人新手机号, 3.修改配偶旧手机号, 4.修改配偶新手机号,5结业验证验证码
    """

    url = "/appStore/appAndPc/store/graduation/sendSmsCode"
    with client.post(url=url, json=data, headers=headers) as r:
        return r
