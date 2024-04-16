import pandas as pd
import streamlit as st


# ---------- functions ----------

def callback1():
    st.session_state.button1_clicked = True

def callback2():
    st.session_state.button2_clicked = True

def callback3():
    st.session_state.button3_clicked = True

# ---------- session state ----------

if "button1_clicked" not in st.session_state:
    st.session_state.button1_clicked = False

if "button2_clicked" not in st.session_state:
    st.session_state.button2_clicked = False

if "button2_clicked" not in st.session_state:
    st.session_state.button2_clicked = False

# ---------- main page ----------

st.markdown("# English Homework Helper")

uploaded_file = st.file_uploader("Upload a .csv file", type=["csv"])

if uploaded_file is not None:

    df = pd.read_csv(uploaded_file, delimiter=";", usecols=["phrase","hint","translation"])

    # st.write(f"columns: {df.columns.to_list()}")
    # st.write(f"row count: {df.shape[0]}")
    st.divider()

    col1, col2, col3 = st.columns(3)
    with col1:
        phrase = st.button(
            "Get new phrase", on_click=callback1, use_container_width=True
        )

    with col2:
        hint = st.button(
            "Show hint", on_click=callback2, use_container_width=True
        )

    with col3:
        translation = st.button(
            "Show translation", on_click=callback3, use_container_width=True
        )

    if phrase or st.session_state.button1_clicked:
        st.session_state.question_pool = df.sample(20)
        st.session_state.current_row = st.session_state.question_pool.sample()
        st.session_state.current_index = st.session_state.current_row.index
        st.session_state.current_phrase = st.session_state.current_row["phrase"].item()
        st.session_state.current_hint = st.session_state.current_row["hint"].item()
        st.session_state.current_translation = st.session_state.current_row["translation"].item()

        st.session_state.current_row_temp = st.session_state.current_row

        if st.session_state.button2_clicked:
            st.write(st.session_state.current_row_temp["hint"].item())
