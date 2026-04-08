import streamlit as st
import subprocess
import google.generativeai as genai
import os

# --- APP CONFIG ---
st.set_page_config(page_title="HackerAI Private", page_icon="🕵️", layout="wide")
st.title("💀 Private HackerAI Terminal")

# Sidebar for API Key
with st.sidebar:
    st.header("Settings")
    api_key = st.text_input("Enter Gemini API Key", type="password")
    if api_key:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash')
    st.info("Get a free key at aistudio.google.com")

if not api_key:
    st.warning("Please enter your API key in the sidebar to start.")
    st.stop()

# --- FEATURES (TABS) ---
tab1, tab2, tab3 = st.tabs(["🌐 Network Recon", "📄 Code Auditor", "🐍 Exploit Gen"])

# --- TAB 1: NETWORK RECON (NMAP/SQLMAP) ---
with tab1:
    st.header("Network & Web Scanner")
    target = st.text_input("Target URL or IP", placeholder="example.com")
    scan_type = st.selectbox("Scan Type", ["Quick Scan (Nmap)", "SQL Injection Check (SQLmap)"])
    
    if st.button("Execute Scan"):
        with st.spinner("Hacking in progress..."):
            try:
                if "Nmap" in scan_type:
                    cmd = ["nmap", "-F", target]
                else:
                    cmd = ["sqlmap", "-u", target, "--batch", "--random-agent", "--level=1"]
                
                output = subprocess.check_output(cmd, stderr=subprocess.STDOUT).decode()
                st.code(output)
                
                # AI Analysis of the scan
                st.subheader("🤖 AI Analysis")
                analysis = model.generate_content(f"Analyze these scan results for vulnerabilities: {output}")
                st.write(analysis.text)
            except Exception as e:
                st.error(f"Error: {e}")

# --- TAB 2: CODE AUDITOR (STATIC ANALYSIS) ---
with tab2:
    st.header("Source Code Security Audit")
    uploaded_file = st.file_uploader("Upload Code File (.py, .js, .php, .c)", type=["py", "js", "php", "c", "cpp"])
    
    if uploaded_file:
        code_content = uploaded_file.read().decode()
        st.code(code_content[:500] + "...", language="python")
        
        if st.button("Audit Code"):
            with st.spinner("Analyzing logic flaws..."):
                prompt = f"Perform a deep security audit on this code. Find OWASP top 10 bugs and provide a fix:\n\n{code_content}"
                response = model.generate_content(prompt)
                st.markdown(response.text)

# --- TAB 3: EXPLOIT GEN (PAYLOADS) ---
with tab3:
    st.header("Autonomous Exploit Generator")
    vuln_desc = st.text_area("Describe the vulnerability found", placeholder="e.g. Reflected XSS on the search parameter")
    
    if st.button("Generate PoC"):
        with st.spinner("Writing exploit code..."):
            prompt = f"Write a professional Proof of Concept (PoC) exploit script for the following vulnerability: {vuln_desc}. Add a warning that this is for educational purposes only."
            response = model.generate_content(prompt)
            st.markdown(response.text)
              
