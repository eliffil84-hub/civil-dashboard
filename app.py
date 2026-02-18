"""
Civil ürün sayısı canlı dashboard (requests tabanlı basit sürüm)
Streamlit Cloud ile uyumlu
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import streamlit as st

SEARCH_KEYWORD = "Civil Baby"

# --------------------------------------------------
# Yardımcı fonksiyon
# --------------------------------------------------

def extract_number(text: str):
    digits = ''.join(filter(str.isdigit, text))
    return int(digits) if digits else None


def get_count(url, selector):
    try:
        r = requests.get(url, timeout=20, headers={"User-Agent": "Mozilla/5.0"})
        if r.status_code != 200:
            return None

        soup = BeautifulSoup(r.text, "html.parser")
        elem = soup.select_one(selector)
        return extract_number(elem.text) if elem else None

    except Exception:
        return None


# --------------------------------------------------
# Site fonksiyonları (requests ile çekilebilenler)
# --------------------------------------------------

def get_civilim_count():
    return get_count(
        f"https://www.civilim.com/arama?q={SEARCH_KEYWORD.replace(' ', '+')}",
        ".product-count",
    )


def get_hepsiburada_count():
    return get_count(
        f"https://www.hepsiburada.com/ara?q={SEARCH_KEYWORD.replace(' ', '+')}",
        ".resultCount",
    )


def get_amazon_count():
    return get_count(
        f"https://www.amazon.com.tr/s?k={SEARCH_KEYWORD.replace(' ', '+')}",
        ".s-result-count",
    )


def get_n11_count():
    return get_count(
        f"https://www.n11.com/arama?q={SEARCH_KEYWORD.replace(' ', '+')}",
        ".resultText",
    )


# --------------------------------------------------
# Veri toplama
# --------------------------------------------------

def collect_data():
    today = datetime.now().strftime("%Y-%m-%d")

    channels = [
        ("civilim.com", get_civilim_count),
        ("Hepsiburada", get_hepsiburada_count),
        ("Amazon TR", get_amazon_count),
        ("N11", get_n11_count),
    ]

    rows = []

    for name, func in channels:
        count = func()
        rows.append((name, SEARCH_KEYWORD, count, today))

    df = pd.DataFrame(rows, columns=["Kanal", "Arama Anahtarı", "Ürün Sayısı", "Tarih"])
    return df


# --------------------------------------------------
# STREAMLIT ARAYÜZÜ
# --------------------------------------------------

st.set_page_config(page_title="Civil Ürün Sayısı", layout="wide")

st.title("Civil Ürün Sayısı Canlı Dashboard")

if st.button("Veriyi Güncelle"):
    df = collect_data()
    st.dataframe(df, use_container_width=True)
    st.bar_chart(df.set_index("Kanal")["Ürün Sayısı"])

st.caption("Bu sürüm yalnızca bot koruması olmayan siteleri gösterir.")

