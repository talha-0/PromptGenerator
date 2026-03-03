import streamlit as st
from datetime import datetime

# --- 1. Constants & Configuration ---
st.set_page_config(page_title="Nano Banana 3 Pro Studio", page_icon="🍌", layout="wide")

# Categories & Items
CATEGORIES = ["Garment (Clothing)", "Accessory (Headsets & Others)", "Beauty & Grooming"]
GARMENT_TYPES = ["blouse", "shirt", "crop top", "sweater", "hoodie", "blazer", "dress", "tunic", "tank top", "bodysuit"]
ACCESSORY_TYPES = ["headset", "sunglasses", "hat", "scarf", "necklace"]
# Expanded Beauty Types
BEAUTY_TYPES = ["perfume", "grooming kit", "facial cleanser", "suncare", "acne cream", "serum"]

# Separated Materials & Styles
GARMENT_FABRICS = ["chiffon", "cotton", "satin", "silk", "linen", "knit", "denim", "leather", "ribbed knit"]
HEADSET_MATERIALS = ["matte polycarbonate", "brushed aluminum", "carbon fiber", "premium soft-touch plastic", "anodized metal", "vegan leather ear cushions"]
PERFUME_STYLES = ["minimalist clear glass bottle", "luxury crystal bottle", "matte black finish", "metallic chrome finish", "elegant frosted glass", "amber apothecary bottle"]
GROOMING_KIT_STYLES = ["premium leather dopp kit", "matte black presentation box", "sustainable kraft packaging", "minimalist travel pouch", "sleek aluminum case"]
# New Skincare Styles for Gen-Z Ads
SKINCARE_STYLES = ["minimalist pastel tube", "frosted glass dropper bottle", "eco-friendly pump bottle", "sleek airless pump", "gen-z bright bold packaging"]
PERFUME_AUDIENCE = ["Men", "Women", "Unisex"]

COLORS = ["blush pink", "black", "white", "navy blue", "emerald green", "burgundy", "pastel blue", "beige", "lavender", "matte black", "silver", "gold", "rose gold"]
FITS = ["regular fit", "loose fit", "oversized fit", "slim fit", "tailored fit", "flowy fit"]
SLEEVES = ["long sleeves", "short sleeves", "sleeveless", "bell sleeves", "puff sleeves", "cap sleeves"]
NECKLINES = ["round neck", "V-neck", "square neck", "scoop neck", "high neck", "off-shoulder"]

AESTHETICS = ["minimalist", "casual chic", "modern elegant", "street style", "business casual", "bohemian", "high-tech commercial", "luxury editorial"]
FRAMING = ["Full Body framing", "Mid-Torso (Waist Up) framing", "Portrait (Head & Shoulders)", "Centered composition", "Amazon-style centered crop", "Macro close-up", "Overhead flatlay"]
BACKGROUNDS = ["clean white studio background", "light gray seamless backdrop", "soft beige background", "lifestyle indoor setting", "urban outdoor setting", "dark moody studio gradient", "water reflections setting", "marble countertop"]
LIGHTING = ["softbox studio lighting", "natural sunlight", "diffused even lighting", "high-key lighting", "dramatic shadows", "neon rim lighting", "caustic light reflections"]
ANGLES = ["straight-on camera at eye level", "low angle", "slightly elevated angle", "Dutch angle", "top-down flatlay", "45-degree product angle"]

# Pose & Model Controls
BODY_ROTATION = ["Facing Camera", "Turned Slightly Left", "Turned Slightly Right", "Profile Left", "Profile Right", "Back View"]
HEAD_POSE = ["Facing Forward", "Turned Left", "Turned Right", "Tilted Up", "Tilted Down", "Looking over shoulder"]
EYE_GAZE = ["Looking at Camera", "Looking Away (Off-camera)", "Looking Up", "Looking Down", "Eyes Closed"]
LIP_STATE = ["Neutral", "Soft Smile", "Parted Lips", "Pout", "Biting Lip", "Wide Smile"]

GENDERS = ["Female", "Male", "Non-binary", "Unspecified"]
HEADSET_STYLES = ["over-ear", "on-ear", "in-ear", "gaming headset", "true wireless earbuds"]

# CSS for cleaner text wrapping
st.markdown("""
    <style>
    code { white-space: pre-wrap !important; word-break: break-word !important; }
    .stCode { border: 1px solid #10b981 !important; border-radius: 8px !important; padding: 8px; }
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

col_inputs, col_pose, col_output = st.columns([1.2, 1.2, 1.5], gap="large")

with col_inputs:
    st.subheader("1. Assets & Product")
    
    c1, c2 = st.columns(2)
    p_img = c1.file_uploader("📦 Product Ref", type=['png', 'jpg'])
    m_img = c2.file_uploader("👤 Model Ref", type=['png', 'jpg'])
    
    mode = st.radio("Generation Mode:", CATEGORIES, key='f_mode')
    
    with st.expander("📦 Product Details", expanded=True):
        use_batch_colors = st.toggle("Generate Multiple Colors", key='f_batch_colors')
        if use_batch_colors:
            selected_colors = st.multiselect("Select Colors", COLORS, default=[COLORS[0], COLORS[1]], key='f_colors_multi')
        else:
            color = st.selectbox("Color", COLORS, key='f_color')
            selected_colors = [color]

        # Dynamic Form based on Mode
        if mode == "Accessory (Headsets & Others)":
            item = st.selectbox("Accessory Type", ACCESSORY_TYPES, key='f_item')
            if item == "headset":
                headset_style = st.selectbox("Headset Style", HEADSET_STYLES, key='f_headset_style')
                material = st.selectbox("Material / Build", HEADSET_MATERIALS, index=0, key='f_material')
                is_product_only = st.checkbox("Product-Only Shot (No Model)", value=False, key='f_product_only')
            else:
                headset_style = None
                material = ""
                is_product_only = st.checkbox("Product-Only Shot (No Model)", value=False, key='f_product_only')
                
        elif mode == "Beauty & Grooming":
            item = st.selectbox("Product Type", BEAUTY_TYPES, key='f_item')
            
            # New Ad Typography Overlay
            st.markdown("##### 📝 Ad Typography Overlay")
            use_ad_text = st.checkbox("Include Text Overlay in Ad", key='f_use_ad_text')
            if use_ad_text:
                ad_title = st.text_input("Ad Title (Short)", "GLOW UP", key='f_ad_title')
                ad_desc = st.text_input("Ad Description", "The ultimate hydration for clear skin.", key='f_ad_desc')
            
            # Specific styling logic based on the beauty item selected
            if item == "perfume":
                audience = st.selectbox("Target Audience", PERFUME_AUDIENCE, key='f_perfume_audience')
                material = st.selectbox("Bottle Style", PERFUME_STYLES, key='f_material')
                is_product_only = st.checkbox("Product-Only Shot (No Model)", value=True, key='f_product_only')
            elif item == "grooming kit":
                audience = None
                material = st.selectbox("Packaging Style", GROOMING_KIT_STYLES, key='f_material')
                is_product_only = st.checkbox("Product-Only Shot (No Model)", value=True, key='f_product_only', help="Grooming kits usually render best without models.")
            else: # facial cleanser, suncare, acne cream, serum
                audience = None
                material = st.selectbox("Packaging Style", SKINCARE_STYLES, key='f_material')
                is_product_only = st.checkbox("Product-Only Shot (No Model)", value=False, key='f_product_only', help="Leave unchecked to generate a lifestyle ad with a model holding/using the product.")
        
        else: # Garment
            item = st.selectbox("Garment Type", GARMENT_TYPES, key='f_item')
            fabric = st.selectbox("Fabric", GARMENT_FABRICS, key='f_fabric')
            col_f1, col_f2 = st.columns(2)
            fit = col_f1.selectbox("Fit", FITS, key='f_fit')
            sleeves = col_f2.selectbox("Sleeves", SLEEVES, key='f_sleeves')
            neckline = st.selectbox("Neckline", NECKLINES, key='f_neckline')
            is_product_only = False
            
        aesthetic = st.selectbox("Aesthetic", AESTHETICS, key='f_aesthetic')

with col_pose:
    st.subheader("2. Direction & Scene")
    
    with st.expander("🎥 Camera & Environment", expanded=True):
        framing = st.selectbox("Framing / Shot Type", FRAMING, key='f_framing')
        camera = st.selectbox("Camera Angle", ANGLES, key='f_camera')
        background = st.selectbox("Background", BACKGROUNDS, key='f_background')
        lighting = st.selectbox("Lighting Setup", LIGHTING, key='f_light')

    with st.expander("🧍‍♀️ Model Direction", expanded=True):
        gender = st.selectbox("Model Gender", GENDERS, key='f_gender', disabled=is_product_only)
        
        if is_product_only:
            st.info("Product-only mode active. Pose controls disabled.")
            
        body = st.selectbox("Body Rotation", BODY_ROTATION, key='f_body', disabled=is_product_only)
        head = st.selectbox("Head Pose", HEAD_POSE, key='f_head', disabled=is_product_only)
        eyes = st.selectbox("Eye Gaze", EYE_GAZE, key='f_eyes', disabled=is_product_only)
        lips = st.selectbox("Lips & Expression", LIP_STATE, key='f_lips', disabled=is_product_only)

    neg_default = "blurry, low resolution, cropped face, face cut off, extra fingers, bad anatomy, harsh shadows, text, watermark, symmetry"
    neg_prompt = st.text_area("Negative Prompt", neg_default, height=80, key='f_neg')

# --- 4. Prompt Generation Logic ---
def build_prompt(target_color):
    # Base Image Conditioning
    task_instruction = ""
    if p_img and m_img:
        task_instruction = "[HYBRID MODE: Integrate product_ref onto model_ref. Retain model identity.]\n"
    elif p_img:
        task_instruction = "[PRODUCT MODE: Use product_ref as the primary reference.]\n"
    elif m_img:
        task_instruction = "[MODEL MODE: Repose model_ref with new product.]\n"

    # Accessory Route
    if mode == "Accessory (Headsets & Others)":
        target_product = f"{target_color} {st.session_state.get('f_headset_style', '')} {item}".strip()
        mat_text = st.session_state.get('f_material', '')
        
        if is_product_only:
            description = f"High-detail commercial product photography of a {target_product}. Close-up and clean product shots. Showcasing a premium {mat_text} build. High-end industrial design, crisp edges, branding-free. "
            posing = ""
        else:
            description = f"Studio commercial photo of a {gender.lower()} model wearing a {target_product}. The accessory features a {mat_text} finish. Focus composition entirely on the headset. Model face is visible but serves as a secondary element. "
            posing = f"Pose: {body.lower()}. Head: {head.lower()}. Gaze: {eyes.lower()}. Expression: {lips.lower()} lips. "
            
        details = ""

    # Beauty & Grooming Route
    elif mode == "Beauty & Grooming":
        mat_text = st.session_state.get('f_material', '')
        use_ad_text = st.session_state.get('f_use_ad_text', False)
        ad_title = st.session_state.get('f_ad_title', '')
        ad_desc = st.session_state.get('f_ad_desc', '')
        
        # Product targeting
        if item == "perfume":
            aud_text = st.session_state.get('f_perfume_audience', 'Unisex')
            target_product = f"{target_color} {mat_text} perfume bottle for {aud_text.lower()}"
        elif item == "grooming kit":
            target_product = f"{target_color} grooming kit arranged in a {mat_text}"
        else:
            target_product = f"{target_color} {mat_text} of {item}"
            
        # Base description depending on model presence
        if is_product_only:
            description = f"High-end macro commercial product photography of a {target_product}. Elegantly arranged layout, appealing textures, beautiful reflections. Clean lines, highly aesthetic Gen-Z marketing style. "
            posing = ""
        else:
            description = f"Trendy Gen-Z lifestyle beauty campaign ad featuring a {target_product} being held or used by a stylish {gender.lower()} model. Sharp focus on the product while the model creates an engaging, natural mood. "
            posing = f"Pose: {body.lower()}. Head: {head.lower()}. Gaze: {eyes.lower()}. Expression: {lips.lower()} lips. "
            
        # Inject typography formatting
        if use_ad_text and (ad_title or ad_desc):
            details = f"Commercial ad layout with stylish graphic design text overlay. Bold typography title reading '{ad_title}'. Subtext product description reading '{ad_desc}'. "
        else:
            details = ""
            
    # Garment Route
    else:
        description = f"Professional fashion photography, {aesthetic} style. {framing} of a {gender.lower()} model wearing a {target_color} {st.session_state.get('f_fabric', '')} {item}. "
        details = f"Garment details: {st.session_state.get('f_fit', '')}, {st.session_state.get('f_sleeves', '')}, {st.session_state.get('f_neckline', '')}. "
        posing = f"Pose: {body.lower()}. Head: {head.lower()}. Gaze: {eyes.lower()}. Expression: {lips.lower()} lips. "

    environment = f"Camera: {camera.lower()}. Environment: {background.lower()}. Lit with {lighting.lower()}. "
    quality = "8k resolution, photorealistic, highly detailed textures, editorial quality."
    
    return f"{task_instruction}{description}{details}{posing}{environment}{quality}"

with col_output:
    st.subheader("3. Output & History")
    
    prompts_to_display = [{"color": c, "text": build_prompt(c)} for c in selected_colors]
    
    # Dynamically remove "text" from negative prompt if the user wants typography
    current_neg = st.session_state.f_neg if 'f_neg' in st.session_state else neg_default
    if mode == "Beauty & Grooming" and st.session_state.get('f_use_ad_text', False):
        current_neg = current_neg.replace("text, ", "").replace(" text", "").replace("text", "")
    
    st.markdown("##### ✨ Generated Prompts")
    for p in prompts_to_display:
        st.caption(f"Variation: {p['color'].upper()}")
        st.code(f"PROMPT:\n{p['text']}\n\nNEGATIVE:\n{current_neg}", language="text")
    
    if st.button("💾 Save Settings to History", use_container_width=True, type="primary"):
        save_color = selected_colors[0] if selected_colors else COLORS[0]
        settings_to_save = {k: v for k, v in st.session_state.items() if k.startswith('f_')}
        settings_to_save['f_batch_colors'] = False
        settings_to_save['f_color'] = save_color
        
        st.session_state.history.insert(0, {
            "time": datetime.now().strftime("%H:%M:%S"),
            "prompt": prompts_to_display[0]['text'],
            "settings": settings_to_save,
            "summary": f"{save_color} {st.session_state.f_item} | {st.session_state.f_framing}"
        })
        st.rerun()

    st.divider()
    st.markdown("##### 📜 Session History")
    if not st.session_state.history:
        st.caption("Saved configurations will appear here.")
    
    history_container = st.container(height=400, border=False)
    with history_container:
        for i, entry in enumerate(st.session_state.history):
            with st.expander(f"🕒 {entry['time']} - {entry['summary']}"):
                st.code(entry['prompt'], language="text")
                if st.button("Re-load Settings", key=f"reload_{i}"):
                    load_history_item(entry)
                    st.rerun()