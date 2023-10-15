# Import the dependencies.
import numpy as np

import sqlalchemy
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
Base.prepare(autoload_with=engine)

# Save references to each table
measurement= Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
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
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/####-##-##<br>"
        f"/api/v1.0/####-##-##/####-##-##"
    )


@app.route("//api/v1.0/precipitation")
def precipitation():

    session = Session(engine)

    
    one_year_eariler = session.query(func.date(func.date("2017-08-23"), "-365 days")).scalar()

    # Perform a query to retrieve the data and precipitation scores
    filtered = session.query(measurement.date, measurement.prcp) \
    .filter(measurement.date >= one_year_eariler) \
    .all()  

    session.close()

    precipitation_data  = {date: prcp for date, prcp in filtered}

    return jsonify(precipitation_data )


@app.route("//api/v1.0/stations")
def stations():

    session = Session(engine)

    
    station_list = session.query(station.name).all()


    session.close()

    stations = [station[0] for station in station_list]

    return jsonify(stations)

@app.route("//api/v1.0/tobs")
def tobs():

    session = Session(engine)

    
    one_year_eariler = session.query(func.date(func.date("2017-08-23"), "-365 days")).scalar()

    unique_id = session.query(measurement.tobs, measurement.date).\
    filter(measurement.station == "USC00519281").\
    filter(measurement.date >= one_year_eariler).\
    all()
 

    session.close()

    unique_id_data  = {date: temp for date, temp in unique_id}

    return jsonify(unique_id_data )

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temperature(start, end=None):

    session = Session(engine)

    query = session.query(
        func.min(measurement.tobs).label('min_temp'),
        func.avg(measurement.tobs).label('avg_temp'),
        func.max(measurement.tobs).label('max_temp')
    ).filter(measurement.date >= start)
    if end:
        query = query.filter(measurement.date <= end)

  
    result = query.one()

    session.close()

    temperature_stats = {
        "min_temp": result.min_temp,
        "avg_temp": result.avg_temp,
        "max_temp": result.max_temp
    }

    return jsonify(temperature_stats)


if __name__ == '__main__':
    app.run(debug=True)