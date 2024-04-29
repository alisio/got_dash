import streamlit as st

options = ["Option 1", "Option 2", "Option 3"]
selected_option = st.session_state.get("my_radio", "")

def handle_button(new_option):
    st.session_state["my_radio"] = new_option

# Update the main() function to add a set of radio buttons using st.radio():
def main():
    st.title("My App")
    for option in options:
        if option == selected_option:
            new_button = st.radio(label=option, index=-1, value=option, on_change=handle_button)
        else:
            new_button = st.radio(label=option, index=-1, on_change=handle_button)

st.radio
            
main()