import random
from calendar import monthrange
from datetime import date, datetime, time, timedelta
from sqlite3 import IntegrityError

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from meteostat import Hourly, Point, units
from pandas.plotting import table
from sqlalchemy import (Column, Date, Float, MetaData, Table, create_engine,
                        select)
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.sql import func

from models import Data, DataToday, Entity, ThermostatHistory, db

mpl.use('Agg')

"""
	updateCurrentMonth will update the current month to the SQL to the current date and then estimate the rest of the month and graph it to monthGraph.png
	updateHistoric updates the historicdata table and the graphs it to historicGraph.png
	cycleRun takes an input time and will update the current date with the new usage values and then replot the month *unfinished*

	All other functions are helper functions for these two.
"""

MONTHS = {
	'Jan': 1,
	'Feb': 2,
	'Mar': 3,
	'Apr': 4,
	'May': 5,
	'Jun': 6,
	'Jul': 7,
	'Aug': 8,
	'Sep': 9,
	'Oct': 10,
	'Nov': 11,
	'Dec': 12
}

# Takes time inputs 1 and 2 and weekend
# returns time 1 if it is the weekend and 2 if it's not the weekend
# used for certain set parameters where something is used more or less if it is the weekend or not
def isWeekend(time1, time2, weekend):
	if weekend:
		return time1
	else:
		return time2

# All get usage functions take in time(in hours) and return kWh usage for that device

# Takes number of lights on n and time and returns electricity usage(kWh)
def getLightUsage(n, time):
	return (n * (time/60))/1000

# Bath fan electricity usage(kWh)
def getBathFanUsage(time):
	return (30 * time)/1000

# Microwave electricity usage(kWh)
def getMicrowaveUsage(time):
	return (1100 * time)/1000

# Stove electricity usage(kWh)
def getStoveUsage(time):
	return (3500 * time)/1000

# Oven electricity usage(kWh)
def getOvenUsage(time):
	return (4000 * time)/1000

# Fridge electricity usage(kWh)
def getRefrigeratorUsage(time):
	return (150 * time)/1000

# TV usage takes lving room TV time usage(timeL) and usage fro bedroom TV usage(timeB)
# returns combined electricity usage(kWh)
def getTVUsage(timeL, timeB):
	return ((636 * timeL)/1000) + ((100 * timeB)/1000) 

# Takes number of Dish Washer loads and returns electricity usage(kWh)
def getDishwasherEUsage(loads):
	time = loads * (45/60)
	return ((1800 * time)/1000) + getWaterheaterUsage(6) 

# Takes number of Dish Washer loads and returns water usage(gal)
def getDishwasherWUsage(loads):
	return loads * 6

# Takes number of Cloths washer loads and returns electricity usage(kWh)
def getClotheswasherEUsage(loads):
	time = loads * .5
	return ((500 * time)/1000) + getWaterheaterUsage(loads * 17)

# Takes number of Cloths washer loads and return water usage(gal)
def getClotheswasherWUsage(loads):
	return loads * 20

# Takes number of Cloths dryer loads and returns electricity usage(kWh) 
def getClothesdryerUsage(loads):
	time = loads * .5
	return (3000 * time)/1000

# Takes gallons of water heated and return electricity usage(kWh)
def getWaterheaterUsage(gal):
	time = gal * (4/60)
	return (45000 * time)/1000

# Takes number of showers and baths and returns electricity usage(kWh)
def getBathEUsage(showers, baths):
	return getWaterheaterUsage((showers * 16.25) + (baths * 19.5))

# Takes number of showers and baths and returns water usage(gal)
def getBathWUsage(showers, baths):
	return (showers * 25) + (baths * 30)

# Takes nubmer of toilet flushes and returns water usage(gal)
def getToiletUsage(flushes):
	return flushes * 1.6

# Takes number Garage door uses counting opens and closes and returns electricity usage(kWh)
def getGarageDoorUsage(uses):
	return (500 * uses)/1000

# Takes number of hours and returns the electricity usage(kWh) for stand by electricity usage
def getGarageInate(hours):
	return (1.5 * hours)/1000	

def outdoorTemp(location = Point(33.5667, -86.75, 196.0)):
    start = datetime.today() - timedelta(hours=1)
    end = datetime.today()
    data = Hourly(location, start, end)
    data.convert(units.imperial)
    temp = data.fetch().loc[:,"temp"].tolist()[0]
    return temp

# HVAC calculations
# Will update the docstring but fully functioning as is
def getHVAC(endTime, inTemp, temp, setTemp, doorOpen, windowOpen, startTime):
	timeE = 0
	runTime = 0
	running = False

	time = startTime
	while (time <= endTime):
		try:
			extTemp = temp[int((time//60)-1)]
		except IndexError:
			break
		if doorOpen:
			inTemp+= (2*((extTemp - inTemp)//10))/5
		if windowOpen:
			inTemp+= (((extTemp - inTemp)//10))/5
		else:
			inTemp+= (2*((extTemp - inTemp)//10))/60
		
		if (abs(inTemp - setTemp) >= 2):
			running = True

		if (running == True and abs(inTemp - setTemp) >= 1):
			inTemp+=(inTemp - setTemp)**0
			runTime+=1
		elif (running == True and abs(inTemp - setTemp) < 1):
			inTemp-=(inTemp - setTemp)
			runTime+=1
			running= False
		time+=1

	return (3500 * runTime/60)/1000, inTemp

# calculate current indoor temperature, as well as the current state of the hvac system
def getIndoorTemp(time_since_update, was_active, last_indoor_temp, set_temp, mode, outdoor_temp, door_open, window_open):
	is_active = was_active
	indoor_temp = last_indoor_temp
	while (time_since_update > 0):
		if mode == 'cool':
			if not is_active and indoor_temp >= (set_temp + 2):
					is_active = True
			if is_active:
				if indoor_temp > set_temp:
					indoor_temp -= 1
				elif indoor_temp <= set_temp:
					is_active = False
		elif mode == 'heat':
			if not is_active and indoor_temp <= (set_temp - 2):
				is_active = True
			if is_active:
				if indoor_temp < set_temp:
					indoor_temp += 1
				elif indoor_temp >= set_temp:
					is_active = False
		elif mode == 'off' and is_active:
			is_active = False
		if door_open:
			indoor_temp += (2*((outdoor_temp - indoor_temp)/10))/5
		if window_open:
			indoor_temp += (((outdoor_temp - indoor_temp)/10))/5
		else:
			indoor_temp += (2*((outdoor_temp - indoor_temp)/10))/60
		time_since_update-=1
	return indoor_temp, is_active

# update hvac information in the database
def updateThermostat():
	latest = ThermostatHistory.query.order_by(ThermostatHistory.id.desc()).first()
	time_since_update = ((datetime.now() - latest.time).total_seconds())//60
	door_open = any(entity.state == True for entity in Entity.query.filter(Entity.name == 'door').all())
	window_open = any(entity.state == True for entity in Entity.query.filter(Entity.name == 'window').all())
	indoor_temp, is_active = getIndoorTemp(time_since_update, latest.is_running, latest.temp, latest.set_temp, latest.mode, outdoorTemp(), door_open, window_open)
	if time_since_update >= 1:
		new = ThermostatHistory(time=datetime.now(), temp=indoor_temp, set_temp=latest.set_temp, mode=latest.mode, is_running=is_active)
		db.session.add(new)
		db.session.commit()
	return indoor_temp

# Calculates daily usage of electricity, water, and total cost using weekend(bool) if it is the weekend(Saturday or Sunday) == True else Fasle
# uses set use time from requirements doc when applicable *still needs set temp from sensor/dashboard*
def dailyUsage(weekend, date, loc):
	e = 0
	w = 0

	run = timedelta(hours = 24, minutes = 0)
	end = timedelta(hours = 8, minutes = 0)
	temp = Hourly(loc, date, date + run)
	temp = temp.fetch()
	temp = (temp.to_numpy()[:,0] * 9/5) + 32
	addE, inTemp = getHVAC(end / timedelta(minutes=1), 70, temp, 70, False, False, 0)

	start = end
	run = timedelta(hours = 0, minutes = 4)
	end = start + run
	addE, inTemp = getHVAC(end / timedelta(minutes=1), inTemp, temp, 70, True, False, start / timedelta(minutes=1))
	e+=addE

	start = end
	run = timedelta(hours = 8, minutes = 56)
	end = start + run
	addE, inTemp = getHVAC(end / timedelta(minutes=1), inTemp, temp, 70, False, False, start / timedelta(minutes=1))
	e+=addE

	start = end
	run = timedelta(hours = 0, minutes = 4)
	end = start + run
	addE, inTemp = getHVAC(end / timedelta(minutes=1), inTemp, temp, 70, True, False, start / timedelta(minutes=1))
	e+=addE

	start = end
	run = timedelta(hours = 6, minutes = 56)
	end = start + run
	addE, inTemp = getHVAC(end / timedelta(minutes=1), inTemp, temp, 70, False, False, start / timedelta(minutes=1))
	e+=addE


	if random.random() < 4/7:
		e += getClotheswasherEUsage(1) + getClothesdryerUsage(1)
		w += getClotheswasherWUsage(1)

	if random.random() < 4/7:
		e += getDishwasherEUsage(1) 
		w += getDishwasherWUsage(1)

	e += getMicrowaveUsage(isWeekend(.5, 20/60, weekend)) + getRefrigeratorUsage(24) + getStoveUsage(isWeekend(.5, 15/60, weekend)) + getOvenUsage(isWeekend(1, 45/60, weekend)) + getTVUsage(isWeekend(8, 4, weekend), isWeekend(4, 2, weekend)) \
	 + getBathEUsage(isWeekend(3, 2, weekend),isWeekend(3, 2, weekend)) + getGarageInate(24) + getGarageDoorUsage(isWeekend(2, 4, weekend))

	eCost = e * .12

	w += getBathWUsage(isWeekend(3, 2, weekend),isWeekend(3, 2, weekend))
	wCost = (w/748) * 2.52

	return [e, w, eCost + wCost]

# Takes in data to plot in the format [["Power Usage"], ["Water Usage"], ["Total Cost"]] each of those being and array of day to day totals of uniform length
# len(["Power Usage"]) == len(["Water Usage"]) == len(["Total Cost"])
# and takes estimated data for the remainder of the month 
# if est is not used: plotMonth(yourData)  assumes yourdata takes up the whole month
# plots data as solid lines red for power, blue for water, and green for cost and plots est(if needed) as dotted lines of the same colors
# returns the plot which can be shown using plot.show() or saved to a file using plot.savefig("fileName.format")
def plotMonth(data, est = [[]]):
	fig = plt.figure(figsize=(10, 5))
	ax = fig.add_subplot()
	ax.plot(np.arange(1,len(data[0]) + 1), data[0], color="red", label="Power Usage (kWh) ");
	ax.plot(np.arange(1,len(data[0]) + 1), data[1], color="blue", label="Water Usage (gal) ");
	ax.plot(np.arange(1,len(data[0]) + 1), data[2], color="green", label="Total Cost ($) ");

	if len(est[0]) > 0:
		est[0].insert(0,data[0][-1])
		est[1].insert(0,data[1][-1])
		est[2].insert(0,data[2][-1])
		range = np.arange(len(data[0]), len(data[0])+len(est[0]))
		ax.plot(range, est[0], color="red", linestyle="dotted");
		ax.plot(range, est[1], color="blue", linestyle="dotted");
		ax.plot(range, est[2], color="green", linestyle="dotted");
		ax.set_xticks(np.arange(1,len(data[0])+len(est[0])))
	else:
		ax.set_xticks(np.arange(1,len(data[0])+1))
	plt.xlabel("Day of The Month")
	plt.legend(bbox_to_anchor=(0, 1.02, 1, .2), loc="lower left", ncol=3, mode="expand")

	return plt

""" Plots the historic data as a table.
	Params: Pandas dataframe
	"""
def plotHistoric(df):
	fig, ax = plt.subplots(figsize=(14, 1.5)) 
	ax.set_axis_off() 
	 
	table(ax, df, loc="center left")

	return plt


# Calculates usage within given date range using the daily usage func
# Returns usage in [[eUsage],[wUsage],[totalCost]]
def rangeUsage(loc, dates):
	data = [[],[],[]]
	for i in dates:
		if i.weekday() < 5:
			weekend = False
		else:
			weekend = True
		u = dailyUsage(weekend, i, loc)
		data[0].append(u[0])
		data[1].append(u[1])
		data[2].append(u[2])
	return data

# Inserts given data with the given dates into the SQL server
def insertData(data, dates):
	insData = []
	for i in range(len(data[0])):
		insData.append({'date' : dates[i].to_pydatetime(), 
			'cost' : data[2][i],
			'e' : data[0][i],
			'w' : data[1][i]})

	stmt = insert(dataTable()).values(insData)
	stmt = stmt.on_conflict_do_update(
		index_elements=['date'],
		set_={'cost' : stmt.excluded.cost, 'e' : stmt.excluded.e, 'w' : stmt.excluded.w}
	)
	conn().execute(stmt)
	return

# Inserts given historic data with the given dates into the SQL server
def insertHistoricData(data,dates):
	insData = []
	for i in range(len(dates)):
		insData.append({'month' : dates[i], 
			'cost' : data[0][i],
			'e' : data[1][i],
			'w' : data[2][i]})
	try:
		conn().execute(historicTable().insert(), insData)
	except IntegrityError:
		pass
	return

# Returns the datatable object for SQL commands
def dataTable():
	metadata_obj = MetaData()
	return Table('data', metadata_obj,
	Column('date', Date, primary_key=True),
	Column('cost', Float),
	Column('e', Float),
	Column('w', Float))

# Returns the historicdata table object fro SQL commands
def historicTable():
	metadata_obj = MetaData()
	return Table('historicdata', metadata_obj,
		Column('month', Date, primary_key=True),
		Column('cost', Float),
		Column('e', Float),
		Column('w', Float))

# Pulls historic data from the database and then plots it
def drawHistoricSQL():
	s = select(historicTable())

	result = conn().execute(s)
	total_e = DataToday.query.with_entities(func.sum(DataToday.e).label('sum')).first().sum
	total_w = DataToday.query.with_entities(func.sum(DataToday.w).label('sum')).first().sum
	total_cost = DataToday.query.with_entities(func.sum(DataToday.cost).label('sum')).first().sum
	data = [[],[],[]]
	monthList = []
	for row in result:
		monthList.append(row[0].strftime("%b"))
		data[0].append(row[3])
		data[1].append(row[2])
		data[2].append(row[1])
	data[0][-1] += total_e
	data[1][-1] += total_w
	data[2][-1] += total_cost
	pTable = pd.DataFrame(data, ["Water Usage (gal)", "Power Usage (kWh)", "Total Cost ($)"], monthList)
	return plotHistoric(pTable)

# refreshes the historic SQL table then plots it and saves it
def updateHistoric(dataOnly = False):
	s = select(dataTable()).order_by(dataTable().c.date)

	result = conn().execute(s)
	month = -1
	currentMonth = 0
	data = [[],[],[]]
	dates = []
	for row in result:
		if row[0].month != currentMonth:
			currentMonth = row[0].month
			month+=1
			dates.append(row[0])
			data[0].append(0)
			data[1].append(0)
			data[2].append(0)
		data[0][month]+= row[1]
		data[1][month]+= row[2]
		data[2][month]+= row[3]

	conn().execute(historicTable().delete())
	insertHistoricData(data, dates)
	if not dataOnly:
		plt = drawHistoricSQL()
		plt.savefig("static/historicGraph.png", transparent=True) # save the figure here
	return dates, data

def getHistoricForTable():
	dates_raw, data_raw = updateHistoric(dataOnly=True)
	dates = []
	for i in range(len(dates_raw)):
		date = dates_raw[i].strftime("%b")
		water = round(data_raw[0][i],1)
		power = round(data_raw[1][i],1)
		total_cost = round(data_raw[2][i], 1)
		dates.append({'date' : date, 'water' : water, 'power' : power, 'cost' : total_cost})
		dates.sort(key=lambda x: MONTHS[x['date']])
	return dates


# Plots the months from SQL server in the given year and month 
def plotMonthSQL(year, month, filename='monthGraph'):
	s = select(dataTable())
	total_e = DataToday.query.with_entities(func.sum(DataToday.e).label('sum')).first().sum
	total_w = DataToday.query.with_entities(func.sum(DataToday.w).label('sum')).first().sum
	total_cost = DataToday.query.with_entities(func.sum(DataToday.cost).label('sum')).first().sum
	result = conn().execute(s)
	data=[[],[],[]]
	maxDay = 0
	for row in result:
		if row[0].month == month and row[0].year == year:
			maxDay+=1
			data[0].append(row[2])
			data[1].append(row[3])
			data[2].append(row[1])
	data[0][-1] += total_e
	data[1][-1] += total_w
	data[2][-1] += total_cost
	if (maxDay < monthrange(year, month)[1]):
		bham = point()
		start = datetime(year, month, maxDay+1)
		end = datetime(year, month, monthrange(year, month)[1])
		dates = pd.date_range(start, end)
		est = rangeUsage(bham, dates)

		plt = plotMonth(data, est)
		plt.savefig(f"static/{filename}.png", transparent=True) # save the figure here
	else:
		plt = plotMonth(data)
		plt.savefig(f"static/{filename}.png", transparent=True) # save the figure here

# Updates the SQL to the current date and estimates for the rest
def updateMonth(year, month, day = None):
	if not day:
		day = monthrange(year, month)[1]
	s = select(dataTable())

	result = conn().execute(s)
	data=[[],[],[]]
	maxDay = 0

	for row in result:
		if row[0].month == month and row[0].year == year:
			maxDay+=1
			
	if maxDay < day:
		newDates = pd.date_range(datetime(year, month, maxDay + 1), datetime(year, month, day))
		newData = rangeUsage(point(), newDates)

		for i in range(len(newData[0])):
			data[0].append(newData[0][i])
			data[1].append(newData[1][i])
			data[2].append(newData[2][i])

		insertData(data, newDates)

# calculate data for current month
def updateCurrentMonth():
	updateMonth(datetime.now().year, datetime.now().month, datetime.now().day)

# calculate usage for today, up to the current time
def updateDataToday():
	latest = DataToday.query.order_by(DataToday.datetime.desc()).first()
	if latest.datetime.date() != date.today():
		total_e = DataToday.query.with_entities(func.sum(DataToday.e).label('sum')).first().sum
		total_w = DataToday.query.with_entities(func.sum(DataToday.w).label('sum')).first().sum
		total_cost = DataToday.query.with_entities(func.sum(DataToday.cost).label('sum')).first().sum
		day = Data.query.filter_by(date=latest.datetime.date()).first()
		day.e += total_e
		day.w += total_w
		day.cost += total_cost
		DataToday.query.delete()
		db.session.commit()
		last_time = datetime.combine(date.today(), time(0,0,0))
	else:
		last_time = latest.datetime
	minutes_since_updated = (datetime.now() - last_time).total_seconds() / 60
	entities = Entity.query.all()
	n_lights_on = 0
	n_showers_on = 0
	bed_tv_is_on = False
	lr_tv_is_on = False

	for entity in entities:
		if entity.type == 'light' and entity.state:
			n_lights_on += 1
		elif entity.type == 'shower' and entity.state:
			n_showers_on += 1
		elif entity.type == 'tv' and entity.name == 'Master Bed TV' and entity.state:
			bed_tv_is_on = True
		elif entity.type == 'tv' and entity.name == 'Living Room TV' and entity.state:
			lr_tv_is_on = True

	e = 0
	w = 0
	cost = 0

	e += getLightUsage(n_lights_on, minutes_since_updated)
	e += getTVUsage(minutes_since_updated if lr_tv_is_on else 0, minutes_since_updated if bed_tv_is_on else 0)
	e += getBathEUsage((minutes_since_updated/15)*n_showers_on, 0)
	w += getBathWUsage((minutes_since_updated/15)*n_showers_on, 0)

	cost = (e * .12) + ((w/748) * 2.52)

	data = DataToday(datetime=datetime.now(), e=e, w=w, cost=cost)
	db.session.add(data)
	db.session.commit()

# run cycle for time, updates db with usage
def cycleRun(cycle: str, time: timedelta):
	minutes = time.total_seconds() / 60
	hours = minutes / 60
	laundry_loads = minutes / 30
	dishes_loads = minutes / 45
	showers = minutes / 15
	baths = minutes / 20
	e = None
	w = None
	if cycle == 'washer':
		e = getClotheswasherEUsage(laundry_loads)
		w = getClotheswasherWUsage(laundry_loads)
	elif cycle == 'dryer':
		e = getClothesdryerUsage(laundry_loads)
	elif cycle == 'dishwasher':
		e = getDishwasherEUsage(dishes_loads)
		w = getDishwasherWUsage(dishes_loads)
	elif cycle == 'shower':
		e = getBathEUsage(showers, 0)
		w = getBathWUsage(showers, 0)
	elif cycle == 'bath':
		e = getBathEUsage(0, baths)
		w = getBathWUsage(0, baths)
	elif cycle == 'stove':
		e = getStoveUsage(hours)
	elif cycle == 'oven':
		e = getOvenUsage(hours)
	elif cycle == 'microwave':
		e = getMicrowaveUsage(hours)
	elif cycle == 'tv_lr':
		e = getTVUsage(hours, 0)
	elif cycle == 'tv_bed':
		e = getTVUsage(0, hours)
	today = Data.query.filter_by(date = date.today()).first()
	#today = list(filter(lambda x: x.date.date() == datetime.today().date(), today))[0]
	if today:
		if e is not None:
			eCost = e * .12
			today.e += e
			today.cost += eCost
		if w is not None:
			wCost = (w/748) * 2.52
			today.w += w
			today.cost += wCost

		db.session.commit()

		

# Gets the connection to the SQL server
def conn():
	engine = create_engine('postgresql://Team7:Team7@138.26.48.83:5432/Team7DB')
	metadata_obj = MetaData()
	return engine.connect()

# Location for Birmingham for waether API can be changed 
def point():
	return Point(33.5667, -86.75, 196.0)
