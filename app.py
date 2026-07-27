import io
import re
import streamlit as st
from weasyprint import HTML

# Custom CSS for enhanced typography, clean readability, and colored headings
st.set_page_config(page_title="Virtual Bundle Listing Creator", layout="wide")

st.markdown("""
    <style>
        /* Global Typography & Background */
        html, body, [class*="css"] {
            font-family: 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            color: #2D3748;
        }
        
        /* Main Title Header */
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
        
        /* Section Headings */
        .section-heading {
            color: #0284C7;
            font-size: 1.35rem;
            font-weight: 600;
            border-bottom: 2px solid #E2E8F0;
            padding-bottom: 0.4rem;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
        }
        
        /* Card Containers */
        .stTextArea label, .stTextInput label {
            color: #1E293B !important;
            font-weight: 600 !important;
            font-size: 0.95rem !important;
        }
        
        /* Primary Button */
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

# App Title & Description
st.markdown('<div class="main-header">📦 Virtual Bundle Listing Creator</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Enter 2 to 5 raw product titles below to automatically generate fully optimized Amazon Virtual Bundle copy deck fields and a downloadable PDF.</div>', unsafe_allow_html=True)

# Input Section
st.markdown('<div class="section-heading">1. Input Raw Product Titles (2 to 5 Products)</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    title_1 = st.text_area("Product 1 Title (Required)", height=90, key="p1")
    title_2 = st.text_area("Product 2 Title (Required)", height=90, key="p2")
    title_3 = st.text_area("Product 3 Title (Optional)", height=90, key="p3")

with col2:
    title_4 = st.text_area("Product 4 Title (Optional)", height=90, key="p4")
    title_5 = st.text_area("Product 5 Title (Optional)", height=90, key="p5")

# Helper Functions
def extract_sizes(text):
    """Extracts weight, volume, or count sizes (e.g., 128oz, 1.5 lb, 8.5 oz)."""
    pattern = r'(\b\d+(\.\d+)?\s*(oz|lb|lbs|kg|g|ml|gallon|pack|ct)\b)'
    matches = re.findall(pattern, text, re.IGNORECASE)
    return [m[0].strip() for m in matches] if matches else []

def extract_brand(text):
    """Extracts leading brand name."""
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
    
    # 1. Short Title (Max 55 Chars)
    short_title = f"{brand} {count_str} {sizes_summary} Bundle"[:55].strip()

    # 2. Bundle Title (Max 200 Chars)
    raw_combined = " & ".join([item['raw'].split('|')[0].split('–')[0].strip() for item in parsed_items])
    full_title = f"{brand} {count_str} Bundle – {raw_combined} Supplement Set for Dogs & Cats – Skin, Coat, Joint & Overall Wellness Support"
    if len(full_title) > 200:
        full_title = full_title[:197] + "..."

    # 3. Bullet Points (5 Items)
    bullets = [
        f"COMPLETE {count_str.upper()} WELLNESS SET: Combines {len(valid_titles)} premium pet supplements into one comprehensive daily routine targeting skin, coat, joint, and immune support.",
        "FULL-SPECTRUM NUTRITION: Packed with essential fatty acids, vitamins, and minerals tailored for dogs and cats of all breeds, ages, and sizes.",
        "SKIN, COAT & JOINT CARE: Deeply nourishes dry skin, reduces shedding, supports joint mobility, and promotes a soft, vibrant, and healthy coat.",
        f"OPTIMAL SIZES FOR DAILY ROUTINE: Includes exact sizes ({', '.join(all_sizes) if all_sizes else 'standard sizes'}) to ensure continuous daily supplementation with maximum value.",
        "EASY TO SERVE MEAL TOPPER: Simple daily application—easily mix or scoop directly onto kibble or wet food for mess-free daily feeding."
    ]

    # 4. Product Description
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

def create_pdf(copy_deck):
    bullet_html = "".join([f"<li>{b}</li>" for b in copy_deck['bullets']])
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            @page {{ size: A4; margin: 15mm; }}
            body {{ font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; color: #1E293B; line-height: 1.5; }}
            .header {{ background-color: #1E3A8A; color: white; padding: 20px; border-radius: 6px; margin-bottom: 20px; }}
            .header h1 {{ margin: 0; font-size: 18pt; }}
            .section {{ margin-bottom: 18px; padding: 12px 15px; border: 1px solid #E2E8F0; border-radius: 6px; background-color: #F8FAFC; }}
            .label {{ font-size: 9pt; font-weight: bold; color: #0284C7; text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 4px; }}
            .content {{ font-size: 10.5pt; font-weight: 500; color: #0F172A; }}
            ul {{ margin: 5px 0 0 0; padding-left: 18px; }}
            li {{ margin-bottom: 6px; font-size: 10pt; }}
            .desc-box {{ white-space: pre-line; font-size: 10pt; color: #334155; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>Virtual Bundle Listing Copy Deck</h1>
        </div>
        <div class="section">
            <div class="label">Bundle Title ({len(copy_deck['bundle_title'])}/200 Max Chars)</div>
            <div class="content">{copy_deck['bundle_title']}</div>
        </div>
        <div class="section">
            <div class="label">Bundle Short Title ({len(copy_deck['bundle_short_title'])}/55 Max Chars)</div>
            <div class="content">{copy_deck['bundle_short_title']}</div>
        </div>
        <div class="section">
            <div class="label">Key Product Features (Bullet Points)</div>
            <ul>{bullet_html}</ul>
        </div>
        <div class="section">
            <div class="label">Product Description</div>
            <div class="desc-box">{copy_deck['description']}</div>
        </div>
    </body>
    </html>
    """
    return HTML(string=html_content).write_pdf()

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

        pdf_data = create_pdf(result)
        st.markdown('<div class="section-heading">3. Download Copy Deck</div>', unsafe_allow_html=True)
        st.download_button(
            label="📥 Download Copy Deck as PDF",
            data=pdf_data,
            file_name="Virtual_Bundle_Copy_Deck.pdf",
            mime="application/pdf"
        )
