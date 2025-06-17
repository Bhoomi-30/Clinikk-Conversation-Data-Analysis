#Create a simple UI way to visualize a conversation given an ID.

import streamlit as st
import pandas as pd

# Load the data
@st.cache_data
def load_data():
    df = pd.read_csv("Sample 100 Convos - Clinikk - To Share - sample-redacted-convos.csv")
    return df.dropna(subset=["content"])

df = load_data()

st.title("📋 Clinikk Conversation Explorer")

# Sidebar: search
st.sidebar.subheader("🔍 Search / Filter")
keyword = st.sidebar.text_input("Filter by keyword", "").strip().lower()

# Filter logic
if keyword:
    df_filtered = df[df['content'].str.lower().str.contains(keyword)]
else:
    df_filtered = df

# Text input for conversation ID
conv_id_input = st.text_input("Enter Conversation ID")

conversation_ids = df_filtered['conversation_id'].unique()

if conv_id_input:
    try:
        conv_id = int(conv_id_input)
    except ValueError:
        st.warning("Please enter a valid numeric conversation ID.")
        st.stop()
else:
    conv_id = st.selectbox("Or select a conversation ID", sorted(conversation_ids))

# Show conversation
convo = df_filtered[df_filtered['conversation_id'] == conv_id].sort_values(by="message_sent_at")

if convo.empty:
    st.error("No conversation found for this ID.")
else:
    st.markdown(f"### 🗂️ Conversation ID: `{conv_id}`")
    for _, row in convo.iterrows():
        sender = row["sender_type"]
        sender_id = row["sender_id"]
        timestamp = row["message_sent_at"]
        msg = row["content"]

        if sender == "user":
            st.markdown(
                f"<div style='background-color:#e3f2fd;color:black;padding:10px;border-radius:10px;margin-bottom:5px'>"
                f"<b>User ({sender_id})</b> <small>{timestamp}</small><br>{msg}</div>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f"<div style='background-color:#fff3e0;color:black;padding:10px;border-radius:10px;margin-bottom:5px'>"
                f"<b>Agent ({sender_id})</b> <small>{timestamp}</small><br>{msg}</div>",
                unsafe_allow_html=True
            )

#Summary stats
st.sidebar.markdown("### 📊 Summary")
st.sidebar.write(f"Total Messages: {len(convo)}")
st.sidebar.write(f"Users: {convo[convo['sender_type']=='user']['sender_id'].nunique()}")
st.sidebar.write(f"Agents: {convo[convo['sender_type']=='agent']['sender_id'].nunique()}")
