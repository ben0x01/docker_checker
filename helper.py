import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOCKER_CHECKER_PATH = os.path.join(BASE_DIR, "data_to_send", "docker_checker.py")
DOCKER_RESTARTER_PATH = os.path.join(BASE_DIR, "data_to_send", "docker_restarter.sh")
PYTHON_INSTALLER_PATH = os.path.join(BASE_DIR, "data_to_send", "py_installer.sh")
SETUP_CRONTAB_PATH = os.path.join(BASE_DIR, "data_to_send", "setup_crontab.sh")