import streamlit as st
from datetime import datetime

st.set_page_config(page_title="Revenue Entry", page_icon="💸", layout="wide")

st.markdown("""
    <style>
    .main-header { font-size:2.2rem; font-weight:700; color:#145DA0; }
    .section-title { color:#1E6091; font-weight:600; font-size:1.2rem; }
    .st-emotion-cache-13k62yr { font-size: 1.1rem; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">💸 New Revenue Entry</div>', unsafe_allow_html=True)
st.caption("Fill in all details about the closed/won deal for proper revenue tracking. Fields with * are required.")

with st.form("revenue_form", clear_on_submit=False):
    # --- SECTION 1: Client & Rep Info ---
    st.markdown('<div class="section-title">👤 Client & Agent Info</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1:
        client_id = st.text_input("Client ID*", placeholder="12345")
        client_name = st.text_input("Client Name")
        sales_rep_id = st.text_input("Sales Rep ID")
        sales_rep_name = st.text_input("Sales Rep Name")
    with c2:
        tour_rep_id = st.text_input("Tour Rep ID")
        tour_rep_name = st.text_input("Tour Rep Name")
        building_id = st.text_input("Building ID")
        building_name = st.text_input("Building Name")
        unit_number = st.text_input("Unit Number")
    with c3:
        tour_id = st.text_input("Tour ID")
        move_in_date = st.date_input("Move-in Date", value=datetime.today())
        tour_date = st.date_input("Tour Date", value=datetime.today())
        lease_term = st.number_input("Lease Term (months)", min_value=1, max_value=48, value=12)
        application_approved_date = st.date_input("Application Approved Date")
    
    st.markdown("---")
    # --- SECTION 2: Date, Month, Year ---
    c4, c5, c6 = st.columns(3)
    with c4:
        month = st.selectbox("Month", [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ], index=datetime.today().month - 1)
    with c5:
        year = st.number_input("Year", min_value=2000, max_value=2100, value=datetime.today().year)
    with c6:
        pass # for layout

    st.markdown("---")
    # --- SECTION 3: Deal Details ---
    with st.expander("🏢 Deal Details", expanded=True):
        cc1, cc2, cc3 = st.columns(3)
        with cc1:
            beds = st.number_input("Beds", min_value=0, max_value=8, step=1, value=1)
            baths = st.number_input("Baths", min_value=1.0, max_value=8.0, step=0.5, value=1.0)
            rent = st.number_input("Base Rent ($)", min_value=0, step=50)
        with cc2:
            concession_free_months = st.number_input("Concession Free Months", min_value=0.0, step=0.5, value=0.0)
            additional_concessions = st.number_input("Additional Concession ($)", min_value=0, step=50, value=0)
            total_concession_value = st.number_input("Total Concession Value ($)", min_value=0, step=50, value=0)
        with cc3:
            net_effective = st.number_input("Net Effective ($)", min_value=0, step=50, value=0)
            commission_percentage = st.slider("Commission (%)", min_value=0, max_value=100, value=100)
            deal_value = st.number_input("Deal Value ($)", min_value=0, step=100, value=0)
        concession_text = st.text_area("Concession Text", placeholder="Enter details about concessions or discounts.")

    st.markdown("---")
    # --- SECTION 4: Invoice & Approval ---
    with st.expander("🧾 Invoice & Application Status", expanded=False):
        d1, d2, d3 = st.columns(3)
        with d1:
            invoice_prepared = st.toggle("Invoice Prepared")
            invoice_prepared_date = st.date_input("Invoice Prepared Date")
            invoice_sent = st.toggle("Invoice Sent")
            invoice_sent_date = st.date_input("Invoice Sent Date")
            invoice_collected = st.toggle("Invoice Collected")
            invoice_collected_date = st.date_input("Invoice Collected Date")
        with d2:
            signed_lease = st.selectbox("Application Approved", ["Not decided yet", "Application Denied", "Application Approved"])
            signed_lease_date = st.date_input("Signed Lease Date")
            is_closed = st.toggle("Is Closed")
            is_closed_date = st.date_input("Closed Date")
        with d3:
            invoice_info_requested = st.toggle("Invoice Info Requested")
            invoice_info_requested_date = st.date_input("Invoice Info Requested Date")
            invoice_info_received = st.toggle("Invoice Info Received")
            invoice_info_received_date = st.date_input("Invoice Info Received Date")
            payment_to_lead_source = st.toggle("Payment To Lead Source")
            payment_to_lead_source_date = st.date_input("Payment To Lead Source Date")

    st.markdown("---")
    # --- SECTION 5: Comments & Disputes ---
    with st.expander("📝 Comments & Disputes", expanded=False):
        dispute_raised = st.toggle("Dispute Raised")
        dispute_raised_date = st.date_input("Dispute Raised Date")
        dispute_resolved = st.toggle("Dispute Resolved")
        dispute_resolved_date = st.date_input("Dispute Resolved Date")
        comments = st.text_area("Comments", placeholder="Any additional comments or notes about this deal.")

    # --- SUBMIT ---
    st.markdown("")
    submitted = st.form_submit_button("💾 Save Revenue Entry", type="primary")

if submitted:
    st.success("✅ Revenue entry captured and ready for database save!")
    st.markdown("#### 📋 Revenue Entry Summary")
    st.json({
        "Client ID": client_id,
        "Client Name": client_name,
        "Tour ID": tour_id,
        "Tour Date": str(tour_date),
        "Month": month,
        "Year": int(year),
        "Sales Rep": f"{sales_rep_id} - {sales_rep_name}",
        "Tour Rep": f"{tour_rep_id} - {tour_rep_name}",
        "Building": f"{building_id} - {building_name}",
        "Unit Number": unit_number,
        "Move-in Date": str(move_in_date),
        "Lease Term": lease_term,
        "Beds": beds,
        "Baths": baths,
        "Base Rent": rent,
        "Concession Free Months": concession_free_months,
        "Additional Concessions": additional_concessions,
        "Total Concession Value": total_concession_value,
        "Net Effective": net_effective,
        "Commission %": commission_percentage,
        "Deal Value": deal_value,
        "Concession Text": concession_text,
        "Invoice Prepared": invoice_prepared,
        "Invoice Prepared Date": str(invoice_prepared_date),
        "Invoice Sent": invoice_sent,
        "Invoice Sent Date": str(invoice_sent_date),
        "Invoice Collected": invoice_collected,
        "Invoice Collected Date": str(invoice_collected_date),
        "Application Approved": signed_lease,
        "Signed Lease Date": str(signed_lease_date),
        "Application Approved Date": str(application_approved_date),
        "Is Closed": is_closed,
        "Closed Date": str(is_closed_date),
        "Invoice Info Requested": invoice_info_requested,
        "Invoice Info Requested Date": str(invoice_info_requested_date),
        "Invoice Info Received": invoice_info_received,
        "Invoice Info Received Date": str(invoice_info_received_date),
        "Payment To Lead Source": payment_to_lead_source,
        "Payment To Lead Source Date": str(payment_to_lead_source_date),
        "Dispute Raised": dispute_raised,
        "Dispute Raised Date": str(dispute_raised_date),
        "Dispute Resolved": dispute_resolved,
        "Dispute Resolved Date": str(dispute_resolved_date),
        "Comments": comments
    })

st.markdown(
    """
    <style>
    div[data-testid="column"] > div > div {
        background-color: #f7fafc;
        border-radius: 14px;
        padding: 1.1rem;
        margin-bottom: 1.2rem;
        border: 1px solid #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True
)
