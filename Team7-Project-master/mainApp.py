import random
import threading
import time
from datetime import datetime as dt
from datetime import timedelta as td

from flask import (Flask, Response, render_template,
                   render_template_string, request, url_for)
from turbo_flask import Turbo

import calculations as c
from models import (AccessLogs, Entity, EntityHistory, Quotes,
                    ThermostatHistory, db)

# Initialize Flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://Team7:Team7@138.26.48.83/Team7DB'
turbo = Turbo(app)
db.init_app(app)

# Get all quotes from the db
with app.app_context():
    quotes = Quotes.query.all()

# Get all entities from the DB
def get_entities():
    return Entity.query.all()

# Re-calculate the current indoor temperature and push the updated temp to the client
def update_in_temp():
    with app.app_context():
        while True:
            time.sleep(61)
            in_temp=c.updateThermostat()
            turbo.push(turbo.replace(render_template_string('<div class="indoortemp" id="indoortemp"><span style="font-weight: bolder;">Indoor</span><br>{{ "%.1f" | format(in_temp) }}&deg;F</div>', in_temp=in_temp), 'indoortemp'))

# On start, begin temperature update thread
@app.before_first_request
def before_first_request():
    threading.Thread(target=update_in_temp).start()

# Disable caching so graph updates properly
@app.after_request
def add_header(r):
    r.cache_control.max_age = 0
    r.cache_control.no_cache = True
    r.cache_control.no_store = True
    r.cache_control.must_revalidate = True
    r.pragma = 'no-cache'
    r.expires = 0
    return r

# Store request information in access_logs table
@app.before_request
def before_request():
    # if request is for one of the defined endpoints, log it (ignore other requests, such as ones for static content)
    paths_to_log = ['index', 'usage', 'debug', 'update', 'update_hvac', 'run_cycle', 'change_graph_month']
    if request.path in (url_for(i) for i in paths_to_log):
        l = AccessLogs(ip=request.remote_addr, time=dt.now(), useragent=request.user_agent.string, action=request.path, data=str(request.get_json(silent=True)))
        db.session.add(l)
        db.session.commit()

# Screen 1, Dashboard
@app.route("/")
def index():
    # generate random quote
    quote = random.choice(quotes)

    # get current hour for greeting
    hour = dt.now().hour

    # update and get current thermostat state
    c.updateThermostat()
    thermostat_state = ThermostatHistory.query.order_by(ThermostatHistory.id.desc()).first()
    db.session.add(thermostat_state)
    db.session.commit()

    # render webpage, include greeting, quote, hvac info, weather info, and entities for floorplan
    return render_template("main.html", \
        greeting="Good morning!" if hour < 12 else ("Good afternoon!" if hour < 18 else "Good evening!"), \
        quote_en=quote.quoteeng, \
        quote_es=quote.quotespa, \
        quote_author=quote.author, \
        out_temp=c.outdoorTemp(), \
        weather='sun', \
        in_temp = thermostat_state.temp, \
        set_temp = thermostat_state.set_temp, \
        mode = thermostat_state.mode, \
        entities=get_entities())

# Screen 2, Usage
@app.route("/usage")
def usage():
    # calculate current usage
    c.updateDataToday()
    c.updateCurrentMonth()
    historic = c.getHistoricForTable()

    # plot usage graph
    c.plotMonthSQL(dt.now().year, dt.now().month)

    # render webpage, include data for table
    return render_template("usage_and_data.html", historic=historic)

# Screen 3, Debug/Sensors and Cycles
@app.route("/debug")
def debug():
    # get the last 50 log entries
    logs = AccessLogs.query.order_by(AccessLogs.id.desc()).limit(50).all()

    # render webpage, include sensor information, cycle information, and logs
    return render_template("sensor_and_cycles.html", 
                sensors = Entity.query.filter_by(is_sensor=True).order_by(Entity.name.asc()).all(),
                cycles = [{'name': 'Washer', 'id': 'washer'}, 
                {'name': 'Dryer', 'id': 'dryer'},
                {'name': 'Dishwasher', 'id': 'dishwasher'},
                {'name': 'Shower', 'id': 'shower'},
                {'name': 'Bath', 'id': 'bath'},
                {'name': 'Stove', 'id': 'stove'},
                {'name': 'Oven', 'id': 'oven'},
                {'name': 'Microwave', 'id': 'microwave'},
                {'name': 'Living Room TV', 'id': 'tv_lr'},
                {'name': 'Bedroom TV', 'id': 'tv_bed'}],
                logs = logs)

# Entity update endpoint
@app.route("/update", methods=['POST'])
def update():
    # update db
    entity = Entity.query.filter_by(id=request.json['id']).first()
    entity.state = request.json['state']
    db.session.commit()

    entity_history = EntityHistory(time=dt.now(), entity_id=request.json['id'], type=entity.type, state=request.json['state'])
    db.session.add(entity_history)
    db.session.commit()

    # update client
    with app.app_context():
        if entity.is_sensor:
            turbo.push(turbo.replace(render_template('sensor_toggle.html', sensor=entity), request.json['id'] + '_tog'))
        turbo.push(turbo.replace(render_template('entity_icon.html', item=entity), request.json['id'] + '_icon'))

    # recalculate usage and update db
    c.updateDataToday()

    # respond OK
    return Response(status=200)

# HVAC update endpoint
@app.route("/update_hvac", methods=['POST'])
def update_hvac():
    # recalculate thermostat state
    c.updateThermostat()

    # get current thermostat state
    state = ThermostatHistory.query.order_by(ThermostatHistory.id.desc()).first()

    # get request args
    mode = request.json.setdefault('mode', None)
    temp_dir = request.json.setdefault('temp_dir', None)

    # change thermostat state based on inputs
    if mode is not None or temp_dir is not None:
        if mode is not None:
            th = ThermostatHistory(time=state.time, set_temp=state.set_temp, temp=state.temp, mode=mode, is_running=state.is_running)
        elif temp_dir is not None:
            if temp_dir == 'up':
                th = ThermostatHistory(time=state.time, set_temp = state.set_temp+1, temp=state.temp, mode=state.mode, is_running=state.is_running)
            elif temp_dir == 'down':
                th = ThermostatHistory(time=state.time, set_temp=state.set_temp-1, temp=state.temp, mode=state.mode, is_running=state.is_running)
            # update client
            turbo.push(turbo.replace(render_template_string('<div class="adjtemp" id="adjtemp">{{ set_temp }}&deg;F</div>', set_temp=th.set_temp), 'adjtemp'))
        
        # update db
        db.session.add(th)
        db.session.commit()
    return Response(status=200)

# Cycle endpoint
@app.route("/run_cycle", methods=['POST'])
def run_cycle():
    # get request args
    id = request.json['id']
    duration = td(hours=int(request.json['time_h']), minutes=int(request.json['time_m']), seconds=int(request.json['time_s']))

    # run cycle (updates usage)
    c.cycleRun(id, duration)
    return Response(status=200)

# Change graph month endpoint
@app.route("/change_graph_month", methods=['POST'])
def change_graph_month():
    # get request args
    month = c.MONTHS[request.json['month']]
    year = dt.now().year

    # plot selected month
    c.plotMonthSQL(year, month, request.json['month'])

    # update client
    turbo.push(turbo.replace(render_template_string('<img height="450" id="graph" src="{{ url_for(\'static\', filename=filename+\'.png\') }}" alt="">', filename=request.json['month']), 'graph'))
    return Response(status=200)

# start webserver
if __name__ == '__main__':
    app.run()
