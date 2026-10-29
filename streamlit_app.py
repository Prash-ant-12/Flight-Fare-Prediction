import streamlit as st
import pickle
import pandas as pd
st.set_page_config(page_title="Flight Fare Prediction", page_icon="✈️")
@st.cache_resource
def load_model():
    with open("flight_rf.pkl","rb") as f: return pickle.load(f)
model=load_model()
st.title("✈️ Flight Fare Prediction")
from datetime import datetime

dep_date = st.date_input("Departure Date")
dep_time = st.time_input("Departure Time")

arr_date = st.date_input("Arrival Date")
arr_time = st.time_input("Arrival Time")

dep = datetime.combine(dep_date, dep_time)
arr = datetime.combine(arr_date, arr_time)
airline=st.selectbox("Airline",["Jet Airways","IndiGo","Air India","Multiple carriers","SpiceJet","Vistara","GoAir","Multiple carriers Premium economy","Jet Airways Business","Vistara Premium economy","Trujet","Air Asia"])
source=st.selectbox("Source",["Banglore","Delhi","Kolkata","Mumbai","Chennai"])
destination=st.selectbox("Destination",["Cochin","Delhi","New_Delhi","Hyderabad","Kolkata","Banglore"])
stops=st.selectbox("Total Stops",[0,1,2,3,4])
if st.button("Predict Fare"):
    jd,jm=dep.day,dep.month; dh,dm=dep.hour,dep.minute; ah,am=arr.hour,arr.minute
    mins=int(abs(arr-dep).total_seconds()//60); duh,dum=mins//60,mins%60
    air={k:0 for k in ["Air India","GoAir","IndiGo","Jet Airways","Jet Airways Business","Multiple carriers","Multiple carriers Premium economy","SpiceJet","Trujet","Vistara","Vistara Premium economy"]}
    if airline in air: air[airline]=1
    s={k:0 for k in["Chennai","Delhi","Kolkata","Mumbai"]}; 
    if source in s:s[source]=1
    d={k:0 for k in["Cochin","Delhi","Hyderabad","Kolkata","New_Delhi"]};
    if destination in d:d[destination]=1
    X=[[stops,jd,jm,dh,dm,ah,am,duh,dum,air["Air India"],air["GoAir"],air["IndiGo"],air["Jet Airways"],air["Jet Airways Business"],air["Multiple carriers"],air["Multiple carriers Premium economy"],air["SpiceJet"],air["Trujet"],air["Vistara"],air["Vistara Premium economy"],s["Chennai"],s["Delhi"],s["Kolkata"],s["Mumbai"],d["Cochin"],d["Delhi"],d["Hyderabad"],d["Kolkata"],d["New_Delhi"]]]
    p=model.predict(X)[0]
    st.success(f"Estimated Flight Fare: ₹ {p:,.2f}")
