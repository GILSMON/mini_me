import streamlit as st
import requests

st.set_page_config(page_title="Mini Me", page_icon="💬", layout="centered")

try:
    BACKEND_URL = st.secrets["BACKEND_URL"]
except (FileNotFoundError, KeyError):
    BACKEND_URL = "http://localhost:8000"

# ── WhatsApp-style theme ────────────────────────────────────────────
st.markdown("""
<style>
/* ─── Reset & base ─── */
.stApp {
    background-color: #efeae2;
    background-image: url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='none' fill-rule='evenodd'%3E%3Cg fill='%23d4ccb9' fill-opacity='0.3'%3E%3Cpath d='M36 34v-4h-2v4h-4v2h4v4h2v-4h4v-2h-4zm0-30V0h-2v4h-4v2h4v4h2V6h4V4h-4zM6 34v-4H4v4H0v2h4v4h2v-4h4v-2H6zM6 4V0H4v4H0v2h4v4h2V6h4V4H6z'/%3E%3C/g%3E%3C/g%3E%3C/svg%3E");
}

/* ─── Hide Streamlit chrome ─── */
#MainMenu, footer, header[data-testid="stHeader"] {
    display: none !important;
}
.stDeployButton {
    display: none !important;
}

/* ─── Main container ─── */
.block-container {
    background-color: transparent !important;
    padding: 0 !important;
    margin: 0 auto !important;
    max-width: 720px !important;
    box-shadow: none !important;
}

/* ─── Sticky top header bar ─── */
.wa-header {
    position: sticky;
    top: 0;
    z-index: 999;
    background-color: #075e54;
    padding: 14px 20px;
    display: flex;
    align-items: center;
    gap: 12px;
    box-shadow: 0 2px 6px rgba(0,0,0,0.15);
}
.wa-header-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background-color: #25d366;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
}
.wa-header-info h3 {
    color: #ffffff;
    margin: 0;
    font-size: 1.05rem;
    font-weight: 600;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}
.wa-header-info p {
    color: #a8d8b0;
    margin: 1px 0 0 0;
    font-size: 0.78rem;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

/* ─── Chat area ─── */
.stChatMessageContainer,
[data-testid="stChatMessageContainer"] {
    padding-bottom: 80px !important;
}

/* ─── Hide ALL avatars (robot icon, user icon) ─── */
.stChatMessage .stAvatar,
[data-testid="stChatMessageAvatarUser"],
[data-testid="stChatMessageAvatarAssistant"],
.stChatMessage img,
.stChatMessage svg {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
}

/* ─── Shared bubble style ─── */
.stChatMessage {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    border: none !important;
    gap: 0 !important;
    max-width: 80% !important;
    padding: 8px 14px !important;
    margin-bottom: 4px !important;
    box-shadow: 0 1px 1px rgba(0,0,0,0.08);
}

/* ─── User bubble — WhatsApp light green, right-aligned ─── */
.stChatMessage[data-testid="chat-message-user"] {
    background-color: #d9fdd3 !important;
    border-radius: 10px 10px 2px 10px !important;
    margin-left: auto !important;
    margin-right: 8px !important;
}

/* ─── Assistant bubble — white, left-aligned ─── */
.stChatMessage[data-testid="chat-message-assistant"] {
    background-color: #ffffff !important;
    border-radius: 10px 10px 10px 2px !important;
    margin-right: auto !important;
    margin-left: 8px !important;
}

/* ─── Text inside bubbles — dark, readable ─── */
.stChatMessage[data-testid="chat-message-user"] *,
.stChatMessage[data-testid="chat-message-assistant"] * {
    color: #111b21 !important;
    font-size: 0.95rem !important;
    line-height: 1.5 !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
}

/* ─── Chat input — fixed at bottom ─── */
.stChatFloatingInputContainer,
[data-testid="stChatInput"] {
    background-color: #f0f2f5 !important;
    border-top: none !important;
    padding: 8px 12px !important;
}
.stChatInput {
    border-radius: 24px !important;
    overflow: hidden;
}
.stChatInput textarea {
    border-radius: 24px !important;
    background-color: #ffffff !important;
    color: #111b21 !important;
    font-size: 0.95rem !important;
    border: 1px solid #d1d7db !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    padding: 10px 16px !important;
}
.stChatInput textarea:focus {
    border-color: #25d366 !important;
    box-shadow: none !important;
}
.stChatInput textarea::placeholder {
    color: #8696a0 !important;
}
.stChatInput button {
    background-color: #25d366 !important;
    border-radius: 50% !important;
    color: white !important;
}

/* ─── Spinner (typing indicator) ─── */
.stSpinner > div {
    border-top-color: #25d366 !important;
}

/* ─── Scrollbar ─── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background-color: #b8b8b8; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background-color: #25d366; }
</style>
""", unsafe_allow_html=True)

# ── Sticky header ───────────────────────────────────────────────────
st.markdown("""
<div class="wa-header">
    <div class="wa-header-avatar">G</div>
    <div class="wa-header-info">
        <h3>Mini Me</h3>
        <p>online</p>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Session state ───────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ── Render chat history ─────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Chat input (pinned to bottom by Streamlit) ─────────────────────
if prompt := st.chat_input("Type a message"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner(""):
            try:
                resp = requests.post(
                    f"{BACKEND_URL}/api/chat",
                    json={"message": prompt},
                    timeout=30,
                )
                resp.raise_for_status()
                answer = resp.json()["answer"]
            except requests.exceptions.ConnectionError:
                answer = "Backend is not reachable. Please try again later."
            except requests.exceptions.RequestException as e:
                answer = f"Something went wrong: {e}"

        st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})
