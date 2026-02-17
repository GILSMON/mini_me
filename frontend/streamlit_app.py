import streamlit as st
import requests

st.set_page_config(page_title="Mini Me", page_icon="💬", layout="centered")

try:
    BACKEND_URL = st.secrets["BACKEND_URL"]
except (FileNotFoundError, KeyError):
    BACKEND_URL = "http://localhost:8000"

# ── Dark + WhatsApp green theme ─────────────────────────────────────
st.markdown("""
<style>
/* ─── Reset & base — dark background ─── */
.stApp {
    background-color: #0b141a !important;
}

/* ─── Hide Streamlit chrome ─── */
#MainMenu, footer, header[data-testid="stHeader"],
.stDeployButton, [data-testid="stToolbar"] {
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
    background-color: #1f2c34;
    padding: 12px 16px;
    display: flex;
    align-items: center;
    gap: 12px;
    border-bottom: 1px solid #2a3942;
}
.wa-header-avatar {
    width: 38px;
    height: 38px;
    border-radius: 50%;
    background-color: #25d366;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
    font-weight: 600;
    color: #ffffff;
    flex-shrink: 0;
}
.wa-header-info h3 {
    color: #e9edef;
    margin: 0;
    font-size: 1rem;
    font-weight: 600;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}
.wa-header-info p {
    color: #25d366;
    margin: 1px 0 0 0;
    font-size: 0.75rem;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

/* ─── Chat area ─── */
.stChatMessageContainer,
[data-testid="stChatMessageContainer"] {
    padding-bottom: 80px !important;
}

/* ─── Hide ALL avatars — nuke every possible selector ─── */
.stChatMessage .stAvatar,
.stChatMessage [data-testid*="avatar"],
.stChatMessage [data-testid*="Avatar"],
.stChatMessage [class*="avatar"],
.stChatMessage [class*="Avatar"],
.stChatMessage > div:first-child,
[data-testid="chatAvatarIcon-user"],
[data-testid="chatAvatarIcon-assistant"],
[data-testid="stChatMessageAvatarUser"],
[data-testid="stChatMessageAvatarAssistant"] {
    display: none !important;
    width: 0 !important;
    height: 0 !important;
    min-width: 0 !important;
    max-width: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
    overflow: hidden !important;
    flex: 0 0 0px !important;
    opacity: 0 !important;
}

/* ─── Shared bubble style ─── */
.stChatMessage {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    border: none !important;
    gap: 0 !important;
    max-width: 80% !important;
    padding: 8px 14px !important;
    margin-bottom: 4px !important;
    box-shadow: 0 1px 2px rgba(0,0,0,0.3);
}

/* ─── User bubble — WhatsApp dark green, right-aligned ─── */
.stChatMessage[data-testid="chat-message-user"] {
    background-color: #005c4b !important;
    border-radius: 10px 10px 2px 10px !important;
    margin-left: auto !important;
    margin-right: 8px !important;
}

/* ─── Assistant bubble — dark gray, left-aligned ─── */
.stChatMessage[data-testid="chat-message-assistant"] {
    background-color: #1f2c34 !important;
    border-radius: 10px 10px 10px 2px !important;
    margin-right: auto !important;
    margin-left: 8px !important;
}

/* ─── Text inside bubbles — white, readable ─── */
.stChatMessage[data-testid="chat-message-user"] *,
.stChatMessage[data-testid="chat-message-assistant"] * {
    color: #ffffff !important;
    font-size: 0.95rem !important;
    line-height: 1.55 !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
}

/* ─── Chat input — dark bottom bar ─── */
.stChatFloatingInputContainer,
[data-testid="stChatInput"] {
    background-color: #1f2c34 !important;
    border-top: 1px solid #2a3942 !important;
    padding: 8px 12px !important;
    position: fixed !important;
    bottom: 0 !important;
    left: 0 !important;
    right: 0 !important;
    z-index: 998 !important;
    max-width: 720px !important;
    margin: 0 auto !important;
}
.stChatInput {
    border-radius: 24px !important;
    overflow: visible !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
}
.stChatInput textarea {
    border-radius: 24px !important;
    background-color: #2a3942 !important;
    color: #ffffff !important;
    font-size: 0.95rem !important;
    border: none !important;
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
    padding: 10px 16px !important;
    min-height: 40px !important;
    max-height: 100px !important;
}
.stChatInput textarea:focus {
    border: none !important;
    box-shadow: none !important;
}
.stChatInput textarea::placeholder {
    color: #8696a0 !important;
}
.stChatInput button {
    background-color: #25d366 !important;
    border-radius: 50% !important;
    color: white !important;
    min-width: 40px !important;
    min-height: 40px !important;
    width: 40px !important;
    height: 40px !important;
    flex-shrink: 0 !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    padding: 0 !important;
}

/* ─── Spinner ─── */
.stSpinner > div {
    border-top-color: #25d366 !important;
}

/* ─── Scrollbar (dark) ─── */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background-color: #374045; border-radius: 10px; }
::-webkit-scrollbar-thumb:hover { background-color: #25d366; }

/* ─── Mobile optimization ─── */
@media (max-width: 768px) {
    .block-container {
        max-width: 100% !important;
        padding: 0 !important;
    }
    .stChatFloatingInputContainer,
    [data-testid="stChatInput"] {
        max-width: 100% !important;
        padding: 6px 8px !important;
    }
    .stChatMessage {
        max-width: 88% !important;
        padding: 6px 12px !important;
    }
    .stChatMessage[data-testid="chat-message-user"] *,
    .stChatMessage[data-testid="chat-message-assistant"] * {
        font-size: 0.9rem !important;
    }
    .wa-header {
        padding: 10px 12px;
        position: fixed !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        z-index: 1000 !important;
    }
    .wa-header-avatar {
        width: 34px;
        height: 34px;
        font-size: 16px;
    }
    .wa-header-info h3 {
        font-size: 0.95rem;
    }
    .stChatInput textarea {
        font-size: 16px !important;
        padding: 8px 12px !important;
    }
    /* Pad content so it's not hidden behind fixed header/input */
    .stChatMessageContainer,
    [data-testid="stChatMessageContainer"] {
        padding-top: 60px !important;
        padding-bottom: 70px !important;
    }
}
</style>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<script>
(function() {
    // Mobile keyboard-aware layout using visualViewport API
    if (!window.visualViewport) return;

    function adjustForKeyboard() {
        var vv = window.visualViewport;
        var inputBar = document.querySelector('[data-testid="stChatInput"]')
            || document.querySelector('.stChatFloatingInputContainer');
        if (!inputBar) return;

        var keyboardHeight = window.innerHeight - vv.height;

        if (keyboardHeight > 100) {
            // Keyboard is open — move input above keyboard
            inputBar.style.bottom = keyboardHeight + 'px';
            // Scroll to latest message
            var msgs = document.querySelectorAll('.stChatMessage');
            if (msgs.length > 0) {
                msgs[msgs.length - 1].scrollIntoView({block: 'end', behavior: 'smooth'});
            }
        } else {
            // Keyboard closed — reset
            inputBar.style.bottom = '0px';
        }
    }

    window.visualViewport.addEventListener('resize', adjustForKeyboard);
    window.visualViewport.addEventListener('scroll', adjustForKeyboard);

    // Auto-scroll to bottom on new messages
    var observer = new MutationObserver(function() {
        var msgs = document.querySelectorAll('.stChatMessage');
        if (msgs.length > 0) {
            setTimeout(function() {
                msgs[msgs.length - 1].scrollIntoView({block: 'end', behavior: 'smooth'});
            }, 100);
        }
    });

    // Observe the chat container for new messages
    setTimeout(function() {
        var chatContainer = document.querySelector('[data-testid="stChatMessageContainer"]')
            || document.querySelector('.stChatMessageContainer')
            || document.querySelector('.block-container');
        if (chatContainer) {
            observer.observe(chatContainer, {childList: true, subtree: true});
        }
    }, 1000);
})();
</script>
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

# ── Beta notice (centered in chat area, like WhatsApp date/encryption pill) ──
if not st.session_state.messages:
    st.markdown("""
    <div style="text-align: center; padding: 20px 16px;">
        <span style="background-color: #1a2930; color: #8696a0; font-size: 0.73rem;
                     padding: 6px 14px; border-radius: 8px; letter-spacing: 0.3px;
                     font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;">
            Beta &middot; Each message is treated independently
        </span>
    </div>
    """, unsafe_allow_html=True)

# ── Render chat history ─────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ── Chat input (pinned to bottom by Streamlit) ─────────────────────
if prompt := st.chat_input("Ask me anything... e.g., What's your favourite movie?"):
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
