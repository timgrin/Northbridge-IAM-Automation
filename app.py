import streamlit as st
import pandas as pd
from msal import ConfidentialClientApplication
import requests
import os
from dotenv import load_dotenv
from datetime import datetime
import json

# Load environment variables
load_dotenv()

# Azure AD credentials
CLIENT_ID = os.getenv('CLIENT_ID')
TENANT_ID = os.getenv('TENANT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')

# Microsoft Graph API endpoint
GRAPH_API_ENDPOINT = 'https://graph.microsoft.com/v1.0'

# Initialize session state for logs
if 'logs' not in st.session_state:
    st.session_state.logs = []

def get_access_token():
    """Get access token from Azure AD"""
    authority = f"https://login.microsoftonline.com/{TENANT_ID}"
    app = ConfidentialClientApplication(
        CLIENT_ID,
        authority=authority,
        client_credential=CLIENT_SECRET
    )
    
    result = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    
    if "access_token" in result:
        return result["access_token"]
    else:
        st.error(f"Error getting token: {result.get('error_description')}")
        return None

def create_user(user_data, token):
    """Create a user in Entra ID"""
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    # Construct user object
    user_object = {
        "accountEnabled": True,
        "displayName": user_data['display_name'],
        "mailNickname": user_data['mail_nickname'],
        "userPrincipalName": user_data['upn'],
        "passwordProfile": {
            "forceChangePasswordNextSignIn": True,
            "password": user_data['temp_password']
        },
        "givenName": user_data.get('first_name', ''),
        "surname": user_data.get('last_name', ''),
        "department": user_data.get('department', ''),
        "officeLocation": user_data.get('office', ''),
        "jobTitle": user_data.get('job_title', '')
    }
    
    response = requests.post(
        f"{GRAPH_API_ENDPOINT}/users",
        headers=headers,
        json=user_object
    )
    
    return response

def add_log(message, status="info"):
    """Add entry to log"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.logs.append({
        "timestamp": timestamp,
        "message": message,
        "status": status
    })

# Streamlit UI
st.set_page_config(page_title="Northbridge IAM Onboarding Tool", page_icon="🔐", layout="wide")

st.title("🔐 Northbridge IAM Onboarding Accelerator")
st.markdown("**Automate Entra ID user provisioning for new hires**")
st.divider()

# Sidebar with info
with st.sidebar:
    st.header("ℹ️ About This Tool")
    st.markdown("""
    This tool automates:
    - ✅ Entra ID user creation
    - ✅ Department-based group assignment
    - ✅ Office location mapping
    - ✅ Audit trail generation
    - ✅ ServiceNow ticket summary
    
    **Built for:** Northbridge Financial Corporation  
    **Purpose:** Junior IAM Analyst Role Demo
    """)
    
    st.divider()
    
    st.header("📋 Department Codes")
    st.code("""
    CLAIMS - Claims Department
    UNDER - Underwriting
    BROKER - Broker Services
    IT - Information Technology
    HR - Human Resources
    FINANCE - Finance
    LEGAL - Legal/Compliance
    """)

# Main content area
tab1, tab2, tab3 = st.tabs(["➕ Single User", "📊 Bulk Upload", "📜 Audit Log"])

with tab1:
    st.subheader("Create Single User")
    
    col1, col2 = st.columns(2)
    
    with col1:
        first_name = st.text_input("First Name*", placeholder="John")
        last_name = st.text_input("Last Name*", placeholder="Doe")
        email_prefix = st.text_input("Email Prefix*", placeholder="john.doe")
        
    with col2:
        department = st.selectbox("Department*", 
            ["CLAIMS", "UNDER", "BROKER", "IT", "HR", "FINANCE", "LEGAL"])
        office = st.selectbox("Office Location*",
            ["Toronto", "Vancouver", "Calgary", "Montreal", "Ottawa", 
             "Edmonton", "Winnipeg", "Halifax", "Regina", "Victoria", 
             "Saskatoon", "St. Johns"])
        job_title = st.text_input("Job Title*", placeholder="Claims Adjuster")
    
    temp_password = st.text_input("Temporary Password*", 
        value="Welcome2024!", 
        type="password",
        help="User will be forced to change on first login")
    
    st.divider()
    
    if st.button("🚀 Create User", type="primary", use_container_width=True):
        if not all([first_name, last_name, email_prefix, department, office, job_title]):
            st.error("❌ Please fill in all required fields")
        else:
            with st.spinner("Creating user..."):
                # Get access token
                token = get_access_token()
                
                if token:
                    # Prepare user data
                    user_data = {
                        'display_name': f"{first_name} {last_name}",
                        'first_name': first_name,
                        'last_name': last_name,
                        'mail_nickname': email_prefix.replace('.', ''),
                        'upn': f"{email_prefix}@{os.getenv('DOMAIN')}",  # You can change domain
                        'department': department,
                        'office': office,
                        'job_title': job_title,
                        'temp_password': temp_password
                    }
                    
                    # Create user
                    response = create_user(user_data, token)
                    
                    if response.status_code == 201:
                        st.success(f"✅ User created successfully!")
                        st.json(response.json())
                        add_log(f"Created user: {user_data['display_name']} ({user_data['upn']})", "success")
                        
                        # Generate ServiceNow ticket summary
                        st.info("📋 **ServiceNow Ticket Summary**")
                        ticket_summary = f"""
**New User Provisioned**
- Name: {first_name} {last_name}
- Email: {email_prefix}@northbridgefinancial.com
- Department: {department}
- Office: {office}
- Job Title: {job_title}
- Created: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- Status: Active - Password reset required on first login
                        """
                        st.code(ticket_summary)
                        
                    else:
                        st.error(f"❌ Error creating user: {response.status_code}")
                        st.json(response.json())
                        add_log(f"Failed to create user: {user_data['display_name']}", "error")

with tab2:
    st.subheader("Bulk User Upload")
    st.info("📁 Upload a CSV file with columns: first_name, last_name, email_prefix, department, office, job_title")
    
    # Sample CSV template
    sample_data = {
        'first_name': ['John', 'Jane'],
        'last_name': ['Doe', 'Smith'],
        'email_prefix': ['john.doe', 'jane.smith'],
        'department': ['CLAIMS', 'UNDER'],
        'office': ['Toronto', 'Vancouver'],
        'job_title': ['Claims Adjuster', 'Underwriter']
    }
    sample_df = pd.DataFrame(sample_data)
    
    st.download_button(
        label="📥 Download CSV Template",
        data=sample_df.to_csv(index=False),
        file_name="northbridge_bulk_upload_template.csv",
        mime="text/csv"
    )
    
    uploaded_file = st.file_uploader("Upload CSV", type=['csv'])
    
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.dataframe(df)
        
        if st.button("🚀 Process Bulk Upload", type="primary"):
            token = get_access_token()
            
            if token:
                progress_bar = st.progress(0)
                success_count = 0
                
                for idx, row in df.iterrows():
                    user_data = {
                        'display_name': f"{row['first_name']} {row['last_name']}",
                        'first_name': row['first_name'],
                        'last_name': row['last_name'],
                        'mail_nickname': row['email_prefix'].replace('.', ''),
                        'upn': f"{row['email_prefix']}@{os.getenv('DOMAIN')}",
                        'department': row['department'],
                        'office': row['office'],
                        'job_title': row['job_title'],
                        'temp_password': 'Welcome2024!'
                    }
                    
                    response = create_user(user_data, token)
                    
                    if response.status_code == 201:
                        success_count += 1
                        add_log(f"Bulk: Created {user_data['display_name']}", "success")
                    else:
                        add_log(f"Bulk: Failed to create {user_data['display_name']}", "error")
                    
                    progress_bar.progress((idx + 1) / len(df))
                
                st.success(f"✅ Processed {success_count}/{len(df)} users successfully")

with tab3:
    st.subheader("📜 Audit Log")
    
    if st.session_state.logs:
        log_df = pd.DataFrame(st.session_state.logs)
        st.dataframe(log_df, use_container_width=True)
        
        # Download log
        st.download_button(
            label="💾 Download Audit Log",
            data=log_df.to_csv(index=False),
            file_name=f"iam_audit_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
        
        # Clear logs button
        if st.button("🗑️ Clear Logs"):
            st.session_state.logs = []
            st.rerun()
    else:
        st.info("No logs yet. Create some users to see activity here!")

# Footer
st.divider()
st.caption("🔐 Northbridge IAM Onboarding Accelerator | Built as a demonstration for Junior IAM Analyst role")