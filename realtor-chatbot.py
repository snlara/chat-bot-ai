import streamlit as st
import pandas as pd
from openai import OpenAI
import os # Added to handle file checking

# 1. DEFINE THE INSTRUCTIONS AT THE TOP
system_instruction = """
You are a specialized Real Estate Assistant for agent Salvador Lara. 
Your strict operational rules:
1. Agent Name: Always identify yourself as an assistant to Salvador Lara.
2. Location: Salvador helps with homes in California, specifically the Hayward area.
3. Property Type: Salvador ONLY deals with "fixer-uppers" and distressed properties. 
4. If a user asks for turnkey/luxury homes or properties outside CA, politely explain Salvador's niche and offer to take their info.
5. Goal: Collect the user's contact info and the property address.
6. Contact: If asked for a phone number, give the office line at 411.
"""

st.set_page_config(page_title="Salvador Lara AI Assistant", page_icon="🏠")
st.title("🏠 Salvador Lara - Hayward Fixer-Upper AI")

# Setup local client
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

# 2. INITIALIZE SESSION STATE
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_instruction}
    ]

# 3. DISPLAY CHAT HISTORY
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 4. CHAT INPUT LOGIC
if prompt := st.chat_input("Ask about Hayward fixer-uppers..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=st.session_state.messages,
                temperature=0.3
            )
            answer = response.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})

            # --- LEAD LOGGING (Moved INSIDE the try block) ---
            new_lead = {"timestamp": pd.Timestamp.now(), "query": prompt, "response": answer}
            df = pd.DataFrame([new_lead])
            
            # Save to leads.csv - only adds header if file doesn't exist
            df.to_csv("leads.csv", mode='a', index=False, header=not os.path.exists("leads.csv"))

        except Exception as e:
            st.error(f"Error connecting to LM Studio: {e}")
            st.info("Make sure LM Studio Server is started and the model is loaded.")