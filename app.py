"""
Student Portfolio Builder
--------------------------
A simple, beginner-friendly Streamlit app that helps students collect
their personal, academic, and professional information and automatically
turns it into a clean, modern portfolio -- viewable inside the app and
downloadable as a self-contained HTML file.

Run locally / in Colab:
    streamlit run app.py

No API keys, no database, no paid services required.
"""

import streamlit as st
from datetime import datetime
import html


# =============================================================================
# PAGE CONFIG (must be the first Streamlit command)
# =============================================================================
st.set_page_config(
    page_title="Student Portfolio Builder",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =============================================================================
# SESSION STATE INITIALIZATION
# Session state is how Streamlit "remembers" data between interactions.
# We initialize every piece of data we need once, the first time the app runs.
# =============================================================================
def init_session_state():
    defaults = {
        # Personal info
        "full_name": "",
        "professional_title": "",
        "email": "",
        "phone": "",
        "location": "",
        "bio": "",
        # Education
        "degree": "",
        "university": "",
        "start_year": "",
        "grad_year": "",
        "coursework": "",
        # Lists that can grow (multiple entries)
        "skills": [],
        "projects": [],
        "certifications": [],
        "experiences": [],
        "achievements": [],
        # Social / professional links
        "linkedin": "",
        "github": "",
        "website": "",
        # Controls whether we show the builder form or the generated portfolio
        "portfolio_generated": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_session_state()


# =============================================================================
# SMALL HELPER FUNCTIONS
# =============================================================================
def safe(text):
    """Return a safe, non-empty display string and escape HTML special chars."""
    if text is None:
        return ""
    return html.escape(str(text).strip())


def has_any_personal_info():
    """Check whether the student has filled in at least the core personal info."""
    return bool(st.session_state.full_name.strip())


def remove_item(list_name, index):
    """Remove an item from a session_state list by index, then refresh the page."""
    try:
        st.session_state[list_name].pop(index)
    except IndexError:
        pass
    st.rerun()


# =============================================================================
# SIDEBAR NAVIGATION
# =============================================================================
with st.sidebar:
    st.title("🎓 Portfolio Builder")
    st.write("Fill in your information, then generate your professional portfolio.")
    st.markdown("---")

    if st.session_state.portfolio_generated:
        st.success("Your portfolio has been generated!")
        if st.button("✏️ Edit My Information", use_container_width=True):
            st.session_state.portfolio_generated = False
            st.rerun()
    else:
        st.info("Complete the form, then click **Generate Portfolio** at the bottom.")

    st.markdown("---")
    st.caption("Built with Python + Streamlit. No sign-up, no database, no API keys.")


# =============================================================================
# PART 1: THE INPUT FORM (shown when the portfolio has not been generated yet)
# =============================================================================
def render_builder():
    st.title("🎓 Student Portfolio Builder")
    st.write(
        "Enter your information below. You can add multiple skills, projects, "
        "certifications, experiences, and achievements. Optional fields can be "
        "left blank."
    )
    st.markdown("---")

    # -------------------------------------------------------------------
    # 1. PERSONAL INFORMATION
    # -------------------------------------------------------------------
    st.header("1️⃣ Personal Information")
    with st.form("personal_info_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            full_name = st.text_input(
                "Full Name *", value=st.session_state.full_name,
                placeholder="e.g. Ayesha Khan"
            )
            email = st.text_input(
                "Email *", value=st.session_state.email,
                placeholder="e.g. ayesha@example.com"
            )
            location = st.text_input(
                "Location", value=st.session_state.location,
                placeholder="e.g. Abbottabad, Pakistan"
            )
        with col2:
            professional_title = st.text_input(
                "Professional Title", value=st.session_state.professional_title,
                placeholder="e.g. Computer Science Student"
            )
            phone = st.text_input(
                "Phone Number", value=st.session_state.phone,
                placeholder="e.g. +92 300 1234567"
            )
        bio = st.text_area(
            "Short Bio / About Me", value=st.session_state.bio,
            placeholder="Write 2-3 sentences about yourself, your interests, and your goals.",
            height=120,
        )

        if st.form_submit_button("💾 Save Personal Information", use_container_width=True):
            st.session_state.full_name = full_name
            st.session_state.professional_title = professional_title
            st.session_state.email = email
            st.session_state.phone = phone
            st.session_state.location = location
            st.session_state.bio = bio
            st.success("Personal information saved.")

    st.markdown("---")

    # -------------------------------------------------------------------
    # 2. EDUCATION
    # -------------------------------------------------------------------
    st.header("2️⃣ Education")
    with st.form("education_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            degree = st.text_input(
                "Degree / Program", value=st.session_state.degree,
                placeholder="e.g. BS Computer Science"
            )
            start_year = st.text_input(
                "Start Year", value=st.session_state.start_year,
                placeholder="e.g. 2022"
            )
        with col2:
            university = st.text_input(
                "University / College", value=st.session_state.university,
                placeholder="e.g. COMSATS University"
            )
            grad_year = st.text_input(
                "Graduation Year", value=st.session_state.grad_year,
                placeholder="e.g. 2026"
            )
        coursework = st.text_area(
            "Relevant Coursework (optional)", value=st.session_state.coursework,
            placeholder="e.g. Data Structures, Machine Learning, Databases",
            height=80,
        )

        if st.form_submit_button("💾 Save Education", use_container_width=True):
            st.session_state.degree = degree
            st.session_state.university = university
            st.session_state.start_year = start_year
            st.session_state.grad_year = grad_year
            st.session_state.coursework = coursework
            st.success("Education information saved.")

    st.markdown("---")

    # -------------------------------------------------------------------
    # 3. SKILLS
    # -------------------------------------------------------------------
    st.header("3️⃣ Skills")
    st.caption("Add skills one at a time. Examples: Python, Machine Learning, Graphic Design.")

    with st.form("skill_form", clear_on_submit=True):
        col1, col2 = st.columns([4, 1])
        with col1:
            new_skill = st.text_input("Skill name", placeholder="e.g. Python", label_visibility="collapsed")
        with col2:
            add_skill = st.form_submit_button("➕ Add Skill", use_container_width=True)
        if add_skill and new_skill.strip():
            st.session_state.skills.append(new_skill.strip())
            st.success(f"Added skill: {new_skill.strip()}")

    if st.session_state.skills:
        st.write("**Your skills:**")
        badge_cols = st.columns(6)
        for i, skill in enumerate(st.session_state.skills):
            with badge_cols[i % 6]:
                st.write(f"🏷️ {skill}")
                if st.button("Remove", key=f"remove_skill_{i}"):
                    remove_item("skills", i)
    else:
        st.info("No skills added yet.")

    st.markdown("---")

    # -------------------------------------------------------------------
    # 4. PROJECTS
    # -------------------------------------------------------------------
    st.header("4️⃣ Projects")
    st.caption("Add as many projects as you like.")

    with st.form("project_form", clear_on_submit=True):
        p_name = st.text_input("Project Name", placeholder="e.g. Student Grade Tracker")
        p_desc = st.text_area("Project Description", placeholder="What does the project do? What problem does it solve?", height=90)
        p_tech = st.text_input("Technologies / Tools Used", placeholder="e.g. Python, Pandas, Streamlit")
        p_link = st.text_input("Project Link (optional)", placeholder="e.g. https://github.com/username/project")

        if st.form_submit_button("➕ Add Project", use_container_width=True):
            if p_name.strip() and p_desc.strip():
                st.session_state.projects.append({
                    "name": p_name.strip(),
                    "description": p_desc.strip(),
                    "tech": p_tech.strip(),
                    "link": p_link.strip(),
                })
                st.success(f"Added project: {p_name.strip()}")
            else:
                st.warning("Please provide at least a project name and description.")

    if st.session_state.projects:
        st.write(f"**You have added {len(st.session_state.projects)} project(s):**")
        for i, proj in enumerate(st.session_state.projects):
            with st.expander(f"📁 {proj['name']}"):
                st.write(proj["description"])
                if proj["tech"]:
                    st.caption(f"Tools: {proj['tech']}")
                if proj["link"]:
                    st.caption(f"Link: {proj['link']}")
                if st.button("🗑️ Remove Project", key=f"remove_project_{i}"):
                    remove_item("projects", i)
    else:
        st.info("No projects added yet.")

    st.markdown("---")

    # -------------------------------------------------------------------
    # 5. CERTIFICATIONS
    # -------------------------------------------------------------------
    st.header("5️⃣ Certifications")
    st.caption("Add any certificates you have earned.")

    with st.form("cert_form", clear_on_submit=True):
        c_name = st.text_input("Certificate Name", placeholder="e.g. Google Data Analytics Certificate")
        c_org = st.text_input("Issuing Organization", placeholder="e.g. Coursera / Google")
        c_year = st.text_input("Year", placeholder="e.g. 2024")

        if st.form_submit_button("➕ Add Certification", use_container_width=True):
            if c_name.strip():
                st.session_state.certifications.append({
                    "name": c_name.strip(),
                    "org": c_org.strip(),
                    "year": c_year.strip(),
                })
                st.success(f"Added certification: {c_name.strip()}")
            else:
                st.warning("Please provide at least the certificate name.")

    if st.session_state.certifications:
        st.write(f"**You have added {len(st.session_state.certifications)} certification(s):**")
        for i, cert in enumerate(st.session_state.certifications):
            col1, col2 = st.columns([5, 1])
            with col1:
                label = cert["name"]
                if cert["org"]:
                    label += f" — {cert['org']}"
                if cert["year"]:
                    label += f" ({cert['year']})"
                st.write(f"🏅 {label}")
            with col2:
                if st.button("Remove", key=f"remove_cert_{i}"):
                    remove_item("certifications", i)
    else:
        st.info("No certifications added yet.")

    st.markdown("---")

    # -------------------------------------------------------------------
    # 6. EXPERIENCE
    # -------------------------------------------------------------------
    st.header("6️⃣ Experience")
    st.caption("Internships, volunteer work, freelance work, or other experience.")

    with st.form("experience_form", clear_on_submit=True):
        e_role = st.text_input("Position / Role", placeholder="e.g. Data Analysis Intern")
        e_org = st.text_input("Organization", placeholder="e.g. ABC Tech Solutions")
        e_duration = st.text_input("Duration", placeholder="e.g. Jun 2025 - Aug 2025")
        e_desc = st.text_area("Description", placeholder="What did you do? What did you learn?", height=90)

        if st.form_submit_button("➕ Add Experience", use_container_width=True):
            if e_role.strip() and e_org.strip():
                st.session_state.experiences.append({
                    "role": e_role.strip(),
                    "org": e_org.strip(),
                    "duration": e_duration.strip(),
                    "description": e_desc.strip(),
                })
                st.success(f"Added experience: {e_role.strip()} at {e_org.strip()}")
            else:
                st.warning("Please provide at least the position and organization.")

    if st.session_state.experiences:
        st.write(f"**You have added {len(st.session_state.experiences)} experience(s):**")
        for i, exp in enumerate(st.session_state.experiences):
            with st.expander(f"💼 {exp['role']} — {exp['org']}"):
                if exp["duration"]:
                    st.caption(exp["duration"])
                st.write(exp["description"])
                if st.button("🗑️ Remove Experience", key=f"remove_exp_{i}"):
                    remove_item("experiences", i)
    else:
        st.info("No experience added yet.")

    st.markdown("---")

    # -------------------------------------------------------------------
    # 7. ACHIEVEMENTS
    # -------------------------------------------------------------------
    st.header("7️⃣ Achievements")
    st.caption("Competitions, awards, hackathons, academic achievements, etc.")

    with st.form("achievement_form", clear_on_submit=True):
        a_title = st.text_input("Achievement Title", placeholder="e.g. 1st Place - University Hackathon 2025")
        a_desc = st.text_area("Details (optional)", placeholder="A short description of the achievement.", height=70)

        if st.form_submit_button("➕ Add Achievement", use_container_width=True):
            if a_title.strip():
                st.session_state.achievements.append({
                    "title": a_title.strip(),
                    "description": a_desc.strip(),
                })
                st.success(f"Added achievement: {a_title.strip()}")
            else:
                st.warning("Please provide an achievement title.")

    if st.session_state.achievements:
        st.write(f"**You have added {len(st.session_state.achievements)} achievement(s):**")
        for i, ach in enumerate(st.session_state.achievements):
            col1, col2 = st.columns([5, 1])
            with col1:
                st.write(f"🏆 **{ach['title']}**")
                if ach["description"]:
                    st.caption(ach["description"])
            with col2:
                if st.button("Remove", key=f"remove_ach_{i}"):
                    remove_item("achievements", i)
    else:
        st.info("No achievements added yet.")

    st.markdown("---")

    # -------------------------------------------------------------------
    # 8. SOCIAL / PROFESSIONAL LINKS
    # -------------------------------------------------------------------
    st.header("8️⃣ Social / Professional Links")
    with st.form("links_form", clear_on_submit=False):
        col1, col2, col3 = st.columns(3)
        with col1:
            linkedin = st.text_input("LinkedIn (optional)", value=st.session_state.linkedin, placeholder="https://linkedin.com/in/username")
        with col2:
            github = st.text_input("GitHub (optional)", value=st.session_state.github, placeholder="https://github.com/username")
        with col3:
            website = st.text_input("Portfolio / Website (optional)", value=st.session_state.website, placeholder="https://yourwebsite.com")

        if st.form_submit_button("💾 Save Links", use_container_width=True):
            st.session_state.linkedin = linkedin
            st.session_state.github = github
            st.session_state.website = website
            st.success("Links saved.")

    st.markdown("---")

    # -------------------------------------------------------------------
    # GENERATE PORTFOLIO BUTTON
    # -------------------------------------------------------------------
    st.header("✅ Ready to Generate Your Portfolio?")
    if not has_any_personal_info():
        st.warning("Please enter at least your **Full Name** in the Personal Information section before generating your portfolio.")

    if st.button("🚀 Generate Portfolio", type="primary", use_container_width=True, disabled=not has_any_personal_info()):
        st.session_state.portfolio_generated = True
        st.rerun()


# =============================================================================
# PART 2: HTML GENERATION (used both for the download button and, optionally,
# for consistent styling reference). We build one self-contained HTML string.
# =============================================================================
def generate_portfolio_html():
    name = safe(st.session_state.full_name) or "Your Name"
    title = safe(st.session_state.professional_title)
    email = safe(st.session_state.email)
    phone = safe(st.session_state.phone)
    location = safe(st.session_state.location)
    bio = safe(st.session_state.bio)

    degree = safe(st.session_state.degree)
    university = safe(st.session_state.university)
    start_year = safe(st.session_state.start_year)
    grad_year = safe(st.session_state.grad_year)
    coursework = safe(st.session_state.coursework)

    # Skills as badges
    skills_html = "".join(
        f'<span class="badge">{safe(s)}</span>' for s in st.session_state.skills
    ) or '<p class="empty-note">No skills listed yet.</p>'

    # Projects as cards
    if st.session_state.projects:
        projects_html = ""
        for proj in st.session_state.projects:
            link_html = (
                f'<a href="{safe(proj["link"])}" target="_blank">🔗 View Project</a>'
                if proj["link"] else ""
            )
            tech_html = f'<p class="tech">🛠 {safe(proj["tech"])}</p>' if proj["tech"] else ""
            projects_html += f"""
            <div class="card">
                <h3>{safe(proj['name'])}</h3>
                <p>{safe(proj['description'])}</p>
                {tech_html}
                {link_html}
            </div>"""
    else:
        projects_html = '<p class="empty-note">No projects listed yet.</p>'

    # Experience
    if st.session_state.experiences:
        experience_html = ""
        for exp in st.session_state.experiences:
            duration_html = f'<span class="duration">{safe(exp["duration"])}</span>' if exp["duration"] else ""
            experience_html += f"""
            <div class="card">
                <h3>{safe(exp['role'])} &mdash; {safe(exp['org'])}</h3>
                {duration_html}
                <p>{safe(exp['description'])}</p>
            </div>"""
    else:
        experience_html = '<p class="empty-note">No experience listed yet.</p>'

    # Certifications
    if st.session_state.certifications:
        certs_html = ""
        for cert in st.session_state.certifications:
            meta = " &middot; ".join(filter(None, [safe(cert["org"]), safe(cert["year"])]))
            certs_html += f"""
            <div class="card small-card">
                <h4>🏅 {safe(cert['name'])}</h4>
                <p class="tech">{meta}</p>
            </div>"""
    else:
        certs_html = '<p class="empty-note">No certifications listed yet.</p>'

    # Achievements
    if st.session_state.achievements:
        achievements_html = "<ul class='achievement-list'>"
        for ach in st.session_state.achievements:
            desc = f" &mdash; {safe(ach['description'])}" if ach["description"] else ""
            achievements_html += f"<li>🏆 <strong>{safe(ach['title'])}</strong>{desc}</li>"
        achievements_html += "</ul>"
    else:
        achievements_html = '<p class="empty-note">No achievements listed yet.</p>'

    # Education block
    if degree or university:
        education_html = f"""
        <div class="card">
            <h3>{degree or 'Degree/Program'}</h3>
            <p class="tech">{university}</p>
            <p class="tech">{start_year} - {grad_year}</p>
            {"<p>" + coursework + "</p>" if coursework else ""}
        </div>"""
    else:
        education_html = '<p class="empty-note">No education information listed yet.</p>'

    # Contact block
    contact_lines = []
    if email:
        contact_lines.append(f"📧 {email}")
    if phone:
        contact_lines.append(f"📞 {phone}")
    if location:
        contact_lines.append(f"📍 {location}")
    contact_html = "<br>".join(contact_lines) or '<p class="empty-note">No contact information provided.</p>'

    # Links block
    links = []
    if st.session_state.linkedin:
        links.append(f'<a href="{safe(st.session_state.linkedin)}" target="_blank">LinkedIn</a>')
    if st.session_state.github:
        links.append(f'<a href="{safe(st.session_state.github)}" target="_blank">GitHub</a>')
    if st.session_state.website:
        links.append(f'<a href="{safe(st.session_state.website)}" target="_blank">Website</a>')
    links_html = " &nbsp;|&nbsp; ".join(links) or '<p class="empty-note">No links provided.</p>'

    year_now = datetime.now().year

    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{name} — Portfolio</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<style>
    :root {{
        --primary: #4f46e5;
        --primary-light: #eef2ff;
        --text-dark: #1f2937;
        --text-muted: #6b7280;
        --bg: #f9fafb;
        --card-bg: #ffffff;
        --border: #e5e7eb;
    }}
    * {{ box-sizing: border-box; }}
    body {{
        font-family: 'Segoe UI', Arial, sans-serif;
        margin: 0;
        background: var(--bg);
        color: var(--text-dark);
        line-height: 1.6;
    }}
    .container {{
        max-width: 900px;
        margin: 0 auto;
        padding: 0 20px 60px 20px;
    }}
    header.hero {{
        background: linear-gradient(135deg, var(--primary), #7c3aed);
        color: white;
        padding: 60px 20px;
        text-align: center;
        margin-bottom: 40px;
    }}
    header.hero h1 {{
        margin: 0 0 8px 0;
        font-size: 2.4em;
    }}
    header.hero p {{
        margin: 0;
        font-size: 1.2em;
        opacity: 0.95;
    }}
    section {{
        margin-bottom: 40px;
    }}
    section h2 {{
        font-size: 1.5em;
        border-bottom: 3px solid var(--primary);
        display: inline-block;
        padding-bottom: 6px;
        margin-bottom: 20px;
        color: var(--text-dark);
    }}
    .card {{
        background: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }}
    .small-card {{
        display: inline-block;
        width: 100%;
    }}
    .card h3 {{ margin-top: 0; margin-bottom: 6px; }}
    .card h4 {{ margin-top: 0; margin-bottom: 6px; }}
    .tech {{ color: var(--text-muted); font-size: 0.92em; margin: 4px 0; }}
    .duration {{ color: var(--text-muted); font-size: 0.9em; }}
    .badge {{
        display: inline-block;
        background: var(--primary-light);
        color: var(--primary);
        padding: 6px 14px;
        border-radius: 20px;
        margin: 4px 6px 4px 0;
        font-size: 0.9em;
        font-weight: 600;
    }}
    .achievement-list {{ list-style: none; padding: 0; }}
    .achievement-list li {{
        background: var(--card-bg);
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 10px;
    }}
    .empty-note {{ color: var(--text-muted); font-style: italic; }}
    a {{ color: var(--primary); text-decoration: none; font-weight: 600; }}
    a:hover {{ text-decoration: underline; }}
    footer {{
        text-align: center;
        color: var(--text-muted);
        font-size: 0.85em;
        padding: 30px 0;
    }}
    @media (max-width: 600px) {{
        header.hero h1 {{ font-size: 1.8em; }}
    }}
</style>
</head>
<body>

<header class="hero">
    <h1>{name}</h1>
    <p>{title}</p>
</header>

<div class="container">

    <section id="about">
        <h2>About Me</h2>
        <p>{bio or '<span class="empty-note">No bio provided yet.</span>'}</p>
    </section>

    <section id="education">
        <h2>Education</h2>
        {education_html}
    </section>

    <section id="skills">
        <h2>Skills</h2>
        <div>{skills_html}</div>
    </section>

    <section id="projects">
        <h2>Projects</h2>
        {projects_html}
    </section>

    <section id="experience">
        <h2>Experience</h2>
        {experience_html}
    </section>

    <section id="certifications">
        <h2>Certifications</h2>
        {certs_html}
    </section>

    <section id="achievements">
        <h2>Achievements</h2>
        {achievements_html}
    </section>

    <section id="contact">
        <h2>Contact</h2>
        <p>{contact_html}</p>
    </section>

    <section id="links">
        <h2>Professional Links</h2>
        <p>{links_html}</p>
    </section>

</div>

<footer>
    Portfolio generated with Student Portfolio Builder &middot; {year_now}
</footer>

</body>
</html>"""
    return html_doc


# =============================================================================
# PART 3: DISPLAY THE GENERATED PORTFOLIO INSIDE STREAMLIT
# =============================================================================
def render_portfolio():
    name = st.session_state.full_name.strip() or "Your Name"
    title = st.session_state.professional_title.strip()

    # ---- Hero / Header ----
    st.markdown(
        f"""
        <div style="
            background: linear-gradient(135deg, #4f46e5, #7c3aed);
            padding: 50px 20px;
            border-radius: 14px;
            text-align: center;
            color: white;
            margin-bottom: 30px;">
            <h1 style="margin-bottom:6px;">{safe(name)}</h1>
            <p style="font-size:1.2em; opacity:0.95; margin:0;">{safe(title)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ---- Download button ----
    portfolio_html = generate_portfolio_html()
    col1, col2 = st.columns([3, 1])
    with col2:
        st.download_button(
            label="⬇️ Download Portfolio (HTML)",
            data=portfolio_html,
            file_name=f"{name.replace(' ', '_').lower()}_portfolio.html",
            mime="text/html",
            use_container_width=True,
        )

    # ---- About Me ----
    st.header("About Me")
    st.write(st.session_state.bio.strip() or "_No bio provided yet._")

    # ---- Education ----
    st.header("🎓 Education")
    if st.session_state.degree or st.session_state.university:
        with st.container(border=True):
            st.subheader(st.session_state.degree or "Degree/Program")
            st.write(st.session_state.university)
            years = " - ".join(filter(None, [st.session_state.start_year, st.session_state.grad_year]))
            if years:
                st.caption(years)
            if st.session_state.coursework:
                st.write(f"**Relevant Coursework:** {st.session_state.coursework}")
    else:
        st.info("No education information provided.")

    # ---- Skills ----
    st.header("🛠️ Skills")
    if st.session_state.skills:
        skill_md = " ".join(f"`{s}`" for s in st.session_state.skills)
        st.markdown(skill_md)
    else:
        st.info("No skills listed.")

    # ---- Projects ----
    st.header("💻 Projects")
    if st.session_state.projects:
        for proj in st.session_state.projects:
            with st.container(border=True):
                st.subheader(proj["name"])
                st.write(proj["description"])
                if proj["tech"]:
                    st.caption(f"🛠 Tools: {proj['tech']}")
                if proj["link"]:
                    st.markdown(f"[🔗 View Project]({proj['link']})")
    else:
        st.info("No projects added yet.")

    # ---- Experience ----
    st.header("💼 Experience")
    if st.session_state.experiences:
        for exp in st.session_state.experiences:
            with st.container(border=True):
                st.subheader(f"{exp['role']} — {exp['org']}")
                if exp["duration"]:
                    st.caption(exp["duration"])
                st.write(exp["description"])
    else:
        st.info("No experience added yet.")

    # ---- Certifications ----
    st.header("🏅 Certifications")
    if st.session_state.certifications:
        cols = st.columns(2)
        for i, cert in enumerate(st.session_state.certifications):
            with cols[i % 2]:
                with st.container(border=True):
                    st.write(f"**{cert['name']}**")
                    meta = " · ".join(filter(None, [cert["org"], cert["year"]]))
                    if meta:
                        st.caption(meta)
    else:
        st.info("No certifications added yet.")

    # ---- Achievements ----
    st.header("🏆 Achievements")
    if st.session_state.achievements:
        for ach in st.session_state.achievements:
            st.markdown(f"- **{ach['title']}**" + (f" — {ach['description']}" if ach["description"] else ""))
    else:
        st.info("No achievements added yet.")

    # ---- Contact ----
    st.header("📬 Contact")
    contact_bits = []
    if st.session_state.email:
        contact_bits.append(f"📧 {st.session_state.email}")
    if st.session_state.phone:
        contact_bits.append(f"📞 {st.session_state.phone}")
    if st.session_state.location:
        contact_bits.append(f"📍 {st.session_state.location}")
    if contact_bits:
        st.write("  \n".join(contact_bits))
    else:
        st.info("No contact information provided.")

    # ---- Professional Links ----
    st.header("🔗 Professional Links")
    link_bits = []
    if st.session_state.linkedin:
        link_bits.append(f"[LinkedIn]({st.session_state.linkedin})")
    if st.session_state.github:
        link_bits.append(f"[GitHub]({st.session_state.github})")
    if st.session_state.website:
        link_bits.append(f"[Website]({st.session_state.website})")
    if link_bits:
        st.write(" &nbsp;|&nbsp; ".join(link_bits))
    else:
        st.info("No links provided.")


# =============================================================================
# MAIN APP LOGIC
# =============================================================================
if st.session_state.portfolio_generated:
    render_portfolio()
else:
    render_builder()
