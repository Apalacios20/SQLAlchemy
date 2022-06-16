import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import numpy as np
import pandas as pd
import scipy.stats as st
import datetime as dt


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"    
    )



@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query for precipitation values pertaining to the date
    recent_date = session.query(Measurement.date).\
    order_by(Measurement.date.desc()).first()

    most_recent_date = dt.datetime.strptime(recent_date[0], '%Y-%m-%d')
    query_date = dt.date(most_recent_date.year -1, most_recent_date.month, most_recent_date.day)

    tot = [Measurement.date,Measurement.prcp]
 
    queryresult = session.query(*tot).\
    filter(Measurement.date >= query_date).all()

    session.close()

    # Convert list of tuples into normal list
    
    date_prcp = {date: prcp for date, prcp in queryresult}

    return jsonify(date_prcp)



@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query for stations in dataset
    station_list = session.query(Measurement.station).distinct().\
    order_by(Measurement.station).all()

    session.close()

    # Convert list of tuples into normal list
    station_names = list(np.ravel(station_list))

    return jsonify(station_names)



@app.route("/api/v1.0/tobs")
def temperature():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    
    # Query to retrieve temperatures and dates for the most active station
    recent_date = session.query(Measurement.date).\
        order_by(Measurement.date.desc()).first()

    most_recent_date = dt.datetime.strptime(recent_date[0], '%Y-%m-%d')
    query_date = dt.date(most_recent_date.year -1, most_recent_date.month, most_recent_date.day)

    tot = Measurement.station, Measurement.tobs, Measurement.date

    most_a = session.query(*tot).\
        filter(Measurement.station == 'USC00519281').\
            filter(Measurement.date >= query_date).all()

    session.close()

    all_passengers = []
    for station, tobs, date in most_a:
        passenger_dict = {}
        passenger_dict["station"] = station
        passenger_dict["tobs"] = tobs
        passenger_dict["date"] = date
        all_passengers.append(passenger_dict)

    return jsonify(all_passengers)     

if __name__ == '__main__':
    app.run(debug=True)

