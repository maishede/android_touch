import os
import time
import psutil
import platform
import logging
import subprocess
from django.conf import settings
from concurrent.futures import ThreadPoolExecutor


class AdbClient(object):
    def __init__(self):
        self.device = None
        self.screenshot_path = os.path.join(settings.BASE_DIR, 'static', 'images', 'screenshot', 'stream.png')
        self.init_conn()

    def init_conn(self):
        self.choose_device()
        self.connect_device()
        self.test_adb_connection()

    def show_devices(self):
        result = subprocess.check_output([self.get_adb(), 'devices'])
        return result

    def choose_device(self):
        devices = self.show_devices()
        devices = devices.decode('utf8')
        devices = devices.replace('List of devices attached', '').replace('device', '')
        device_list = devices.split()
        if len(device_list) >= 1:
            self.device = device_list[0]
        else:
            logging.error('未找到设备')

    def get_adb(self):
        ADB_PATH = 'adb'
        try:
            try:
                ADB_PATH = settings.ADB_BINARY
                return ADB_PATH
            except:
                pass
            if platform.system() == 'Windows':
                adb_paths = self.find_process('adb.exe')
            else:
                adb_paths = self.find_process('adb')
            if not len(adb_paths):
                logging.warning('未查找到adb')
                return ADB_PATH
            else:
                return adb_paths.pop()
        except:
            return ADB_PATH

    def test_adb_connection(self):
        self.adb_command(['kill-server'])
        self.adb_command(['start-server'])
        time.sleep(2)

    def connect_device(self):
        result = subprocess.check_output([self.get_adb(), '-s', self.device, 'root'])
        logging.info(result)
        self.adb_command(['remount'])

    @staticmethod
    def find_process(name):
        proc = set()
        for p in psutil.process_iter(attrs=['name']):
            if (name == p.info['name']):
                proc.add(p.exe())
        return proc

    def adb_command(self, cmd_list, shell=False, silent=False):
        args = [self.get_adb(),
                '-s',
                self.device]
        if shell:
            args += ['shell']
        args += cmd_list
        try:
            result = subprocess.check_output(
                args,
                stderr=subprocess.STDOUT)
            return result
        except Exception:
            import traceback
            logging.error(traceback.format_exc())
            if not silent:
                logging.error('adb运行失败')
            return None

    def screen_stream(self):
        self.adb_command(['screencap', '-p', '/data/local/screen.png'], True)
        self.adb_command(['pull', '/data/local/screen.png', self.screenshot_path])

    def touch_screen(self, x, y):
        if isinstance(x, int):
            x = str(x)
        if isinstance(y, int):
            y = str(y)
        with ThreadPoolExecutor(2) as exector:
            cmd_list = ['input', 'tap', x, y]
            exector.submit(self.adb_command, cmd_list, True)

adb_conn = AdbClient()