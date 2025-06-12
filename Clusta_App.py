import streamlit as st
import pandas as pd

# Load database
@st.cache_data
def load_data():
    df = pd.read_csv("MVP_CG_DATABASE - Cream_Products.csv", dtype=str)
    df['Barcode'] = df['Barcode'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
    return df

df = load_data()

st.title("Cosmetic Safety Checker")

barcode_input = st.text_input("Enter Barcode")

if barcode_input:
    record = df[df['Barcode'] == barcode_input.strip()]
    
    if record.empty:
        st.error("🚫 Product not found")
    else:
        row = record.iloc[0].fillna('')
        carcinogen = row.get("Carcinogen", "")
        safety_class = '✅ Safe'
        if "high" in carcinogen.lower():
            safety_class = '🔴 High Risk'
        elif "medium" in carcinogen.lower():
            safety_class = '🟡 Medium Risk'
        
        st.markdown(f"""
        ### {row.get("Brand/Product", "Unknown Product")}
        **Barcode:** {row.get("Barcode", "")}  
        **Carcinogen Risk:** {carcinogen}  
        **Allergens:** {row.get("Allergen", "")}  
        **Fragrance:** {row.get("Fragrance", "")}  
        **Endocrine Disruptor:** {row.get("Endocrine disruptor", "")}  
        **Ingredients:** {row.get("Ingredients", "")}  
        **Safety Status:** {safety_class}
        """)
