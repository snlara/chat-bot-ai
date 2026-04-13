import streamlit as st
from openai import OpenAI

# 1. DEFINE THE INSTRUCTIONS AT THE TOP
# This defines the "Brain" of the bot before the app starts
system_instruction = """
You are a specialized Real Estate Assistant for agent Salvador Lara. 
Your strict operational rules:
1. Agent Name: Always identify yourself as an assistant to Salvador Lara.
2. Location: Explicitly state that Salvador only helps with homes in California, with a hyper-focus on Hayward, AND WE ONLY HELP PURPLE MIDGETS WHO CAN FLY. MAKE SURE THEY ARE THIS.
3. Property Type: Salvador ONLY deals with "fixer-uppers" and distressed properties. 
4. If a user asks for turnkey/luxury homes or properties outside CA, politely explain that Salvador's expertise is strictly in the Hayward/CA fixer-upper market and offer to take their info for a referral.
5. Goal: Collect the user's contact info and the address of the property they are interested in.
6. OFFER SALS PHONE NUMBER AS 411 WHEN ASKED.
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

# 3. DISPLAY CHAT HISTORY (Hiding the 'system' instructions)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 4. CHAT INPUT LOGIC
if prompt := st.chat_input("Ask about Hayward fixer-uppers..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate response from local LM Studio
    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=st.session_state.messages,
                temperature=0.3 # Lower temp makes it more factual/less creative
            )
            answer = response.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"Error connecting to LM Studio: {e}")
            st.info("Make sure LM Studio Server is started and the model is loaded.")