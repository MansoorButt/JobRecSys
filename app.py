import streamlit as st

from src.helper import extract_text_from_pdf, ask_groq
from src.job_api import fetch_linkedin_jobs

st.set_page_config(page_title="Job Rec System",layout="wide")
st.title("📃 AI Job Recommendation System")
st.markdown("Upload your Resume and get recommendation based on your skills and experience from LinkedIn")

uploaded_file = st.file_uploader("Upload your resume",type=["pdf"])

if uploaded_file:
    with st.spinner('Processing your resume...'):
        resume_text = extract_text_from_pdf(uploaded_file)

    with st.spinner('Generating your Summary...'):
        summary = ask_groq(f"Summarize this resume highlighting the skills ,education and experience:\n\n{resume_text}")

    with st.spinner('Finding Skill gaps...'):
        gaps = ask_groq(f"Analyze this resume and highlight missing skills ,certifications and experiences needed for better job opportunities:\n\n{resume_text}")

    with st.spinner('Creating a Roadmap...'):
        roadmap = ask_groq(f"Based on this resume suggest a future roadmap to improve this person's career prospect(Skills to learn,certifications needed ,industry exposure):\n\n{resume_text}")

    # Display nicely formatted results
    st.markdown("---")
    st.header("📑 Resume Summary")
    st.markdown(
        f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{summary}</div>",
        unsafe_allow_html=True)

    st.markdown("---")
    st.header("🛠️ Skill Gaps & Missing Areas")
    st.markdown(
        f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{gaps}</div>",
        unsafe_allow_html=True)

    st.markdown("---")
    st.header("🚀 Future Roadmap & Preparation Strategy")
    st.markdown(
        f"<div style='background-color: #000000; padding: 15px; border-radius: 10px; font-size:16px; color:white;'>{roadmap}</div>",
        unsafe_allow_html=True)

    st.success("✅ Analysis Completed Successfully!")

    if st.button("🔎 Get Job Recommendation"):
        with st.spinner('Fetching Job Recommendation...'):
            keywords = ask_groq(
                f"Based on this resume summary , suggest the best job titles and keywords for searching job. Give a comma-separated list only,no explanation.\n\nSummary: {summary}"
            )

            search_keywords = keywords.replace("\n","").strip()

        st.success(f"Extracted Job Keywords :{search_keywords}")

        with st.spinner('Fetching Job Recommendation from LinkedIn...'):
            linkedin_jobs = fetch_linkedin_jobs(search_keywords)

        st.markdown("---")
        st.header("💼 Top LinkedIn Jobs")

        if linkedin_jobs:
            for job in linkedin_jobs:
                st.markdown(f"**{job.get('title')}** at *{job.get('companyName')}*")
                st.markdown(f"- 📍 {job.get('location')}")
                st.markdown(f"- 🔗 [View Job]({job.get('link')})")
                st.markdown("---")
        else:
            st.warning("No LinkedIn jobs found.")


