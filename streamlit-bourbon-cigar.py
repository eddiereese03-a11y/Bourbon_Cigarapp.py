import streamlit as st
import json

# Page configuration
st.set_page_config(
    page_title="Bourbon & Cigar Pairing",
    page_icon="🥃",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #78350f 0%, #92400e 50%, #1c1917 100%);
    }
    .stButton>button {
        background-color: #d97706;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        padding: 0.5rem 2rem;
        border: none;
    }
    .stButton>button:hover {
        background-color: #f59e0b;
    }
    .pairing-card {
        background-color: #292524;
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #d97706;
        margin: 1rem 0;
    }
    .shop-card {
        background-color: #292524;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #d97706;
        margin: 0.5rem 0;
    }
    h1, h2, h3, h4 {
        color: #fef3c7 !important;
    }
    .stSelectbox label, .stTextInput label {
        color: #fde68a !important;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'pairing' not in st.session_state:
    st.session_state.pairing = None

# Data
bourbons = [
    {
        "name": "Buffalo Trace",
        "profile": "Light & Sweet",
        "notes": "Vanilla, caramel, honey",
        "proof": 90,
        "bestWith": ["Connecticut Shade", "Dominican Mild"]
    },
    {
        "name": "Maker's Mark",
        "profile": "Smooth & Wheated",
        "notes": "Butterscotch, wheat, vanilla",
        "proof": 90,
        "bestWith": ["Connecticut Shade", "Ecuadorian Connecticut"]
    },
    {
        "name": "Woodford Reserve",
        "profile": "Rich & Balanced",
        "notes": "Tobacco, cocoa, spice",
        "proof": 90.4,
        "bestWith": ["Habano Wrapper", "Nicaraguan Medium"]
    },
    {
        "name": "Knob Creek",
        "profile": "Bold & Robust",
        "notes": "Oak, caramel, char",
        "proof": 100,
        "bestWith": ["Maduro", "Nicaraguan Full"]
    },
    {
        "name": "Elijah Craig Small Batch",
        "profile": "Complex & Rich",
        "notes": "Dark fruit, leather, oak",
        "proof": 94,
        "bestWith": ["Maduro", "Habano Oscuro"]
    },
    {
        "name": "Wild Turkey 101",
        "profile": "Spicy & Full-bodied",
        "notes": "Rye spice, caramel, oak",
        "proof": 101,
        "bestWith": ["Nicaraguan Full", "Ligero-heavy blend"]
    }
]

cigars = [
    {
        "name": "Connecticut Shade",
        "profile": "Mild & Creamy",
        "notes": "Cream, nuts, cedar",
        "strength": "Mild",
        "bestWith": ["Buffalo Trace", "Maker's Mark"]
    },
    {
        "name": "Dominican Mild",
        "profile": "Smooth & Mellow",
        "notes": "Toast, butter, hay",
        "strength": "Mild",
        "bestWith": ["Buffalo Trace", "Maker's Mark"]
    },
    {
        "name": "Ecuadorian Connecticut",
        "profile": "Silky & Refined",
        "notes": "Almond, white pepper, grass",
        "strength": "Mild-Medium",
        "bestWith": ["Maker's Mark", "Woodford Reserve"]
    },
    {
        "name": "Habano Wrapper",
        "profile": "Medium & Spicy",
        "notes": "Pepper, earth, leather",
        "strength": "Medium",
        "bestWith": ["Woodford Reserve", "Elijah Craig Small Batch"]
    },
    {
        "name": "Nicaraguan Medium",
        "profile": "Balanced & Flavorful",
        "notes": "Coffee, cocoa, wood",
        "strength": "Medium",
        "bestWith": ["Woodford Reserve", "Knob Creek"]
    },
    {
        "name": "Maduro",
        "profile": "Rich & Sweet",
        "notes": "Chocolate, espresso, molasses",
        "strength": "Medium-Full",
        "bestWith": ["Knob Creek", "Elijah Craig Small Batch"]
    },
    {
        "name": "Habano Oscuro",
        "profile": "Bold & Complex",
        "notes": "Dark chocolate, leather, earth",
        "strength": "Full",
        "bestWith": ["Elijah Craig Small Batch", "Wild Turkey 101"]
    },
    {
        "name": "Nicaraguan Full",
        "profile": "Powerful & Intense",
        "notes": "Black pepper, cedar, earth",
        "strength": "Full",
        "bestWith": ["Knob Creek", "Wild Turkey 101"]
    },
    {
        "name": "Ligero-heavy blend",
        "profile": "Extra Full & Bold",
        "notes": "Espresso, dark spice, oak",
        "strength": "Full+",
        "bestWith": ["Wild Turkey 101", "Knob Creek"]
    }
]

def find_pairing(item_name, mode):
    """Find pairing for bourbon or cigar"""
    if mode == "bourbon":
        bourbon = next((b for b in bourbons if b["name"] == item_name), None)
        if not bourbon:
            return None
        
        matching_cigars = [c for c in cigars if any(
            match in c["name"] or c["name"] in match 
            for match in bourbon["bestWith"]
        )]
        
        reasoning = get_bourbon_reasoning(bourbon, matching_cigars[0] if matching_cigars else None)
        
        return {
            "type": "bourbon",
            "item": bourbon,
            "matches": matching_cigars,
            "reasoning": reasoning
        }
    else:
        cigar = next((c for c in cigars if c["name"] == item_name), None)
        if not cigar:
            return None
        
        matching_bourbons = [b for b in bourbons if any(
            match in b["name"] or b["name"] in match 
            for match in cigar["bestWith"]
        )]
        
        reasoning = get_cigar_reasoning(cigar, matching_bourbons[0] if matching_bourbons else None)
        
        return {
            "type": "cigar",
            "item": cigar,
            "matches": matching_bourbons,
            "reasoning": reasoning
        }

def get_bourbon_reasoning(bourbon, cigar):
    """Generate reasoning for bourbon pairing"""
    if not cigar:
        return ""
    
    proof_level = "moderate" if bourbon["proof"] < 95 else "high"
    strength_match = ("milder" if "Mild" in cigar["strength"] else 
                     "fuller-bodied" if "Full" in cigar["strength"] else "medium-bodied")
    
    return (f"The {bourbon['profile'].lower()} character of {bourbon['name']} "
            f"({bourbon['proof']} proof) complements the {strength_match} "
            f"{cigar['profile'].lower()} profile beautifully. The bourbon's "
            f"{bourbon['notes'].split(',')[0]} notes won't overpower the cigar's "
            f"{cigar['notes'].split(',')[0]} flavors, creating a harmonious balance.")

def get_cigar_reasoning(cigar, bourbon):
    """Generate reasoning for cigar pairing"""
    if not bourbon:
        return ""
    
    return (f"This {cigar['strength'].lower()} strength cigar with "
            f"{cigar['profile'].lower()} characteristics pairs wonderfully with "
            f"{bourbon['name']}'s {bourbon['profile'].lower()} profile. The "
            f"{cigar['notes'].split(',')[0]} from the cigar enhances the "
            f"{bourbon['notes'].split(',')[0]} in the bourbon.")

# Header
st.title("🥃 Bourbon & Cigar Pairing")
st.markdown("### Find your perfect match")

# Mode selection
col1, col2 = st.columns(2)
with col1:
    if st.button("🍷 I Have Bourbon", use_container_width=True):
        st.session_state.mode = "bourbon"
with col2:
    if st.button("🚬 I Have a Cigar", use_container_width=True):
        st.session_state.mode = "cigar"

# Initialize mode if not set
if 'mode' not in st.session_state:
    st.session_state.mode = "bourbon"

# Display current mode
mode_icon = "🍷" if st.session_state.mode == "bourbon" else "🚬"
mode_text = "Bourbon" if st.session_state.mode == "bourbon" else "Cigar"
st.markdown(f"### {mode_icon} Selected: {mode_text}")

# Item selection
current_list = bourbons if st.session_state.mode == "bourbon" else cigars
item_names = [item["name"] for item in current_list]

selected_item = st.selectbox(
    f"Select your {mode_text.lower()}:",
    [""] + item_names,
    format_func=lambda x: "-- Choose --" if x == "" else x
)

# Find pairing button
if st.button("🔍 Find Perfect Pairing", use_container_width=True):
    if selected_item:
        st.session_state.pairing = find_pairing(selected_item, st.session_state.mode)
    else:
        st.warning("Please select an item first")

# Display pairing results
if st.session_state.pairing:
    pairing = st.session_state.pairing
    
    st.markdown("## 🎯 Your Perfect Pairing")
    
    col1, col2, col3 = st.columns([1, 0.3, 1])
    
    with col1:
        item_icon = "🍷" if pairing["type"] == "bourbon" else "🚬"
        st.markdown(f"### {item_icon} You Have")
        st.markdown(f"""
        <div class="pairing-card">
            <h3>{pairing['item']['name']}</h3>
            <p style="color: #fde68a;"><em>{pairing['item']['profile']}</em></p>
            <p style="color: #fcd34d; font-size: 0.9em;">{pairing['item']['notes']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### →")
    
    with col3:
        match_icon = "🚬" if pairing["type"] == "bourbon" else "🍷"
        st.markdown(f"### {match_icon} Pair With")
        if pairing["matches"]:
            match = pairing["matches"][0]
            st.markdown(f"""
            <div class="pairing-card">
                <h3>{match['name']}</h3>
                <p style="color: #fde68a;"><em>{match['profile']}</em></p>
                <p style="color: #fcd34d; font-size: 0.9em;">{match['notes']}</p>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("No specific match found")
    
    # Reasoning
    if pairing["reasoning"]:
        st.markdown("### 💡 Why this pairing works:")
        st.markdown(f"""
        <div class="pairing-card">
            <p style="color: #fef3c7;">{pairing['reasoning']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Other options
    if len(pairing["matches"]) > 1:
        st.markdown("### 🌟 Other great options:")
        cols = st.columns(2)
        for idx, match in enumerate(pairing["matches"][1:]):
            with cols[idx % 2]:
                st.markdown(f"""
                <div class="shop-card">
                    <h4>{match['name']}</h4>
                    <p style="color: #fde68a; font-size: 0.85em;">{match['profile']}</p>
                </div>
                """, unsafe_allow_html=True)
