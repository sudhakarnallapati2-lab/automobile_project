import streamlit as st
import requests

API_URL = "https://uninlaid-causticly-mitsuko.ngrok-free.dev"
st.set_page_config(page_title="Car Damage System", layout="wide")

if "token" not in st.session_state:
    st.session_state.token = None

# ---------- LOGIN ----------
def login_page():
    st.title("🔐 Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        data = {"username": email, "password": password}
        try:
            response = requests.post(f"{API_URL}/login", data=data)
            if response.status_code == 200:
                token = response.json()["access_token"]
                st.session_state.token = token
                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Invalid email or password")
        except Exception as e:
            st.error(f"❌ Cannot connect to server: {e}")


# ---------- REGISTER ----------
def register_page():
    st.title("🧾 Register New User")
    name = st.text_input("Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        payload = {"name": name, "email": email, "password": password}
        try:
            response = requests.post(f"{API_URL}/register", json=payload)
            if response.status_code == 200:
                st.success("✅ Registration successful! Go to Login.")
            else:
                st.error(f"❌ Error: {response.text}")
        except Exception as e:
            st.error(f"❌ Cannot connect to server: {e}")


# ---------- DASHBOARD ----------
def dashboard():
    st.title("✅ Logged in as User")

    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    try:
        user = requests.get(f"{API_URL}/users/me", headers=headers).json()
        st.subheader("User Profile")
        st.write(user)
    except Exception as e:
        st.error(f"❌ Could not load user data: {e}")

    if st.button("Logout"):
        st.session_state.token = None
        st.rerun()


# ---------- ROUTER ----------
page = st.sidebar.selectbox("Menu", ["Login", "Register", "Dashboard"])

if page == "Login":
    login_page()
elif page == "Register":
    register_page()
elif page == "Dashboard":
    if st.session_state.token:
        dashboard()
    else:
        st.error("⚠ Please login first")
