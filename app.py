import numpy as np
import datetime as dt
import sqlalchemy
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    # """List all available api routes."""
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # 
    prev_year = dt.date(2017,8,23) - dt.timedelta(days = 365)

    # Perform a query to retrieve the data and precipitation scores
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_year).all()
    precipitation_data = {date:precipitation for date, precipitation in results}
    return jsonify(precipitation_data)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    station_q = session.query(Station.station).all()

    station = list(np.ravel(station_q))

    return jsonify(station)

@app.route("/api/v1.0/tobs")
def temps():
    # Create our session (link) from Python to the DB
    # Query the last 12 months of temperature observation data for the most active station in terms of number of temperature observations...
    prev_year = dt.date(2017,8,23) - dt.timedelta(days = 365)
    temperature = session.query(Measurement.station, Measurement.date, Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= prev_year)
    temp = list(np.ravel(temperature))

    return jsonify(temp)


@app.route("/api/v1.0/start_date")
@app.route("/api/v1.0/<start_date>/<last_date>")
def start_temp(start_date,last_date):

    results_recent = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date >= start_date).filter(Measurement.date <= last_date).all()
    results_past = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).filter(Measurement.date <= start_date).filter(Measurement.date <= last_date).all()
    temp_2 = list(np.ravel(results_recent))
    return jsonify(temp_2)





if __name__ == '__main__':
    app.run(debug=True)
