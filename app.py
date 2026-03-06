import streamlit as st
import pandas as pd
import os
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# page layout
st.set_page_config(layout="wide")

# hide streamlit menu/footer
st.markdown("""
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# auto refresh every 3 seconds
st_autorefresh(interval=3000)

# create csv if not exists
if not os.path.exists("feedback.csv"):
    pd.DataFrame(columns=["feedback","time"]).to_csv("feedback.csv", index=False)

# create question file if missing
if not os.path.exists("question.txt"):
    with open("question.txt","w") as f:
        f.write("What do you mean by Engineering?")

# read question
with open("question.txt","r") as f:
    question = f.read()

st.title("Anonymous Feedback System")

st.markdown(f"### {question}")

# feedback form
with st.form("feedback_form", clear_on_submit=True):

    feedback = st.text_area("Write your feedback")

    submitted = st.form_submit_button("Submit Feedback")

    if submitted:

        if feedback.strip() == "":
            st.warning("Please write feedback before submitting.")

        else:

            time = datetime.now().strftime("%H:%M:%S")

            new_data = pd.DataFrame([[feedback, time]],
                                    columns=["feedback","time"])

            df = pd.read_csv("feedback.csv")
            df = pd.concat([df,new_data], ignore_index=True)

            df.to_csv("feedback.csv", index=False)

            st.success("Feedback submitted anonymously")

st.header("Live Feedback")

df = pd.read_csv("feedback.csv")

# show total responses
st.write(f"Total Responses: {len(df)}")

# newest first
df = df[::-1]

for i, row in df.iterrows():

    feedback_text = row["feedback"]
    time = row["time"]

    # newest feedback
    if i == df.index[0]:

        st.markdown(f"""
        <h1 style='font-weight:bold; color:#00FFD1; text-align:center'>
        💬 {feedback_text}
        </h1>
        <p style='text-align:center'>{time}</p>
        """, unsafe_allow_html=True)

    # older feedback
    else:

        st.markdown(f"""
        <p style='font-size:18px'>
        💬 {feedback_text} ({time})
        </p>
        """, unsafe_allow_html=True)

        st.divider()
