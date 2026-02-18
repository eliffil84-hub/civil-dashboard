import streamlit as st
import pandas as pd

st.title("Civil Ürün Sayısı Dashboard")

data = {
    "Kanal": ["civilim.com", "Hepsiburada", "Amazon TR", "N11"],
    "Ürün Sayısı": [120, 95, 60, 40]
}

df = pd.DataFrame(data)

st.dataframe(df, use_container_width=True)
st.bar_chart(df.set_index("Kanal"))
