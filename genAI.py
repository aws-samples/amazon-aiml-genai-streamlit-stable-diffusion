import streamlit as st
import glib as glib
from io import BytesIO

def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["password"]:
            st.session_state["password_correct"] = True
            # del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

def s3_uploader(checkbox, filename, filebytes):
    if checkbox:
        glib.uploadFileToS3(filename, filebytes)
    st.session_state.filename = ''

some_prompts = {
    "default" : "Type or Select prompt. Something like - pencil sketch of pizza and some cake",
    "prompt-1": "Portrait photo side profile, looking away, serious eyes, 50mm portrait photography, hard rim lighting photography–beta –ar 2:3 –beta –upbeta –upbeta",
    "prompt-2": "High Quality, Intricately Detailed, Hyper-Realistic Lawyer Portrait Photography, Volumetric Lighting, Full Character, 4k, In Workwear, boca",
    "prompt-3": "Street style photo portrait, clear edge definition, unique and one-of-a-kind pieces, light brown and light amber, Fujifilm X-T4, Sony FE 85mm f/1.4 GM, —quality 2 —s 750 —v 5.2",
    "prompt-4": "a person in 8k resolution, photorealistic masterpiece by Aaron Horkey and Jeremy Mann, intricately detailed fluid gouache painting by Jean Baptiste, professional photography, natural lighting, volumetric lighting, maximalist, concept art, intricately detailed, complex, elegant, expansive cover"
}

# Perform some crude state management
if "input_img" not in st.session_state:
    st.session_state.input_img = ''
if "gen_img" not in st.session_state:
    st.session_state.gen_img = ''


# start rendering the App
if not check_password():
    st.stop()

st.subheader("GenAI Application (beta)")

input_img = ''
input_slider = 60
uploaded_file = st.file_uploader("**Input Image**")
if uploaded_file:
    # remove rotation (when using smart-phone camera) and resize
    input_img = glib.remove_rotation(uploaded_file.getvalue())
    st.session_state.input_img = input_img
else:
    input_img = st.session_state.input_img

if input_img:
    st.image(input_img)
    input_slider = st.slider("Image strength", 1, 100, 60)

selection = st.selectbox("**Load Prompt**", some_prompts.keys())
prompt_text = st.text_area("**Input Text Prompt**", value = some_prompts[selection], 
                           height=50, key="prompt")

process_button = st.button("Generate", type="primary")

gen_img = ''
st.subheader("Generated Image")
if process_button:
    with st.spinner("Drawing..."):
        image_bytes = input_img.getvalue() if input_img else None
        gen_img = glib.get_altered_image_from_model(prompt_content=prompt_text, image_bytes=image_bytes,
                                                    img_strength=input_slider)
        st.session_state.gen_img = gen_img
else:
    gen_img = st.session_state.gen_img
    
# generated output and download elements
if gen_img:
    st.image(gen_img)
    img_bytes = gen_img.getvalue()
    
    # placeholder for outputs
    outs = st.empty().container()
    checkbox = outs.checkbox("Upload for printing", value=True, key="checkbox")
    filename = outs.text_input("Image name (add .jpg)", key="filename")
    
    # Check if the filename already exists
    if filename and checkbox and glib.checkFileinS3(filename):
        filename = ''
        st.error("File already exists")
    
    outs.download_button(label="Download",
        data=img_bytes, 
        file_name=filename,
        mime="image/jpg",
        disabled=not filename,
        on_click=s3_uploader, 
        args=[checkbox, filename, img_bytes])