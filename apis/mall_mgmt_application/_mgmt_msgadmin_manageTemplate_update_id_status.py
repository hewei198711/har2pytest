import os

from util.client import client

params = {
    "id": 0,  # id
    "status": 0,  # status
}

headers = {
    "authorization": f"bearer {os.environ['access_token']}",
    "content-length": "0",
}


def _mgmt_msgadmin_manageTemplate_update_id_status(params=params, headers=headers):
    """
    updateStatus
    /mgmt/msgadmin/manageTemplate/update/{id}/{status}

    参数说明:
    - id: id
    - status: status
    """

    url = f"/mgmt/msgadmin/manageTemplate/update/{params['id']}/{params['status']}"
    with client.get(url=url, headers=headers) as r:
        return r
