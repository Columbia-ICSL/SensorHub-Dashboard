# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import traceback

from apps.home import blueprint
from flask import render_template, request
from jinja2 import TemplateNotFound


@blueprint.route('/')
def dashboard():
    slot1 = {
        'slot': 1,
        'name': 'Air Quality',
        'sensors': zip(['PM Sensor'], range(1))
    }
    slot2 = {
        'slot': 2,
        'name': 'Wind',
        'sensors': zip(['Wind Speed Sensor'], range(1))
    }
    slot3 = {
        'slot': 3,
        'name': 'Multi-purpose Air Sensor',
        'sensors': zip(['CO2 Sensor', 'Temperature & Humidity Sensor', 'Air Pressure Sensor'], range(3))
    }
    return render_template('dashboard/main.html', segment="dashboard", modules=[slot1, slot2, slot3])


@blueprint.route('/data')
def data():
    return render_template('data/main.html', segment="data")


@blueprint.route('/setting/<module_name>')
def sensor_setting(module_name):
    module_info = {
        'name': module_name,
        'settings': {
            'Temperature Humidity': {
                'Samples per second': 2
            },
            'CO2': {
                'Samples per second': 1
            }
        }
    }
    return render_template('setting/main.html', module=module_info)


@blueprint.route('/<template>')
def route_template(template):
    try:

        if not template.endswith('.html'):
            template += '.html'

        # Detect the current page
        segment = get_segment(request)

        # Serve the file (if exists) from app/templates/home/FILE.html
        return render_template("home/" + template, segment=segment)

    except TemplateNotFound:
        return render_template('home/page-404.html'), 404

    except:
        traceback.print_exc()
        return render_template('home/page-500.html'), 500


# Helper - Extract current page name from request
def get_segment(request):
    try:

        segment = request.path.split('/')[-1]

        if segment == '':
            segment = 'index'

        return segment

    except:
        return None
