from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
import streamlit as st
from datetime import date, datetime
import json
import boto3
import tempfile

# ---------------- AWS ----------------
s3 = boto3.client(
    "s3",
    aws_access_key_id=st.secrets["AWS_ACCESS_KEY"],
    aws_secret_access_key=st.secrets["AWS_SECRET_ACCESS_KEY"],
    region_name="ap-south-1"
)

st.set_page_config(layout="wide")
st.title("Resume Builder")
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

if "valid_user" not in st.session_state:
    st.session_state.valid_user = False
if not st.session_state.valid_user:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            st.markdown("### 🔐 Login")

            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            if st.button("Login"):
                if username == st.secrets["APP_USERNAME"] and password == st.secrets["APP_PASSWORD"]:
                    st.session_state.valid_user = True
                    st.session_state.user = st.secrets["APP_USERNAME"]
                    st.rerun()
                else:
                    st.error("Invalid credentials")
            st.stop()


# ---------------- INIT ----------------
def init_role():
    return {
        "Name": "TANMAY MELANTA",
        "Contact": {
            "Address": "Thane, Maharashtra",
            "Email": "tanmaymelanta@gmail.com",
            "Phone": "7738321398",
            "LinkedIn": "https://www.linkedin.com/in/tanmay-melanta/",
            "GitHub": "https://github.com/tanmaymelanta"
        },
        "Target Roles": "",
        "Summary": "",
        "Skills": [],
        "Experience": [],
        "Projects": [],
        "Education": [],
        "Certifications": [],
        "Languages": []
    }

def upload_to_s3(data, filename):
    s3.put_object(
        Bucket="resume-tanmay",
        Key=f"resume-json/{filename}.json",
        Body=json.dumps(data, default=str),
        ContentType="application/json"
    )

def load_resume_from_s3(default_data, filename):
    try:
        obj = s3.get_object(Bucket="resume-tanmay", Key=f"resume-json/{filename}.json")
        return json.loads(obj["Body"].read())
    except:
        return default_data

def format_date(value):
    if isinstance(value, str):
        value = datetime.strptime(value, "%Y-%m-%d")
    return value.strftime("%b %Y")

def create_resume_from_data(data, output_pdf):
    doc = SimpleDocTemplate(output_pdf, rightMargin=30, leftMargin=30, topMargin=20, bottomMargin=20)

    # ---------- STYLES ----------
    name_style = ParagraphStyle(name="Name", fontName="Helvetica-Bold", fontSize=16, alignment=TA_CENTER,
                                spaceAfter=10)
    contact_style = ParagraphStyle(name="Contact", fontName="Helvetica", fontSize=9, alignment=TA_CENTER,
                                   textColor="#444444", spaceAfter=8)
    section_style = ParagraphStyle(name="Section", fontName="Helvetica-Bold", fontSize=11, spaceBefore=6,
                                   spaceAfter=5)
    divider = HRFlowable(width="100%", thickness=0.5, color="#999999", spaceBefore=4, spaceAfter=7)
    divider_white = HRFlowable(width="100%", thickness=0, color="#ffffff", spaceBefore=0, spaceAfter=0)
    body_style_bold = ParagraphStyle(name="Body", fontName="Helvetica-Bold", fontSize=9, leading=12)
    body_style = ParagraphStyle(name="Body", fontName="Helvetica", fontSize=9, leading=12)
    bullet_style = ParagraphStyle(name="Bullet", fontName="Helvetica", fontSize=9, leading=12, leftIndent=12,
                                  firstLineIndent=0, spaceAfter=2)
    content = []

    # ---------- HEADER ----------
    content.append(Paragraph(data["Name"], name_style))

    contact = data["Contact"]
    contact_text = f"""
    {contact['Address']} • {contact['Phone']} •
    <a href="mailto:{contact['Email']}">{contact['Email']}</a> •
    <a href="{contact['LinkedIn']}">linkedin.com/in/tanmay-melanta</a> •
    <a href="{contact['GitHub']}">github.com/tanmaymelanta</a>
    """
    content.append(Paragraph(contact_text, contact_style))

    # ---------- SUMMARY ----------
    content.append(Paragraph(data["Target Roles"], body_style_bold))
    content.append(Paragraph(data["Summary"], body_style))

    # ---------- SKILLS ----------
    content.append(Paragraph("SKILLS", section_style))
    content.append(divider)
    for skill in data["Skills"]:
        content.append(
            Paragraph(f"<b>{skill['title']}:</b> {skill['items']}", body_style)
        )

    # ---------- EXPERIENCE ----------
    content.append(Paragraph("EXPERIENCE", section_style))
    content.append(divider)

    for exp in data["Experience"]:
        start = format_date(exp["start"])
        end = "Present" if exp["present"] else format_date(exp["end"])

        left = Paragraph(f"<b>{exp['role']} | {exp['company']}</b>", body_style)
        right = Paragraph(f"<b>{start} – {end}</b>", body_style)
        table = Table([[left, right]], colWidths=[440, 100])
        table.setStyle(TableStyle([('ALIGN', (1, 0), (1, 0), 'RIGHT'), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
        table.keepWithNext = True
        content.append(table)

        for i, line in enumerate(exp["desc"].split("\n")):
            p = Paragraph(line, bullet_style, bulletText="•")
            p.keepWithNext = True
            content.append(p)
        content.append(Spacer(1, 4))
        content.append(divider_white)
    content.append(divider_white)

    # ---------- PROJECTS ----------
    content.append(Paragraph("PROJECTS", section_style))
    content.append(divider)

    for proj in data["Projects"]:
        left = Paragraph(f"<b>{proj['name']}</b>", body_style)
        right = Paragraph(f"<b>{proj['mon']} {proj['year']}</b>", body_style)
        table = Table([[left, right]], colWidths=[470, 60])
        table.setStyle(TableStyle([('ALIGN', (1, 0), (1, 0), 'RIGHT'), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
        table.keepWithNext = True
        content.append(table)

        for i, line in enumerate(proj["desc"].split("\n")):
            p = Paragraph(line, bullet_style, bulletText="•")
            p.keepWithNext = True
            content.append(p)
        content.append(Spacer(1, 4))
        content.append(divider_white)

    # ---------- EDUCATION ----------
    content.append(Paragraph("EDUCATION", section_style))
    content.append(divider)

    for edu in data["Education"]:
        left = Paragraph(f"<b>{edu['degree']}</b><br/>{edu['school']}", body_style)
        right = Paragraph(f"<b>{edu['year']}</b>", body_style)
        table = Table([[left, right]], colWidths=[490, 40])
        table.setStyle(TableStyle([('ALIGN', (1, 0), (1, 0), 'RIGHT'), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
        table.keepWithNext = True
        content.append(table)

    # ---------- CERTIFICATIONS ----------
    content.append(Paragraph("CERTIFICATIONS", section_style))
    content.append(divider)

    for cert in data["Certifications"]:
        left = Paragraph(f"<b><a href='{cert['url']}'>{cert['name']}</a></b>", body_style)
        right = Paragraph(f"<b>{cert['year']}</b>", body_style)
        table = Table([[left, right]], colWidths=[490, 40])
        table.setStyle(TableStyle([('ALIGN', (1, 0), (1, 0), 'RIGHT'), ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')]))
        table.keepWithNext = True
        content.append(table)

    # ---------- BUILD ----------
    doc.build(content)

def generate_and_upload_pdf(data, foldername):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        pdf_path = tmp.name
    create_resume_from_data(data, pdf_path)

    s3.upload_file(
        pdf_path,
        "resume-tanmay",
        f"resume/{foldername}/Tanmay_Melanta_Resume.pdf",
        ExtraArgs={"ContentType": "application/pdf"}
    )

# ---------------- SESSION ----------------
if "resume_data" not in st.session_state:
    st.session_state.resume_data = {
        "DS": init_role(),
        "CDE": init_role(),
        "SA": init_role()
    }

if "edit_mode" not in st.session_state:
    st.session_state.edit_mode = {
        "DS": False,
        "CDE": False,
        "SA": False
    }

# ---------------- TABS ----------------
tab1, tab2, tab3 = st.tabs([
    "Data Scientist",
    "Cloud Data Engineer",
    "Solutions Architect"
])

tabs = {
    "DS": tab1,
    "CDE": tab2,
    "SA": tab3
}

# ---------------- MAIN ----------------
for role_key, tab in tabs.items():
    with tab:

        # Load once
        if f"loaded_{role_key}" not in st.session_state:
            st.session_state.resume_data[role_key] = load_resume_from_s3(
                st.session_state.resume_data[role_key],
                f"{role_key}_resume"
            )
            st.session_state[f"loaded_{role_key}"] = True

        data = st.session_state.resume_data[role_key]

        st.subheader(f"{role_key} Resume")
        st.write(f"https://resume-tanmay.s3.ap-south-1.amazonaws.com/resume/{role_key}/Tanmay_Melanta_Resume.pdf")

        # -------- Buttons --------
        c1, c2 = st.columns(2)

        with c1:
            if st.button(f"Edit {role_key}", use_container_width=True):
                st.session_state.edit_mode[role_key] = True

        with c2:
            if st.button(f"Save {role_key}", use_container_width=True):
                st.session_state.edit_mode[role_key] = False
                upload_to_s3(data, f"{role_key}_resume")
                generate_and_upload_pdf(data, f"{role_key}")

        disabled = not st.session_state.edit_mode[role_key]

        # ---------- BASIC INFO ----------
        data["Target Roles"] = st.text_input(
            "Target Roles",
            data["Target Roles"],
            key=f"{role_key}_target",
            disabled=disabled
        )

        data["Summary"] = st.text_area(
            "Summary",
            data["Summary"],
            key=f"{role_key}_summary",
            disabled=disabled
        )

        # ---------- SKILLS ----------
        st.subheader("Skills")

        if st.session_state.edit_mode[role_key] and st.button(f"Add Skill {role_key}"):
            data["Skills"].append({"title": "", "items": ""})
        delete_index = None

        for i in range(len(data["Skills"])):
            s = data["Skills"][i]
            c1, c2, c3 = st.columns([4, 6, 1])
            s["title"] = c1.text_input("Title", s["title"], key=f"{role_key}_skill_title_{i}", disabled=disabled)
            s["items"] = c2.text_input("Items", s["items"], key=f"{role_key}_skill_items_{i}", disabled=disabled)
            c3.markdown("""<div style="height:28px;"></div>""", unsafe_allow_html=True)
            if st.session_state.edit_mode[role_key] and c3.button("❌", key=f"{role_key}_del_skill_{i}"):
                delete_index = i

        if delete_index is not None:
            data["Skills"].pop(delete_index)
            st.rerun()

        # ---------- EXPERIENCE ----------
        st.subheader("Experience")

        if st.session_state.edit_mode[role_key] and st.button(f"Add Exp {role_key}"):
            data["Experience"].append({
                "company": "",
                "role": "",
                "start": date.today(),
                "end": date.today(),
                "present": False,
                "desc": ""
            })

        for i, e in enumerate(data["Experience"]):
            c1, c2 = st.columns([3.5, 1])
            c1.markdown(f"##### Experience {i+1}")
            if st.session_state.edit_mode[role_key] and c2.button("Delete", key=f"{role_key}_del_exp_{i}", use_container_width=True):
                data["Experience"].pop(i)
                st.rerun()

            c1, c2 = st.columns(2)
            e["company"] = c1.text_input("Company", e["company"], key=f"{role_key}_comp_{i}", disabled=disabled)
            e["role"] = c2.text_input("Role", e["role"], key=f"{role_key}_role_{i}", disabled=disabled)

            c1, c2, c3 = st.columns(3)
            e["start"] = c1.date_input("Start", e["start"], key=f"{role_key}_start_{i}", disabled=disabled)
            e["end"] = c2.date_input("End", e["end"], key=f"{role_key}_end_{i}", disabled=disabled)
            c3.markdown("""<div style="height:34px;"></div>""", unsafe_allow_html=True)
            e["present"] = c3.checkbox("Present", e["present"], key=f"{role_key}_present_{i}", disabled=disabled)

            e["desc"] = st.text_area("Description", e["desc"], key=f"{role_key}_desc_{i}", disabled=disabled)

        # ---------- PROJECTS ----------
        st.subheader("Projects")

        if st.session_state.edit_mode[role_key] and st.button(f"Add Project {role_key}"):
            data["Projects"].append({"name": "", "year": "", "desc": ""})

        for i, p in enumerate(data["Projects"]):
            c1, c2 = st.columns([3.5, 1])
            c1.markdown(f"##### Project {i+1}")
            if st.session_state.edit_mode[role_key] and c2.button("Delete", key=f"{role_key}_del_proj_{i}", use_container_width=True):
                data["Projects"].pop(i)
                st.rerun()

            c1, c2, c3 = st.columns([4, 1, 1])
            p["name"] = c1.text_input("Project Name", p["name"], key=f"{role_key}_proj_name_{i}", disabled=disabled)
            default_index = months.index(p["mon"])
            p["mon"] = c2.selectbox("Month", months, index=default_index, key=f"{role_key}_proj_mon_{i}", disabled=disabled)
            p["year"] = c3.text_input("Year", p["year"], key=f"{role_key}_proj_year_{i}", disabled=disabled)
            p["desc"] = st.text_area("Description", p["desc"], key=f"{role_key}_proj_desc_{i}", disabled=disabled)

        # ---------- EDUCATION ----------
        st.subheader("Education")

        if st.session_state.edit_mode[role_key] and st.button(f"Add Edu {role_key}"):
            data["Education"].append({"school": "", "degree": "", "year": ""})

        for i, ed in enumerate(data["Education"]):
            c1, c2 = st.columns([3.5, 1])
            c1.markdown(f"##### Education {i+1}")
            if st.session_state.edit_mode[role_key] and c2.button("Delete", key=f"{role_key}_del_ed_{i}", use_container_width=True):
                data["Education"].pop(i)
                st.rerun()

            ed["school"] = st.text_input("School", ed["school"], key=f"{role_key}_school_{i}", disabled=disabled)
            ed["degree"] = st.text_input("Degree", ed["degree"], key=f"{role_key}_degree_{i}", disabled=disabled)
            ed["year"] = st.text_input("Year", ed["year"], key=f"{role_key}_year_{i}", disabled=disabled)

        # ---------- CERTIFICATIONS ----------
        st.subheader("Certifications")
        if st.session_state.edit_mode[role_key] and st.button(f"Add Cert {role_key}"):
            data["Certifications"].append({"name": "", "url": "", "year": ""})

        for i, c in enumerate(data["Certifications"]):
            c1, c2, c3, c4 = st.columns([3, 4, 1, 1])
            c["name"] = c1.text_input("Certification", c["name"], key=f"{role_key}_cert_{i}", disabled=disabled)
            c["url"] = c2.text_input("Link", c["url"], key=f"{role_key}_cert_url_{i}", disabled=disabled)
            c["year"] = c3.text_input("Year", c["year"], key=f"{role_key}_cert_year_{i}", disabled=disabled)
            c4.markdown("""<div style="height:28px;"></div>""", unsafe_allow_html=True)
            if st.session_state.edit_mode[role_key] and c4.button("Delete", key=f"{role_key}_del_cert_{i}",use_container_width=True):
                data["Certifications"].pop(i)
                st.rerun()

        # ---------- LANGUAGES ----------
        st.subheader("Languages")

        if st.session_state.edit_mode[role_key] and st.button(f"Add Language"):
            data["Languages"].append({"name": ""})

        for i, l in enumerate(data["Languages"]):
            c1, c2 = st.columns([3.5, 1])
            l["name"] = c1.text_input("Language", l["name"], key=f"{role_key}_lang_{i}", disabled=disabled)
            c2.markdown("""<div style="height:28px;"></div>""", unsafe_allow_html=True)
            if st.session_state.edit_mode[role_key] and c2.button("Delete", key=f"{role_key}_del_lang_{i}"):
                data["Languages"].pop(i)
                st.rerun()
                
        # ---------- PREVIEW ----------
        st.subheader("Preview JSON")
        st.json(data)
