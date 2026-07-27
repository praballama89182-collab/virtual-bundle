import re
import streamlit as st

# Page Configuration
st.set_page_config(page_title="Virtual Bundle Listing Creator", layout="wide")

# Looker Studio / Clean Dashboard Styling
st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            color: #0F172A;
            background-color: #F1F5F9;
        }
        
        .dashboard-header {
            background-color: #0F172A;
            color: #FFFFFF;
            padding: 18px 24px;
            border-radius: 8px;
            margin-bottom: 20px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        .dashboard-title {
            font-size: 1.6rem;
            font-weight: 700;
            margin: 0;
            color: #F8FAFC;
        }
        .dashboard-subtitle {
            font-size: 0.9rem;
            color: #94A3B8;
            margin-top: 4px;
        }

        .card-container {
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #E2E8F0;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        
        .section-heading {
            color: #0284C7;
            font-size: 1.1rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 15px;
            border-bottom: 2px solid #E2E8F0;
            padding-bottom: 6px;
        }

        /* Light Green Copy Buttons */
        div[data-testid="stButton"] > button {
            background-color: #86EFAC !important;
            color: #064E3B !important;
            font-size: 0.8rem !important;
            font-weight: 700 !important;
            border-radius: 4px !important;
            border: 1px solid #4ADE80 !important;
            padding: 2px 10px !important;
            height: auto !important;
        }
        div[data-testid="stButton"] > button:hover {
            background-color: #4ADE80 !important;
            color: #022C22 !important;
        }

        /* Primary Action Button Override */
        .main-btn > div[data-testid="stButton"] > button {
            background-color: #0284C7 !important;
            color: #FFFFFF !important;
            font-size: 1rem !important;
            padding: 10px 20px !important;
            width: 100%;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="dashboard-header">
        <div class="dashboard-title">📦 Virtual Bundle Listing Creator (Amazon US)</div>
        <div class="dashboard-subtitle">Title Phrase Auto-Extraction & Copy Deck Generator</div>
    </div>
""", unsafe_allow_html=True)

# Helper Parsing Functions
def extract_sizes_from_title(title):
    """Extracts size/weight/pack patterns directly present inside the title string."""
    pattern = r'(\b\d+(\.\d+)?\s*(oz|ozs|lb|lbs|kg|g|ml|gallon|pack of \d+|\d+\s*pack)\b)'
    matches = re.findall(pattern, title, re.IGNORECASE)
    found_sizes = [m[0].strip() for m in matches]
    return list(dict.fromkeys(found_sizes)) if found_sizes else ["Standard Size"]

def extract_phrases_from_title(title):
    """Parses raw title into clean keyword phrase chunks for selection options."""
    # Split by common delimiters (|, –, -, commas)
    chunks = re.split(r'[|–\-,]', title)
    clean_phrases = []
    
    for c in chunks:
        # Strip brand name and boilerplate fillers
        text = re.sub(r'(for Dogs and Cats|for Dogs|for Cats|Supplement|Helps|Promotes)', '', c, flags=re.IGNORECASE).strip()
        words = text.split()
        if len(words) >= 1:
            # Create short phrase chunks (1 to 3 words)
            phrase = " ".join(words[:3])
            if len(phrase) > 2 and phrase not in clean_phrases:
                clean_phrases.append(phrase)
                
    return clean_phrases if clean_phrases else ["Product"]

def extract_brand(text):
    words = text.split()
    return " ".join(words[:2]) if len(words) >= 2 else (words[0] if words else "Brand")


# SECTION 1: COMPONENT INPUTS
st.markdown('<div class="card-container"><div class="section-heading">1. Component ASINs & Raw Title Parsing</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    asin_1 = st.text_input("Product 1 ASIN", value="B0002XJ3GS", key="asin1")
    title_1 = st.text_area(
        "Product 1 Title", 
        value="Life Line Pet Nutrition Wild Alaskan Fish Oil for Dogs and Cats 128oz – Omega 3 Fish Oil Supplement for Skin & Coat, Brain, Eye & Heart Health", 
        height=85, 
        key="p1"
    )
    # Dynamic suggestions pulled directly from Title 1
    p1_size_options = extract_sizes_from_title(title_1)
    p1_phrase_options = extract_phrases_from_title(title_1)
    
    p1_size = st.selectbox("Select Product 1 Size (Extracted)", p1_size_options, key="p1_s")
    p1_phrase = st.selectbox("Select Product 1 Phrase/Type (Extracted)", p1_phrase_options, key="p1_p")

with col2:
    asin_2 = st.text_input("Product 2 ASIN", value="B0002XJ3GT", key="asin2")
    title_2 = st.text_area(
        "Product 2 Title", 
        value="Life Line Organic Ocean Kelp Supplement for Dogs, Cats, Horses & Livestock | Natural Source of Iodine for Skin, Shiny Coat & Immune Support | Helps Reduce Tartar, Shedding & Aids Digestion – 1.5 lb", 
        height=85, 
        key="p2"
    )
    # Dynamic suggestions pulled directly from Title 2
    p2_size_options = extract_sizes_from_title(title_2)
    p2_phrase_options = extract_phrases_from_title(title_2)
    
    p2_size = st.selectbox("Select Product 2 Size (Extracted)", p2_size_options, key="p2_s")
    p2_phrase = st.selectbox("Select Product 2 Phrase/Type (Extracted)", p2_phrase_options, key="p2_p")

st.markdown('</div>', unsafe_allow_html=True)


# SECTION 2: COPY GENERATION LOGIC
def generate_bundle_deck():
    brand = extract_brand(title_1)
    
    # Short Title (Brand + Selected Extracted Phrase/Size - Max 55 Chars)
    short_title = f"{brand} {p1_size} {p1_phrase} + {p2_size} {p2_phrase}"[:55].strip()

    # Main Bundle Title (Brand First + Both Extracted Phrases & Sizes - Max 200 Chars)
    main_title = f"{brand} {p1_size} {p1_phrase} & {p2_size} {p2_phrase} Set – Omega 3 & Iodine Supplement for Dogs & Cats – Skin, Coat, Joint & Immune Support"
    if len(main_title) > 200:
        main_title = main_title[:197] + "..."

    # 5 Merged Bullets
    bullets = [
        f"DUAL-ACTION WELLNESS SET: Combines {p1_size} {p1_phrase} and {p2_size} {p2_phrase} into a complete daily routine for dogs and cats of all breeds and ages.",
        f"SKIN & COAT NOURISHMENT: Rich in EPA and DHA Omega-3 fatty acids from pure fish oil to soothe dry, itchy skin, reduce shedding, and promote joint flexibility.",
        f"NATURAL IODINE & DENTAL CARE: 100% Organic ocean kelp provides bioavailable iodine, trace minerals, and natural enzymes to aid digestion and help reduce plaque and tartar buildup.",
        f"BULK SIZES FOR CONTINUOUS CARE: Features exact full-size supplies ({p1_size} liquid bottle + {p2_size} kelp tub) offering maximum value for multi-pet households.",
        "EASY TO SERVE MEAL TOPPER: Simple daily application—easily pump or scoop directly over dry kibble or wet food for mess-free daily absorption."
    ]

    # Product Description
    description = (
        f"Elevate your pet's daily care with the {brand} {p1_size} {p1_phrase} & {p2_size} {p2_phrase} Set. "
        f"Specially formulated for dogs and cats, this comprehensive two-part supplement pair targets essential everyday health needs.\n\n"
        f"Included in This Bundle:\n"
        f"• Item 1 (ASIN: {asin_1}): {title_1}\n"
        f"• Item 2 (ASIN: {asin_2}): {title_2}\n\n"
        f"Simply add both toppers to your pet's daily food for complete internal and external health support!"
    )

    return {
        "bundle_title": main_title,
        "bundle_short_title": short_title,
        "bullets": bullets,
        "description": description
    }

st.markdown('<div class="main-btn">', unsafe_allow_html=True)
run = st.button("🚀 Generate Copy Deck from Title Phrases")
st.markdown('</div>', unsafe_allow_html=True)

if run or 'bundle_data' in st.session_state:
    if run:
        st.session_state.bundle_data = generate_bundle_deck()

    res = st.session_state.bundle_data

    st.markdown('<br><div class="card-container"><div class="section-heading">2. Generated Bundle Listing Fields (Editable)</div>', unsafe_allow_html=True)

    # Output Titles Row
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📋 Copy Bundle Title", key="cp_t"):
            st.toast("Bundle Title copied!")
        val_t = st.text_input("Bundle Title (Brand First + Sizes)", value=res['bundle_title'], key="out_title")
        st.caption(f"Length: **{len(val_t)}/200** characters {'🟢' if len(val_t) <= 200 else '🔴 Exceeds Limit'}")

    with c2:
        if st.button("📋 Copy Short Title", key="cp_st"):
            st.toast("Short Title copied!")
        val_st = st.text_input("Bundle Short Title (Max 55 Chars)", value=res['bundle_short_title'], key="out_stitle")
        st.caption(f"Length: **{len(val_st)}/55** characters {'🟢' if len(val_st) <= 55 else '🔴 Exceeds Limit'}")

    st.markdown("<br>", unsafe_allow_html=True)
    
    # Feature Bullet Points
    st.markdown("**5 Merged Feature Bullet Points:**")
    for idx, b in enumerate(res['bullets'], 1):
        c_b1, c_b2 = st.columns([5, 1])
        with c_b1:
            st.text_area(f"Bullet {idx}", value=b, height=70, key=f"out_b_{idx}")
        with c_b2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button(f"📋 Copy B{idx}", key=f"cp_b_{idx}"):
                st.toast(f"Bullet {idx} copied!")

    # Product Description
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📋 Copy Description", key="cp_desc"):
        st.toast("Description copied!")
    st.text_area("Product Description", value=res['description'], height=180, key="out_desc")

    st.markdown('</div>', unsafe_allow_html=True)
