import streamlit as st
from typing import Dict, List
from datetime import datetime
import requests

# ================== MISTRAL (OLLAMA) SETUP ==================
OLLAMA_URL = "http://localhost:11434/api/generate"

def call_mistral(prompt: str) -> str:
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        return response.json().get("response", "").strip()
    except Exception as e:
        return "(AI temporarily unavailable)"

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="AI-Assisted Internship & Opportunity Navigator",
    page_icon="🎓",
    layout="wide"
)

# ================== RAW DATASET ==================
RAW_DATA = [
    { "id": 1, "title": "Women in AI Research Fellowship", "organization": "ABC Foundation", "description": "A 6-month remote research fellowship for women in STEM focused on AI and ML.", "type": "fellowship", "year_min": 2, "year_max": 4, "tags": ["ai", "machine learning", "research", "women"], "deadline": "2026-01-20" },
  { "id": 2, "title": "Google Software Engineering Internship", "organization": "Google", "description": "A software engineering internship focusing on backend development and scalable systems.", "type": "internship", "year_min": 2, "year_max": 4, "tags": ["software engineering", "backend", "systems"], "deadline": "2025-12-31" },
  { "id": 3, "title": "AI for Social Good Research Program", "organization": "UNICEF AI Lab", "description": "A program applying AI to education access, poverty mapping, and healthcare analytics.", "type": "research", "year_min": 1, "year_max": 4, "tags": ["ai", "social good", "health", "education"], "deadline": "2026-02-10" },
  { "id": 4, "title": "Microsoft Codess Scholarship", "organization": "Microsoft", "description": "A scholarship and mentorship program supporting women in computer science.", "type": "scholarship", "year_min": 1, "year_max": 4, "tags": ["women", "computer science", "scholarship"], "deadline": "2026-01-15" },
  { "id": 5, "title": "IIT Delhi ML Winter School", "organization": "IIT Delhi", "description": "A hands-on program covering ML, CV, NLP and mathematical foundations.", "type": "program", "year_min": 1, "year_max": 4, "tags": ["machine learning", "nlp", "computer vision"], "deadline": "2025-12-28" },
  { "id": 6, "title": "Google STEP Internship", "organization": "Google", "description": "An internship for first and second-year students interested in software engineering.", "type": "internship", "year_min": 1, "year_max": 2, "tags": ["software", "engineering", "coding", "women"], "deadline": "2025-12-30" },
  { "id": 7, "title": "Amazon ML Summer School", "organization": "Amazon India", "description": "Covers supervised learning, deep learning, and ML systems.", "type": "program", "year_min": 2, "year_max": 4, "tags": ["machine learning", "deep learning"], "deadline": "2025-12-20" },
  { "id": 8, "title": "MITACS Globalink Research Internship", "organization": "Mitacs", "description": "Research internship with Canadian professors on STEM projects.", "type": "research", "year_min": 2, "year_max": 3, "tags": ["research", "international", "canada"], "deadline": "2026-03-15" },
  { "id": 9, "title": "Microsoft AI for Accessibility Grant", "organization": "Microsoft Research", "description": "Funding for students using AI to improve accessibility for people with disabilities.", "type": "fellowship", "year_min": 1, "year_max": 4, "tags": ["ai", "accessibility", "ethics"], "deadline": "2026-02-01" },
  { "id": 10, "title": "IIT Bombay Research Bootcamp in Data Science", "organization": "IIT Bombay", "description": "A project-based bootcamp covering ML pipelines, data preprocessing, and DS fundamentals.", "type": "program", "year_min": 1, "year_max": 4, "tags": ["data science", "python", "research"], "deadline": "2025-12-22" },
  { "id": 11, "title": "Grace Hopper Celebration Student Scholarship", "organization": "AnitaB.org", "description": "Scholarship for women in computing to attend the Grace Hopper Celebration.", "type": "scholarship", "year_min": 1, "year_max": 4, "tags": ["women", "computing", "conference"], "deadline": "2026-04-01" },
  { "id": 12, "title": "Stanford AI Research Apprenticeship", "organization": "Stanford AI Lab", "description": "A remote apprenticeship for undergraduates passionate about academic AI and ML research.", "type": "research", "year_min": 2, "year_max": 4, "tags": ["ai", "research", "deep learning", "nlp"], "deadline": "2026-02-20" },
  { "id": 13, "title": "Women Techmakers Engineering Fellowship", "organization": "Google", "description": "A fellowship that provides mentorship, project funding, and training for women in tech.", "type": "fellowship", "year_min": 2, "year_max": 4, "tags": ["women", "engineering", "mentorship"], "deadline": "2026-01-25" },
  { "id": 14, "title": "Deep Learning Indaba Mentorship Program", "organization": "Indaba", "description": "A mentorship program connecting students globally with African ML researchers.", "type": "program", "year_min": 1, "year_max": 4, "tags": ["deep learning", "machine learning", "mentorship"], "deadline": "2026-03-10" },
  { "id": 15, "title": "OpenAI Responsible AI Fellowship", "organization": "OpenAI", "description": "A prestigious fellowship for students working on safe, ethical, and socially responsible AI.", "type": "fellowship", "year_min": 3, "year_max": 4, "tags": ["ai safety", "ethics", "policy", "research"], "deadline": "2026-03-30" }
]

# ================== DATA PROCESSING ==================
def process_data(raw_data: List[Dict]) -> List[Dict]:
    processed = []
    today = datetime.now()

    for item in raw_data:
        deadline_date = datetime.strptime(item["deadline"], "%Y-%m-%d")
        deadline_days = (deadline_date - today).days

        processed.append({
            "id": item["id"],
            "title": item["title"],
            "type": item["type"].capitalize(),
            "required_skills": item["tags"],
            "eligible_years": list(range(item["year_min"], item["year_max"] + 1)),
            "deadline_days": deadline_days,
            "description": f"{item['organization']}: {item['description']}"
        })

    return processed

OPPORTUNITIES = process_data(RAW_DATA)

# ================== SESSION STATE ==================
if "profile" not in st.session_state:
    st.session_state.profile = {
        "skills": [],
        "interests": "",
        "academic_year": None
    }

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I can help you explore opportunities using AI."}
    ]

# ================== OPTIONS ==================
SKILL_OPTIONS = sorted(list(set(tag for opp in RAW_DATA for tag in opp["tags"])))
INTEREST_OPTIONS = ["AI", "ML", "Data Science", "Research", "Women in Tech"]

# ================== SCORING LOGIC ==================
def calculate_relevance_score(opp, profile):
    score = 0
    reasons = []

    user_skills = [s.lower() for s in profile["skills"]]
    user_year = profile["academic_year"]
    user_interest = profile["interests"].lower() if profile["interests"] else ""

    matched = [s for s in user_skills if s in [r.lower() for r in opp["required_skills"]]]
    if matched:
        score += 40
        reasons.append(f"✓ Skills match: {', '.join(matched)}")

    if user_year in opp["eligible_years"]:
        score += 15
        reasons.append("✓ Eligible for your academic year")

    if user_interest and user_interest in opp["description"].lower():
        score += 15
        reasons.append(f"✓ Matches interest in {user_interest}")

    if 0 <= opp["deadline_days"] <= 14:
        score += 15
        reasons.append("🚨 Closing soon")

    return score, reasons

def get_ranked_recommendations(profile, opportunities):
    ranked = []
    for opp in opportunities:
        score, reasons = calculate_relevance_score(opp, profile)
        if score > 0:
            ranked.append((opp, score, reasons))
    return sorted(ranked, key=lambda x: x[1], reverse=True)

# ================== CHAT HANDLER (MISTRAL) ==================
def handle_chat_query(query):
    prompt = f"""
You are an AI career assistant.
Available opportunities: {len(OPPORTUNITIES)}.
User question: "{query}"

Respond clearly and briefly.
"""
    return call_mistral(prompt)

# ================== UI ==================
st.title("🚀 AI-Assisted Opportunity Navigator")
st.markdown("---")

with st.sidebar:
    st.header("👤 Your Profile")
    with st.form("profile_form"):
        skills = st.multiselect("Skills", SKILL_OPTIONS)
        interest = st.selectbox("Interest", [""] + INTEREST_OPTIONS)
        year = st.selectbox("Academic Year", [None, 1, 2, 3, 4])

        if st.form_submit_button("Save"):
            st.session_state.profile = {
                "skills": skills,
                "interests": interest,
                "academic_year": year
            }
            st.success("Profile updated")
            st.rerun()

col1, col2 = st.columns([0.65, 0.35])

# ================== RECOMMENDATIONS ==================
with col1:
    st.subheader("📋 Recommendations")

    recommendations = get_ranked_recommendations(
        st.session_state.profile,
        OPPORTUNITIES
    )

    if not recommendations:
        st.info("Set your profile to get recommendations.")

    for opp, score, reasons in recommendations:
        st.markdown(f"### {opp['title']}")
        st.caption(f"{opp['type']} | {opp['deadline_days']} days left")
        st.write(opp["description"])
        st.metric("Match Score", score)

        with st.expander("Why recommended?"):
            for r in reasons:
                st.write(r)

            ai_prompt = f"""
Student profile:
Skills: {st.session_state.profile['skills']}
Interest: {st.session_state.profile['interests']}
Year: {st.session_state.profile['academic_year']}

Opportunity:
{opp['title']} - {opp['description']}

Explain in 2 lines why this is suitable.
"""
            st.markdown("🧠 **AI Explanation:**")
            st.write(call_mistral(ai_prompt))

        st.markdown("---")

# ================== AI CHAT ==================
with col2:
    st.subheader("💬 AI Assistant")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Ask about opportunities..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        reply = handle_chat_query(prompt)
        st.session_state.messages.append({"role": "assistant", "content": reply})
        with st.chat_message("assistant"):
            st.markdown(reply)
