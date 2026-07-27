import re
import streamlit as st

# Page Configuration
st.set_page_config(page_title="Virtual Bundle Listing Creator", layout="wide")

st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: 'Inter', -apple-system, sans-serif;
            color: #0F172A;
            background-color: #F1F5F9;
        }
        .dashboard-header {
            background-color: #0F172A;
            color: #FFFFFF;
            padding: 18px 24px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .dashboard-title { font-size: 1.6rem; font-weight: 700; color: #F8FAFC; margin: 0; }
        .dashboard-subtitle { font-size: 0.9rem; color: #94A3B8; margin-top: 4px; }
        .card-container {
            background-color: #FFFFFF;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid #E2E8F0;
            margin-bottom: 20px;
        }
        .section-heading {
            color: #0284C7;
            font-size: 1.1rem;
            font-weight: 700;
            text-transform: uppercase;
            margin-bottom: 15px;
            border-bottom: 2px solid #E2E8F0;
            padding-bottom: 6px;
        }
        div[data-testid="stButton"] > button {
            background-color: #86EFAC !important;
            color: #064E3B !important;
            font-size: 0.8rem !important;
            font-weight: 700 !important;
            border-radius: 4px !important;
            border: 1px solid #4ADE80 !important;
            padding: 2px 10px !important;
        }
        div[data-testid="stButton"] > button:hover {
            background-color: #4ADE80 !important;
        }
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
        <div class="dashboard-subtitle">ASIN & Raw Title Bundle Copy Deck Generator</div>
    </div>
""", unsafe_allow_html=True)

st.markdown('<div class="card-container"><div class="section-heading">1. Component Details (ASINs & Titles)</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    asin_1 = st.text_input("Product 1 ASIN", value="B0002XJ3GS", key="asin1")
    title_1 = st.text_area("Product 1 Title (Required)", value="Life Line Pet Nutrition Wild Alaskan Fish Oil for Dogs and Cats 128oz – Omega 3 Fish Oil Supplement for Skin & Coat, Brain, Eye & Heart Health", height=85, key="p1")
    p1_type = st.selectbox("Product 1 Type Option", ["Fish Oil", "Omega 3 Oil", "Salmon Oil"], key="p1_t")
    p1_size = st.selectbox("Product 1 Size/Pack Option", ["128oz", "64oz", "8.5oz", "Pack of 2"], key="p1_s")

with col2:
    asin_2 = st.text_input("Product 2 ASIN", value="B0002XJ3GT", key="asin2")
    title_2 = st.text_area("Product 2 Title (Required)", value="Life Line Organic Ocean Kelp Supplement for Dogs, Cats, Horses & Livestock | Natural Source of Iodine for Skin, Shiny Coat & Immune Support | Helps Reduce Tartar, Shedding & Aids Digestion – 1.5 lb", height=85, key="p2")
    p2_type = st.selectbox("Product 2 Type Option", ["Ocean Kelp", "Kelp Powder", "Kelp Supp"], key="p2_t")
    p2_size = st.selectbox("Product 2 Size/Pack Option", ["1.5lb", "1lb", "8oz", "Pack of 2"], key="p2_s")

st.markdown('</div>', unsafe_allow_html=True)

def extract_brand(text):
    words = text.split()
    return " ".join(words[:2]) if len(words) >= 2 else (words[0] if words else "Brand")

def generate_bundle_deck():
    brand = extract_brand(title_1)
    
    # 1. Short Title Formula (Brand + Selected Sizes & Types)
    short_title = f"{brand} {p1_size} {p1_type} + {p2_size} {p2_type}"[:55].strip()

    # 2. Bundle Title (Brand First + Sizes + Types + Benefits - Max 200 Chars)
    main_title = f"{brand} {p1_size} {p1_type} & {p2_size} {p2_type} Supplement Set for Dogs & Cats – Omega 3 & Iodine for Skin, Coat, Joint & Dental Care"
    if len(main_title) > 200:
        main_title = main_title[:197] + "..."

    # 3. Merged Bullets
    bullets = [
        f"DUAL-ACTION SKIN & DENTAL SUPPORT: Combines {p1_size} pure {p1_type} and {p2_size} {p2_type} to target essential daily health needs from coat nourishment to plaque and tartar reduction.",
        f"RICH OMEGA-3 EPA & DHA: {p1_type} deeply hydrates dry, itchy skin, reduces excessive shedding, supports joint mobility, and promotes brain and heart function across all breeds.",
        f"ORGANIC IODINE & DIGESTIVE CARE: 100% natural {p2_type} provides bioavailable iodine, trace minerals, and natural enzymes to boost digestion, enhance immune response, and keep coats shiny.",
        f"BULK VALUE FOR CONTINUOUS CARE: Combines a full {p1_size} liquid bottle and a {p2_size} tub to deliver an extended supply for daily multi-pet households.",
        "EASY DAILY MEAL TOPPER: Simple daily application—easily mix or scoop directly onto kibble or wet food for mess-free daily feeding."
    ]

    # 4. Description
    description = (
        f"Elevate your pet's daily nutrition with the {brand} {p1_size} {p1_type} & {p2_size} {p2_type} Set. "
        f"Designed specifically for dogs and cats, this comprehensive two-part supplement pair targets essential everyday health needs.\n\n"
        f"Included in This Bundle:\n"
        f"• Item 1 ({asin_1}): {title_1}\n"
        f"• Item 2 ({asin_2}): {title_2}\n\n"
        f"Simply add both toppers to your pet's daily meals for complete internal and external health care!"
    )

    return {
        "bundle_title": main_title,
        "bundle_short_title": short_title,
        "bullets": bullets,
        "description": description
    }

st.markdown('<div class="main-btn">', unsafe_allow_html=True)
run = st.button("🚀 Generate Optimized Copy Deck")
st.markdown('</div>', unsafe_allow_html=True)

if run or 'bundle_data' in st.session_state:
    if run:
        st.session_state.bundle_data = generate_bundle_deck()

    res = st.session_state.bundle_data

    st.markdown('<br><div class="card-container"><div class="section-heading">2. Generated Copy Deck Fields (Editable)</div>', unsafe_allow_html=True)

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
    st.markdown("**5 Merged Feature Bullet Points:**")
    for idx, b in enumerate(res['bullets'], 1):
        c_b1, c_b2 = st.columns([5, 1])
        with c_b1:
            st.text_area(f"Bullet {idx}", value=b, height=70, key=f"out_b_{idx}")
        with c_b2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button(f"📋 Copy B{idx}", key=f"cp_b_{idx}"):
                st.toast(f"Bullet {idx} copied!")

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("📋 Copy Description", key="cp_desc"):
        st.toast("Description copied!")
    st.text_area("Product Description", value=res['description'], height=180, key="out_desc")

    st.markdown('</div>', unsafe_allow_html=True)
