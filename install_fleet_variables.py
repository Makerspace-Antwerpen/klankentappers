#!/bin/python3
from balena import Balena
import getpass
'''
script to set service environment variables to a default value
make sure to install the balena sdk: `pip3 install balena-sdk`
'''

login = "token"

ENV_LIST = {
    'AI_SAMPLE_DIR': '$HOME/recordings',
    'EVENT_END_THRESHOLD': '0',
    'EVENT_PADDING_TIME': '5',
    'EVENT_START_THRESHOLD_DB': '10',
    'MIC_AUDIODEVICE': '1',
    'MIC_REF_DBA': '90.0',
    'MIC_REF_RMS': '0.03',
    'TB_INTERVAL_TIME': '5',
    'TB_SECRET': "xx",
    'TB_SERVER': "xx",
    'TZ': "Europe/Brussels"
}


def set_envs(balena, app_id: str, service_name: str, ENV_LIST: dict):
    for i in ENV_LIST:
        print(i)
        balena.models.environment_variables.service_environment_variable.create(
            app_id, service_name, i, ENV_LIST[i])

if __name__ == '__main__':
    balena = Balena()
    app_id = "1796091"  # => find this on the dashboard
    service_name = "meter"

    # Either you login via username/pw or via token
    if login == "username":
        user = input("balena username?")
        pw = getpass.getpass(prompt='balena password? ')
        credentials = {
            'username': user, 'password': pw
        }
        balena.auth.login(**credentials)
    elif login == "token":
        auth_token = "<balena_token>" # => retrieve a token on your balena account via settings
        balena.auth.login_with_token(auth_token)
    if balena.auth.is_logged_in():
        print('You are logged in!')
        set_envs(balena, app_id=app_id,
                 service_name=service_name, ENV_LIST=ENV_LIST)
    else:
        print('You are not logged in!')