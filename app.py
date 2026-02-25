import streamlit as st
from datetime import datetime

# --- 1. Constants & Configuration ---
st.set_page_config(page_title="Nano Banana 3 Pro Studio", page_icon="🍌", layout="wide")

# Expanded Constants (Restored from your original React app)
GARMENT_TYPES = ["blouse", "shirt", "crop top", "sweater", "hoodie", "blazer", "dress", "tunic", "tank top", "bodysuit"]
COLORS = ["blush pink", "black", "white", "navy blue", "emerald green", "burgundy", "pastel blue", "beige", "lavender"]
FABRICS = ["chiffon", "cotton", "satin", "silk", "linen", "knit", "denim", "leather", "ribbed knit"]
FITS = ["regular fit", "loose fit", "oversized fit", "slim fit", "tailored fit", "flowy fit"]
SLEEVES = ["long sleeves", "short sleeves", "sleeveless", "bell sleeves", "puff sleeves", "cap sleeves"]
NECKLINES = ["round neck", "V-neck", "square neck", "scoop neck", "high neck", "off-shoulder"]
AESTHETICS = ["minimalist", "casual chic", "modern elegant", "street style", "business casual", "bohemian"]

# Scene & Framing Controls
FRAMING = ["Full Body framing", "Mid-Torso (Waist Up) framing", "Portrait (Head & Shoulders)", "Centered composition", "Amazon-style centered crop"]
BACKGROUNDS = ["clean white studio background", "light gray seamless backdrop", "soft beige background", "lifestyle indoor setting", "urban outdoor setting"]
LIGHTING = ["softbox studio lighting", "natural sunlight", "diffused even lighting", "high-key lighting", "dramatic shadows"]
ANGLES = ["straight-on camera at eye level", "low angle", "slightly elevated angle", "Dutch angle"]

# Pose Controls
BODY_ROTATION = ["Frontal (Facing Camera)", "Slightly Left", "Slightly Right", "Profile Left", "Profile Right", "Back View"]
HEAD_POSE = ["Facing Forward", "Turned Left", "Turned Right", "Tilted Up", "Tilted Down", "Looking over shoulder"]
EYE_GAZE = [
    "Looking at Camera", 
    "Looking Away (Off-camera)", 
    "Looking Up", 
    "Looking Down", 
    "Eyes Closed"
]
LIP_STATE = ["Neutral", "Soft Smile", "Parted Lips", "Pout", "Biting Lip", "Wide Smile"]

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
st.markdown("Upload reference images, define the exact garment details, and direct your model.")

col_inputs, col_pose, col_output = st.columns([1.2, 1.2, 1.5], gap="large")

with col_inputs:
    st.subheader("1. Assets & Garment")
    
    # Image Uploads
    c1, c2 = st.columns(2)
    p_img = c1.file_uploader("📦 Product Ref", type=['png', 'jpg'], help="Upload the garment/item")
    m_img = c2.file_uploader("👤 Model Ref", type=['png', 'jpg'], help="Upload the model's face/body")
    
    # Garment Builder
    with st.expander("🧵 Garment Details", expanded=True):
        item = st.selectbox("Garment Type", GARMENT_TYPES, key='f_item')
        
        # Batch Color Toggle
        use_batch_colors = st.toggle("Generate Multiple Colors", key='f_batch_colors')
        if use_batch_colors:
            selected_colors = st.multiselect("Select Colors", COLORS, default=[COLORS[0], COLORS[1]], key='f_colors_multi')
        else:
            color = st.selectbox("Color", COLORS, key='f_color')
            selected_colors = [color]

        fabric = st.selectbox("Fabric", FABRICS, key='f_fabric')
        col_f1, col_f2 = st.columns(2)
        fit = col_f1.selectbox("Fit", FITS, key='f_fit')
        sleeves = col_f2.selectbox("Sleeves", SLEEVES, key='f_sleeves')
        neckline = st.selectbox("Neckline", NECKLINES, key='f_neckline')
        aesthetic = st.selectbox("Aesthetic", AESTHETICS, key='f_aesthetic')

with col_pose:
    st.subheader("2. Direction & Scene")
    
    with st.expander("🎥 Camera & Environment", expanded=True):
        framing = st.selectbox("Framing / Shot Type", FRAMING, key='f_framing')
        camera = st.selectbox("Camera Angle", ANGLES, key='f_camera')
        background = st.selectbox("Background", BACKGROUNDS, key='f_background')
        lighting = st.selectbox("Lighting Setup", LIGHTING, key='f_light')

    with st.expander("🧍‍♀️ Model Direction", expanded=True):
        body = st.selectbox("Body Rotation", BODY_ROTATION, key='f_body')
        head = st.selectbox("Head Pose", HEAD_POSE, key='f_head')
        eyes = st.selectbox("Eye Gaze", EYE_GAZE, key='f_eyes')
        lips = st.selectbox("Lips & Expression", LIP_STATE, key='f_lips')
    
    neg_default = "blurry, low resolution, cropped face, face cut off, extra fingers, distorted hands, bad anatomy, harsh shadows, overexposed lighting, watermark, background clutter"
    neg_prompt = st.text_area("Negative Prompt", neg_default, height=80, key='f_neg')

# --- 4. Prompt Generation Logic ---
def build_prompt(target_color):
    # Image Conditioning
    task_instruction = ""
    if p_img and m_img:
        task_instruction = "[HYBRID MODE: Drape product_ref onto model_ref. Retain identity.]\n"
    elif p_img:
        task_instruction = "[PRODUCT MODE: Generate fashion model wearing product_ref.]\n"
    elif m_img:
        task_instruction = f"[MODEL MODE: Repose model_ref. Dress them in new garment.]\n"

    # Description
    description = f"Professional fashion photography, {aesthetic} style. {framing} of a model wearing a {target_color} {item}. "
    garment_details = f"Garment details: {fabric}, {fit}, {sleeves}, {neckline}. "
    
    # Direction
    posing = f"Pose: {body.lower()}. Head: {head.lower()}. Gaze: {eyes.lower()}. Expression: {lips.lower()} lips. "
    
    # Environment
    environment = f"Camera: {camera.lower()}. Environment: {background.lower()}. Lit with {lighting.lower()}. "
    quality = "8k resolution, photorealistic, highly detailed skin texture, editorial magazine quality."
    
    return f"{task_instruction}{description}{garment_details}{posing}{environment}{quality}"

with col_output:
    st.subheader("3. Output & History")
    
    # Generate the prompt(s) dynamically
    prompts_to_display = []
    for c in selected_colors:
        prompts_to_display.append({"color": c, "text": build_prompt(c)})
    
    st.markdown("##### ✨ Generated Prompts")
    for p in prompts_to_display:
        st.caption(f"Variation: {p['color'].upper()}")
        st.code(f"PROMPT:\n{p['text']}\n\nNEGATIVE:\n{st.session_state.f_neg if 'f_neg' in st.session_state else neg_default}", language="text")
    
    # Save to History
    if st.button("💾 Save Settings to History", use_container_width=True, type="primary"):
        # We save the single-color state to history so it reloads cleanly
        save_color = selected_colors[0] if selected_colors else COLORS[0]
        settings = {
            'f_item': st.session_state.f_item, 'f_color': save_color, 'f_batch_colors': False,
            'f_fabric': st.session_state.f_fabric, 'f_fit': st.session_state.f_fit,
            'f_sleeves': st.session_state.f_sleeves, 'f_neckline': st.session_state.f_neckline,
            'f_aesthetic': st.session_state.f_aesthetic, 'f_framing': st.session_state.f_framing,
            'f_background': st.session_state.f_background, 'f_light': st.session_state.f_light,
            'f_camera': st.session_state.f_camera, 'f_body': st.session_state.f_body,
            'f_head': st.session_state.f_head, 'f_eyes': st.session_state.f_eyes,
            'f_lips': st.session_state.f_lips, 'f_neg': st.session_state.f_neg
        }
        st.session_state.history.insert(0, {
            "time": datetime.now().strftime("%H:%M:%S"),
            "prompt": prompts_to_display[0]['text'], # Just save the first one for preview
            "settings": settings,
            "summary": f"{save_color} {item} | {framing}"
        })
        st.rerun()

    # History Display
    st.divider()
    st.markdown("##### 📜 Session History")
    if not st.session_state.history:
        st.caption("Saved configurations will appear here.")
    
    history_container = st.container(height=300, border=False)
    with history_container:
        for i, entry in enumerate(st.session_state.history):
            with st.expander(f"🕒 {entry['time']} - {entry['summary']}"):
                st.code(entry['prompt'], language="text")
                if st.button("Re-load Settings", key=f"reload_{i}"):
                    load_history_item(entry)
                    st.rerun()