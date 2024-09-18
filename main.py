import config

from server_connecter import SshConnector
from helper import DOCKER_CHECKER_PATH, PYTHON_INSTALLER_PATH, DOCKER_RESTARTER_PATH, SETUP_CRONTAB_PATH

if __name__ == '__main__':
    ssh = SshConnector(host=config.host, login=config.username, password=config.password)

    ssh.create_connection()

    ssh.create_work_directory()

    ssh.send_files_give_permission(PYTHON_INSTALLER_PATH, "/root/modules/py_installer.sh")
    ssh.send_files_give_permission(DOCKER_CHECKER_PATH, "/root/modules/docker_checker.py")
    ssh.send_files_give_permission(DOCKER_RESTARTER_PATH, "/root/modules/docker_restarter.sh")
    ssh.send_files_give_permission(SETUP_CRONTAB_PATH, "/root/modules/setup_crontab.sh")

    ssh.execute_command("/root/modules/py_installer.sh")
    ssh.execute_command("/root/modules/setup_crontab.sh")

    ssh.close_connection()