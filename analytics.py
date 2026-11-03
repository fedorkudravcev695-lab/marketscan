import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
from bs4 import BeautifulSoup
import random
import time

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

# 2. СИСТЕМА ПОДПИСКИ (Пока имитация)
if 'subscribed' not in st.session_state:
    st.session_state.subscribed = False

# 3. БОКОВАЯ ПАНЕЛЬ
st.sidebar.header("🗂 Навигация")
page = st.sidebar.radio("Выбери раздел:", 
    ["📊 Демо-аналитика", "🌐 Парсер Книг", "🛒 Wildberries", "🔵 Ozon"])

st.sidebar.divider()

# Блок подписки в сайдбаре
st.sidebar.header("💳 Подписка")
if not st.session_state.subscribed:
    st.sidebar.warning("У вас нет подписки. Вы видите рекламу.")
    if st.sidebar.button("Оплатить 50 ₽ / неделя"):
        st.session_state.subscribed = True
        st.sidebar.success("✅ Подписка оформлена! Реклама убрана.")
        time.sleep(1)
        st.rerun()
else:
    st.sidebar.success("⭐ Premium активен. Рекламы нет.")
    if st.sidebar.button("Отменить подписку"):
        st.session_state.subscribed = False
        st.rerun()

# 4. РЕКЛАМНЫЙ БАННЕР (Показывается только без подписки)
if not st.session_state.subscribed:
    st.markdown("""
    <div style="background-color: #ffeb3b; padding: 15px; border-radius: 10px; text-align: center; border: 2px dashed #f44336; margin-bottom: 20px;">
        <h3 style="color: #d32f2f; margin: 0;">📢 ЗДЕСЬ МОЖЕТ БЫТЬ ВАША РЕКЛАМА!</h3>
        <p style="margin: 5px 0 0 0; color: #333;">Оформите подписку за 50 ₽ в неделю, чтобы убрать баннеры и получить доступ ко всем данным.</p>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# ВКЛАДКА 1: ДЕМО-АНАЛИТИКА
# ==========================================
if page == "📊 Демо-аналитика":
    st.title("📊 MarketScan: Аналитика конкурентов")
    if not st.session_state.subscribed:
        st.info("💡 Вы видите только 1 график. Оформите подписку, чтобы видеть все данные.")
    
    df = pd.DataFrame(np.random.randn(20, 3), columns=["Цена", "Продажи", "Рейтинг"])
    st.line_chart(df)

# ==========================================
# ВКЛАДКА 2: РЕАЛЬНЫЙ ПАРСЕР КНИГ
# ==========================================
elif page == "🌐 Парсер Книг":
    st.title("🌐 Живой парсер (Books to Scrape)")
    if not st.session_state.subscribed:
        st.warning("⚠️ В бесплатной версии данные обновляются раз в час. В Premium — каждую минуту.")
        
    @st.cache_data(ttl=3600 if not st.session_state.subscribed else 60)
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
# ВКЛАДКА 3: WILDBERRIES
# ==========================================
elif page == "🛒 Wildberries":
    st.title("🛒 Аналитика Wildberries")
    
    # Поле для API ключа
    st.subheader("🔑 Подключение к вашему магазину")
    api_key = st.text_input("Введите ваш API-ключ от WB Партнёры:", type="password")
    
    if api_key:
        st.success("✅ Ключ принят! (Функция запроса к WB API будет добавлена на следующем уроке)")
    else:
        st.info("Введите ключ, чтобы увидеть аналитику вашего магазина. Ключ можно получить в личном кабинете WB Партнёры -> Настройки -> API.")
    
    st.divider()
    
    # Демонстрация
    if st.button("🔍 Показать пример анализа цен"):
        with st.spinner("Робот анализирует нишу..."):
            brands = ["Nike", "Adidas", "Puma", "Reebok", "NoName"]
            data = [{"Бренд": random.choice(brands), "Цена (руб)": random.randint(1500, 12000), "Продажи": random.randint(10, 500)} for _ in range(10)]
            wb_df = pd.DataFrame(data)
            
            # Если НЕТ подписки - показываем только таблицу, графики скрыты (Paywall)
            st.dataframe(wb_df, use_container_width=True, hide_index=True)
            
            if not st.session_state.subscribed:
                st.error("🔒 Графики и глубокий анализ скрыты. Оформите подписку за 50 ₽, чтобы увидеть их!")
            else:
                fig = px.scatter(wb_df, x="Цена (руб)", y="Продажи", color="Бренд", size="Продажи", title="Карта цен и продаж")
                st.plotly_chart(fig, use_container_width=True)
                st.success("⭐ Вы видите этот график, потому что у вас есть Premium!")

# ==========================================
# ВКЛАДКА 4: OZON
# ==========================================
elif page == "🔵 Ozon":
    st.title("🔵 Аналитика Ozon")
    st.info("💡 В реальности здесь будет подключение по API-ключам продавца Ozon.")
