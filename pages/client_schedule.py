import streamlit as st
from datetime import datetime, time
import psycopg2
import os
from dotenv import load_dotenv
import json

# Load environment variables
load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

st.set_page_config(page_title="Schedule Tour", page_icon="📅", layout="wide")

# Add custom CSS for better visual appeal (matching requirements page)
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
    .building-container {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #e1e5e9;
        margin-bottom: 15px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Get client_id from URL and fetch client info
params = st.query_params
client_id = params.get("client_id", [None])[0] if "client_id" in params else None
if client_id is not None:
    client_id = str(client_id)

# Fetch client name from database
client_name = "Unknown Client"
building_names = []  # List to store building names for suggestions

if client_id:
    try:
        conn = psycopg2.connect(DB_URL, sslmode='require')
        cur = conn.cursor()
        
        # Fetch client name
        cur.execute("SELECT fullname FROM client WHERE id = %s", (client_id,))
        result = cur.fetchone()
        if result:
            client_name = result[0]
        
        # Fetch all building names for suggestions from 'building' table
        try:
            cur.execute("""
                SELECT DISTINCT name 
                FROM building
                WHERE name IS NOT NULL 
                ORDER BY name
            """)
            building_results = cur.fetchall()
            building_names = [row[0] for row in building_results if row[0]]
        except Exception as building_error:
            st.warning(f"Could not fetch building suggestions: {building_error}")
            building_names = []
        
        cur.close()
        conn.close()
    except Exception as e:
        st.error(f"Error fetching client info: {e}")

# Wrap the form in a styled container
st.markdown('<div class="form-container">', unsafe_allow_html=True)
st.markdown(f'<div class="form-title">📅 Schedule Tour for {client_name} | {client_id or "No ID"}</div>', unsafe_allow_html=True)

with st.expander("Instructions", expanded=False):
    st.markdown("""
    - Fill in the tour details for each building/unit the client wishes to visit.
    - Click **Add New Building to Tour** to add more buildings for the same tour.
    - All fields marked * are required.
    - **Building Name**: Select from existing buildings in the database or choose 'Enter Custom Building' to add a new one.
    """)

# Display building suggestions count if available
if building_names:
    st.info(f"💡 {len(building_names)} building suggestions are available in the dropdown.")

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
    st.markdown('<div class="building-container">', unsafe_allow_html=True)
    st.subheader(f"🏢 Building #{idx + 1}")
    col1, col2, col3 = st.columns([1,1,1.5])
    with col1:
        # Building name with improved dropdown suggestions
        if building_names:
            # Create a more user-friendly dropdown with search functionality
            building_options = building_names + ["-- Enter Custom Building --"]
            
            # Use selectbox with index to make first building the default
            selected_building = st.selectbox(
                f"Building Name *", 
                options=building_options,
                index=0,  # Default to first building in list
                key=f"building_select_{idx}",
                help="🔍 Search and select from existing buildings in the database, or choose 'Enter Custom Building' to add a new one"
            )
            
            if selected_building == "-- Enter Custom Building --":
                building = st.text_input(
                    "Custom Building Name *", 
                    key=f"building_custom_{idx}",
                    help="Enter the building name manually",
                    placeholder="Type new building name here..."
                )
            else:
                building = selected_building
                # Show a small info about the selected building
                st.caption(f"✅ Selected: {selected_building}")
        else:
            # Fallback to text input if no building data available
            building = st.text_input(
                f"Building Name *", 
                key=f"building_{idx}", 
                help="Required field - No building suggestions available",
                placeholder="Enter building name..."
            )
        
        unit_number = st.text_input("Unit #", key=f"unit_{idx}")
        price = st.number_input("Price ($)", min_value=0.0, step=100.0, format="%.2f", key=f"price_{idx}")
    with col2:
        tour_date = st.date_input("Date *", value=datetime.today(), key=f"date_{idx}", help="Required field")
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
    st.markdown("#### 👤 Leasing/Agent Details")
    col4, col5 = st.columns([1,1])
    with col4:
        leasing_agent = st.text_input("Leasing Agent Name", key=f"leasing_agent_{idx}")
        leasing_agent_email = st.text_input("Leasing Agent Email", key=f"leasing_agent_email_{idx}")
    with col5:
        leasing_agent_phone = st.text_input("Leasing Agent Phone", key=f"leasing_agent_phone_{idx}")
        comment = st.text_area("Comment", key=f"comment_{idx}", height=68)
    # Save this building's data
    schedule_data.append({
        "client_id": client_id,
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
    st.markdown('</div>', unsafe_allow_html=True)
    if idx < st.session_state["num_buildings"] - 1:
        st.divider()

# Function to save schedule data to database
def save_schedule_to_db(schedule_data, close_conf):
    """Save tour schedule data to database"""
    try:
        conn = psycopg2.connect(DB_URL, sslmode='require')
        cur = conn.cursor()
        
        for building_data in schedule_data:
            # Insert or update schedule data (you may need to adjust table name and columns)
            query = """
                INSERT INTO client_schedule (
                    client_id, building_name, unit_number, price, tour_date, tour_time,
                    tour_type, status, booked_via, touring_rep, selected_by,
                    leasing_agent_name, leasing_agent_email, leasing_agent_phone,
                    comment, close_confidence, created_at
                ) VALUES (
                    %(client_id)s, %(building)s, %(unit_number)s, %(price)s, %(tour_date)s, %(tour_time)s,
                    %(tour_type)s, %(status)s, %(booked_via)s, %(touring_rep)s, %(selected_by)s,
                    %(leasing_agent)s, %(leasing_agent_email)s, %(leasing_agent_phone)s,
                    %(comment)s, %s, NOW()
                )
            """
            # Add close_confidence to each building record
            building_data_with_conf = building_data.copy()
            cur.execute(query, (*building_data_with_conf.values(), close_conf))
        
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Database error: {e}")
        # Fallback: save to JSON file like requirements page
        try:
            schedule_record = {
                "client_id": client_id,
                "close_confidence": close_conf,
                "buildings": schedule_data,
                "created_at": datetime.now().isoformat()
            }
            with open("client_schedules.json", "a") as file:
                file.write(json.dumps(schedule_record) + "\n")
            return True
        except Exception as json_error:
            st.error(f"Failed to save to file: {json_error}")
            return False

# Validation function
def validate_schedule_data(schedule_data):
    """Validate required fields in schedule data"""
    errors = []
    for idx, building in enumerate(schedule_data):
        building_name = building["building"].strip() if building["building"] else ""
        if not building_name or building_name == "-- Enter Custom Building --":
            errors.append(f"Building #{idx + 1}: Building name is required")
        if not building["tour_date"]:
            errors.append(f"Building #{idx + 1}: Tour date is required")
    return errors

# Main Close Confidence Score
st.divider()
close_conf = st.slider(
    "🎯 Close Confidence Score (0-100):",
    min_value=0, max_value=100, value=50,
    help="How likely is the client to close while on tour? Rate from 0 to 100."
)

# --- SUBMIT ---
if st.button("📅 Submit Schedule", type="primary"):
    # Validate form data
    validation_errors = validate_schedule_data(schedule_data)
    
    if validation_errors:
        st.error("❌ Please fix the following errors:")
        for error in validation_errors:
            st.error(f"• {error}")
    elif not client_id:
        st.error("❌ No client ID provided. Please access this page from the client list.")
    else:
        # Save to database
        success = save_schedule_to_db(schedule_data, close_conf)
        if success:
            st.success("✅ Tour schedule saved successfully!")
            st.balloons()
            # Optionally display summary
            with st.expander("📋 Schedule Summary", expanded=False):
                st.write(f"**Client:** {client_name} (ID: {client_id})")
                st.write(f"**Close Confidence Score:** {close_conf}%")
                st.write(f"**Number of Buildings:** {len(schedule_data)}")
                for idx, building in enumerate(schedule_data):
                    if building["building"]:
                        st.write(f"**Building #{idx + 1}:** {building['building']} - {building['tour_date']} at {building['tour_time']}")
        else:
            st.error("❌ Failed to save schedule. Please try again.")

st.markdown('</div>', unsafe_allow_html=True)  # Close the container
