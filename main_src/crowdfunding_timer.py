import streamlit as st
import time

def countdown_timer(duration):
    while duration:
        mins, secs = divmod(duration, 60)
        timer = f'{mins:02d}:{secs:02d}'
        st.write(f'Time remaining: {timer}')
        time.sleep(1)
        duration -= 1
        st.session_state.timer_duration = duration  # Update the timer duration in session state
