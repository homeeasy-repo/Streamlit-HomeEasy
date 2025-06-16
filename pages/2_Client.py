import streamlit as st
import pandas as pd
import psycopg2
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode
import webbrowser
from datetime import datetime, timezone
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
DB_URL = os.getenv("DATABASE_URL")

@st.cache_data(show_spinner=True)
def fetch_clients(offset=0, limit=20):
    try:
        conn = psycopg2.connect(DB_URL, sslmode='require')
        st.success("Database connection established successfully.")
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        return pd.DataFrame()
    query = f'''
        SELECT id, fullname, stage, lastactivity, created, assigned_employee_name
        FROM client
        ORDER BY created DESC
        OFFSET {offset} LIMIT {limit}
    '''
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def human_readable_time_diff(dt):
    now = datetime.now(timezone.utc)
    diff = now - dt
    minutes = int(diff.total_seconds() // 60)
    if minutes < 60:
        return f"{minutes} minutes ago"
    hours = minutes // 60
    if hours < 24:
        return f"{hours} hours ago"
    days = hours // 24
    return f"{days} days ago"

def calc_age(created):
    now = datetime.now(timezone.utc)
    diff = now - created
    minutes = int(diff.total_seconds() // 60)
    if minutes < 60:
        return f"{minutes} minutes"
    hours = minutes // 60
    if hours < 24:
        return f"{hours} hours"
    days = hours // 24
    return f"{days} days"

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
        .ag-theme-streamlit .ag-cell, .ag-theme-streamlit .ag-cell-value, .ag-theme-streamlit .ag-row, .ag-theme-streamlit .ag-center-cols-container, .ag-theme-streamlit .ag-full-width-row, .ag-theme-streamlit .ag-row-group-leaf-indent {
            font-size: 40px !important;
            font-family: 'Inter', sans-serif !important;
            line-height: 1.4 !important;
        }
        .ag-theme-streamlit .ag-header, .ag-theme-streamlit .ag-header-cell, .ag-theme-streamlit .ag-header-cell-label {
            font-size: 32px !important;
            font-family: 'Inter', sans-serif !important;
            background: #f1f5f9;
            color: #222;
            font-weight: 600;
        }
        .ag-theme-streamlit .ag-row {
            background: #fff;
        }
    </style>
""", unsafe_allow_html=True)
st.title("👤 Client List")
search_query = st.text_input("Global Search", "", key="global_search")

page_size = 30
# If search is active, fetch from DB directly for accurate results
if search_query:
    if search_query.isdigit():
        query = f"""
            SELECT id, fullname, stage, lastactivity, created, assigned_employee_name
            FROM client
            WHERE id = {int(search_query)}
            ORDER BY created DESC
        """
    else:
        query = f"""
            SELECT id, fullname, stage, lastactivity, created, assigned_employee_name
            FROM client
            WHERE LOWER(fullname) LIKE '%{search_query.lower()}%'
            ORDER BY created DESC
        """
    try:
        conn = psycopg2.connect(DB_URL, sslmode='require')
        df = pd.read_sql(query, conn)
        conn.close()
    except Exception as e:
        st.error(f"Database connection failed: {e}")
        st.stop()
else:
    if 'client_offset' not in st.session_state:
        st.session_state['client_offset'] = 0
    if 'client_data' not in st.session_state:
        st.session_state['client_data'] = fetch_clients(0, page_size)
    df = st.session_state['client_data']

# Convert datetimes
if not df.empty:
    df['lastactivity'] = pd.to_datetime(df['lastactivity'], utc=True)
    df['created'] = pd.to_datetime(df['created'], utc=True)
    df['Last Activity'] = df['lastactivity'].apply(human_readable_time_diff)
    df['Created Date'] = df['created'].dt.strftime('%Y-%m-%d')
    df['Age'] = df['created'].apply(calc_age)
    df = df.rename(columns={
        'id': 'Client ID',
        'fullname': 'Client Name',
        'stage': 'Stage',
        'assigned_employee_name': 'Sale Rep'
    })
    # Add a 'Links' column with default value 'None' for the dropdown
    df['Links'] = df['Client ID']  # Pass Client ID to renderer
    display_cols = ['Client ID', 'Client Name', 'Stage', 'Last Activity', 'Created Date', 'Age', 'Sale Rep', 'Links']
    df = df[display_cols]

# 1) Define a class-based cellRenderer for the dropdown
from st_aggrid import JsCode

dropdown_renderer = JsCode("""
class DropdownCellRenderer {
  init(params) {
    // 1) build the <select>
    this.eGui = document.createElement('select');
    this.eGui.style.width = '100%';
    this.eGui.innerHTML = `
      <option value="">Select…</option>
      <option value="requirement">Requirements</option>
      <option value="schedule">Schedule</option>
      <option value="dead">Dead</option>
    `;
    // 2) wire up the redirect
    this.eGui.addEventListener('change', () => {
      const val = this.eGui.value;
      if (!val) return;
      // 3) grab the top-level Streamlit URL
      const full = window.top.location.href;
      // 4) cut off anything from '/client' onward
      const base = full.split('/client')[0];
      // 5) build our multipage query
      const qp = new URLSearchParams({
        page:      'Client Requirement',
        client_id: params.value,
        action:    val
      });
      // 6) open in a new tab
      window.open(`${base}?${qp.toString()}`, '_blank');
      this.eGui.value = '';  // reset dropdown
    });
  }
  getGui() { return this.eGui; }
}
""")

gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_column(
    "Links",
    header_name="Links",
    cellRenderer=dropdown_renderer,
    editable=False,
    filter=False,
    sortable=False,
)
gb.configure_pagination(paginationAutoPageSize=True)
gb.configure_default_column(resizable=True, filter=True, sortable=True)

# 3) Make sure you still have:
response = AgGrid(
    df,
    gridOptions=gb.build(),
    theme="streamlit",
    allow_unsafe_jscode=True,   # ← this is critical
    unsafe_allow_html=True,
    fit_columns_on_grid_load=True,
    height=900,
    width='100%',
    enable_enterprise_modules=False,
    reload_data=True,
    columns_auto_size_mode='FIT_ALL_COLUMNS_TO_VIEW'
)

# Infinite scroll: load more when user scrolls to bottom
if not search_query and st.button("Load more clients"):
    st.session_state['client_offset'] += page_size
    new_df = fetch_clients(st.session_state['client_offset'], page_size)
    if not new_df.empty:
        st.session_state['client_data'] = pd.concat([st.session_state['client_data'], new_df], ignore_index=True)
    else:
        st.info("No more clients to load.")
