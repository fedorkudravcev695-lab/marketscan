import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
from bs4 import BeautifulSoup
import random

# 1. НАСТРОЙКА СТРАНИЦЫ
st.set_page_config(page_title="MarketScan Pro", page_icon="📊", layout="wide")
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stDeployButton {display:none;}
            div[data-testid="stStatusWidget"] {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# 2. БОКОВАЯ ПАНЕЛЬ
st.sidebar.header("🗂 Навигация")
page = st.sidebar.radio("Выбери раздел:", 
    ["📊 Демо-аналитика", "🌐 Парсер Книг (Реальный)", "🛒 Wildberries", "🔵 Ozon"])

# ==========================================
# ВКЛАДКА 1: ДЕМО-АНАЛИТИКА
# ==========================================
if page == "📊 Демо-аналитика":
    st.title("📊 MarketScan: Аналитика конкурентов")
    st.markdown("*(Это демо-данные. Переключи вкладку слева!)*")
    # (Код демо-вкладки оставляем прежним, я его сократил для удобства)
    df = pd.DataFrame(np.random.randn(20, 3), columns=["Цена", "Продажи", "Рейтинг"])
    st.line_chart(df)

# ==========================================
# ВКЛАДКА 2: РЕАЛЬНЫЙ ПАРСЕР КНИГ
# ==========================================
elif page == "🌐 Парсер Книг (Реальный)":
    st.title("🌐 Живой парсер (Books to Scrape)")
    
    @st.cache_data(ttl=60)
    def get_books():
        url = "http://books.toscrape.com/"
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        data = []
        for book in soup.find_all('article', class_='product_pod'):
            title = book.find('h3').find('a')['title']
            price = float(book.find('p', class_='price_color').text.replace('Â£', '').replace('£', ''))
            data.append({"Название": title, "Цена (GBP)": price})
        return pd.DataFrame(data)

    with st.spinner("🤖 Робот собирает данные..."):
        books_df = get_books()
    st.dataframe(books_df, use_container_width=True, hide_index=True)

# ==========================================
# ВКЛАДКА 3: WILDBERRIES (Имитация)
# ==========================================
elif page == "🛒 Wildberries":
    st.title("🛒 Аналитика Wildberries")
    st.warning("⚠️ Внимание: Это симуляция. Настоящий парсинг WB требует обхода капчи и прокси-серверов (уровень 'Босс').")
    
    search_query = st.text_input("Введите товар для поиска (например: Кроссовки, Футболка):", "Кроссовки")
    
    if st.button("🔍 Найти на WB"):
        with st.spinner("Робот ищет товары на Wildberries..."):
            # Генерируем реалистичные данные
            brands = ["Nike", "Adidas", "Puma", "Reebok", "NoName", "Demix"]
            data = []
            for i in range(10):
                data.append({
                    "Бренд": random.choice(brands),
                    "Товар": f"{search_query} модель {i+1}",
                    "Цена (руб)": random.randint(1500, 12000),
                    "Рейтинг": round(random.uniform(3.5, 5.0), 1),
                    "Отзывы": random.randint(10, 5000),
                    "Продавец": f"ИП Иванов {i}"
                })
            wb_df = pd.DataFrame(data)
            
            st.success(f"✅ Найдено {len(wb_df)} товаров по запросу '{search_query}'")
            st.dataframe(wb_df, use_container_width=True, hide_index=True)
            
            # График цен
            fig = px.scatter(wb_df, x="Цена (руб)", y="Рейтинг", size="Отзывы", 
                             color="Бренд", hover_name="Товар", title="Карта цен и рейтинга")
            st.plotly_chart(fig, use_container_width=True)

# ==========================================
# ВКЛАДКА 4: OZON (Имитация)
# ==========================================
elif page == "🔵 Ozon":
    st.title("🔵 Аналитика Ozon")
    st.info("💡 В реальности здесь будет код, который стучится в Ozon Seller API по ключу продавца.")
    
    search_query = st.text_input("Введите категорию Ozon:", "Электроника")
    
    if st.button("🔍 Проанализировать Ozon"):
        with st.spinner("Анализируем нишу Ozon..."):
            brands = ["Samsung", "Apple", "Xiaomi", "Huawei", "Honor"]
            data = []
            for i in range(8):
                data.append({
                    "Бренд": random.choice(brands),
                    "Товар": f"{search_query} {i+1}",
                    "Цена (руб)": random.randint(5000, 80000),
                    "В наличии": random.randint(0, 100),
                    "Ozon Карта (скидка)": f"{random.randint(5, 30)}%"
                })
            ozon_df = pd.DataFrame(data)
            
            st.success("✅ Данные Ozon загружены!")
            st.dataframe(ozon_df, use_container_width=True, hide_index=True)
            
            # Круговая диаграмма распределения брендов
            fig = px.pie(ozon_df, names="Бренд", values="Цена (руб)", title="Доля брендов в нише по цене")
            st.plotly_chart(fig, use_container_width=True)