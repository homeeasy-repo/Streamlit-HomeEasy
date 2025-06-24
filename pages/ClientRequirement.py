import streamlit as st
from datetime import datetime, time
from pages.save_to_db import save_to_db  # Changed to absolute import

st.set_page_config(page_title="Client Requirements", page_icon="🏡", layout="wide")

# Add custom CSS for better visual appeal
st.markdown(
    """
    <style>
    .form-container {
        background-color: #f9f9f9;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .form-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        margin-bottom: 10px;
    }
    .form-section {
        margin-bottom: 20px;
    }
    .form-divider {
        border-top: 1px solid #ddd;
        margin: 20px 0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Wrap the form in a styled container
st.markdown('<div class="form-container">', unsafe_allow_html=True)
st.markdown('<div class="form-title">🏡 Add Client Housing Requirement</div>', unsafe_allow_html=True)

# Get client_id from URL
params = st.query_params
client_id = params.get("client_id", [None])[0] if "client_id" in params else None
if client_id is not None:
    client_id = str(client_id)  # Explicitly convert to string

# Debug: Log the client_id to verify its value
st.write(f"Debug: Retrieved client_id = {client_id}")

with st.form("req_form", clear_on_submit=False):
    st.subheader("📝 Basic Info")
    c1, c2, c3 = st.columns(3)
    with c1:
        move_in_date = st.date_input("Move-In Date*", value=datetime.today())
        move_in_date_max = st.date_input("Max Move-In Date (optional)")
        tour_date = st.date_input("Preferred Tour Date")
    with c2:
        budget = st.number_input("Budget ($)*", min_value=0, step=100)
        max_budget = st.number_input("Max Budget ($)", min_value=0, step=100)
        sqft = st.number_input("Square Feet*", min_value=0, step=50)
        sqft_max = st.number_input("Max Square Feet", min_value=0, step=50)
    with c3:
        beds = st.number_input("Bedrooms*", min_value=0, step=1)
        baths = st.number_input("Bathrooms*", min_value=0.0, step=0.5, value=0.0)  # Ensure all numerical arguments are floats
        lease_term = st.number_input("Lease Term (months)", min_value=0, step=1)

    st.divider()

    st.subheader("📍 Preferences")
    c1, c2 = st.columns(2)
    with c1:
        pets = st.selectbox("Pet Policy", options=[
            (-1, '------'), (4, "No Pet"), (0,"Has Pets"), (1,"Has Cats Only"), (2,"Has Dogs Only"), (3,"Has Dangerous Pets")
        ], format_func=lambda x: x[1])
        pets = pets[0]
        pets_comment = st.text_area("Pet Comments")
        washer_dryer = st.selectbox("Washer/Dryer Preference", options=[
            (0, "Any"), (1, "Yes"), (3, "No"), (4, "Select Units")
        ], format_func=lambda x: x[1])
        washer_dryer = washer_dryer[0]
        parking = st.selectbox("Parking", options=[
            (0, "------"), (1, "Yes"), (3, "No"), (4, "Select Units"), (5, "Assigned Parking"),
            (6,"Attached Parking"), (7,"Garage Parking"), (8, "Offsite Parking")
        ], format_func=lambda x: x[1])
        parking = parking[0]
        parking_comment = st.text_area("Parking Comments")
        amenities = st.multiselect("Amenities", options=[
            'air condition', 'gym', 'laundry', 'park', 'parking', 'pool', 'storage'
        ])
    with c2:
        zip_codes = st.text_input("Zip Codes (comma separated)")
        neighborhood = st.text_input("Neighborhoods (comma separated)")
        neighborhood_specific = st.checkbox("Only buildings in specified neighborhoods")
        special_needs = st.text_area("Special Needs")
        building_must_haves = st.text_area("Building Must-Haves")
        unit_must_haves = st.text_area("Unit Must-Haves")
        preference = st.selectbox("Rental vs Condo Preference", ["Rental", "Condo"])

    st.divider()

    st.subheader("👤 Client Info")
    c1, c2 = st.columns(2)
    with c1:
        personality = st.text_input("Client Personality")
        people_living = st.number_input("Number of People Living*", min_value=1, step=1, value=1)
        work_location = st.text_input("Work Location")
        commuting = st.text_input("Commuting Info")
        moving_reason = st.text_input("Moving Reason")
        comment = st.text_area("Other Comments")
    with c2:
        section8 = st.checkbox("Section 8 Client")
        monthly_income = st.number_input("Monthly Income", min_value=0, step=100)
        credit_score = st.number_input("Credit Score", min_value=0, step=10)
        cosigner = st.checkbox("Cosigner Required?")
        cosigner_comment = st.text_area("Cosigner Notes")

    st.divider()

    st.subheader("💼 Broker & Tour Info")
    c1, c2 = st.columns(2)
    with c1:
        another_broker = st.radio("Working with Another Broker?", ["No", "Yes"])
        another_broker_comment = st.text_area("Another Broker Comments")
    with c2:
        confirm_tour = st.radio("Tour Confirmed?", ["No", "Yes"])
        tour_person = st.text_input("Who will be touring?")

    st.divider()

    st.subheader("🕒 Weekly Availability")
    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    availability = {}
    for day in days:
        c1, c2, c3 = st.columns(3)
        with c1:
            available = st.checkbox(day, key=f"{day}_check")
        with c2:
            start = st.time_input(f"{day} start", value=time(9, 0), key=f"{day}_start")
        with c3:
            end = st.time_input(f"{day} end", value=time(17, 0), key=f"{day}_end")
        availability[day] = {"available": available, "start": start, "end": end}

    st.divider()

    # Submit
    submitted = st.form_submit_button("💾 Save")

# --- HANDLE SUBMIT ---
if submitted:
    if not all([move_in_date, budget, sqft, beds, baths]):
        st.error("❌ Required fields missing.")
    else:
        form_data = {
            "client_id": client_id if client_id else None,  # Keep client_id as a string
            "move_in_date": move_in_date,
            "move_in_date_max": move_in_date_max,
            "budget": budget,
            "budget_max": max_budget,
            "beds": int(beds),
            "baths": float(baths),
            "sqft": sqft,
            "sqft_max": sqft_max,
            "parking": str(parking),
            "pets": str(pets),
            "washer_dryer": str(washer_dryer),
            "zip": [z.strip() for z in zip_codes.split(",") if z.strip()],
            "neighborhood": [n.strip() for n in neighborhood.split(",") if n.strip()],
            "amenities": amenities,
            "comment": comment,
            "pets_comment": pets_comment,
            "parking_comment": parking_comment,
            "moving_reason": moving_reason,
            "work_location": work_location,
            "commuting": commuting,
            "people_living": int(people_living),
            "building_must_haves": building_must_haves,
            "unit_must_haves": unit_must_haves,
            "special_needs": special_needs,
            "preference": preference,
            "personality": personality,
            "another_broker": another_broker == "Yes",
            "another_broker_comment": another_broker_comment,
            "confirm_tour": confirm_tour == "Yes",
            "tour_person": tour_person,
            "availability": availability,
            "lease_term": lease_term,
            "section8": section8,
            "monthly_income": monthly_income,
            "credit_score": credit_score,
            "cosigner": cosigner,
            "cosigner_comment": cosigner_comment,
            "neighborhood_specific": neighborhood_specific,
            "tour_date": tour_date
        }

        success = save_to_db(form_data)
        if success:
            st.success("✅ Client requirements saved successfully.")
        else:
            st.error("❌ Failed to save requirements. Check logs.")

st.markdown('</div>', unsafe_allow_html=True)  # Close the container
