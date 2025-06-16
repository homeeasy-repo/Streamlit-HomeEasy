import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Client Requirements", page_icon="🏡", layout="wide")

# --- HEADER ---
st.markdown(
    """
    <style>
    .big-title { font-size:2.5rem; font-weight:700; color:#134074; }
    .subtitle { font-size:1.2rem; color:#333; }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown('<div class="big-title">🏡 Add Client Housing Requirement</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Provide all necessary details below. Fields with <span style="color:#ef476f">*</span> are required.</div>', unsafe_allow_html=True)
st.markdown("---")

# --- GET CLIENT ID FROM URL (if available) ---
params = st.query_params
client_id = params.get("client_id", [None])[0] if "client_id" in params else None
if client_id:
    st.markdown(f"**Client ID:** `{client_id}`")
st.markdown("")

# --- FORM LAYOUT ---
with st.form("req_form", clear_on_submit=False):
    # --- SECTION 1: Basic Info ---
    st.subheader("📝 Basic Information")
    c1, c2, c3, c4 = st.columns([1.3,1,1,1])

    with c1:
        move_in_date = st.date_input("Move-In Date*", value=datetime.today())
        max_move_in_date = st.date_input("Max Move-In Date (optional)")
        tour_date = st.date_input("Preferred Tour Date*")
    with c2:
        budget = st.number_input("Budget ($)*", min_value=0, step=100)
        max_budget = st.number_input("Max Budget ($)", min_value=0, step=100)
        sqft = st.number_input("Square Feet*", min_value=0, step=50)
        max_sqft = st.number_input("Max Square Feet", min_value=0, step=50)
    with c3:
        beds = st.selectbox("Bedrooms*", [1,2,3,4,5], index=0)
        baths = st.selectbox("Bathrooms*", [1,1.5,2,2.5,3,3.5,4], index=0)
        lease_term = st.slider("Lease Term (months)", 1, 36, 12)
    with c4:
        people_count = st.number_input("No. of Residents*", min_value=1, max_value=20, value=1, step=1)
        section8 = st.toggle("Section 8 Client?", value=False)
        rent_vs_condo = st.radio("Rental or Condo*", ["Rental","Condo"], horizontal=True)

    st.markdown("---")

    # --- SECTION 2: Location & Preferences ---
    with st.expander("📍 Location & Preferences", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            neighborhoods = st.text_input("Neighborhoods (comma separated)")
            amenities = st.text_input("Required Amenities")
            zip_codes = st.text_input("Zip Codes (comma separated)")
        with c2:
            parking = st.selectbox("Parking", ["Not specified", "Garage", "Street", "Lot"], index=0)
            parking_comment = st.text_area("Parking Notes")
            wd_pref = st.selectbox("Washer/Dryer Preference", ["Any","In-Unit","On-Site","None"], index=0)
            pet_policy = st.selectbox("Pet Policy", ["No preference","No Pets","Cats OK","Dogs OK"], index=0)
            pets_comment = st.text_area("Pet Notes")

    st.markdown("---")

    # --- SECTION 3: More Client Details ---
    with st.expander("👤 Additional Client Details", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            moving_reason = st.text_input("Reason for Moving")
            work_loc = st.text_input("Work Location")
            commute = st.text_input("Commute Preferences")
            personality = st.text_input("Client Personality")
            special_needs = st.text_area("Special Needs")
            building_must_haves = st.text_area("Building Must-Haves")
            unit_must_haves = st.text_area("Unit Must-Haves")
        with c2:
            monthly_income = st.number_input("Monthly Income ($)", min_value=0, step=100)
            credit_score = st.number_input("Credit Score", min_value=0, step=10)
            cosigner = st.checkbox("Requires Cosigner?")
            cosigner_comment = st.text_area("Cosigner Notes")
            additional_comments = st.text_area("Other Comments")

    st.markdown("---")

    # --- SECTION 4: Broker/Tour Info ---
    with st.expander("💼 Broker & Tour Details", expanded=False):
        c1, c2 = st.columns(2)
        with c1:
            other_broker = st.radio("Working with another broker?", ["No","Yes"], horizontal=True)
            other_broker_comments = st.text_area("If yes, provide details.")
        with c2:
            confirm_tour = st.radio("Tour Confirmed?", ["No","Yes"], horizontal=True)
            who_touring = st.text_input("Who will be touring?")

    st.markdown("---")

    # --- SECTION 5: Availability ---
    with st.expander("🕒 Client Weekly Availability", expanded=False):
        st.markdown("Specify available days and times for tours/calls.")
        days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        availability = {}
        for day in days:
            c1, c2, c3 = st.columns([1,2,2])
            with c1:
                available = st.checkbox(day, key=f"{day}_inc")
            with c2:
                start = st.time_input(f"{day} start", value=datetime.strptime("09:00", "%H:%M").time(), key=f"{day}_start")
            with c3:
                end = st.time_input(f"{day} end", value=datetime.strptime("17:00", "%H:%M").time(), key=f"{day}_end")
            availability[day] = {"available": available, "start": str(start), "end": str(end)}

    # --- SUBMIT ---
    st.markdown("")
    submit = st.form_submit_button("💾 Save Requirements", type="primary")

# --- ON SUBMIT: Show summary ---
if submit:
    # --- Simple required fields check (expand as needed) ---
    errors = []
    if not move_in_date: errors.append("Move-In Date is required.")
    if not tour_date: errors.append("Tour Date is required.")
    if not budget: errors.append("Budget is required.")
    if not sqft: errors.append("Square Feet is required.")
    if not beds: errors.append("Beds is required.")
    if not baths: errors.append("Baths is required.")

    if errors:
        st.error("Please fill all required fields:\n" + "\n".join(errors))
    else:
        st.success("✅ Requirements captured! (Ready to save to the database.)")
        st.markdown("### Requirements Summary")
        st.json({
            "Client ID": client_id,
            "Move-In": str(move_in_date),
            "Budget": f"${budget} - ${max_budget or 'N/A'}",
            "Beds/Baths": f"{beds} beds / {baths} baths",
            "Lease Term": lease_term,
            "Neighborhoods": neighborhoods,
            "Amenities": amenities,
            "Zip Codes": zip_codes,
            "Parking": parking,
            "Washer/Dryer": wd_pref,
            "Pet Policy": pet_policy,
            "Special Needs": special_needs,
            "People": people_count,
            "Tour Date": str(tour_date),
            "Section 8": section8,
            "Rental/Condo": rent_vs_condo,
            "Availability": availability,
        })

# --- Optional: Custom style tweaks ---
st.markdown(
    """
    <style>
    div[data-testid="column"] > div > div {
        background-color: #f8fafc;
        border-radius: 12px;
        padding: 1.3rem;
        margin-bottom: 1.2rem;
        border: 1px solid #e0e0e0;
    }
    .st-emotion-cache-13k62yr { font-size: 1.1rem; }
    </style>
    """, unsafe_allow_html=True
)
