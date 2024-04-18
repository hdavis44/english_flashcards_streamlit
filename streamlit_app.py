import pandas as pd
import streamlit as st


# ---------- config ----------

# st.set_page_config(layout="wide")
state = st.session_state


# ---------- functions ----------

def callback1():
    state.button1_clicked = True

def callback2():
    state.button2_clicked = True

def callback3():
    state.button3_clicked = True

def callback4():
    state.button4_clicked = True

def callback5():
    state.button5_clicked = True

def callback_text():
    state.user_translation = state.user_input
    state.user_input = ""

# ---------- session state ----------

if "button1_clicked" not in state:
    state.button1_clicked = False

if "button2_clicked" not in state:
    state.button2_clicked = False

if "button3_clicked" not in state:
    state.button3_clicked = False

if "button4_clicked" not in state:
    state.button4_clicked = False

if "button5_clicked" not in state:
    state.button5_clicked = False

if "df" not in state:
    state.df = None

if "question_pool" not in state:
    state.question_pool = None

if "df_remaining" not in state:
    state.df_remaining = None

if "current_row" not in state:
    state.current_row = None

if "user_translation" not in state:
    state.user_translation = ""

# ---------- main page ----------

st.markdown("## English Homework Helper")

uploaded_file = st.file_uploader("Upload a .csv homework file", type=["csv"], label_visibility="collapsed")

if uploaded_file is not None:

    if state.df is None:
        state.df = pd.read_csv(uploaded_file, delimiter=";", usecols=["phrase","hint","translation"])

    if state.df_remaining is None:
        state.df_remaining = state.df.copy()

    if state.question_pool is None:
        sample_size = 20
        if state.df_remaining.shape[0] < 20:
            sample_size = state.df_remaining.shape[0]
        state.question_pool = state.df_remaining.sample(sample_size, replace=False)
        state.df_remaining = state.df_remaining[~state.df_remaining.index.isin(state.question_pool.index.to_list())]

    # st.write(
    #     f"There are {state.df.shape[0]} phrases in this file. Selecting {state.question_pool.shape[0]} random phrases to practice with."
    # )

    # st.divider()

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
        user_translation = st.text_input(
            "translation",
            label_visibility="collapsed",
            key="user_input",
            placeholder="my translation",
            on_change=callback_text
        )

    if phrase:

        state.user_translation = None
        # state.button2_clicked = False
        # state.button3_clicked = False

        if state.question_pool is None:
            state.question_pool = state.df.sample(20)

        state.current_row = state.question_pool.sample()
        state.current_index = state.current_row.index
        state.current_phrase = state.current_row["phrase"].item()
        state.current_hint = state.current_row["hint"].item()
        state.current_translation = state.current_row["translation"].item()

        with col1:
            st.markdown(state.current_phrase)

    elif hint:
        if state.button1_clicked:
            with col1:
                st.markdown(state.current_phrase)
            with col2:
                st.markdown(state.current_hint)

    elif translation or state.user_translation:
        if state.button1_clicked:
            with col1:
                st.markdown(state.current_phrase)
            with col2:
                st.markdown(state.current_hint)
            with col3:
                st.markdown(f"Your answer: {state.user_translation}")
                st.markdown(f"Correct answer: {state.current_translation}")

            col4, col5 = st.columns(2)
            with col4:
                correct = st.button(":heavy_check_mark:", on_click=callback4, use_container_width=True)
            with col5:
                incorrect = st.button(":x:", on_click=callback5, use_container_width=True)

            if correct:
                pass
            elif incorrect:
                pass
