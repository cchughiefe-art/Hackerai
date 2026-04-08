import streamlit as st
import google.generativeai as genai

# --- UI CONFIG ---
st.set_page_config(page_title="HackerAI Clone", layout="centered")

# Custom CSS to mimic the sleek mobile dark-mode UI
st.markdown("""
    <style>
    .stApp { background-color: #000000; color: #FFFFFF; }
    .stChatInputContainer { bottom: 20px; }
    .greeting { text-align: center; margin-top: 100px; font-size: 24px; font-weight: bold; }
    </style>
""", unsafe_allow_html=True)

# --- APP STATE ---
if "messages" not in st.session_state:
    st.session_state.messages = []
if "mode" not in st.session_state:
    st.session_state.mode = "Ask"
if "model_choice" not in st.session_state:
    st.session_state.model_choice = "Gemini 3 Flash"

# --- TOP NAVIGATION ---
col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    if st.button("Upgrade Plan", use_container_width=True):
        st.toast("Pro features coming soon!")

# --- MAIN GREETING ---
if not st.session_state.messages:
    st.markdown('<p class="greeting">What\'s on the scope today, Courage?</p>', unsafe_allow_html=True)

# --- CHAT HISTORY ---
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- BOTTOM CONTROLS ---
# Mimicking the floating selector bar in your screenshot
c1, c2, c3 = st.columns([1, 1, 2])
with c1:
    mode_btn = st.popover(f"💬 {st.session_state.mode}")
    if mode_btn.button("Ask (Talk)"): st.session_state.mode = "Ask"
    if mode_btn.button("Agent (Execute)"): st.session_state.mode = "Agent"

with c2:
    model_btn = st.popover(f"🤖 {st.session_state.model_choice}")
    if model_btn.button("Gemini 3 Flash"): st.session_state.model_choice = "Gemini 3 Flash"
    if model_btn.button("Claude Sonnet 4.6"): st.session_state.model_choice = "Claude Sonnet 4.6"
    if model_btn.button("Grok 4.1"): st.session_state.model_choice = "Grok 4.1"

# --- CHAT INPUT ---
if prompt := st.chat_input("Ask, learn, brainstorm"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # AI RESPONSE LOGIC
    with st.chat_message("assistant"):
        # Fix: Use 'gemini-3-flash-preview' for the 2026 API
        genai.configure(api_key=st.secrets["GEMINI_KEY"])
        model = genai.GenerativeModel('gemini-3-flash-preview')
        
        # Add system context based on Mode
        context = "You are a passive security consultant." if st.session_state.mode == "Ask" else "You are an active penetration testing agent."
        full_prompt = f"{context}\nUser says: {prompt}"
        
        response = model.generate_content(full_prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
