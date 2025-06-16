# pages/client_requirement.py

import streamlit as st
import psycopg2
import json
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

# 1️⃣ Read URL query-params
params    = st.experimental_get_query_params()
client_id = params.get("client_id", [None])[0]
action    = params.get("action",    ["requirement"])[0]

if not client_id:
    st.error("No client_id provided in the URL.")
    st.stop()

st.title(f"Add Requirement for {client_id}")

# 2️⃣ Build the form with all your fields
with st.form("req_form"):
    # Required fields
    move_in_date      = st.date_input("Move in Date *",     key="move_in")
    max_move_in_date  = st.date_input("Max Move in Date",    key="max_move")
    tour_date         = st.date_input("Preferred Tour Date *", key="tour_date")

    budget            = st.number_input("Budget *",           min_value=0, key="budget")
    max_budget        = st.number_input("Max Budget",         min_value=0, key="max_budget")

    sqft              = st.number_input("Square Feet *",      min_value=0, key="sqft")
    max_sqft          = st.number_input("Max Square Feet",    min_value=0, key="max_sqft")

    beds              = st.number_input("Beds *",              min_value=0, key="beds")
    baths             = st.number_input("Baths *",             min_value=0.0, step=0.5, key="baths")

    lease_term        = st.number_input("Lease Term (months)", min_value=0, key="lease_term")
    neighborhoods     = st.text_input("Only buildings in the specified neighborhoods", key="neigh")
    section8          = st.checkbox("Section 8 Client",      key="sec8")

    parking           = st.selectbox("Parking", ["", "Garage", "Street", "Lot"], key="parking")
    pet_policy        = st.selectbox("Pet Policy", ["", "No Pets", "Cats OK", "Dogs OK"], key="pet_policy")
    wd_pref           = st.selectbox("WD Preference", ["Any","In-Unit","On-Site","None"], key="wd")

    parking_comment   = st.text_area("Parking Comment",      key="park_comment")
    pets_comment      = st.text_area("Pets Comment",         key="pet_comment")

    # … continue for all fields …  
    # Neighborhood, Amenities, Zip Code
    neighborhoods_txt = st.text_input("Neighborhood",       key="neigh_txt")
    amenities         = st.text_input("Amenities",          key="amenities")
    zip_codes         = st.text_input("Zip Code",           key="zips")

    additional_comments = st.text_area("Additional Comments", key="add_comments")
    people_count        = st.number_input("Number of people",   min_value=1, key="people")
    moving_reason       = st.text_input("Moving Reason",       key="mv_reason")
    work_loc            = st.text_input("Work Location",      key="work_loc")
    commute             = st.text_input("Commute",             key="commute")

    # Rental vs Condo, Personality, Must-haves, etc.
    rent_vs_condo       = st.selectbox("Rental vs Condo Preference?", ["Rental","Condo"], key="rvsc")
    personality         = st.text_input("Client Personality Details", key="pers")
    building_must_haves = st.text_area("Building must haves", key="bldg_must")
    unit_must_haves     = st.text_area("Unit must haves",    key="unit_must")
    special_needs       = st.text_area("Special Needs",       key="spec_needs")

    # Broker questions
    other_broker        = st.selectbox("Working with another broker?", ["","Yes","No"], key="other_broker")
    other_broker_comments = st.text_area("Another broker comments", key="broker_comments")
    confirm_tour        = st.selectbox("Did they confirm to tour?", ["","Yes","No"], key="confirm_tour")
    who_touring         = st.text_input("Who will be touring?", key="who_tour")

    # Income, Credit, Cosigner
    monthly_income      = st.number_input("Monthly Income", min_value=0, key="income")
    credit_score        = st.number_input("Credit Score",  min_value=0, key="credit")
    cosigner            = st.checkbox("Cosigner", key="cosigner")
    cosigner_comment    = st.text_area("Cosigner Comment", key="cosigner_comment")

    # Availability: Monday–Sunday
    st.markdown("**Availability**")
    availability = {}
    for day in ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]:
        c1, c2, c3 = st.columns([1,2,2])
        with c1:
            include = st.checkbox(day, key=f"{day}_inc")
        with c2:
            start = st.time_input(f"{day} start", key=f"{day}_start")
        with c3:
            end   = st.time_input(f"{day} end",   key=f"{day}_end")
        availability[day] = {"include": include, "start": str(start), "end": str(end)}

    submit = st.form_submit_button("Save and Search")

# 3️⃣ On submit: write into Postgres
if submit:
    try:
        conn = psycopg2.connect(DB_URL, sslmode="require")
        cur  = conn.cursor()
        cur.execute("""
            INSERT INTO client_requirements (
              client_id, move_in_date, max_move_in_date, preferred_tour_date,
              budget, max_budget, sqft, max_sqft, beds, baths,
              lease_term, only_neighborhoods, section8, parking, pet_policy, wd_pref,
              parking_comment, pets_comment, neighborhoods_txt, amenities, zip_codes,
              additional_comments, people_count, moving_reason, work_loc, commute,
              rent_vs_condo, personality, building_must_haves, unit_must_haves, special_needs,
              other_broker, other_broker_comments, confirm_tour, who_touring,
              monthly_income, credit_score, cosigner, cosigner_comment,
              availability_json, created_on
            )
            VALUES (
              %(client_id)s, %(move_in_date)s, %(max_move_in_date)s, %(preferred_tour_date)s,
              %(budget)s, %(max_budget)s, %(sqft)s, %(max_sqft)s, %(beds)s, %(baths)s,
              %(lease_term)s, %(only_neighborhoods)s, %(section8)s, %(parking)s, %(pet_policy)s, %(wd_pref)s,
              %(parking_comment)s, %(pets_comment)s, %(neighborhoods_txt)s, %(amenities)s, %(zip_codes)s,
              %(additional_comments)s, %(people_count)s, %(moving_reason)s, %(work_loc)s, %(commute)s,
              %(rent_vs_condo)s, %(personality)s, %(building_must_haves)s, %(unit_must_haves)s, %(special_needs)s,
              %(other_broker)s, %(other_broker_comments)s, %(confirm_tour)s, %(who_touring)s,
              %(monthly_income)s, %(credit_score)s, %(cosigner)s, %(cosigner_comment)s,
              %(availability_json)s, NOW()
            )
        """, {
            "client_id": client_id,
            "move_in_date": move_in_date,
            "max_move_in_date": max_move_in_date,
            "preferred_tour_date": tour_date,
            "budget": budget,
            "max_budget": max_budget,
            "sqft": sqft,
            "max_sqft": max_sqft,
            "beds": beds,
            "baths": baths,
            "lease_term": lease_term,
            "only_neighborhoods": neighborhoods,
            "section8": section8,
            "parking": parking,
            "pet_policy": pet_policy,
            "wd_pref": wd_pref,
            "parking_comment": parking_comment,
            "pets_comment": pets_comment,
            "neighborhoods_txt": neighborhoods_txt,
            "amenities": amenities,
            "zip_codes": zip_codes,
            "additional_comments": additional_comments,
            "people_count": people_count,
            "moving_reason": moving_reason,
            "work_loc": work_loc,
            "commute": commute,
            "rent_vs_condo": rent_vs_condo,
            "personality": personality,
            "building_must_haves": building_must_haves,
            "unit_must_haves": unit_must_haves,
            "special_needs": special_needs,
            "other_broker": other_broker,
            "other_broker_comments": other_broker_comments,
            "confirm_tour": confirm_tour,
            "who_touring": who_touring,
            "monthly_income": monthly_income,
            "credit_score": credit_score,
            "cosigner": cosigner,
            "cosigner_comment": cosigner_comment,
            "availability_json": json.dumps(availability),
        })
        conn.commit()
        cur.close()
        conn.close()
        st.success("Requirements saved!")
    except Exception as e:
        st.error(f"Failed to save: {e}")
