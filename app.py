import streamlit as st
import requests
import pandas as pd
from datetime import datetime

# -----------------------------------
# Configuration
# -----------------------------------

API_KEY = "a3f417b116fa4104b3c547e8ee9d32e1"
BASE_URL = "https://newsapi.org/v2/top-headlines"

st.set_page_config(
    page_title="Advanced News Dashboard",
    page_icon="📰",
    layout="wide"
)

# -----------------------------------
# Sidebar
# -----------------------------------

st.sidebar.title("News Filters")

country_options = {
    "India": "in",
    "United States": "us",
    "United Kingdom": "gb",
    "Australia": "au",
    "Canada": "ca",
    "Germany": "de",
    "France": "fr",
    "Japan": "jp"
}

category_options = [
    "general",
    "business",
    "entertainment",
    "health",
    "science",
    "sports",
    "technology"
]

selected_country = st.sidebar.selectbox(
    "Select Country",
    list(country_options.keys())
)

selected_category = st.sidebar.selectbox(
    "Select Category",
    category_options
)

keyword = st.sidebar.text_input(
    "Search Keywords",
    placeholder="AI, Tesla, Cricket..."
)

article_count = st.sidebar.slider(
    "Number of Articles",
    min_value=5,
    max_value=50,
    value=15
)

search_btn = st.sidebar.button("Fetch News")

# -----------------------------------
# Fetch Function
# -----------------------------------

@st.cache_data(ttl=300)
def get_news(country, category, query, page_size):
    params = {
        "apiKey": API_KEY,
        "country": country,
        "category": category,
        "pageSize": page_size
    }

    if query:
        params["q"] = query

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        return response.json()

    return {
        "status": "error",
        "message": response.text
    }

# -----------------------------------
# Header
# -----------------------------------

st.title("📰 Advanced News Dashboard")
st.markdown(
    "Search and filter breaking news by location, category and keywords."
)

# -----------------------------------
# Fetch Data
# -----------------------------------

if search_btn:

    with st.spinner("Fetching latest news..."):

        data = get_news(
            country_options[selected_country],
            selected_category,
            keyword,
            article_count
        )

        if data["status"] != "ok":
            st.error(data.get("message", "Failed to fetch news"))
            st.stop()

        articles = data.get("articles", [])

        if not articles:
            st.warning("No articles found.")
            st.stop()

        st.success(f"{len(articles)} articles found")

        # Summary Table
        table_data = []

        for article in articles:
            table_data.append({
                "Title": article["title"],
                "Source": article["source"]["name"],
                "Published": article["publishedAt"][:10]
            })

        st.subheader("News Overview")
        st.dataframe(
            pd.DataFrame(table_data),
            use_container_width=True
        )

        st.divider()

        # News Cards
        for article in articles:

            title = article.get("title", "No Title")
            source = article.get("source", {}).get("name", "Unknown")
            image = article.get("urlToImage")
            description = article.get("description")
            url = article.get("url")
            published = article.get("publishedAt")

            with st.container():

                col1, col2 = st.columns([1, 3])

                with col1:
                    if image:
                        st.image(image, use_container_width=True)

                with col2:
                    st.subheader(title)

                    st.caption(
                        f"Source: {source} | Published: {published}"
                    )

                    if description:
                        st.write(description)

                    st.link_button(
                        "Read Full Article",
                        url
                    )

                st.divider()

else:
    st.info("Use the filters in the sidebar and click 'Fetch News'.")
