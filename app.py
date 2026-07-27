import io
import re
import streamlit as st

# Page Setup & Styling
st.set_page_config(page_title="Virtual Bundle Listing Creator", layout="wide")

st.markdown("""
    <style>
        html, body, [class*="css"] {
            font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            color: #2D3748;
        }
        .main-header {
            color: #1E3A8A;
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0.2rem;
            letter-spacing: -0.5px;
        }
        .sub-header {
            color: #4A5568;
            font-size: 1.05rem;
            margin-bottom: 1.5rem;
        }
        .section-heading {
            color: #0284C7;
            font-size: 1.35rem;
            font-weight: 600;
            border-bottom: 2px solid #E2E8F0;
            padding-bottom: 0.4rem;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
        }
        .stTextArea label, .stTextInput label {
            color: #1E293B !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
        }
        .stButton>button {
            background-color: #0284C7 !important;
            color: white !important;
            font-weight: 600 !important;
            border-radius: 6px !important;
            padding: 0.6rem 1.2rem !important;
            border: none !important;
            font-size: 1rem !important;
            width: 100%;
        }
        .stButton>button:hover {
            background-color: #0369A1 !important;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">📦 Virtual Bundle Listing Creator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Enter 2 to 5 raw product titles below to automatically generate fully optimized Amazon Virtual Bundle copy deck fields and downloadable files.</div>', unsafe_allow_html=True)

st.markdown('<div class="section-heading">1. Input Raw Product Titles (2 to 5 Products)</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    title_1 = st.text_area("Product 1 Title (Required)", height=90, key="p1")
    title_2 = st.text_area("Product 2 Title (Required)", height=90, key="p2")
    title_3 = st.text_area("Product 3 Title (Optional)", height=90, key="p3")

with col2:
    title_4 = st.text_area("Product 4 Title (Optional)", height=90, key="p4")
    title_5 = st.text_area("Product 5 Title (Optional)", height=90, key="p5")

def extract_sizes(text):
    pattern = r'(\b\d+(\.\d+)?\s*(oz|lb|lbs|kg|g|ml|gallon|pack|ct)\b)'
    matches = re.findall(pattern, text, re.IGNORECASE)
    return [m[0].strip() for m in matches] if matches else []

def extract_brand(text):
    words = text.split()
    return " ".join(words[:2]) if len(words) >= 2 else (words[0] if words else "Brand")

def generate_bundle_copy(titles):
    valid_titles = [t.strip() for t in titles if t and t.strip()]
    if len(valid_titles) < 2:
        return None, "Please enter at least 2 product titles to form a bundle."

    brand = extract_brand(valid_titles[0])
    parsed_items = []
    all_sizes = []
    
    for idx, t in enumerate(valid_titles, 1):
        sizes = extract_sizes(t)
        if sizes:
            all_sizes.extend(sizes)
        parsed_items.append({'num': idx, 'raw': t, 'sizes': sizes})

    count_str = f"{len(valid_titles)}-Pack"
    sizes_summary = " ".join(all_sizes[:2]) if all_sizes else "Set"
    
    short_title = f"{brand} {count_str} {sizes_summary} Bundle"[:55].strip()

    raw_combined = " & ".join([item['raw'].split('|')[0].split('–')[0].strip() for item in parsed_items])
    full_title = f"{brand} {count_str} Bundle – {raw_combined} Supplement Set for Dogs & Cats – Skin, Coat, Joint & Overall Wellness Support"
    if len(full_title) > 200:
        full_title = full_title[:197] + "..."

    bullets = [
        f"COMPLETE {count_str.upper()} WELLNESS SET: Combines {len(valid_titles)} premium pet supplements into one comprehensive daily routine targeting skin, coat, joint, and immune support.",
        "FULL-SPECTRUM NUTRITION: Packed with essential fatty acids, vitamins, and minerals tailored for dogs and cats of all breeds, ages, and sizes.",
        "SKIN, COAT & JOINT CARE: Deeply nourishes dry skin, reduces shedding, supports joint mobility, and promotes a soft, vibrant, and healthy coat.",
        f"OPTIMAL SIZES FOR DAILY ROUTINE: Includes exact sizes ({', '.join(all_sizes) if all_sizes else 'standard sizes'}) to ensure continuous daily supplementation with maximum value.",
        "EASY TO SERVE MEAL TOPPER: Simple daily application—easily mix or scoop directly onto kibble or wet food for mess-free daily feeding."
    ]

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

def make_text_deck(copy_deck):
    text = f"=== AMAZON VIRTUAL BUNDLE COPY DECK ===\n\n"
    text += f"BUNDLE TITLE ({len(copy_deck['bundle_title'])}/200 Max Chars):\n{copy_deck['bundle_title']}\n\n"
    text += f"BUNDLE SHORT TITLE ({len(copy_deck['bundle_short_title'])}/55 Max Chars):\n{copy_deck['bundle_short_title']}\n\n"
    text += "KEY PRODUCT FEATURES (BULLET POINTS):\n"
    for idx, b in enumerate(copy_deck['bullets'], 1):
        text += f"• {b}\n"
    text += f"\nPRODUCT DESCRIPTION:\n{copy_deck['description']}\n"
    return text

st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 Generate Virtual Bundle Copy Deck"):
    raw_list = [title_1, title_2, title_3, title_4, title_5]
    result, err = generate_bundle_copy(raw_list)

    if err:
        st.error(err)
    else:
        st.success("Bundle copy successfully generated!")
        st.markdown('<div class="section-heading">2. Generated Bundle Fields</div>', unsafe_allow_html=True)

        col_a, col_b = st.columns(2)
        with col_a:
            st.text_input("Bundle Title (Max 200 Chars)", value=result['bundle_title'], help=f"Character count: {len(result['bundle_title'])}")
        with col_b:
            st.text_input("Bundle Short Title (Max 55 Chars)", value=result['bundle_short_title'], help=f"Character count: {len(result['bundle_short_title'])}")

        st.markdown("**Bullet Points (5 Features):**")
        for idx, b in enumerate(result['bullets'], 1):
            st.text_area(f"Bullet {idx}", value=b, height=70)

        st.markdown("**Product Description:**")
        st.text_area("Description", value=result['description'], height=180)

        txt_data = make_text_deck(result)
        st.markdown('<div class="section-heading">3. Download Copy Deck</div>', unsafe_allow_html=True)
        st.download_button(
            label="📥 Download Copy Deck (.txt)",
            data=txt_data,
            file_name="Virtual_Bundle_Copy_Deck.txt",
            mime="text/plain"
        )
