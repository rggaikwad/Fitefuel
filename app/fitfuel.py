import streamlit as st
import pandas as pd
import sqlite3
from datetime import datetime
import plotly.express as px

# Database setup
def init_db():
    conn = sqlite3.connect("fitfuel.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                 id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 username TEXT UNIQUE, 
                 password TEXT, 
                 age INTEGER, 
                 weight FLOAT, 
                 height FLOAT, 
                 gender TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS meals (
                 id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 username TEXT, 
                 date TEXT, 
                 meal_type TEXT, 
                 meal_name TEXT, 
                 calories INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS feedback (
                 id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 username TEXT, 
                 query TEXT, 
                 rating INTEGER)''')
    conn.commit()
    conn.close()

# User authentication
def authenticate(username, password):
    conn = sqlite3.connect("fitfuel.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user

# Main App
init_db()
st.title("FitFuel - Your Personal Diet Planner")

# Check session state for login
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

# Login/Register
if not st.session_state['logged_in']:
    menu = ["Login", "Register"]
    choice = st.sidebar.selectbox("Menu", menu)
    
    if choice == "Login":
        st.subheader("Login to Your Account")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if authenticate(username, password):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.rerun()
            else:
                st.warning("Incorrect Username or Password")
else:
    # Dashboard with tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["Home", "Meal Planning", "Calorie Tracker", "Feedback & Report", "Balanced Diet Chart"])
    
    with tab1:
        with tab1:

            st.subheader("Welcome to FitFuel")
            st.write("FitFuel helps you plan meals, track calories, and maintain a healthy diet!")
            st.write("Explore our Balanced Diet recommendations and Meal Planning features to achieve your health goals effectively.")
            st.write("**Key Features:**")
            st.markdown("- **Personalized Meal Planning**: Choose meals based on dietary preferences.")
            st.markdown("- **Calorie Tracking**: Monitor your daily calorie intake.")
            st.markdown("- **Balanced Diet Guidance**: Get diet recommendations based on your food choices.")
    with tab2:
        st.subheader("Meal Planning")
        meal_types = ["Breakfast", "Lunch", "Dinner", "Snacks"]
        selected_meal_type = st.selectbox("Select Meal Type", meal_types)
        meal_options = {
            "Breakfast": ["Poha", "Paratha", "Oats", "Smoothie", "Other"],
            "Lunch": ["Biryani", "Dal Tadka", "Paneer Butter Masala", "Chapati & Sabzi", "Other"],
            "Dinner": ["Khichdi", "Pasta", "Grilled Chicken", "Soup", "Other"],
            "Snacks": ["Fruits", "Nuts", "Yogurt", "Sandwich", "Other"]
        }
        meal_name = st.selectbox("Select Meal", meal_options[selected_meal_type])
        calories = st.number_input("Calories", min_value=0, max_value=2000)
        if st.button("Add Meal"):
            conn = sqlite3.connect("fitfuel.db")
            c = conn.cursor()
            c.execute("INSERT INTO meals (username, date, meal_type, meal_name, calories) VALUES (?, ?, ?, ?, ?)", 
                      (st.session_state['username'], datetime.today().strftime('%Y-%m-%d'), selected_meal_type, meal_name, calories))
            conn.commit()
            conn.close()
            st.success("Meal Added Successfully!")
    
    with tab3:
        st.subheader("Advanced Calorie Tracking")
        conn = sqlite3.connect("fitfuel.db")
        df = pd.read_sql_query(f"SELECT date, meal_type, meal_name, calories FROM meals WHERE username='{st.session_state['username']}'", conn)
        conn.close()
        st.dataframe(df)
        if not df.empty:
            fig = px.line(df, x='date', y='calories', color='meal_type', title='Calorie Intake Over Time')
            st.plotly_chart(fig)
    
    with tab4:
        st.subheader("Feedback & Report")
        query = st.text_area("Enter your queries or feedback")
        rating = st.slider("Rate the app", 1, 5, 3)
        if st.button("Submit Feedback"):
            conn = sqlite3.connect("fitfuel.db")
            c = conn.cursor()
            c.execute("INSERT INTO feedback (username, query, rating) VALUES (?, ?, ?)", (st.session_state['username'], query, rating))
            conn.commit()
            conn.close()
            st.success("Thanks for your feedback!")
    
    with tab5:
        st.subheader("Balanced Diet Chart")
        food_items = ["Rice", "Dal", "Paneer", "Chicken", "Fruits", "Vegetables", "Milk", "Eggs"]
        food_choice = st.selectbox("Select a Food Item", food_items)
        balanced_diets = {
            "Rice": "Balanced Diet: Add Dal, Vegetables, and Yogurt for a complete meal.",
            "Dal": "Balanced Diet: Combine with Rice, Roti, and Salad for best nutrition.",
            "Paneer": "Balanced Diet: Add Whole Grains and Nuts for a protein-rich diet.",
            "Chicken": "Balanced Diet: Pair with Brown Rice and Steamed Veggies for a lean meal.",
            "Fruits": "Balanced Diet: Mix with Nuts and Yogurt for a healthy snack.",
            "Vegetables": "Balanced Diet: Combine with Whole Grains and Protein sources like Lentils.",
            "Milk": "Balanced Diet: Best paired with Whole Grains or Fruits.",
            "Eggs": "Balanced Diet: Add Whole Wheat Toast and Avocado for a healthy breakfast."
        }
        if food_choice in balanced_diets:
            st.write(balanced_diets[food_choice])
