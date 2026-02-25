import streamlit as st
from datetime import datetime

# --- 1. Constants & Configuration ---
GARMENT_TYPES = ["blouse", "shirt", "crop top", "sweater", "hoodie", "blazer", "tunic", "cardigan", "bodysuit", "tank top", "headset", "jewelry"]
COLORS = ["blush pink", "black", "white", "navy blue", "emerald green", "burgundy", "pastel blue", "beige", "lavender", "mustard yellow"]
GAZE_TYPES = ["Looking at camera", "Looking away", "Gazing downward", "Looking left", "Looking right", "Eyes closed"]
LIP_TYPES = ["Neutral/Closed", "Slight smile", "Parted lips", "Determined/Pout", "Wide smile"]
ORIENTATION = ["Frontal", "Three-quarter left", "Three-quarter right", "Profile left", "Profile right", "Back view"]

st.set_page_config(page_title="Nano Banana 3 Studio", page_icon="🍌", layout="wide")

# --- 2. Session State Management ---
if 'history' not in st.session_state:
    st.session_state.history = []

# --- 3. UI Styling ---
st.markdown("""
    <style>
    .main { background-color: #0d0d0d; color: #efefef; }
    .stSelectbox label, .stRadio label { font-weight: bold; color: #10b981 !important; }
    .history-card { 
        background-color: #1a1a1a; 
        border-left: 5px solid #10b981; 
        padding: 15px; 
        border-radius: 5px; 
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. Sidebar: Advanced Controls ---
with st.sidebar:
    st.title("🍌 Nano Banana 3")
    st.subheader("Global Composition")
    
    # NEW: Full Body vs Portrait Toggle
    framing = st.radio("Shot Type", ["Full Body", "Upper Body / Portrait"], index=0)
    
    st.divider()
    st.subheader("Model Anatomy & Pose")
    gaze = st.selectbox("Eye Gaze Direction", GAZE_TYPES)
    lips = st.selectbox("Mouth Expression", LIP_TYPES)
    pose = st.selectbox("Body Rotation", ORIENTATION)
    
    st.divider()
    st.subheader("Technical Specs")
    lighting = st.selectbox("Lighting Setup", ["Softbox Studio", "Cinematic Rim Light", "High-Key Commercial", "Natural Sunlight"])
    negative = st.text_area("Negative Prompt", "lowres, text, error, cropped, worst quality, low quality, jpeg artifacts, watermark, duplicate, morbid, mutilated, extra fingers, poorly drawn hands, mutation, deformed")

# --- 5. Main Panel ---
st.title("AI Fashion Refinement Studio")

col_left, col_right = st.columns([1.5, 1])

with col_left:
    st.subheader("Step 1: Reference Assets")
    c1, c2 = st.columns(2)
    with c1:
        prod_img = st.file_uploader("Upload Product (Headset/Clothing)", type=['png', 'jpg', 'webp'])
    with c2:
        model_img = st.file_uploader("Upload Model (Identity/Pose)", type=['png', 'jpg', 'webp'])

    st.subheader("Step 2: Garment Specs")
    g1, g2, g3 = st.columns(3)
    with g1:
        g_item = st.selectbox("Item", GARMENT_TYPES)
    with g2:
        g_color = st.selectbox("Color", COLORS)
    with g3:
        fabric = st.text_input("Fabric Type", "Satin/Cotton")

    # --- Robust Prompt Logic for Nano Banana 3 ---
    def generate_nano_3_prompt():
        # Handle Framing Logic
        frame_desc = "A high-end full-body fashion photography shot" if framing == "Full Body" else "A professional medium-shot portrait"
        
        # Build Core Instruction
        prompt = f"{frame_desc} of a model wearing a {g_color} {g_item} made of {fabric}. "
        
        # Add Spatial/Positional Adjustments
        prompt += f"Model is {pose.lower()} with eyes {gaze.lower()} and {lips.lower()}. "
        
        # Add Environment/Lighting
        prompt += f"Environment is a clean studio with {lighting.lower()}. "
        
        if prod_img and model_img:
            prompt += "(Hybrid Mode: Composite the texture and design from product_ref onto model_ref silhouette) "
        elif prod_img:
            prompt += "(Product-to-Image: Generate model around the product_ref while preserving its geometry) "
        elif model_img:
            prompt += "(Edit Mode: Maintain facial identity from model_ref but modify pose/expression) "
        
        prompt += "8k resolution, highly detailed skin texture, masterwork."
        return prompt

    final_prompt = generate_nano_3_prompt()
    
    st.divider()
    st.subheader("🚀 Final Output Instruction")
    st.info("Copy this into the Nano Banana 3 text field.")
    st.code(final_prompt, language="text")

    if st.button("Save Prompt to Session"):
        st.session_state.history.insert(0, {
            "time": datetime.now().strftime("%I:%M %p"),
            "prompt": final_prompt,
            "framing": framing
        })

# --- 6. History Panel ---
with col_right:
    st.subheader("📜 Refinement History")
    if not st.session_state.history:
        st.write("No generations yet this session.")
    
    for entry in st.session_state.history:
        st.markdown(f"""
        <div class="history-card">
            <small>{entry['time']} | <strong>{entry['framing']}</strong></small><br>
            <p style="font-size: 0.85em;">{entry['prompt'][:150]}...</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Re-load", key=entry['time']):
            st.write("Prompt copied to clipboard logic would go here.")