import streamlit as st
from datetime import datetime, time

st.set_page_config(page_title="Schedule Tour", layout="wide")

st.title("Schedule Tour for Sanda Potkrajac | 731602")

with st.expander("Instructions", expanded=False):
    st.markdown("""
    - Fill in the tour details for each building/unit the client wishes to visit.
    - Click **Add New Building to Tour** to add more buildings for the same tour.
    - All fields marked * are required.
    """)

# Store the number of building forms in session state
if "num_buildings" not in st.session_state:
    st.session_state["num_buildings"] = 1

# Option to add more building fields
if st.button("Add New Building to Tour", help="Add another building/unit to this tour"):
    st.session_state["num_buildings"] += 1

st.divider()

# Collect data for all building entries
schedule_data = []

for idx in range(st.session_state["num_buildings"]):
    with st.container(border=True):
        st.subheader(f"Building #{idx + 1}")
        col1, col2, col3 = st.columns([1,1,1.5])
        with col1:
            building = st.text_input(f"🏢 Building Name *", key=f"building_{idx}")
            unit_number = st.text_input("Unit #", key=f"unit_{idx}")
            price = st.number_input("Price", min_value=0.0, step=100.0, format="%.2f", key=f"price_{idx}")
        with col2:
            tour_date = st.date_input("Date *", value=datetime.today(), key=f"date_{idx}")
            tour_time = st.time_input("Time", value=time(10,0), key=f"time_{idx}")
            tour_type = st.selectbox(
                "Tour Type", 
                options=["Any", "In-Person", "Virtual", "Self Guided", "Videos Only"], 
                key=f"type_{idx}"
            )
        with col3:
            status = st.selectbox(
                "Status", 
                options=["Pending", "Confirmed", "Done", "Cancelled"], 
                key=f"status_{idx}",
            )
            booked_via = st.selectbox(
                "Booking Confirmed Via",
                options=["-----", "Phone", "Email", "Call", "Online"],
                key=f"booked_via_{idx}",
            )
            touring_rep = st.text_input("Touring Rep", key=f"touring_rep_{idx}")
            selected_by = st.selectbox(
                "Selected By",
                options=["Sales Rep", "Client", "Property"],
                key=f"selected_by_{idx}",
            )
        st.markdown("#### Leasing/Agent Details")
        col4, col5 = st.columns([1,1])
        with col4:
            leasing_agent = st.text_input("Leasing Agent Name", key=f"leasing_agent_{idx}")
            leasing_agent_email = st.text_input("Leasing Agent Email", key=f"leasing_agent_email_{idx}")
        with col5:
            leasing_agent_phone = st.text_input("Leasing Agent Phone", key=f"leasing_agent_phone_{idx}")
            comment = st.text_area("Comment", key=f"comment_{idx}", height=68)  # Updated height to meet minimum requirement
        # Save this building's data
        schedule_data.append({
            "building": building,
            "unit_number": unit_number,
            "price": price,
            "tour_date": str(tour_date),
            "tour_time": str(tour_time),
            "tour_type": tour_type,
            "status": status,
            "booked_via": booked_via,
            "touring_rep": touring_rep,
            "selected_by": selected_by,
            "leasing_agent": leasing_agent,
            "leasing_agent_email": leasing_agent_email,
            "leasing_agent_phone": leasing_agent_phone,
            "comment": comment,
        })
        st.divider()

# Main Close Confidence Score
close_conf = st.slider(
    "Close Confidence Score (0-100):",
    min_value=0, max_value=100, value=50,
    help="How much likely is the client to close while on tour? Rate from 0 to 100."
)

# --- SUBMIT ---
if st.button("Submit Schedule", type="primary"):
    # Here, you can process or save schedule_data and close_conf
    st.success("Tour schedule submitted!")
    st.write("Close Confidence Score:", close_conf)
    st.write("Tour Buildings Data:", schedule_data)
