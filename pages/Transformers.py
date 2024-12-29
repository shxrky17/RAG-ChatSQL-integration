import streamlit as st

# Set page configuration
st.set_page_config(page_title="Yash's Portfolio", layout="wide")
st.markdown("""
    <header style="text-align: center; padding: 10px; background-color: black; margin-top: 30px;">
        <p style="background-color: red">&copy; 2024 Yash. All Rights Reserved.</p>
    </header>
""", unsafe_allow_html=True)
st.markdown("""
    <style>
        .img{
            width: 10px;
            height: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# HTML structure with class
st.markdown("""<div class="img">""", unsafe_allow_html=True)
st.image("assets/a.webp")  # Just load the image
st.markdown("""</div>""", unsafe_allow_html=True)

# Inject custom CSS for styling
# Inject custom CSS for styling
st.markdown("""
    <style>
        body {
            border: 5px solid #4CAF50;  # Add a green border
            padding: 20px;  # Optional: adds space between the border and content
            border-radius: 10px;  # Optional: adds rounded corners to the border
        }

        .header {
            font-size: 3em;
            color: #3b3b3b;
            text-align: left;
            font-family: 'Helvetica', sans-serif;
        }

        .subheader {
            font-size: 1.5em;
            color: #2b2b2b;
            text-align: center;
        }

        .content {
            font-size: 1.2em;
            color: #555;
        }

        .contact-section {
            background-color: #white;
            padding: 50px 10px;
        }

        .portfolio-item {
            padding: 20px;
            border: 1px solid #ddd;
            border-radius: 10px;
            margin-bottom: 20px;
        }

        .portfolio-item img {
            width: 100%;
            height: auto;
            border-radius: 10px;
        }

        .button {
            display: inline-block;
            padding: 10px 20px;
            padding-right:20px;
            margin-top: 20px;
            font-size: 1em;
            background-color: #4CAF50;
            color: white;
            text-align: center;
            border-radius: 5px;
            text-decoration: none;
        }

        .button:hover {
            background-color: #white;
        }

        .contact-button {
            display: inline-block;
            padding: 12px 30px;
            background-color: #4CAF50;
            color: white;
            font-size: 1.2em;
            text-align: center;
            border-radius: 5px;
            text-decoration: none;
            cursor: pointer;
            width: 100%;
        }

        .contact-button:hover {
            background-color: #45a049;
        }
    </style>
""", unsafe_allow_html=True)


# Title Section (Home)
st.title("Welcome to My Portfolio")

# Add a brief introduction
st.subheader("Hi! I'm Yash, a passionate developer.")
st.write("I specialize in Full-Stack Web Development, Machine Learning, and Data Science. "
         "Feel free to browse my work and get in touch.")

# About Section
st.header("About Me")
st.write("I'm a passionate learner who loves solving problems with technology. "
         "I have experience in multiple fields, including Machine Learning, Web Development, and DevOps. "
         "I believe in building impactful solutions and continuously improving my skills.")

# Projects Section
st.header("Projects")

# Project 1
col1, col2,col3 = st.columns([1, 2,1])
with col1:
    st.image("assets/project1.jpg", caption="Project 1", use_column_width=True)
with col2:
    st.subheader("Project 1: Web App Development")
    st.write("Description: A web application that allows users to track their tasks and manage daily activities. "
             "Built with React and Flask. Hosted on AWS.")
    st.markdown("[Check it out](https://www.youtube.com/watch?v=9n4Ch2Dgex0&t=948s)", unsafe_allow_html=True)

# Project 2
col1, col2,col3 = st.columns([1, 2,1])
with col1:
    st.image("assets/project2.jpg", caption="Project 2", use_column_width=True)
with col2:
    st.subheader("Project 2: Machine Learning Model")
    st.write("Description: A machine learning model that predicts house prices based on various features. "
             "Built with Python and Scikit-Learn.")
    st.markdown("[View the code](https://github.com/username/project2)", unsafe_allow_html=True)

# Project 3
col1, col2,col3 = st.columns([1, 2,1])
with col1:
    st.image("assets/project3.jpg", caption="Project 3", use_column_width=True)
with col2:
    st.subheader("Project 3: Data Visualization Dashboard")
    st.write("Description: A dashboard built with Plotly and Dash to visualize sales data and performance metrics.")
    st.markdown("[View the demo](https://example.com)", unsafe_allow_html=True)

# Contact Section
st.markdown("<div class='contact-section'>", unsafe_allow_html=True)
st.header("Contact Me")
st.write("Feel free to reach out if you want to collaborate on a project or just say hi!")

# Create a form in Streamlit to handle contact submission
with st.form(key="contact_form"):
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    message = st.text_area("Your Message")
    
    # Add a submit button
    submit_button = st.form_submit_button("Send Message")
    
    # Handle form submission
    if submit_button:
        if name and email and message:
            st.success("Your message has been sent! I'll get back to you soon.")
        else:
            st.error("Please fill out all the fields.")
st.markdown("</div>", unsafe_allow_html=True)

# Footer Section
st.markdown("""
    <footer style="text-align: center; padding: 10px; background-color: #f1f1f1; margin-top: 30px;">
        <p>&copy; 2024 Yash. All Rights Reserved.</p>
    </footer>
""", unsafe_allow_html=True)
