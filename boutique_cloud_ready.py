import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
import pandas as pd
from datetime import date, datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
import pywhatkit as kit
import urllib.parse

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Boutique Management System",
    page_icon="🏪",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1e3a8a;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .success-box {
        padding: 15px;
        border-radius: 5px;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    .warning-box {
        padding: 15px;
        border-radius: 5px;
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        color: #856404;
    }
    
    /* Enhanced Button Styling */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(102, 126, 234, 0.3);
        text-transform: none;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        box-shadow: 0 6px 12px rgba(102, 126, 234, 0.4);
        transform: translateY(-2px);
    }
    
    .stButton>button:active {
        transform: translateY(0px);
        box-shadow: 0 2px 4px rgba(102, 126, 234, 0.3);
    }
    
    /* Download Button Styling */
    .stDownloadButton>button {
        width: 100%;
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        font-size: 15px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 6px rgba(79, 172, 254, 0.3);
    }
    
    .stDownloadButton>button:hover {
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
        box-shadow: 0 6px 12px rgba(79, 172, 254, 0.4);
        transform: translateY(-2px);
    }
    
    /* Form Submit Button */
    .stForm button[type="submit"] {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 14px 28px;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 8px rgba(245, 87, 108, 0.3);
        width: 100%;
    }
    
    .stForm button[type="submit"]:hover {
        background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%);
        box-shadow: 0 6px 14px rgba(245, 87, 108, 0.4);
        transform: translateY(-2px);
    }
    
    /* Radio Button Styling */
    .stRadio > label {
        background: white;
        padding: 12px 20px;
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
        font-weight: 500;
    }
    
    .stRadio > label:hover {
        border-color: #667eea;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
    }
    
    /* Selectbox Styling */
    .stSelectbox > div > div {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        transition: all 0.3s ease;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #667eea;
        box-shadow: 0 2px 8px rgba(102, 126, 234, 0.2);
    }
    
    /* Input Field Styling */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #e0e0e0;
        padding: 10px 15px;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] .stRadio > label {
        color: white !important;
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        font-weight: 700 !important;
        font-size: 16px !important;
    }
    
    [data-testid="stSidebar"] .stRadio > label:hover {
        background: rgba(255, 255, 255, 0.2);
        border-color: rgba(255, 255, 255, 0.4);
    }
    
    /* Sidebar Title and Text */
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div {
        color: white !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stSidebar"] .stMarkdown {
        color: white !important;
        font-weight: 700 !important;
        font-size: 18px !important;
    }
    
    /* Sidebar Metrics */
    [data-testid="stSidebar"] [data-testid="stMetricLabel"] {
        color: white !important;
        font-weight: 700 !important;
        font-size: 15px !important;
    }
    
    [data-testid="stSidebar"] [data-testid="stMetricValue"] {
        color: white !important;
        font-weight: 800 !important;
        font-size: 24px !important;
    }
    
    /* Radio button text specifically */
    [data-testid="stSidebar"] .stRadio label {
        color: white !important;
        font-weight: 700 !important;
        font-size: 16px !important;
    }
    
    [data-testid="stSidebar"] .stRadio > div > label > div {
        color: white !important;
        font-weight: 700 !important;
    }
    
    /* Metric Styling */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
    
    /* Dataframe Styling */
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# =====================================================
# DATABASE CONNECTION
# =====================================================

@st.cache_resource
def get_connection():
    try:
        # Get database URL from Streamlit secrets or environment
        try:
            database_url = st.secrets.get("DATABASE_URL", os.getenv("DATABASE_URL"))
        except:
            database_url = os.getenv("DATABASE_URL")
        
        if not database_url:
            st.error("⚠️ DATABASE_URL not found! Please add it to Streamlit secrets or .env file")
            st.stop()
        
        conn = psycopg2.connect(database_url)
        return conn
    except Exception as e:
        st.error(f"❌ Database connection failed: {e}")
        st.info("💡 Make sure DATABASE_URL is correctly set in Streamlit Cloud secrets")
        st.stop()

conn = get_connection()
cursor = conn.cursor()

# Enhanced database schema with additional fields
cursor.execute("""
CREATE TABLE IF NOT EXISTS sales (
    id SERIAL PRIMARY KEY,
    customer_name TEXT,
    customer_phone TEXT,
    sale_date TEXT,
    vendor TEXT,
    product_category TEXT,
    product_description TEXT,
    buying_price REAL,
    selling_price REAL,
    amount_paid REAL,
    pending_amount REAL,
    payment_received INTEGER,
    delay_status INTEGER DEFAULT 0,
    payment_method TEXT,
    notes TEXT,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()

# =====================================================
# HELPER FUNCTIONS
# =====================================================

def calculate_metrics():
    """Calculate key business metrics"""
    df = pd.read_sql_query("SELECT * FROM sales", conn)
    
    if df.empty:
        return {
            'total_sales': 0,
            'total_profit': 0,
            'total_pending': 0,
            'delayed_payments': 0
        }
    
    metrics = {
        'total_sales': len(df),
        'total_profit': (df['selling_price'] - df['buying_price']).sum(),
        'total_pending': df['pending_amount'].sum(),
        'delayed_payments': df[df['delay_status'] == 1]['pending_amount'].sum()
    }
    
    return metrics

def export_to_excel(df):
    """Export dataframe to Excel with formatting"""
    output = BytesIO()
    
    # Create a copy of the dataframe for export
    export_df = df.copy()
    
    # Add calculated columns
    export_df['profit'] = export_df['selling_price'] - export_df['buying_price']
    export_df['profit_margin_%'] = ((export_df['profit'] / export_df['selling_price']) * 100).round(2)
    export_df['payment_status'] = export_df['payment_received'].map({0: 'Pending', 1: 'Received'})
    export_df['delayed'] = export_df['delay_status'].map({0: 'No', 1: 'Yes'})
    
    # Reorder columns for better readability
    columns_order = [
        'id', 'customer_name', 'customer_phone', 'sale_date', 
        'product_category', 'product_description', 'vendor',
        'buying_price', 'selling_price', 'profit', 'profit_margin_%',
        'amount_paid', 'pending_amount', 'payment_status', 'delayed',
        'payment_method', 'notes', 'created_at'
    ]
    
    # Only include columns that exist in the dataframe
    columns_order = [col for col in columns_order if col in export_df.columns]
    export_df = export_df[columns_order]
    
    # Rename columns for better presentation
    export_df.columns = [col.replace('_', ' ').title() for col in export_df.columns]
    
    # Write to Excel with formatting
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        export_df.to_excel(writer, sheet_name='All Sales', index=False)
        
        # Get the workbook and worksheet
        workbook = writer.book
        worksheet = writer.sheets['All Sales']
        
        # Auto-adjust column widths
        for idx, col in enumerate(export_df.columns):
            max_length = max(
                export_df[col].astype(str).apply(len).max(),
                len(col)
            )
            worksheet.column_dimensions[chr(65 + idx)].width = min(max_length + 2, 50)
    
    output.seek(0)
    return output

def send_reminder(customer_name, pending_amount):
    """Placeholder for SMS/Email reminder functionality"""
    st.success(f"Reminder sent to {customer_name} for ₹{pending_amount}")

# =====================================================
# LOGIN FUNCTION
# =====================================================

def login():
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("<h1 style='text-align: center; color: #1e3a8a;'>Boutique Login</h1>", unsafe_allow_html=True)
        st.markdown("---")
        
        with st.form("login_form"):
            username = st.text_input("👤 Username", placeholder="Enter username")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter password")
            
            col_a, col_b, col_c = st.columns([1, 2, 1])
            with col_b:
                submit = st.form_submit_button("Login", use_container_width=True)
            
            if submit:
                # Get credentials from environment variables or Streamlit secrets
                # Priority: Streamlit secrets > Environment variables > Default values
                try:
                    correct_username = st.secrets.get("USERNAME", os.getenv("USERNAME", "vinay"))
                    correct_password = st.secrets.get("PASSWORD", os.getenv("PASSWORD", "1234"))
                except:
                    correct_username = os.getenv("USERNAME", "vinay")
                    correct_password = os.getenv("PASSWORD", "1234")
                
                if username == correct_username and password == correct_password:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.rerun()
                else:
                    st.error("❌ Invalid credentials. Please try again.")

# =====================================================
# CUSTOMER MANAGEMENT
# =====================================================

def get_all_customers():
    """Get list of all unique customers"""
    cursor.execute("""
        SELECT DISTINCT customer_name, customer_phone 
        FROM sales 
        WHERE customer_name IS NOT NULL AND customer_name != ''
        ORDER BY customer_name
    """)
    return cursor.fetchall()

def get_customer_details(customer_name):
    """Get details of a specific customer"""
    cursor.execute("""
        SELECT customer_name, customer_phone 
        FROM sales 
        WHERE customer_name = %s
        LIMIT 1
    """, (customer_name,))
    return cursor.fetchone()

# =====================================================
# ADD SALE (ENHANCED)
# =====================================================

def add_sale():
    st.markdown("<div class='main-header'>➕ Add New Sale</div>", unsafe_allow_html=True)
    
    # Customer Type Selection
    st.subheader("👤 Select Customer Type")
    customer_type = st.radio(
        "Customer Type",
        ["🆕 New Customer", "👥 Existing Customer"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Initialize variables
    customer = ""
    customer_phone = ""
    
    # Handle customer selection
    if customer_type == "👥 Existing Customer":
        customers = get_all_customers()
        
        if customers:
            # Create a list of customer display names
            customer_options = [f"{name} - {phone if phone else 'No phone'}" for name, phone in customers]
            
            selected_customer = st.selectbox(
                "Select Existing Customer",
                customer_options,
                help="Choose from your existing customers"
            )
            
            # Extract customer name from selection
            if selected_customer:
                customer = selected_customer.split(" - ")[0]
                customer_details = get_customer_details(customer)
                if customer_details:
                    customer_phone = customer_details[1] if customer_details[1] else ""
                
                # Display customer info
                col_info1, col_info2 = st.columns(2)
                with col_info1:
                    st.info(f"**Customer:** {customer}")
                with col_info2:
                    st.info(f"**Phone:** {customer_phone if customer_phone else 'Not provided'}")
        else:
            st.warning("⚠️ No existing customers found. Please add a new customer.")
            customer_type = "🆕 New Customer"
    
    with st.form("sale_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Customer Information")
            
            if customer_type == "🆕 New Customer":
                customer = st.text_input("Customer Name *", placeholder="Enter customer name")
                customer_phone = st.text_input("Phone Number", placeholder="+91 XXXXXXXXXX")
            else:
                # For existing customers, show as disabled/readonly
                customer = st.text_input("Customer Name *", value=customer, disabled=True)
                customer_phone = st.text_input("Phone Number", value=customer_phone, disabled=True)
            
            sale_date = st.date_input("Sale Date", date.today())
            
        with col2:
            st.subheader("Product Information")
            product_category = st.selectbox(
                "Category *",
                ["Sarees", "Salwar Suits", "Lehengas", "Kurtis", "Western Wear", 
                 "Accessories", "Kids Wear", "Other"]
            )
            product_description = st.text_area("Product Description", placeholder="Describe the product")
            vendor = st.text_input("Vendor Name", placeholder="Enter vendor name")
        
        st.subheader("Pricing & Payment")
        
        col3, col4, col5 = st.columns(3)
        
        with col3:
            buying_price = st.number_input("Buying Price (₹) *", min_value=0.0, step=100.0)
        with col4:
            selling_price = st.number_input("Selling Price (₹) *", min_value=0.0, step=100.0)
        with col5:
            amount_paid = st.number_input("Amount Paid (₹)", min_value=0.0, step=100.0)
        
        pending_amount = selling_price - amount_paid
        profit = selling_price - buying_price
        
        col6, col7 = st.columns(2)
        with col6:
            st.metric("Pending Amount", f"₹ {pending_amount:,.2f}")
        with col7:
            st.metric("Expected Profit", f"₹ {profit:,.2f}")
        
        payment_method = st.selectbox(
            "Payment Method",
            ["Cash", "UPI", "Card", "Bank Transfer", "Part Payment"]
        )
        
        notes = st.text_area("Additional Notes", placeholder="Any special notes about this sale")
        
        submitted = st.form_submit_button("💾 Save Sale", use_container_width=True)
        
        if submitted:
            if not customer or buying_price == 0 or selling_price == 0:
                st.error("⚠️ Please fill in all required fields (*)")
            else:
                cursor.execute("""
                INSERT INTO sales 
                (customer_name, customer_phone, sale_date, vendor, product_category, 
                 product_description, buying_price, selling_price, amount_paid, 
                 pending_amount, payment_received, delay_status, payment_method, notes)
                VALUES (%s, %s, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (customer, customer_phone, str(sale_date), vendor, product_category,
                 product_description, buying_price, selling_price, amount_paid, 
                 pending_amount, 1 if pending_amount == 0 else 0, 0, payment_method, notes))
                
                conn.commit()
                st.success("✅ Sale Added Successfully!")
                st.balloons()
                st.rerun()

# =====================================================
# REVIEW ACCOUNTS (ENHANCED)
# =====================================================

def review_accounts():
    st.markdown("<div class='main-header'>📋 Review Accounts</div>", unsafe_allow_html=True)
    
    df = pd.read_sql_query("SELECT * FROM sales", conn)
    
    if df.empty:
        st.info("📭 No sales available. Add your first sale!")
        return
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        customer_filter = st.text_input("🔍 Search Customer", placeholder="Enter name")
    with col2:
        category_filter = st.selectbox("Category", ["All"] + df["product_category"].unique().tolist())
    with col3:
        payment_status = st.selectbox("Payment Status", ["All", "Paid", "Pending"])
    with col4:
        delay_filter = st.selectbox("Delay Status", ["All", "No Delay", "Delayed"])
    
    # Apply filters
    filtered_df = df.copy()
    
    if customer_filter:
        filtered_df = filtered_df[filtered_df["customer_name"].str.contains(customer_filter, case=False, na=False)]
    
    if category_filter != "All":
        filtered_df = filtered_df[filtered_df["product_category"] == category_filter]
    
    if payment_status == "Paid":
        filtered_df = filtered_df[filtered_df["payment_received"] == 1]
    elif payment_status == "Pending":
        filtered_df = filtered_df[filtered_df["payment_received"] == 0]
    
    if delay_filter == "No Delay":
        filtered_df = filtered_df[filtered_df["delay_status"] == 0]
    elif delay_filter == "Delayed":
        filtered_df = filtered_df[filtered_df["delay_status"] == 1]
    
    # Summary Metrics
    st.subheader("📊 Summary")
    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
    
    with metric_col1:
        st.metric("Total Transactions", len(filtered_df))
    with metric_col2:
        total_profit = (filtered_df["selling_price"] - filtered_df["buying_price"]).sum()
        st.metric("Total Profit", f"₹ {total_profit:,.2f}")
    with metric_col3:
        total_pending = filtered_df["pending_amount"].sum()
        st.metric("Total Pending", f"₹ {total_pending:,.2f}")
    with metric_col4:
        total_revenue = filtered_df["selling_price"].sum()
        st.metric("Total Revenue", f"₹ {total_revenue:,.2f}")
    
    st.markdown("---")
    
    # Display data
    display_df = filtered_df[[
        "id", "customer_name", "customer_phone", "sale_date", "product_category",
        "buying_price", "selling_price", "amount_paid", "pending_amount",
        "payment_method", "delay_status"
    ]].copy()
    
    display_df["delay_status"] = display_df["delay_status"].map({0: "No", 1: "Yes"})
    display_df = display_df.rename(columns={
        "id": "ID",
        "customer_name": "Customer",
        "customer_phone": "Phone",
        "sale_date": "Date",
        "product_category": "Category",
        "buying_price": "Buy Price",
        "selling_price": "Sell Price",
        "amount_paid": "Paid",
        "pending_amount": "Pending",
        "payment_method": "Payment",
        "delay_status": "Delayed"
    })
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    # Download options
    col_csv, col_excel = st.columns(2)
    
    with col_csv:
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download as CSV",
            data=csv,
            file_name=f"sales_report_{date.today()}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col_excel:
        excel_file = export_to_excel(filtered_df)
        st.download_button(
            label="📊 Download as Excel",
            data=excel_file,
            file_name=f"sales_report_{date.today()}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    
    # Mark Payment Received
    st.markdown("---")
    st.subheader("💰 Mark Payment Received")
    
    pending_df = filtered_df[filtered_df["pending_amount"] > 0]
    
    if pending_df.empty:
        st.success("🎉 All payments received!")
    else:
        for _, row in pending_df.iterrows():
            col_a, col_b, col_c = st.columns([3, 2, 1])
            
            with col_a:
                st.write(f"**{row['customer_name']}** - {row['product_category']}")
            with col_b:
                st.write(f"Pending: ₹{row['pending_amount']:,.2f}")
            with col_c:
                if st.button("✅ Received", key=f"pay_{row['id']}"):
                    cursor.execute("""
                    UPDATE sales 
                    SET payment_received = 1,
                        amount_paid = selling_price,
                        pending_amount = 0
                    WHERE id = %s
                    """, (row["id"],))
                    conn.commit()
                    st.success(f"Payment updated for {row['customer_name']}")
                    st.rerun()

# =====================================================
# UPDATE TRANSACTION (ENHANCED)
# =====================================================

def update_transaction():
    st.markdown("<div class='main-header'>✏️ Update Transaction</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_name = st.text_input("🔍 Search Customer Name", placeholder="Enter customer name")
    with col2:
        search_id = st.number_input("Or Search by ID", min_value=0, step=1)
    
    if search_name or search_id > 0:
        if search_name:
            df = pd.read_sql_query(
                "SELECT * FROM sales WHERE customer_name LIKE %s",
                conn,
                params=(f"%{search_name}%",)
            )
        else:
            df = pd.read_sql_query(
                "SELECT * FROM sales WHERE id = %s",
                conn,
                params=(search_id,)
            )
        
        if df.empty:
            st.warning("⚠️ No transaction found.")
            return
        
        st.dataframe(df, use_container_width=True)
        
        selected_id = st.selectbox("Select Transaction ID to Update", df["id"].tolist())
        
        if selected_id:
            sale = df[df["id"] == selected_id].iloc[0]
            
            st.markdown("---")
            st.subheader("Modify Transaction Details")
            
            with st.form("update_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    new_customer = st.text_input("Customer Name", value=sale["customer_name"])
                    new_phone = st.text_input("Phone", value=sale.get("customer_phone", ""))
                    new_category = st.selectbox(
                        "Category",
                        ["Sarees", "Salwar Suits", "Lehengas", "Kurtis", "Western Wear", 
                         "Accessories", "Kids Wear", "Other"],
                        index=["Sarees", "Salwar Suits", "Lehengas", "Kurtis", "Western Wear", 
                               "Accessories", "Kids Wear", "Other"].index(sale.get("product_category", "Other"))
                    )
                
                with col2:
                    new_amount_paid = st.number_input(
                        "Update Amount Paid (₹)",
                        value=float(sale["amount_paid"]),
                        min_value=0.0,
                        step=100.0
                    )
                    mark_delay = st.checkbox(
                        "Mark as Delayed Payment",
                        value=bool(sale["delay_status"])
                    )
                    new_payment_method = st.selectbox(
                        "Payment Method",
                        ["Cash", "UPI", "Card", "Bank Transfer", "Part Payment"],
                        index=["Cash", "UPI", "Card", "Bank Transfer", "Part Payment"].index(
                            sale.get("payment_method", "Cash")
                        )
                    )
                
                new_notes = st.text_area("Notes", value=sale.get("notes", ""))
                
                new_pending = sale["selling_price"] - new_amount_paid
                st.metric("New Pending Amount", f"₹ {new_pending:,.2f}")
                
                col_submit, col_delete = st.columns(2)
                
                with col_submit:
                    update_button = st.form_submit_button("💾 Update Transaction", use_container_width=True)
                
                with col_delete:
                    delete_button = st.form_submit_button("🗑️ Delete Transaction", use_container_width=True)
                
                if update_button:
                    cursor.execute("""
                    UPDATE sales
                    SET customer_name = %s,
                        customer_phone = %s,
                        product_category = ?,
                        amount_paid = ?,
                        pending_amount = ?,
                        delay_status = ?,
                        payment_method = ?,
                        notes = ?,
                        payment_received = ?
                    WHERE id = %s
                    """,
                    (new_customer, new_phone, new_category, new_amount_paid, new_pending, 
                     int(mark_delay), new_payment_method, new_notes, 
                     1 if new_pending == 0 else 0, selected_id))
                    
                    conn.commit()
                    st.success("✅ Transaction Updated Successfully!")
                    st.rerun()
                
                if delete_button:
                    cursor.execute("DELETE FROM sales WHERE id = %s", (selected_id,))
                    conn.commit()
                    st.success("🗑️ Transaction Deleted Successfully!")
                    st.rerun()

# =====================================================
# ANALYTICS DASHBOARD (ENHANCED)
# =====================================================

def analytics_dashboard():
    st.markdown("<div class='main-header'>📊 Business Analytics Dashboard</div>", unsafe_allow_html=True)
    
    df = pd.read_sql_query("SELECT * FROM sales", conn)
    
    if df.empty:
        st.info("📭 No sales data available. Start adding sales!")
        return
    
    df["sale_date"] = pd.to_datetime(df["sale_date"])
    df["profit"] = df["selling_price"] - df["buying_price"]
    df["profit_margin"] = (df["profit"] / df["selling_price"] * 100).round(2)
    
    # Key Metrics Row
    st.subheader("🎯 Key Performance Indicators")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        total_sales = len(df)
        st.metric("Total Sales", total_sales)
    
    with col2:
        total_revenue = df["selling_price"].sum()
        st.metric("Total Revenue", f"₹ {total_revenue:,.0f}")
    
    with col3:
        total_profit = df["profit"].sum()
        st.metric("Total Profit", f"₹ {total_profit:,.0f}")
    
    with col4:
        total_pending = df["pending_amount"].sum()
        st.metric("Total Pending", f"₹ {total_pending:,.0f}")
    
    with col5:
        avg_profit_margin = df["profit_margin"].mean()
        st.metric("Avg Profit %", f"{avg_profit_margin:.1f}%")
    
    st.markdown("---")
    
    # Visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends", "👥 Customers", "📦 Categories", "💸 Payments"])
    
    with tab1:
        col1, col2 = st.columns(2)
        
        with col1:
            # Monthly Revenue & Profit
            df["month"] = df["sale_date"].dt.to_period("M").astype(str)
            monthly_data = df.groupby("month").agg({
                "selling_price": "sum",
                "profit": "sum"
            }).reset_index()
            
            fig1 = go.Figure()
            fig1.add_trace(go.Bar(
                x=monthly_data["month"],
                y=monthly_data["selling_price"],
                name="Revenue",
                marker_color='#667eea'
            ))
            fig1.add_trace(go.Bar(
                x=monthly_data["month"],
                y=monthly_data["profit"],
                name="Profit",
                marker_color='#764ba2'
            ))
            fig1.update_layout(
                title="Monthly Revenue vs Profit",
                xaxis_title="Month",
                yaxis_title="Amount (₹)",
                barmode='group',
                height=400
            )
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            # Sales Trend
            daily_sales = df.groupby("sale_date").size().reset_index(name="count")
            fig2 = px.line(
                daily_sales,
                x="sale_date",
                y="count",
                title="Sales Trend Over Time",
                markers=True
            )
            fig2.update_traces(line_color='#FF1493')
            fig2.update_layout(height=400)
            st.plotly_chart(fig2, use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            # Top Customers by Revenue
            top_customers = df.groupby("customer_name")["selling_price"].sum().nlargest(10).reset_index()
            fig3 = px.bar(
                top_customers,
                x="selling_price",
                y="customer_name",
                orientation='h',
                title="Top 10 Customers by Revenue",
                color="selling_price",
                color_continuous_scale="Purples"
            )
            fig3.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig3, use_container_width=True)
        
        with col2:
            # Customer Pending Analysis
            st.subheader("💰 Customer Pending Amounts")
            customer_pending = df.groupby("customer_name")["pending_amount"].sum()
            customer_pending = customer_pending[customer_pending > 0].sort_values(ascending=False)
            
            if len(customer_pending) > 0:
                st.dataframe(
                    customer_pending.reset_index().rename(
                        columns={"customer_name": "Customer", "pending_amount": "Pending (₹)"}
                    ),
                    use_container_width=True,
                    hide_index=True
                )
                
                # Send reminder option
                selected_customer = st.selectbox("Send Reminder To:", customer_pending.index.tolist())
                if st.button("📧 Send Payment Reminder"):
                    send_reminder(selected_customer, customer_pending[selected_customer])
            else:
                st.success("🎉 No pending payments!")
    
    with tab3:
        col1, col2 = st.columns(2)
        
        with col1:
            # Category Distribution
            category_sales = df.groupby("product_category").size().reset_index(name="count")
            fig4 = px.pie(
                category_sales,
                values="count",
                names="product_category",
                title="Sales Distribution by Category",
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            fig4.update_layout(height=400)
            st.plotly_chart(fig4, use_container_width=True)
        
        with col2:
            # Category Profitability
            category_profit = df.groupby("product_category")["profit"].sum().reset_index()
            fig5 = px.bar(
                category_profit,
                x="product_category",
                y="profit",
                title="Profitability by Category",
                color="profit",
                color_continuous_scale="Viridis"
            )
            fig5.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig5, use_container_width=True)
    
    with tab4:
        col1, col2 = st.columns(2)
        
        with col1:
            # Payment Method Distribution
            payment_method = df.groupby("payment_method").size().reset_index(name="count")
            fig6 = px.pie(
                payment_method,
                values="count",
                names="payment_method",
                title="Payment Method Distribution",
                hole=0.4
            )
            fig6.update_layout(height=400)
            st.plotly_chart(fig6, use_container_width=True)
        
        with col2:
            # Payment Status
            payment_status = df.groupby("payment_received").size().reset_index(name="count")
            payment_status["payment_received"] = payment_status["payment_received"].map({
                0: "Pending", 1: "Received"
            })
            fig7 = px.bar(
                payment_status,
                x="payment_received",
                y="count",
                title="Payment Status Overview",
                color="payment_received",
                color_discrete_map={"Pending": "#FFA500", "Received": "#28a745"}
            )
            fig7.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig7, use_container_width=True)
    
    # Detailed Analytics Table
    st.markdown("---")
    st.subheader("📋 Detailed Sales Analysis")
    
    analysis_df = df[[
        "customer_name", "sale_date", "product_category", 
        "buying_price", "selling_price", "profit", "profit_margin",
        "amount_paid", "pending_amount"
    ]].copy()
    
    analysis_df = analysis_df.rename(columns={
        "customer_name": "Customer",
        "sale_date": "Date",
        "product_category": "Category",
        "buying_price": "Buy Price",
        "sell_price": "Sell Price",
        "profit": "Profit",
        "profit_margin": "Margin %",
        "amount_paid": "Paid",
        "pending_amount": "Pending"
    })
    
    st.dataframe(analysis_df, use_container_width=True, hide_index=True)
    
    # Download options for analytics
    col_csv_a, col_excel_a = st.columns(2)
    
    with col_csv_a:
        csv_analytics = df.to_csv(index=False)
        st.download_button(
            label="📥 Download All Data as CSV",
            data=csv_analytics,
            file_name=f"complete_sales_data_{date.today()}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col_excel_a:
        excel_analytics = export_to_excel(df)
        st.download_button(
            label="📊 Download All Data as Excel",
            data=excel_analytics,
            file_name=f"complete_sales_data_{date.today()}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )

# =====================================================
# CUSTOMER LIST
# =====================================================

def customer_list():
    st.markdown("<div class='main-header'>👥 Customer List</div>", unsafe_allow_html=True)
    
    df = pd.read_sql_query("SELECT * FROM sales", conn)
    
    if df.empty:
        st.info("📭 No customers yet. Add your first sale to see customers here.")
        return
    
    # Get unique customers with their details
    customer_summary = df.groupby(['customer_name', 'customer_phone']).agg({
        'id': 'count',  # Total transactions
        'selling_price': 'sum',  # Total sales value
        'pending_amount': 'sum',  # Total pending
        'sale_date': 'max'  # Last purchase date
    }).reset_index()
    
    customer_summary['profit'] = df.groupby('customer_name').apply(
        lambda x: (x['selling_price'] - x['buying_price']).sum()
    ).values
    
    customer_summary.columns = [
        'Customer Name', 'Phone', 'Total Transactions', 
        'Total Sales (₹)', 'Pending Amount (₹)', 'Last Purchase', 'Total Profit (₹)'
    ]
    
    # Sort by total sales
    customer_summary = customer_summary.sort_values('Total Sales (₹)', ascending=False)
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Customers", len(customer_summary))
    with col2:
        st.metric("Avg Sales per Customer", f"₹ {customer_summary['Total Sales (₹)'].mean():,.0f}")
    with col3:
        customers_with_pending = len(customer_summary[customer_summary['Pending Amount (₹)'] > 0])
        st.metric("Customers with Pending", customers_with_pending)
    with col4:
        st.metric("Total Customer Value", f"₹ {customer_summary['Total Sales (₹)'].sum():,.0f}")
    
    st.markdown("---")
    
    # Search functionality
    search_customer = st.text_input("🔍 Search Customer", placeholder="Enter customer name")
    
    if search_customer:
        customer_summary = customer_summary[
            customer_summary['Customer Name'].str.contains(search_customer, case=False, na=False)
        ]
    
    # Display customer list
    st.subheader("📋 Customer Details")
    st.dataframe(
        customer_summary.style.format({
            'Total Sales (₹)': '₹{:,.2f}',
            'Pending Amount (₹)': '₹{:,.2f}',
            'Total Profit (₹)': '₹{:,.2f}'
        }),
        use_container_width=True,
        hide_index=True
    )
    
    # Download customer list
    col_csv, col_excel = st.columns(2)
    
    with col_csv:
        csv = customer_summary.to_csv(index=False)
        st.download_button(
            label="📥 Download Customer List (CSV)",
            data=csv,
            file_name=f"customer_list_{date.today()}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col_excel:
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            customer_summary.to_excel(writer, sheet_name='Customers', index=False)
        output.seek(0)
        
        st.download_button(
            label="📊 Download Customer List (Excel)",
            data=output,
            file_name=f"customer_list_{date.today()}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
    
    st.markdown("---")
    
    # Individual customer details
    st.subheader("🔍 View Individual Customer History")
    
    customer_names = customer_summary['Customer Name'].tolist()
    selected = st.selectbox("Select a customer to view details", customer_names)
    
    if selected:
        customer_df = df[df['customer_name'] == selected].sort_values('sale_date', ascending=False)
        
        st.write(f"### Purchase History for **{selected}**")
        
        # Customer metrics
        col_a, col_b, col_c, col_d = st.columns(4)
        with col_a:
            st.metric("Total Purchases", len(customer_df))
        with col_b:
            st.metric("Total Spent", f"₹ {customer_df['selling_price'].sum():,.0f}")
        with col_c:
            st.metric("Total Pending", f"₹ {customer_df['pending_amount'].sum():,.0f}")
        with col_d:
            customer_profit = (customer_df['selling_price'] - customer_df['buying_price']).sum()
            st.metric("Profit from Customer", f"₹ {customer_profit:,.0f}")
        
        # Purchase history table
        history_df = customer_df[[
            'sale_date', 'product_category', 'product_description',
            'selling_price', 'amount_paid', 'pending_amount', 'payment_method'
        ]].copy()
        
        history_df.columns = [
            'Date', 'Category', 'Description', 'Price (₹)', 
            'Paid (₹)', 'Pending (₹)', 'Payment Method'
        ]
        
        st.dataframe(history_df, use_container_width=True, hide_index=True)

# =====================================================
# REMINDERS & ALERTS
# =====================================================

def reminders_alerts():
    st.markdown("<div class='main-header'>🔔 Reminders & Alerts</div>", unsafe_allow_html=True)
    
    df = pd.read_sql_query("SELECT * FROM sales", conn)
    
    if df.empty:
        st.info("No data available.")
        return
    
    df["sale_date"] = pd.to_datetime(df["sale_date"])
    
    # Overdue Payments (more than 30 days)
    st.subheader("⚠️ Overdue Payments (30+ days)")
    overdue = df[
        (df["pending_amount"] > 0) & 
        ((datetime.now() - df["sale_date"]).dt.days > 30)
    ]
    
    if len(overdue) > 0:
        for _, row in overdue.iterrows():
            days_overdue = (datetime.now() - row["sale_date"]).days
            col1, col2, col3 = st.columns([3, 2, 2])
            
            with col1:
                st.write(f"**{row['customer_name']}**")
                st.caption(f"Sale Date: {row['sale_date'].strftime('%Y-%m-%d')}")
            with col2:
                st.write(f"Pending: ₹{row['pending_amount']:,.2f}")
                st.caption(f"{days_overdue} days overdue")
            with col3:
                if st.button(f"📧 Send Reminder", key=f"remind_{row['id']}"):
                    send_reminder(row['customer_name'], row['pending_amount'])
                if st.button(f"✅ Mark Paid", key=f"paid_{row['id']}"):
                    cursor.execute("""
                    UPDATE sales 
                    SET payment_received = 1, amount_paid = selling_price, pending_amount = 0
                    WHERE id = %s
                    """, (row["id"],))
                    conn.commit()
                    st.rerun()
    else:
        st.success("✅ No overdue payments!")
    
    st.markdown("---")
    
    # Recent High-Value Sales
    st.subheader("💎 Recent High-Value Sales (₹10,000+)")
    high_value = df[df["selling_price"] >= 10000].sort_values("sale_date", ascending=False).head(10)
    
    if len(high_value) > 0:
        st.dataframe(
            high_value[["customer_name", "sale_date", "product_category", "selling_price", "profit"]],
            use_container_width=True,
            hide_index=True
        )
    else:
        st.info("No high-value sales yet.")

# =====================================================
# MAIN APP
# =====================================================

def main():
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    
    if not st.session_state.logged_in:
        login()
    else:
        # Sidebar
        with st.sidebar:
            st.markdown("### Boutique Management")
            st.markdown(f"**User:** {st.session_state.get('username', 'Admin')}")
            st.markdown("---")
            
            # Quick Stats
            metrics = calculate_metrics()
            st.metric("💰 Total Pending", f"₹ {metrics['total_pending']:,.0f}")
            st.metric("📈 Total Profit", f"₹ {metrics['total_profit']:,.0f}")
            st.metric("📊 Total Sales", metrics['total_sales'])
            
            st.markdown("---")
            
            page = st.radio(
                "Navigation",
                ["🏠 Dashboard", "➕ Add Sale", "📋 Review Accounts", 
                 "✏️ Update Transaction", "👥 Customer List", "📊 Analytics", 
                 "🔔 Reminders", "🚪 Logout"],
                label_visibility="collapsed"
            )
        
        # Main content
        if page == "🏠 Dashboard":
            st.markdown("<div class='main-header'>🏠 Dashboard</div>", unsafe_allow_html=True)
            
            metrics = calculate_metrics()
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Sales", metrics['total_sales'], "transactions")
            with col2:
                st.metric("Total Profit", f"₹ {metrics['total_profit']:,.0f}")
            with col3:
                st.metric("Total Pending", f"₹ {metrics['total_pending']:,.0f}")
            with col4:
                st.metric("Delayed Payments", f"₹ {metrics['delayed_payments']:,.0f}")
            
            st.markdown("---")
            
            # Export Section
            st.subheader("📊 Export All Sales Data")
            
            df_all = pd.read_sql_query("SELECT * FROM sales", conn)
            
            if not df_all.empty:
                col_info, col_export = st.columns([2, 1])
                
                with col_info:
                    st.info(f"💾 Ready to export {len(df_all)} sales records with complete details including profit, margins, and payment status.")
                
                with col_export:
                    excel_all = export_to_excel(df_all)
                    st.download_button(
                        label="📊 Download Complete Data (Excel)",
                        data=excel_all,
                        file_name=f"all_sales_data_{date.today()}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
            else:
                st.info("No data available to export yet.")
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.info("💡 **Quick Tip:** Use the Analytics page for detailed insights!")
            
            with col2:
                if metrics['total_pending'] > 0:
                    st.warning(f"⚠️ You have ₹{metrics['total_pending']:,.0f} in pending payments.")
        
        elif page == "➕ Add Sale":
            add_sale()
        
        elif page == "📋 Review Accounts":
            review_accounts()
        
        elif page == "✏️ Update Transaction":
            update_transaction()
        
        elif page == "👥 Customer List":
            customer_list()
        
        elif page == "📊 Analytics":
            analytics_dashboard()
        
        elif page == "🔔 Reminders":
            reminders_alerts()
        
        elif page == "🚪 Logout":
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()

if __name__ == "__main__":
    main()
