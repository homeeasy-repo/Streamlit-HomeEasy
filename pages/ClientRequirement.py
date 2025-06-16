"""
Client Requirements Page

This page allows users to input and manage client housing requirements.
"""

import streamlit as st
import pandas as pd
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Client Requirements",
    page_icon="📋",
    layout="wide"
)

# Page header with styling
st.title("Client Housing Requirements")
st.markdown("Enter detailed housing requirements for your clients")

# Get client ID from URL parameter or dropdown
params = st.query_params
client_id = params.get("client_id", [None])[0]

if not client_id:
    # Create a mock client list for demonstration
    demo_clients = [
        {"id": "CL001", "name": "John Doe"},
        {"id": "CL002", "name": "Jane Smith"},
        {"id": "CL003", "name": "Robert Johnson"}
    ]
    
    selected_client = st.selectbox(
        "Select Client",
        options=[f"{client['id']} - {client['name']}" for client in demo_clients],
        index=0
    )
    
    client_id = selected_client.split(" - ")[0]

st.subheader(f"Requirements for Client: {client_id}")

# Create tabs for different sections
tab1, tab2, tab3 = st.tabs(["Basic Requirements", "Property Details", "Schedule & Notes"])

with tab1:
    col1, col2 = st.columns(2)
    
    with col1:
        move_in_date = st.date_input("Move-in Date", datetime.today())
        budget = st.number_input("Budget ($)", min_value=0, value=2000, step=100)
        max_budget = st.number_input("Maximum Budget ($)", min_value=0, value=2500, step=100)
        
    with col2:
        beds = st.slider("Bedrooms", 0, 5, 2)
        baths = st.slider("Bathrooms", 0.0, 5.0, 1.0, 0.5)
        lease_term = st.slider("Lease Term (months)", 1, 24, 12)

with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        neighborhoods = st.multiselect(
            "Preferred Neighborhoods",
            ["Downtown", "Midtown", "Uptown", "Westside", "Eastside"]
        )
        
        amenities = st.multiselect(
            "Required Amenities",
            ["Pool", "Gym", "Covered Parking", "Pet Friendly", "Elevator", "Doorman", "Rooftop", "Laundry"]
        )
        
    with col2:
        parking = st.radio("Parking", ["Required", "Preferred", "Not needed"])
        
        pet_policy = st.selectbox(
            "Pet Policy",
            ["No Pets", "Cats Only", "Small Dogs Only", "All Pets Welcome"]
        )
        
        special_requirements = st.text_area("Special Requirements")

with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        # Availability table
        st.subheader("Client Availability")
        
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        availability = {}
        
        for day in days:
            col_day, col_avail = st.columns([1, 3])
            with col_day:
                st.write(day)
            with col_avail:
                available = st.checkbox("Available", key=f"avail_{day}")
                if available:
                    time_range = st.select_slider(
                        f"Time Range for {day}",
                        options=["Morning", "Afternoon", "Evening", "All Day"],
                        value="All Day",
                        key=f"time_{day}"
                    )
                    availability[day] = time_range
    
    with col2:
        # Additional notes
        tour_notes = st.text_area("Tour Notes")
        agent_notes = st.text_area("Agent Notes (Private)")

# Save button with success message
if st.button("Save Requirements", type="primary"):
    # Mock saving data
    st.success("Client requirements saved successfully!")
    
    # Show a summary of the data
    st.subheader("Summary of Requirements")
    
    summary_data = {
        "Client ID": client_id,
        "Move-in Date": move_in_date,
        "Budget Range": f"${budget} - ${max_budget}",
        "Size": f"{beds} bed, {baths} bath",
        "Lease Term": f"{lease_term} months",
        "Neighborhoods": ", ".join(neighborhoods) if neighborhoods else "Any",
        "Top Amenities": ", ".join(amenities[:3]) if amenities else "None specified"
    }
    
    # Display as a nice table
    st.table(pd.DataFrame([summary_data]).set_index("Client ID"))
