import re
import streamlit as st

# Page Configuration
st.set_page_config(page_title="Virtual Bundle Listing Creator", layout="wide")

# Looker Studio-Inspired Custom Styling
st.markdown("""
    <style>
        /* Global Font & Background */
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            color: #0F172A;
            background-color: #F1F5F9;
        }
        
        /* Dashboard Top Header */
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

        /* Looker Studio Card Styling */
        .card-container {
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #E2E8F0;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        
        /* Section Headings */
        .section-heading {
            color: #0284C7;
            font-size: 1.15rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 15px;
            border-bottom: 2px solid #E2E8F0;
            padding-bottom: 6px;
        }

        /* Light Green Copy Buttons Above Boxes */
        div[data-testid="stButton"] > button {
            background-color: #86EFAC !important; /* Light Green */
            color: #064E3B !important; /* Dark Green Text */
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

# Dashboard Banner
st.markdown("""
    <div class="dashboard-header">
        <div class="dashboard-title">📦 Virtual Bundle Listing Creator</div>
        <div class="dashboard-subtitle">Amazon Virtual Bundle Copy Deck Automation & Optimization Dashboard</div>
    </div>
""", unsafe_allow_html=True)

# SECTION 1: INPUT CARD
st.markdown('<div class="card-container"><div class="section-heading">1. Input Raw Product Titles</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    title_1 = st.text_area("Product 1 Title (Required)", height=85, key="p1")
    title_2 = st.text_area("Product 2 Title (Required)", height=85, key="p2")
    title_3 = st.text_area("Product 3 Title (Optional)", height=85, key="p3")

with col2:
    title_4 = st.text_area("Product 4 Title (Optional)", height=85, key="p4")
    title_5 = st.text_area("Product 5 Title (Optional)", height=85, key="p5")

st.markdown('</div>', unsafe_allow_html=True)

# Parsing Helpers
def extract_sizes(text):
    pattern = r'(\b\d+(\.\d+)?\s*(oz|lb|lbs|kg|g|ml|gallon|pack|ct)\b)'
    matches = re.findall(pattern, text, re.IGNORECASE)
    return [m[0].strip() for m in matches] if matches else []

def extract_brand(text):
    words = text.split()
    return " ".join(words[:2]) if len(words) >= 2 else (words[0] if words else "Brand")

def extract_product_type_and_size(raw_title):
    """Extracts short product type and size from raw title."""
    sizes = extract_sizes(raw_title)
    size_str = sizes[0] if sizes else ""
    
    # Strip common fluff words to isolate core product type
    cleaned = re.sub(r'(for Dogs & Cats|Omega-3|Supplement|Anti-Inflammatory|Pet|Wild|Premium)', '', raw_title, flags=re.IGNORECASE)
    parts = [p.strip() for p in cleaned.split('|')[0].split('–')[0].split() if len(p) > 2]
    
    prod_type = " ".join(parts[:2]) if len(parts) >= 2 else (" ".join(parts) if parts else "Item")
    return f"{size_str} {prod_type}".strip()

def generate_bundle_copy(titles):
    valid = [t.strip() for t in titles if t and t.strip()]
    if len(valid) < 2:
        return None, "Please enter at least 2 product titles to generate a virtual bundle."

    brand = extract_brand(valid[0])
    parsed_items = []
    all_sizes = []
    short_components = []
    
    for idx, t in enumerate(valid, 1):
        sizes = extract_sizes(t)
        if sizes:
            all_sizes.extend(sizes)
        
        item_short = extract_product_type_and_size(t)
        short_components.append(item_short)
        
        parsed_items.append({'num': idx, 'raw': t, 'sizes': sizes})

    count_str = f"{len(valid)}-Pack"
    
    # 1. Short Title (Brand + Each Product Type & Size - Max 55 Chars)
    joined_short = " + ".join(short_components)
    short_title = f"{brand} {joined_short}"
    if len(short_title) > 55:
        short_title = short_title[:52] + "..."

    # 2. Main Bundle Title (200 Chars Limit)
    raw_combined = " & ".join([item['raw'].split('|')[0].split('–')[0].strip() for item in parsed_items])
    full_title = f"{brand} {count_str} Bundle – {raw_combined} Supplement Set for Dogs & Cats – Skin, Coat, Joint & Overall Wellness Support"
    if len(full_title) > 200:
        full_title = full_title[:197] + "..."

    # 3. Bullets
    bullets = [
        f"COMPLETE {count_str.upper()} WELLNESS SET: Combines {len(valid)} premium pet supplements into one comprehensive daily routine targeting skin, coat, joint, and immune support.",
        "FULL-SPECTRUM NUTRITION: Packed with essential fatty acids, vitamins, and minerals tailored for dogs and cats of all breeds, ages, and sizes.",
        "SKIN, COAT & JOINT CARE: Deeply nourishes dry skin, reduces shedding, supports joint mobility, and promotes a soft, vibrant, and healthy coat.",
        f"OPTIMAL SIZES FOR DAILY ROUTINE: Includes exact sizes ({', '.join(all_sizes) if all_sizes else 'standard sizes'}) to ensure continuous daily supplementation with maximum value.",
        "EASY TO SERVE MEAL TOPPER: Simple daily application—easily mix or scoop directly onto kibble or wet food for mess-free daily feeding."
    ]

    # 4. Description
    desc_items = "\n".join([f"• Item {item['num']}: {item['raw']}" for item in parsed_items])
    description = (
        f"Elevate your pet's daily care with the {brand} {count_str} Virtual Bundle. "
        f"Specially selected to work together, this set provides complete nutritional coverage for your pets.\n\n"
        f"What's Included in This Bundle:\n{desc_items}\n\n"
        f"Designed for seamless daily feeding—simply add the recommended doses directly into your pet's food!"
    )

    return {
        "bundle_title": full_title,
        "bundle_short_title": short_title,
        "bullets": bullets,
        "description": description
    }, None

# SECTION 2: GENERATION ACTION
st.markdown('<div class="main-btn">', unsafe_allow_html=True)
run = st.button("🚀 Generate Optimized Copy Deck")
st.markdown('</div>', unsafe_allow_html=True)

if run or 'bundle_data' in st.session_state:
    if run:
        data, err = generate_bundle_copy([title_1, title_2, title_3, title_4, title_5])
        if err:
            st.error(err)
            st.stop()
        st.session_state.bundle_data = data

    res = st.session_state.bundle_data

    st.markdown('<br><div class="card-container"><div class="section-heading">2. Generated Copy Deck Fields (Editable)</div>', unsafe_allow_html=True)

    # Titles Row
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📋 Copy Bundle Title", key="cp_t"):
            st.toast("Bundle Title copied to clipboard!")
        val_t = st.text_input("Bundle Title", value=res['bundle_title'], key="out_title")
        st.caption(f"Length: **{len(val_t)}/200** characters {'🟢' if len(val_t) <= 200 else '🔴 Exceeds Limit'}")

    with c2:
        if st.button("📋 Copy Short Title", key="cp_st"):
            st.toast("Short Title copied to clipboard!")
        val_st = st.text_input("Bundle Short Title (Brand + Each Type & Size)", value=res['bundle_short_title'], key="out_stitle")
        st.caption(f"Length: **{len(val_st)}/55** characters {'🟢' if len(val_st) <= 55 else '🔴 Exceeds Limit'}")

    st.markdown("<br>", unsafe_allow_html=True)

    # Bullets
    st.markdown("**5 Feature Bullet Points:**")
    for idx, b in enumerate(res['bullets'], 1):
        c_b1, c_b2 = st.columns([5, 1])
        with c_b1:
            st.text_area(f"Bullet {idx}", value=b, height=70, key=f"out_b_{idx}")
        with c_b2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button(f"📋 Copy B{idx}", key=f"cp_b_{idx}"):
                st.toast(f"Bullet {idx} copied!")

    # Description
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📋 Copy Description", key="cp_desc"):
        st.toast("Product Description copied!")
    st.text_area("Product Description", value=res['description'], height=180, key="out_desc")

    st.markdown('</div>', unsafe_allow_html=True)
