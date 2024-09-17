import streamlit as st

from haystack.dataclasses import ChatMessage

from canvas import post_to_canvas, get_courses
from syllabi import setup_pipeline, chat_with_ai


# Page config
st.set_page_config(page_title="Syllabus Creator Assistant", page_icon="📚", layout="wide")

# Initialize Streamlit session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'conversation_started' not in st.session_state:
    st.session_state.conversation_started = False
if "latest_syllabus" not in st.session_state:
    st.session_state.latest_syllabus = None
if "pipe" not in st.session_state:
    st.session_state.pipe = setup_pipeline()
if "canvas_courses" not in st.session_state:
    st.session_state.canvas_courses = {}

# Streamlit UI
st.title("Syllabus Creator Assistant")

# Reset button
if st.sidebar.button("Reset Conversation"):
    st.session_state.messages = []
    st.session_state.latest_syllabus = None
    st.session_state.conversation_started = False
    st.rerun()

# Canvas integration
st.sidebar.header("Canvas Integration")

canvas_api_key= st.sidebar.text_input("Enter Canvas API key:",type="password")

if canvas_api_key:
    if st.sidebar.button("Get Courses"):
        with st.spinner("Fetching courses..."):
            st.session_state.canvas_courses = get_courses(access_token=canvas_api_key, api_url="https://auburn.instructure.com/api/v1")
        st.sidebar.success("Courses fetched successfully!")

    if st.session_state.canvas_courses:
        course_list = st.sidebar.selectbox("Select Canvas Course:", list(st.session_state.canvas_courses.keys()))
        course_id = st.session_state.canvas_courses[course_list]
    else:
        course_list = None
        course_id = None


    if st.sidebar.button("Post Syllabus to Canvas"):
        if not course_id or not canvas_api_key:
            st.sidebar.warning("Please enter both Course ID and Canvas API Key.")
        else:
            final_message = st.session_state.messages + [ChatMessage.from_user("Give me the entire syllabus and nothing else.")]
            final_response = chat_with_ai(final_message, st.session_state.pipe)
            st.session_state.latest_syllabus = final_response.split("[FINAL_SYLLABUS]")[1].strip()

            if st.session_state.latest_syllabus:
                try:
                    if post_to_canvas(course_id, st.session_state.latest_syllabus, canvas_api_key):
                        st.sidebar.success("Syllabus successfully posted to Canvas!")
                    else:
                        st.sidebar.error("Failed to post syllabus to Canvas. Please check your course ID and API key and try again.")
                except Exception as e:
                    st.sidebar.error(f"Error posting to Canvas: {str(e)}")
            else:
                st.sidebar.warning("Please generate a syllabus before posting.")


# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message.role):
        st.markdown(message.content)

# Initialize conversation if not started
if not st.session_state.conversation_started:
    st.session_state.conversation_started = True
    initial_message = ChatMessage.from_assistant("Hello! I'm here to help you create a syllabus. Let's start with the basics. What course are you creating a syllabus for?")
    st.session_state.messages.append(initial_message)
    with st.chat_message("assistant"):
        st.markdown(initial_message.content)

# Chat input
if prompt := st.chat_input("Type your message here..."):
    st.session_state.messages.append(ChatMessage.from_user(prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

# Generate AI response
    with st.chat_message("assistant"):
        full_response = chat_with_ai(st.session_state.messages, st.session_state.pipe)
        st.markdown(full_response)
    assistant_message = ChatMessage.from_assistant(full_response)
    st.session_state.messages.append(assistant_message)

    # Check if the response contains a final syllabus
    if "[FINAL_SYLLABUS]" in full_response:
        st.session_state.latest_syllabus = full_response.split("[FINAL_SYLLABUS]")[1].strip()
        st.success("Syllabus generated successfully!")

