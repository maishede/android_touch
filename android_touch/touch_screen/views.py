from django.shortcuts import render
import os
import time
import json
import logging
import traceback
from django.conf import settings
from touch_screen.helpers import adb_conn
from django.http import HttpResponse

# Create your views here.

# screen_path = os.path.join(settings.BASE_DIR, 'templates', 'touch_screen', 'dynamic_analyzer.html')
screen_path = 'dynamic_analyzer.html'


# adb_conn = AdbClient()


def show_screen(request, ):
    # ac = AdbClient()
    # ac.screen_stream()
    return render(request, screen_path, {})


def touch_screen(request, ):
    params = request.GET
    x = params.get('x', None)
    y = params.get('y', None)
    try:
        x = float(x)
        x = '%.2f' % x
    except:
        logging.error('x: %s, error: %s' % (x, traceback.format_exc()))
        return render(request, screen_path, {})
    try:
        y = float(y)
        y = '%.2f' % y
    except:
        logging.error('y: %s, error: %s' % (y, traceback.format_exc()))
        return render(request, screen_path, {})
    # ac = AdbClient()
    # 先点击屏幕再点击截图
    adb_conn.touch_screen(x, y)
    time.sleep(0.5)
    adb_conn.screen_stream()

    # return render(request, screen_path, {})
    return HttpResponse(json.dumps({"a": "a"}), content_type="application/json")


def slide(request, ):
    params = request.GET
    direction = params.get('direction', None)
    if not direction:
        return HttpResponse(json.dumps({'a': 'a'}), content_type='application/json')
    if direction not in ['left', 'right']:
        return HttpResponse(json.dumps({'a': 'a'}), content_type='application/json')
    adb_conn.slide(direction)
    time.sleep(0.5)
    adb_conn.screen_stream()
    return HttpResponse(json.dumps({'a': 'a'}), content_type='application/json')


def home(request,):
    adb_conn.home()
    adb_conn.home()
    time.sleep(0.5)
    adb_conn.screen_stream()
    return HttpResponse(json.dumps({'a': 'a'}), content_type='application/json')


def refresh(request,):
    adb_conn.screen_stream()
    return HttpResponse(json.dumps({'a': 'a'}), content_type='application/json')