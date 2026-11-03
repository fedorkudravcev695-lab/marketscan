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

# 2. СИСТЕМА ПОДПИСКИ (Имитация)
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

# 4. РЕКЛАМНЫЙ БАННЕР
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
    
    st.subheader("🔑 Подключение к вашему магазину")
    api_key = st.text_input("Введите ваш API-ключ от WB Партнёры:", type="password", key="wb_key")
    
    if api_key:
        st.success("✅ Ключ принят! (Функция запроса к WB API будет добавлена на следующем уроке)")
    else:
        st.info("Введите ключ, чтобы увидеть аналитику вашего магазина.")
    
    st.divider()
    
    if st.button("🔍 Показать пример анализа цен WB"):
        with st.spinner("Робот анализирует нишу..."):
            brands = ["Nike", "Adidas", "Puma", "Reebok", "NoName"]
            data = [{"Бренд": random.choice(brands), "Цена (руб)": random.randint(1500, 12000), "Продажи": random.randint(10, 500)} for _ in range(10)]
            wb_df = pd.DataFrame(data)
            
            st.dataframe(wb_df, use_container_width=True, hide_index=True)
            
            if not st.session_state.subscribed:
                st.error("🔒 Графики и глубокий анализ скрыты. Оформите подписку за 50 ₽, чтобы увидеть их!")
            else:
                fig = px.scatter(wb_df, x="Цена (руб)", y="Продажи", color="Бренд", size="Продажи", title="Карта цен и продаж")
                st.plotly_chart(fig, use_container_width=True)
                st.success("⭐ Вы видите этот график, потому что у вас есть Premium!")

# ==========================================
# ВКЛАДКА 4: OZON (НОВЫЙ ФУНКЦИОНАЛ!)
# ==========================================
elif page == "🔵 Ozon":
    st.title("🔵 Аналитика Ozon")
    
    st.subheader("🔑 Подключение к вашему магазину Ozon")
    ozon_key = st.text_input("Введите ваш Client ID и Api-Key от Ozon Seller:", type="password", key="ozon_key")
    
    if ozon_key:
        st.success("✅ Ключ принят! (Интеграция с Ozon API появится позже)")
    else:
        st.info("Введите ключ, чтобы увидеть аналитику вашего магазина.")
    
    st.divider()
    
    if st.button("🔍 Проанализировать нишу Ozon"):
        with st.spinner("Робот собирает данные с Ozon..."):
            # Генерируем данные под Ozon (электроника, подороже)
            brands = ["Samsung", "Apple", "Xiaomi", "Huawei", "Honor"]
            categories = ["Смартфон", "Наушники", "Ноутбук", "Умные часы", "Планшет"]
            
            data = []
            for i in range(10):
                price = random.randint(5000, 80000)
                discount = random.randint(5, 30)
                data.append({
                    "Бренд": random.choice(brands),
                    "Товар": random.choice(categories),
                    "Цена (руб)": price,
                    "Скидка по карте Ozon (%)": discount,
                    "Цена с картой (руб)": int(price * (1 - discount / 100))
                })
            ozon_df = pd.DataFrame(data)
            
            # Показываем таблицу всем
            st.dataframe(ozon_df, use_container_width=True, hide_index=True)
            
            # Paywall (замок) для графиков
            if not st.session_state.subscribed:
                st.error("🔒 Круговая диаграмма и анализ брендов скрыты. Оформите подписку за 50 ₽, чтобы увидеть их!")
            else:
                st.subheader("📊 Доля брендов в нише")
                fig = px.pie(ozon_df, names="Бренд", values="Цена (руб)", 
                             title="Распределение бюджета по брендам", hole=0.4,
                             color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(fig, use_container_width=True)
                st.success("⭐ Вы видите этот график, потому что у вас есть Premium!")
