# 🔐 Northbridge IAM Onboarding Automation

**Automated user provisioning tool built for Northbridge Financial Corporation**

Demo project created for the Junior IAM Analyst role application.

---

## 📺 Demo Video

**[Watch 5-minute demo here](https://www.loom.com/share/4e88170aee084c11a97366933a27a87c)**

---

## 🎯 What This Tool Does

- ✅ Automates Entra ID user creation via Microsoft Graph API
- ✅ Department and office-based attribute assignment (7 Canadian locations)
- ✅ Bulk CSV upload for high-volume onboarding
- ✅ Audit trail with downloadable compliance logs
- ✅ ServiceNow ticket summary generation

**Impact:** Reduces provisioning time from 90 minutes to under 10 minutes per user.

**Estimated ROI:** ~400 hours/year saved (~$20,000 in labor costs)

---

## 🔍 Security Findings

As part of this project, I conducted a security assessment of Northbridge's external IAM posture.

**Key Finding:** Username enumeration vulnerability in password reset portal  
**Severity:** Medium-High  
**Full Analysis:** [IAM-Security-Audit.pdf](./IAM-Security-Audit.pdf)

---

## 🛠️ Technical Stack

- Python 3.11
- Streamlit (web interface)
- Microsoft Graph API (Entra ID integration)
- MSAL (authentication)
- Azure AD Dynamic Groups

---

## 📸 Screenshots
### Compliance Audit Log
<img width="1583" height="629" alt="Audit log" src="https://github.com/user-attachments/assets/7abea372-1f5e-4d94-8cb6-e9f2895eef13" />

### Single User Creation
<img width="1897" height="863" alt="First user creation" src="https://github.com/user-attachments/assets/9179aecc-5f21-4b27-aac6-c3535a4c5f26" />

### Successful User Provisioning with ServiceNow Ticket Summary
<img width="1622" height="752" alt="First user creation successful" src="https://github.com/user-attachments/assets/51b9c041-0afa-4a5c-9f78-c0d0e754a4e2" />

### Bulk User Creation
<img width="1897" height="849" alt="Bulk user creation" src="https://github.com/user-attachments/assets/e28f2da3-c4a9-4c70-bc54-087ffed61404" />

### Microsoft Azure Portal Verification - Users Created by Tool
<img width="1869" height="413" alt="Azure audit log" src="https://github.com/user-attachments/assets/4f72f954-f650-4e89-a3a3-7fa3712cf7a4" />


---

## 🚀 How to Run (For Technical Review)

### Prerequisites
- Python 3.8+
- Azure subscription with Entra ID
- App registration with Graph API permissions

### Installation
```bash
# Clone repository
git clone https://github.com/timgrin/northbridge-iam-automation.git
cd northbridge-iam-automation

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure credentials (create .env file)
CLIENT_ID=your-client-id
TENANT_ID=your-tenant-id
CLIENT_SECRET=your-client-secret
DOMAIN=yourcompany.onmicrosoft.com

# Run application
streamlit run app.py
```

---

## 📋 Required Azure Permissions

Microsoft Graph API (Application permissions):
- `User.ReadWrite.All`
- `Group.ReadWrite.All`
- `Directory.ReadWrite.All`

---

## 💡 Production Roadmap

This is a prototype. For production deployment, I would add:

- [ ] Persistent database for audit logs (Azure SQL / Table Storage)
- [ ] Direct ServiceNow API integration
- [ ] Automated offboarding workflows
- [ ] CyberArk privileged account provisioning
- [ ] Email notifications to new hires
- [ ] HR system integration (Workday, SAP)
- [ ] Role-based access control for the tool
- [ ] Advanced error handling and rollback

---

## 📧 Contact

**Built by:** Timilehin Odumuyiwa  
**Email:** odumuyiwatimilehin@gmail.com 
**LinkedIn:** https://www.linkedin.com/in/odumuyiwa/

**Purpose:** Demonstration project for Junior IAM Analyst role at Northbridge Financial Corporation

---

## 📄 License

MIT License - Built for demonstration purposes.
```
