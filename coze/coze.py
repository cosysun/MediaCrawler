from cozepy import Coze, TokenAuth, COZE_CN_BASE_URL, Message, ChatEventType, JWTOAuthApp


tianwen_bot_id = "7455807846782238731"
user_id = "1234567890"
person_test_key = "pat_FETnAzc55F1rGCsaYwluaUOXbSUnEAVCIQ0VFCzrHQtSDRN7TLedJJPbwyWVJ5XU"
workflow_id = ""


def get_access_token():
    access_token = generate_access_token()
    return access_token


def generate_access_token():
    # client ID
    jwt_oauth_client_id = "1150287804115"
    # private key
    jwt_oauth_private_path = "pem/coze_private_key.pem"
    # public key id
    jwt_oauth_public_key_id = "Tc1N9oFIasFMb7ooYhdhlp0b_MeKp2qUWMqM_TbKS68"
    with open(jwt_oauth_private_path, "r") as f:
        jwt_oauth_private_key = f.read()

    jwt_oauth_app = JWTOAuthApp(
        client_id=jwt_oauth_client_id,
        private_key=jwt_oauth_private_key,
        public_key_id=jwt_oauth_public_key_id,
        base_url=COZE_CN_BASE_URL
    )
    oauth_token = jwt_oauth_app.get_access_token()
    return oauth_token.access_token


def run_workflow(workflow_id, params=None):
    """
    运行工作流
    """
    coze = Coze(auth=TokenAuth(get_access_token()), base_url=COZE_CN_BASE_URL)
    workflow = coze.workflows.runs.create(
        workflow_id=workflow_id,
        parameters=params)
    print("workflow.data", workflow.data)


params = {"home_page_url": "https://www.xiaohongshu.com/user/profile/64c087c7000000001403f8e6",
          "cookie": "acw_tc=0a00d86f17384716962788648e3e297bd873d910b7ee532b9fb8a7b10a5819;abRequestId=42fef2fd-9b27-5ea4-b22b-2a138dcdd5b6;webBuild=4.55.1;a1=194c4fcecf0a3kd61ryk7qif88w1ahlj4b4qdt9tb30000283450;webId=85076ba1b03667240310e68cc9fc080c;websectiga=3fff3a6f9f07284b62c0f2ebf91a3b10193175c06e4f71492b60e056edcdebb2;sec_poison_id=8667f086-4946-4b61-998a-59fde9406a15;gid=yj4S4iSif84fyj4S4iSdSD9ji80qTfKyFvTW49DA3iYYEAq8y0x1Vf888JYq4288yjYijDyf;web_session=0400694b8b14ca53ac3542b1ab354bea25477d;xsecappid=xhs-pc-web"}
run_workflow("7461452402248892416", params)
