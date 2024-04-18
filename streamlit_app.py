import pandas as pd
import streamlit as st


# ---------- config ----------

# st.set_page_config(layout="wide")


# ---------- functions ----------

def callback1():
    st.session_state.button1_clicked = True

def callback2():
    st.session_state.button2_clicked = True

def callback3():
    st.session_state.button3_clicked = True

def callback4():
    st.session_state.button4_clicked = True

def callback5():
    st.session_state.button5_clicked = True


# ---------- session state ----------

if "button1_clicked" not in st.session_state:
    st.session_state.button1_clicked = False

if "button2_clicked" not in st.session_state:
    st.session_state.button2_clicked = False

if "button3_clicked" not in st.session_state:
    st.session_state.button3_clicked = False

if "button4_clicked" not in st.session_state:
    st.session_state.button4_clicked = False

if "button5_clicked" not in st.session_state:
    st.session_state.button5_clicked = False

if "df" not in st.session_state:
    st.session_state.df = None

if "question_pool" not in st.session_state:
    st.session_state.question_pool = None

if "current_row" not in st.session_state:
    st.session_state.current_row = None

# ---------- main page ----------

st.markdown("# English Homework Helper")

uploaded_file = st.file_uploader("Upload a .csv homework file", type=["csv"])

if uploaded_file is not None:

    if st.session_state.df is None:
        st.session_state.df = pd.read_csv(uploaded_file, delimiter=";", usecols=["phrase","hint","translation"])

    st.write(f"There are {st.session_state.df.shape[0]} phrases in this file.")

    col4, col5 = st.columns(2)

    with col4:
        practice_twenty = st.button(
            "Practice twenty phrases", on_click=callback4, use_container_width=True
        )

    with col5:
        practice_all = st.button(
            "Practice all phrases", on_click=callback5, use_container_width=True
        )

    st.divider()

    # if practice_twenty:
    #     st.session_state.button1_clicked = False
    #     st.session_state.button2_clicked = False
    #     st.session_state.button3_clicked = False

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

    if phrase:

        if st.session_state.question_pool is None:
            st.session_state.question_pool = st.session_state.df.sample(20)

        st.session_state.current_row = st.session_state.question_pool.sample()
        st.session_state.current_index = st.session_state.current_row.index
        st.session_state.current_phrase = st.session_state.current_row["phrase"].item()
        st.session_state.current_hint = st.session_state.current_row["hint"].item()
        st.session_state.current_translation = st.session_state.current_row["translation"].item()

        with col1:
            st.markdown(st.session_state.current_phrase)

    if hint:
        if st.session_state.button1_clicked:
            with col1:
                st.markdown(st.session_state.current_phrase)
            with col2:
                st.markdown(st.session_state.current_hint)

    if translation:
        if st.session_state.button2_clicked:
            if st.session_state.button1_clicked:
                with col1:
                    st.markdown(st.session_state.current_phrase)
                with col2:
                    st.markdown(st.session_state.current_hint)
                with col3:
                    st.markdown(st.session_state.current_translation)
