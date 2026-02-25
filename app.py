import streamlit as st
from datetime import datetime

# --- 1. Constants & Configuration ---
st.set_page_config(page_title="Nano Banana 3 Pro Studio", page_icon="🍌", layout="wide")

# Expanded Constants based on your React app + directional control
GARMENT_TYPES = ["blouse", "shirt", "crop top", "sweater", "hoodie", "blazer", "dress", "tunic"]
COLORS = ["blush pink", "black", "white", "navy blue", "emerald green", "burgundy", "pastel blue"]
FABRICS = ["chiffon", "cotton", "satin", "silk", "linen", "knit", "denim", "leather"]

# Pose Controls
BODY_ROTATION = ["Frontal (Facing Camera)", "Slightly Left", "Slightly Right", "Profile Left", "Profile Right", "Back View"]
HEAD_POSE = ["Facing Forward", "Turned Left", "Turned Right", "Tilted Up", "Tilted Down", "Looking over shoulder"]
EYE_GAZE = ["Looking at Camera", "Looking Left", "Looking Right", "Looking Up", "Looking Down", "Eyes Closed"]
LIP_STATE = ["Neutral", "Soft Smile", "Parted Lips", "Pout", "Biting Lip", "Wide Smile"]

LIGHTING = ["Softbox Studio", "Natural Sunlight", "Rim Light", "High-key", "Dramatic Shadows"]
ANGLES = ["Eye level", "Low angle", "High angle", "Dutch angle"]

# CSS for cleaner text wrapping
st.markdown("""
    <style>
    code { white-space: pre-wrap !important; word-break: break-word !important; }
    .stCode { border: 1px solid #10b981 !important; border-radius: 8px; }
    </style>
    """, unsafe_allow_html=True)

# --- 2. State Management ---
if 'history' not in st.session_state:
    st.session_state.history = []

def load_history_item(item):
    for key, value in item['settings'].items():
        st.session_state[key] = value

# --- 3. UI Layout ---
st.title("🍌 Nano Banana 3 Pro: Director's Dashboard")
st.markdown("Upload reference images and direct your model's exact pose, gaze, and expression.")

# Create 3 columns for a professional dashboard feel
col_inputs, col_pose, col_output = st.columns([1.2, 1.2, 1.5], gap="large")

with col_inputs:
    st.subheader("1. Assets & Styling")
    
    # Image Uploads
    c1, c2 = st.columns(2)
    p_img = c1.file_uploader(" Product Ref", type=['png', 'jpg'], help="Upload the garment/item")
    m_img = c2.file_uploader(" Model Ref", type=['png', 'jpg'], help="Upload the model's face/body")
    
    st.divider()
    
    # Garment Details
    st.markdown("##### Garment Details")
    item = st.selectbox("Garment Type", GARMENT_TYPES, key='f_item')
    color = st.selectbox("Color", COLORS, key='f_color')
    fabric = st.selectbox("Fabric", FABRICS, key='f_fabric')
    
    st.markdown("##### Scene Details")
    lighting = st.selectbox("Lighting Setup", LIGHTING, key='f_light')
    camera = st.selectbox("Camera Angle", ANGLES, key='f_camera')

with col_pose:
    st.subheader("2. Direct the Model")
    
    body = st.selectbox(" Body Rotation", BODY_ROTATION, key='f_body')
    head = st.selectbox(" Head Pose", HEAD_POSE, key='f_head')
    eyes = st.selectbox(" Eye Gaze", EYE_GAZE, key='f_eyes')
    lips = st.selectbox(" Lips & Expression", LIP_STATE, key='f_lips')
    
    st.divider()
    neg_default = "blurry, low resolution, cropped face, face cut off, extra fingers, distorted hands, bad anatomy, harsh shadows"
    neg_prompt = st.text_area("Negative Prompt", neg_default, height=100, key='f_neg')

# --- 4. Prompt Generation Logic ---
def build_prompt():
    # 1. Image Conditioning Instructions (Crucial for Nano Banana 3)
    task_instruction = ""
    if p_img and m_img:
        task_instruction = "[HYBRID MODE: Drape the uploaded product_ref onto the uploaded model_ref. Retain model's facial identity.]\n"
    elif p_img:
        task_instruction = "[PRODUCT MODE: Generate a high-end fashion model wearing the exact uploaded product_ref.]\n"
    elif m_img:
        task_instruction = f"[MODEL MODE: Repose the uploaded model_ref. Dress them in a {color} {fabric} {item}.]\n"

    # 2. Main Description
    description = f"Professional {camera.lower()} studio fashion photography of a model wearing a {color} {fabric} {item}. "
    
    # 3. Directional Posing
    posing = f"Body positioning: {body.lower()}. "
    posing += f"Head direction: {head.lower()}. "
    posing += f"Eye gaze: {eyes.lower()}. "
    posing += f"Facial expression: {lips.lower()} lips. "
    
    # 4. Environment & Quality
    environment = f"Lit with {lighting.lower()}. 8k resolution, photorealistic, intricate skin texture, masterpiece."
    
    final_prompt = f"{task_instruction}{description}{posing}{environment}"
    return final_prompt

with col_output:
    st.subheader("3. Output & History")
    
    # Generate the prompt dynamically
    current_prompt = build_prompt()
    
    st.markdown("##### ✨ Generated Prompt")
    st.code(f"PROMPT:\n{current_prompt}\n\nNEGATIVE:\n{st.session_state.f_neg if 'f_neg' in st.session_state else neg_default}", language="text")
    
    if st.button("💾 Save to History", use_container_width=True, type="primary"):
        settings = {
            'f_item': st.session_state.f_item, 'f_color': st.session_state.f_color, 
            'f_fabric': st.session_state.f_fabric, 'f_light': st.session_state.f_light,
            'f_camera': st.session_state.f_camera, 'f_body': st.session_state.f_body,
            'f_head': st.session_state.f_head, 'f_eyes': st.session_state.f_eyes,
            'f_lips': st.session_state.f_lips, 'f_neg': st.session_state.f_neg
        }
        st.session_state.history.insert(0, {
            "time": datetime.now().strftime("%H:%M:%S"),
            "prompt": current_prompt,
            "settings": settings,
            "summary": f"{color} {item} | Body: {body} | Eyes: {eyes}"
        })
        st.rerun()

    # History Display
    st.divider()
    st.markdown("##### 📜 Session History")
    if not st.session_state.history:
        st.caption("Saved prompts will appear here.")
    
    # Wrap history in a container with a fixed height to allow scrolling if it gets too long
    history_container = st.container(height=400, border=False)
    with history_container:
        for i, entry in enumerate(st.session_state.history):
            with st.expander(f"🕒 {entry['time']} - {entry['summary']}"):
                st.code(entry['prompt'], language="text")
                if st.button("Re-load Settings", key=f"reload_{i}"):
                    load_history_item(entry)
                    st.rerun()