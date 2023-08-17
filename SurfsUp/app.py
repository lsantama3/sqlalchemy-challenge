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
measurement = Base.classes.measurement
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
        f"Hello, this is thethe Homepage for Hawaiian Climate Analysis. The avaliable routes are listed below.<br/>"
        f"Precipitation Analysis for the Previous 12 Months:<br/>"
        f"/api/v1.0/precipitation <br/>"
        f"List of Stations:<br/>"
        f"/api/v1.0/stations <br/>"
        f"Dates and Temperature Observations of the Most-Active Station for the Previous Year of Data:<br/>"
        f"/api/v1.0/tobs <br/>"
        f"List of the Minimum Temperature, the Average Temperature, and the Maximum Temperature for a Specified Start or Start-End Range.<br/>"
        f"Temperature Data Based On Start Date:<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd] <br/>"
        f"Temperature Data Based On Specified Date Range:<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd] <br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    results = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= "2016-08-23").\
        all()

    session.close()
    
    prcp_data = []
    for date,prcp  in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
               
        prcp_data.append(prcp_dict)

    return jsonify(prcp_data)

@app.route("/api/v1.0/stations")
def stations():
    
    results = session.query(station.station).\
                 order_by(station.station).all()

    session.close()

   
    stations_list = list(np.ravel(results))

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():
 
    results = session.query(measurement.date,  measurement.tobs,measurement.prcp).\
                filter(measurement.date >= '2016-08-24').\
                filter(measurement.station=='USC00519281').\
                order_by(measurement.date).all()

    session.close()
    
    tobs_list = []
    for prcp, date,tobs in results:
       tobs_dict = {}
       tobs_dict["prcp"] = prcp
       tobs_dict["date"] = date
       tobs_dict["tobs"] = tobs
       
       tobs_list.append(tobs_dict)

       return jsonify(tobs_list)
   
@app.route("/api/v1.0/<start_date>")
def Start_date(start_date):

    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
                filter(measurement.date >= start_date).all()

    session.close()

    # Create a dictionary from the row data and append to a list of start_date_tobs
    start_date_tobs = []
    for min, avg, max in results:
        start_date_tobs_dict = {}
        start_date_tobs_dict["min_temp"] = min
        start_date_tobs_dict["avg_temp"] = avg
        start_date_tobs_dict["max_temp"] = max
        start_date_tobs.append(start_date_tobs_dict) 
    return jsonify(start_date_tobs)

@app.route("/api/v1.0/<start_date>/<end_date>")
def Start_end_date(start_date, end_date):

    results = session.query(func.min(measurement.tobs), func.avg(measurement.tobs), func.max(measurement.tobs)).\
                filter(measurement.date >= start_date).filter(measurement.date <= end_date).all()

    session.close()
  
    # Create a dictionary from the row data and append to a list of start_end_date_tobs
    start_end_tobs = []
    for min, avg, max in results:
        start_end_tobs_dict = {}
        start_end_tobs_dict["min_temp"] = min
        start_end_tobs_dict["avg_temp"] = avg
        start_end_tobs_dict["max_temp"] = max
        start_end_tobs.append(start_end_tobs_dict) 
    

    return jsonify(start_end_tobs)

if __name__ == "__main__":
    app.run(debug=False)    
