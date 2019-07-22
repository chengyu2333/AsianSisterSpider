import io
import time
import os
import sys


log_path = "logs"

if not os.path.exists(log_path):
    os.makedirs(log_path)


def log_error(msg):
    f = io.open(log_path + "/error-" + time.strftime("%Y-%m-%d", time.localtime()) + ".log", 'a', encoding="utf-8")
    log = time.ctime() + " | \t" + msg + "\r\n\n"
    sys.stdout.write("\033[1;31m" + str(log) + "\033[0m")
    f.write(log)
    f.close()


def log_info(msg):
    f = io.open(log_path + "/info-" + time.strftime("%Y-%m-%d", time.localtime()) + ".log", 'a', encoding="utf-8")
    log = time.ctime() + " | \t" + msg + "\r\n\n"
    sys.stdout.write("\033[1;32m" + str(log) + "\033[0m")
    f.write(log)
    f.close()


def log_success(msg):
    f = io.open(log_path + "/success-" + time.strftime("%Y-%m-%d", time.localtime()) + ".log", 'a', encoding="utf-8")
    log = time.ctime() + " | \t" + msg + "\r\n\n"
    sys.stdout.write("\033[1;33m" + str(log) + "\033[0m")
    f.write(log)
    f.close()
