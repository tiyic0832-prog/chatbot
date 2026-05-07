# import streamlit as st
# import anthropic
# from dotenv import load_dotenv
# import os
# import json
# import uuid
# from datetime import datetime

# load_dotenv()

# try:
#     client = anthropic.Anthropic(
#         api_key=os.getenv("ANTHROPIC_API_KEY"),
#         base_url=os.getenv("ANTHROPIC_BASE_URL")
#     )
# except Exception as e:
#     st.error("❌ API Key missing or wrong. Check your .env file.")
#     st.stop()

# MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")
# SESSIONS_FILE = "sessions.json"

# SYSTEM_PROMPT = """You are Claude, an AI assistant made by Anthropic. You are helpful, harmless, and honest.
# Answer questions thoroughly and accurately.
# Use markdown formatting, bullet points,  and structure when it helps clarity.
# Be conversational but professional."""

# def load_sessions():
#     if os.path.exists(SESSIONS_FILE):
#         with open(SESSIONS_FILE, "r") as f:
#             return json.load(f)
#     return {}

# def save_sessions(sessions):
#     with open(SESSIONS_FILE, "w") as f:
#         json.dump(sessions, f)

# def new_session_id():
#     return str(uuid.uuid4())[:8]

# def truncate(text, n=26):
#     return text if len(text) <= n else text[:n] + "…"

# if "sessions" not in st.session_state:
#     st.session_state.sessions = load_sessions()
# if "active_id" not in st.session_state:
#     st.session_state.active_id = None
# if "rename_id" not in st.session_state:
#     st.session_state.rename_id = None
# if "menu_open" not in st.session_state:
#     st.session_state.menu_open = None

# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');

# html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }

# [data-testid="stSidebar"] {
#     background-color: #f9f9f9 !important;
#     border-right: 1px solid #e8e8e8 !important;
# }

# [data-testid="stSidebar"] button {
#     all: unset !important;
#     display: block !important;
#     width: 100% !important;
#     padding: 6px 10px !important;
#     border-radius: 7px !important;
#     font-size: 13px !important;
#     font-family: 'Inter', sans-serif !important;
#     color: #374151 !important;
#     cursor: pointer !important;
#     transition: background 0.1s !important;
#     text-align: left !important;
#     box-sizing: border-box !important;
#     overflow: hidden !important;
#     text-overflow: ellipsis !important;
#     white-space: nowrap !important;
#     line-height: 1.4 !important;
# }
# [data-testid="stSidebar"] button:hover { background: #efefef !important; }

# .new-chat button {
#     background: #5b21b6 !important;
#     color: white !important;
#     font-weight: 600 !important;
#     font-size: 13.5px !important;
#     padding: 9px 14px !important;
#     border-radius: 9px !important;
#     text-align: center !important;
#     width: 100% !important;
# }
# .new-chat button:hover { background: #4c1d95 !important; color: white !important; }

# .row-active button {
#     background: #ede9fe !important;
#     color: #5b21b6 !important;
#     font-weight: 500 !important;
# }

# .dot-btn button {
#     padding: 2px 7px !important;
#     font-size: 15px !important;
#     color: #bbb !important;
#     width: auto !important;
#     border-radius: 5px !important;
#     letter-spacing: 1px !important;
# }
# .dot-btn button:hover { background: #e0e0e0 !important; color: #333 !important; }

# .menu-item button {
#     padding: 7px 14px !important;
#     font-size: 13px !important;
#     color: #333 !important;
#     border-radius: 6px !important;
#     width: 100% !important;
# }
# .menu-item button:hover { background: #f0f0f0 !important; }
# .menu-delete button { color: #dc2626 !important; }
# .menu-delete button:hover { background: #fee2e2 !important; }

# .menu-card {
#     background: white;
#     border: 1px solid #e5e5e5;
#     border-radius: 10px;
#     box-shadow: 0 4px 16px rgba(0,0,0,0.10);
#     padding: 5px;
#     margin-top: 2px;
#     margin-left: 8px;
# }

# [data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div {
#     margin-bottom: 0px !important;
#     padding-bottom: 0px !important;
# }
# [data-testid="stSidebar"] [data-testid="stHorizontalBlock"] {
#     gap: 4px !important;
#     margin: 1px 0 !important;
# }

# .main .block-container { max-width: 720px !important; padding-top: 1.5rem !important; }
# h1 { font-size: 22px !important; font-weight: 600 !important; }
# </style>
# """, unsafe_allow_html=True)

# # ── Sidebar ───────────────────────────────────────────────────────────────────
# with st.sidebar:
#     st.markdown("**💬 Sessions**")
#     st.markdown("<br>", unsafe_allow_html=True)

#     st.markdown('<div class="new-chat">', unsafe_allow_html=True)
#     if st.button("＋  New Chat", key="new_chat"):
#         sid = new_session_id()
#         st.session_state.sessions[sid] = {
#             "name": None,
#             "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
#             "messages": []
#         }
#         st.session_state.active_id = sid
#         st.session_state.rename_id = None
#         st.session_state.menu_open = None
#         st.rerun()
#     st.markdown('</div>', unsafe_allow_html=True)

#     st.markdown("---")

#     for sid, session in sorted(st.session_state.sessions.items(), key=lambda x: x[1].get("created", ""), reverse=True):
#         is_active = sid == st.session_state.active_id
#         display_name = session.get("name") or session.get("created", "New Chat")
#         menu_open = st.session_state.menu_open == sid

#         if st.session_state.rename_id == sid:
#             new_name = st.text_input("", value=display_name, key=f"rename_{sid}", label_visibility="collapsed")
#             c1, c2 = st.columns(2)
#             with c1:
#                 if st.button("✅ Save", key=f"save_{sid}", use_container_width=True):
#                     st.session_state.sessions[sid]["name"] = new_name
#                     st.session_state.rename_id = None
#                     save_sessions(st.session_state.sessions)
#                     st.rerun()
#             with c2:
#                 if st.button("Cancel", key=f"cancel_{sid}", use_container_width=True):
#                     st.session_state.rename_id = None
#                     st.rerun()
#         else:
#             col_name, col_dot = st.columns([5, 1])

#             with col_name:
#                 if is_active:
#                     st.markdown('<div class="row-active">', unsafe_allow_html=True)
#                 if st.button(truncate(display_name), key=f"open_{sid}", use_container_width=True):
#                     st.session_state.active_id = sid
#                     st.session_state.menu_open = None
#                     st.rerun()
#                 if is_active:
#                     st.markdown('</div>', unsafe_allow_html=True)

#             with col_dot:
#                 st.markdown('<div class="dot-btn">', unsafe_allow_html=True)
#                 if st.button("···", key=f"dot_{sid}"):
#                     st.session_state.menu_open = None if menu_open else sid
#                     st.rerun()
#                 st.markdown('</div>', unsafe_allow_html=True)

#             if menu_open:
#                 st.markdown('<div class="menu-card">', unsafe_allow_html=True)
#                 st.markdown('<div class="menu-item">', unsafe_allow_html=True)
#                 if st.button("✏️  Rename", key=f"ren_{sid}", use_container_width=True):
#                     st.session_state.rename_id = sid
#                     st.session_state.menu_open = None
#                     st.rerun()
#                 st.markdown('</div>', unsafe_allow_html=True)
#                 st.markdown('<div class="menu-item menu-delete">', unsafe_allow_html=True)
#                 if st.button("🗑  Delete", key=f"del_{sid}", use_container_width=True):
#                     del st.session_state.sessions[sid]
#                     if st.session_state.active_id == sid:
#                         st.session_state.active_id = None
#                     st.session_state.menu_open = None
#                     save_sessions(st.session_state.sessions)
#                     st.rerun()
#                 st.markdown('</div>', unsafe_allow_html=True)
#                 st.markdown('</div>', unsafe_allow_html=True)

# # ── Main Chat ─────────────────────────────────────────────────────────────────
# # ── Auto New Chat ─────────────────────────────────────────────────────────────
# if st.session_state.active_id is None:
#     sid = new_session_id()
#     st.session_state.sessions[sid] = {
#         "name": None,
#         "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
#         "messages": []
#     }
#     st.session_state.active_id = sid
#     st.rerun()

# # ── Main Chat ─────────────────────────────────────────────────────────────────
# st.title("Nexus AI")
# active_id = st.session_state.active_id
# display_name = st.session_state.sessions[active_id].get("name") or st.session_state.sessions[active_id].get("created", "New Chat")
# st.caption(f"{display_name}")

# for msg in st.session_state.sessions[active_id]["messages"]:
#     with st.chat_message(msg["role"]):
#         st.write(msg["content"])

# # ── Input ─────────────────────────────────────────────────────────────────────
# user_input = st.chat_input("Ask anything...")

# if user_input:
#     if not st.session_state.sessions[active_id].get("name") and len(st.session_state.sessions[active_id]["messages"]) == 0:
#         st.session_state.sessions[active_id]["name"] = truncate(user_input, 35)
#         save_sessions(st.session_state.sessions)

#     st.session_state.sessions[active_id]["messages"].append({"role": "user", "content": user_input})
#     save_sessions(st.session_state.sessions)

#     with st.chat_message("user"):
#         st.write(user_input)

#     with st.chat_message("assistant"):
#         with st.spinner("Thinking..."):
#             try:
#                 response = client.messages.create(
#                     model=MODEL,
#                     max_tokens=4096,
#                     system=SYSTEM_PROMPT,
#                     messages=st.session_state.sessions[active_id]["messages"]
#                 )
#                 answer = response.content[0].text
#                 st.write(answer)

#                 st.session_state.sessions[active_id]["messages"].append({"role": "assistant", "content": answer})
#                 save_sessions(st.session_state.sessions)

#             except anthropic.AuthenticationError:
#                 st.error("❌ Invalid API Key.")
#             except anthropic.RateLimitError:
#                 st.error("⚠️ Rate limit hit. Wait and try again.")
#             except anthropic.APIConnectionError:
#                 st.error("🌐 Connection error. Check internet.")
#             except Exception as e:
#                 st.error(f"❌ Error: {str(e)}")



import streamlit as st
import anthropic
import os
import uuid
from datetime import datetime
from supabase import create_client

# ── Clients ───────────────────────────────────────────────────────────────────
try:
    client = anthropic.Anthropic(
        api_key=st.secrets["ANTHROPIC_API_KEY"],
        base_url=st.secrets["ANTHROPIC_BASE_URL"]
    )
except Exception as e:
    st.error("❌ Anthropic API Key missing. Check your secrets.")
    st.stop()

try:
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
except Exception as e:
    st.error("❌ Supabase connection failed. Check your secrets.")
    st.stop()

MODEL = st.secrets["ANTHROPIC_MODEL"]

SYSTEM_PROMPT = """You are Claude, an AI assistant made by Anthropic. You are helpful, harmless, and honest.
Answer questions thoroughly and accurately.
Use markdown formatting, bullet points, and structure when it helps clarity.
Be conversational but professional."""

# ── Supabase helpers ──────────────────────────────────────────────────────────
def load_sessions():
    try:
        res = supabase.table("sessions").select("*").execute()
        return {row["id"]: row["data"] for row in res.data}
    except:
        return {}

def save_session(sid, data):
    try:
        supabase.table("sessions").upsert({"id": sid, "data": data}).execute()
    except Exception as e:
        st.warning(f"⚠️ Could not save session: {e}")

def delete_session(sid):
    try:
        supabase.table("sessions").delete().eq("id", sid).execute()
    except Exception as e:
        st.warning(f"⚠️ Could not delete session: {e}")

# ── Helpers ───────────────────────────────────────────────────────────────────
def new_session_id():
    return str(uuid.uuid4())[:8]

def truncate(text, n=26):
    return text if len(text) <= n else text[:n] + "…"

# ── Session State Init ────────────────────────────────────────────────────────
if "sessions" not in st.session_state:
    st.session_state.sessions = load_sessions()
if "active_id" not in st.session_state:
    st.session_state.active_id = None
if "rename_id" not in st.session_state:
    st.session_state.rename_id = None
if "menu_open" not in st.session_state:
    st.session_state.menu_open = None

# ── Styles ────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
html, body, [class*="css"] { font-family: 'Inter', sans-serif !important; }
[data-testid="stSidebar"] {
    background-color: #f9f9f9 !important;
    border-right: 1px solid #e8e8e8 !important;
}
[data-testid="stSidebar"] button {
    all: unset !important;
    display: block !important;
    width: 100% !important;
    padding: 6px 10px !important;
    border-radius: 7px !important;
    font-size: 13px !important;
    font-family: 'Inter', sans-serif !important;
    color: #374151 !important;
    cursor: pointer !important;
    transition: background 0.1s !important;
    text-align: left !important;
    box-sizing: border-box !important;
    overflow: hidden !important;
    text-overflow: ellipsis !important;
    white-space: nowrap !important;
    line-height: 1.4 !important;
}
[data-testid="stSidebar"] button:hover { background: #efefef !important; }
.new-chat button {
    background: #5b21b6 !important;
    color: white !important;
    font-weight: 600 !important;
    font-size: 13.5px !important;
    padding: 9px 14px !important;
    border-radius: 9px !important;
    text-align: center !important;
    width: 100% !important;
}
.new-chat button:hover { background: #4c1d95 !important; color: white !important; }
.row-active button { background: #ede9fe !important; color: #5b21b6 !important; font-weight: 500 !important; }
.dot-btn button {
    padding: 2px 7px !important;
    font-size: 15px !important;
    color: #bbb !important;
    width: auto !important;
    border-radius: 5px !important;
    letter-spacing: 1px !important;
}
.dot-btn button:hover { background: #e0e0e0 !important; color: #333 !important; }
.menu-item button { padding: 7px 14px !important; font-size: 13px !important; color: #333 !important; border-radius: 6px !important; width: 100% !important; }
.menu-item button:hover { background: #f0f0f0 !important; }
.menu-delete button { color: #dc2626 !important; }
.menu-delete button:hover { background: #fee2e2 !important; }
.menu-card { background: white; border: 1px solid #e5e5e5; border-radius: 10px; box-shadow: 0 4px 16px rgba(0,0,0,0.10); padding: 5px; margin-top: 2px; margin-left: 8px; }
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] > div { margin-bottom: 0px !important; padding-bottom: 0px !important; }
[data-testid="stSidebar"] [data-testid="stHorizontalBlock"] { gap: 4px !important; margin: 1px 0 !important; }
.main .block-container { max-width: 720px !important; padding-top: 1.5rem !important; }
h1 { font-size: 22px !important; font-weight: 600 !important; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("**💬 Sessions**")
    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown('<div class="new-chat">', unsafe_allow_html=True)
    if st.button("＋  New Chat", key="new_chat"):
        sid = new_session_id()
        new_data = {
            "name": None,
            "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "messages": []
        }
        st.session_state.sessions[sid] = new_data  # ✅ memory mein rakho
        st.session_state.active_id = sid
        st.session_state.rename_id = None
        st.session_state.menu_open = None
        st.rerun()    
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown("---")

    for sid, session in sorted(st.session_state.sessions.items(), key=lambda x: x[1].get("created", ""), reverse=True):
        is_active = sid == st.session_state.active_id
        display_name = session.get("name") or session.get("created", "New Chat")
        menu_open = st.session_state.menu_open == sid

        if st.session_state.rename_id == sid:
            new_name = st.text_input("", value=display_name, key=f"rename_{sid}", label_visibility="collapsed")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("✅ Save", key=f"save_{sid}", use_container_width=True):
                    st.session_state.sessions[sid]["name"] = new_name
                    st.session_state.rename_id = None
                    save_session(sid, st.session_state.sessions[sid])
                    st.rerun()
            with c2:
                if st.button("Cancel", key=f"cancel_{sid}", use_container_width=True):
                    st.session_state.rename_id = None
                    st.rerun()
        else:
            col_name, col_dot = st.columns([5, 1])
            with col_name:
                if is_active:
                    st.markdown('<div class="row-active">', unsafe_allow_html=True)
                if st.button(truncate(display_name), key=f"open_{sid}", use_container_width=True):
                    st.session_state.active_id = sid
                    st.session_state.menu_open = None
                    st.rerun()
                if is_active:
                    st.markdown('</div>', unsafe_allow_html=True)
            with col_dot:
                st.markdown('<div class="dot-btn">', unsafe_allow_html=True)
                if st.button("···", key=f"dot_{sid}"):
                    st.session_state.menu_open = None if menu_open else sid
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

            if menu_open:
                st.markdown('<div class="menu-card">', unsafe_allow_html=True)
                st.markdown('<div class="menu-item">', unsafe_allow_html=True)
                if st.button("✏️  Rename", key=f"ren_{sid}", use_container_width=True):
                    st.session_state.rename_id = sid
                    st.session_state.menu_open = None
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('<div class="menu-item menu-delete">', unsafe_allow_html=True)
                if st.button("🗑  Delete", key=f"del_{sid}", use_container_width=True):
                    del st.session_state.sessions[sid]
                    delete_session(sid)
                    if st.session_state.active_id == sid:
                        st.session_state.active_id = None
                    st.session_state.menu_open = None
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

# ── Auto New Chat ─────────────────────────────────────────────────────────────
if st.session_state.active_id is None:
    sid = new_session_id()
    new_data = {
        "name": None,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "messages": []
    }
    st.session_state.sessions[sid] = new_data
    st.session_state.active_id = sid
    st.rerun()

# ── Main Chat ─────────────────────────────────────────────────────────────────
st.title("Nexus AI")
active_id = st.session_state.active_id
display_name = st.session_state.sessions[active_id].get("name") or st.session_state.sessions[active_id].get("created", "New Chat")
st.caption(f"{display_name}")

for msg in st.session_state.sessions[active_id]["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# ── Input ─────────────────────────────────────────────────────────────────────
user_input = st.chat_input("Ask anything...")

if user_input:
    if not st.session_state.sessions[active_id].get("name") and len(st.session_state.sessions[active_id]["messages"]) == 0:
        st.session_state.sessions[active_id]["name"] = truncate(user_input, 35)

    st.session_state.sessions[active_id]["messages"].append({"role": "user", "content": user_input})
    save_session(active_id, st.session_state.sessions[active_id])

    with st.chat_message("user"):
        st.write(user_input)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = client.messages.create(
                    model=MODEL,
                    max_tokens=4096,
                    system=SYSTEM_PROMPT,
                    messages=st.session_state.sessions[active_id]["messages"]
                )
                answer = response.content[0].text
                st.write(answer)
                st.session_state.sessions[active_id]["messages"].append({"role": "assistant", "content": answer})
                save_session(active_id, st.session_state.sessions[active_id])

            except anthropic.AuthenticationError:
                st.error("❌ Invalid API Key.")
            except anthropic.RateLimitError:
                st.error("⚠️ Rate limit hit. Wait and try again.")
            except anthropic.APIConnectionError:
                st.error("🌐 Connection error. Check internet.")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")