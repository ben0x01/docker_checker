import paramiko
from scp import SCPClient
import os


class SshConnector:
    def __init__(self, host, login, password):
        self.ssh = paramiko.SSHClient()
        self.hostname = host
        self.login = login
        self.password = password
        self.scp = None

    def create_connection(self):
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.ssh.connect(self.hostname, username=self.login, password=self.password)

        self.scp = SCPClient(self.ssh.get_transport())

    def create_work_directory(self):
        self.execute_command(f"mkdir modules")

    def send_files_give_permission(self, local_file_path, remote_file_path):
        if not os.path.exists(local_file_path):
            print(f"File '{local_file_path}' not found.")
            return
        self.scp.put(local_file_path, remote_file_path)
        print(f"File '{local_file_path}' sent to '{remote_file_path}'.")

        self.execute_command(f"chmod +x {remote_file_path}")
        print(f"Made '{remote_file_path}' executable.")

    def execute_command(self, command):
        stdin, stdout, stderr = self.ssh.exec_command(f"{command}")
        output = stdout.read().decode()
        error = stderr.read().decode()

        if output:
            print("Output:")
            print(output)
        if error:
            print("Error:")
            print(error)

    def close_connection(self):
        if self.scp:
            self.scp.close()
        self.ssh.close()
