import streamlit as st
import google.generativeai as genai

genai.configure(api_key="AIzaSyDyA7SzD1dFuIyxQQqjngZmO6UZPLWN1es")
model = genai.GenerativeModel("models/gemini-1.5-flash")

PROMPT_TEMPLATES = {
    "Career Roadmap": """
You are a career coach. Create a structured {weeks}-week roadmap for someone with skills in {domain} who wants to become a {goal}.
Each week must include:
- Topics to learn
- Hands-on tasks
- Free and paid resources
- Certification guidance (if requested)
User preferences:
- Learning style: {style}
- Budget: {budget}
- Certifications: {certs}
- Region: {region}
""",
    "Skill Gap Analyzer": """
User knows: {domain}
Wants to become: {goal}
Generate a {weeks}-week roadmap to fill the skill gap.
Include weekly goals, resources, and any certifications if needed.
Preferred learning: {style}, Budget: {budget}, Certifications: {certs}
""",
    "Self-Development": """
Create a personalized {weeks}-week roadmap to improve in {domain}.
Include: emotional development, daily habits, free tools, motivational tasks, and journaling prompts.
""",
    "Exam Prep": """
Generate a {weeks}-week preparation plan for the {domain} exam.
Include:
- Daily or weekly topics
- Mock tests and past paper sources
- Free and paid video/book resources
- Time management tips
- Certification/test series if applicable
"""
}

st.set_page_config(page_title="Roadmap Generator", layout="wide")

st.title("Roadmap Generator")
st.subheader("Generate a step-by-step plan tailored to your goals")

st.divider()

col1, col2 = st.columns(2)

with col1:
    domain = st.text_input("Your current skills or background", value="Data Science")
    goal = st.text_input("Target role or goal", value="Machine Learning Engineer")
    use_case = st.selectbox("Type of roadmap", list(PROMPT_TEMPLATES.keys()))

with col2:
    weeks = st.slider("Duration (in weeks)", 4, 16, 6)
    style = st.selectbox("Preferred learning method", ["Video Courses", "Books", "Projects", "Mixed"])
    budget = st.radio("Budget", ["Free Only", "Free + Paid"])
    certs = st.radio("Do you want certifications?", ["Yes", "No"])
    region = st.text_input("Your region", value="India")

if st.button("Generate"):
    try:
        prompt_template = PROMPT_TEMPLATES[use_case]
        prompt = prompt_template.format(
            domain=domain,
            goal=goal or domain,
            weeks=weeks,
            style=style,
            budget=budget,
            certs=certs,
            region=region
        )

        with st.spinner("Generating your roadmap..."):
            response = model.generate_content(prompt)
            st.success("Roadmap ready.")
            st.code(response.text, language="markdown")

    except Exception as e:
        st.error(f"Something went wrong: {str(e)}")

st.divider()
st.caption("Generated using Streamlit and Gemini AI.")
