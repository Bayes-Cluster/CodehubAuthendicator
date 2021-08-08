from jupyterhub.auth import Authenticator
from tornado import gen
from paramiko import SSHClient, AuthenticationException, AutoAddPolicy
from traitlets import Int, Unicode


class CodehubAutheticator(Authenticator):
    server_address = Unicode(
        config=True,
        help='Address of LDAP server'
    )
    server_port = Int(
        config=True,
        help='Port of LDAP server',
    )

    @gen.coroutine
    def authenticate(self, handler, data):
        with SSHClient() as ssh:
            ssh.set_missing_host_key_policy(AutoAddPolicy())
            try:
                ssh.connect(self.server_address, port=self.server_port,
                            username=data['username'],
                            password=data['password'],
                            password=data["totp"])
            except AuthenticationException:
                return
            return data['username']
