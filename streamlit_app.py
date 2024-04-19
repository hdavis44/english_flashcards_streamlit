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
    state.user_input = None

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

if "df_remaining" not in state:
    state.df_remaining = None

if "df_question_pool" not in state:
    state.df_question_pool = None

if "df_complete" not in state:
    state.df_complete = None

if "df_review" not in state:
    state.df_review = None

if "current_row" not in state:
    state.current_row = None

if "user_translation" not in state:
    state.user_translation = None

SAMPLE_SIZE = 20

# ---------- main page ----------

st.markdown("## English Homework Helper")

uploaded_file = st.file_uploader("Upload a .csv homework file", type=["csv"], label_visibility="collapsed")

if uploaded_file is not None:

    st.divider()

    if state.df is None:
        state.df = pd.read_csv(uploaded_file, delimiter=";", usecols=["phrase","hint","translation"])

    if state.df_remaining is None:
        state.df_remaining = state.df.copy()

    if state.df_question_pool is None:
        state.df_question_pool = state.df_remaining.sample(SAMPLE_SIZE, replace=False)
        state.df_remaining = state.df_remaining[~state.df_remaining.index.isin(state.df_question_pool.index.to_list())]

    if state.df_complete is None:
        state.df_complete = pd.DataFrame({"phrase":[], "hint":[], "translation":[]})

    if state.df_review is None:
        state.df_review = pd.DataFrame({"phrase":[], "hint":[], "translation":[]})

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
        state.current_row = state.df_question_pool.sample()
        state.current_index = state.current_row.index
        state.current_phrase = state.current_row["phrase"].item()
        state.current_hint = state.current_row["hint"].item()
        state.current_translation = state.current_row["translation"].item()
        with col1:
            st.markdown(state.current_phrase)

    if hint:
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
        state.df_complete.loc[state.current_index[0]] = state.current_row.loc[state.current_index[0]]
        state.df_question_pool.drop(index=state.current_index, inplace=True)
        if state.df_question_pool.shape[0] == 0:
            state.df_question_pool = state.df_review.copy()
            state.df_review = pd.DataFrame({"phrase":[], "hint":[], "translation":[]})
            if state.df_question_pool.shape[0] == 0:
                if state.df_remaining.shape[0] < SAMPLE_SIZE:
                    state.df_question_pool = state.df_remaining.copy()
                else:
                    state.df_question_pool = state.df_remaining.sample(SAMPLE_SIZE)
                state.df_remaining = state.df_remaining[~state.df_remaining.index.isin(state.df_question_pool.index.to_list())]

    elif incorrect:
        state.df_review.loc[state.current_index[0]] = state.current_row.loc[state.current_index[0]]
        state.df_question_pool.drop(index=state.current_index, inplace=True)

        if state.df_question_pool.shape[0] == 0:
            state.df_question_pool = state.df_review.copy()
            state.df_review = pd.DataFrame({"phrase":[], "hint":[], "translation":[]})
            if state.df_question_pool.shape[0] == 0:
                if state.df_remaining.shape[0] < SAMPLE_SIZE:
                    state.df_question_pool = state.df_remaining.copy()
                    if state.df_question_pool.shape[0] == 0:
                        st.empty()
                else:
                    state.df_question_pool = state.df_remaining.sample(SAMPLE_SIZE)
                state.df_remaining = state.df_remaining[~state.df_remaining.index.isin(state.df_question_pool.index.to_list())]

# ---------- TESTING ----------

    # if state.button1_clicked:
    #     col6, col7, col8, col9 = st.columns(4)
    #     with col6:
    #         st.write(f"state.current_phrase")
    #         st.write(state.current_phrase)
    #     with col7:
    #         st.write(f"state.df_question_pool:")
    #         st.write(state.df_question_pool["phrase"])
    #     with col8:
    #         st.write(f"state.df_complete:")
    #         st.write(state.df_complete["phrase"])
    #     with col9:
    #         st.write(f"state.df_review:")
    #         st.write(state.df_review["phrase"])
