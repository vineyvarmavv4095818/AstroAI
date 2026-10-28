
import time
from datetime import datetime, date
import streamlit as st
from app import ask_gemini, ask_ollama, ask_knowledge



st.set_page_config(
    page_title="AstroAI | Space Assistant",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(

    """

<style>

@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700&family=DM+Sans:wght@400;500;700&display=swap');


:root {
    --ink: #080d1b;
    --panel: #111a30;
    --panel-2: #1a2745;
    --line: #2b3b60;
    --text: #edf1ff;
    --muted: #a5b2d0;
    --ember: #9585ff;
}


html, body, .stApp, [class*="css"] { font-family: 'DM Sans', sans-serif; }

.stApp {

    background:

        radial-gradient(1100px 480px at 80% -8%, rgba(255,180,84,0.08), transparent 60%),

        radial-gradient(900px 400px at 0% 100%, rgba(80,110,255,0.06), transparent 60%),

        var(--ink);

    color: var(--text);

}

.block-container { max-width: 1480px; padding: 2rem 2.5rem 6rem; }

#MainMenu, footer { visibility: hidden; }


/* Match Streamlit's top header to the app background */
[data-testid="stHeader"] {
    background: var(--ink) !important;
}


/* Keep all page content below the Streamlit toolbar */
[data-testid="stMainBlockContainer"] {
    padding-top: 2.5rem !important;
}

/* Add consistent spacing to the main content */
.block-container {
    padding-top: 2.5rem !important;
}


/* Keep the full application background dark */
.stApp,
[data-testid="stAppViewContainer"],
[data-testid="stMain"] {
    background-color: var(--ink) !important;
}


h1, h2, h3, .display {

    font-family: 'Fraunces', serif !important;

    color: var(--text) !important;

    letter-spacing: -0.01em;

}

p, label, li, span { color: var(--text); }

[data-testid="stCaptionContainer"], .stCaption { color: var(--muted) !important; }

/* ---------- Sidebar ---------- */

[data-testid="stSidebar"] { background: var(--panel); border-right: 1px solid var(--line); }

[data-testid="stSidebar"] .block-container { padding-top: 1.5rem; }


.brand {
    font-family: 'Fraunces', serif;
    font-size: 1.7rem;
    font-weight: 700;
    line-height: 1.1;
    color: #FF8F00!important;
    text-shadow: 0 0 14px rgba(149, 133, 255, 0.22);
}

.brand-sub {
    font-family: 'Fraunces', serif;
    color: #a5b2d0 !important;
    font-size: 0.85rem;
    margin-top: 2px;
}

.brand-sub { color: var(--muted); font-size: 0.85rem; margin-top: 2px; }

.side-label { color: var(--muted); font-size: 0.85rem; margin: 0.3rem 0 0.2rem; }

[data-testid="stSidebar"] [role="radiogroup"] { gap: 0.25rem; }

[data-testid="stSidebar"] [role="radiogroup"] label {

    padding: 0.55rem 0.8rem; border-radius: 8px; border: 1px solid transparent;

    width: 100%; cursor: pointer;

}

[data-testid="stSidebar"] [role="radiogroup"] label:hover { background: var(--panel-2); }

[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {

    background: var(--panel-2); border-color: var(--line); border-left: 3px solid var(--ember);

}

[data-testid="stSidebar"] [role="radiogroup"] label > div:first-child { display: none; }

/* Recent chat buttons in sidebar */

[data-testid="stSidebar"] .stButton > button {

    font-size: 0.88rem; padding: 0.4rem 0.7rem; white-space: nowrap;

    overflow: hidden; text-overflow: ellipsis;

}

/* ---------- Page header ---------- */

.page-head { border-bottom: 1px solid var(--line); padding-bottom: 1.1rem; margin-bottom: 1.6rem; }

.page-head h1 { font-size: 2.4rem; font-weight: 700; margin: 0; padding: 0; }

.page-head p { color: var(--muted); font-size: 1.05rem; margin: 0.4rem 0 0; max-width: 70ch; font-family: 'Fraunces', serif;}

/* ---------- Buttons ---------- */

.stButton > button, .stDownloadButton > button {

    background: var(--panel); color: var(--text); border: 1px solid var(--line);

    border-radius: 10px; padding: 0.6rem 1rem; font-weight: 500; text-align: left;

    transition: border-color .15s ease, background .15s ease;

}

.stButton > button:hover, .stDownloadButton > button:hover {

    background: var(--panel-2); border-color: var(--ember); color: var(--text);

}

.stButton > button:focus-visible { outline: 2px solid var(--ember); outline-offset: 2px; }

.stButton > button[kind="primary"] {

    background: var(--ember); color: #1a1204; border-color: var(--ember);

    font-weight: 700; text-align: center;

}

.stButton > button[kind="primary"]:hover { background: #ffc378; }


/* ---------- Inputs ---------- */
.stTextInput input,
.stTextArea textarea,
[data-testid="stChatInput"] textarea {
    background: #ffffff !important;
    color: #172033 !important;
    -webkit-text-fill-color: #172033 !important;
    caret-color: #5145d9 !important;
    border: 1px solid #cbd3e5 !important;
    border-radius: 10px !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder,
[data-testid="stChatInput"] textarea::placeholder {
    color: #68738b !important;
    -webkit-text-fill-color: #68738b !important;
    opacity: 1 !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus,
[data-testid="stChatInput"] textarea:focus {
    border-color: #9585ff !important;
    box-shadow: 0 0 0 1px #9585ff !important;
}

[data-baseweb="select"] > div {
    background: var(--panel) !important;
    border-color: var(--line) !important;
    border-radius: 10px;
}

/* ---------- Chat ---------- */

[data-testid="stChatMessage"] {

    background: var(--panel); border: 1px solid var(--line);

    border-radius: 12px; padding: 1rem 1.2rem; margin-bottom: 0.7rem;

}

[data-testid="stChatInput"] { border-radius: 14px; }

.msg-meta { color: var(--muted); font-size: 0.8rem; margin-top: 0.4rem; }

/* ---------- Containers ---------- */

[data-testid="stVerticalBlockBorderWrapper"] {

    background: var(--panel); border: 1px solid var(--line); border-radius: 12px;

}

.model-tag {

    display: inline-block; padding: 2px 10px; border: 1px solid var(--line);

    border-radius: 999px; color: var(--muted); font-size: 0.8rem;

}

.model-tag.live { border-color: var(--ember); color: var(--ember); }

/* ---------- Landing hero (empty chat) ---------- */

.hero-big { padding: 2.2rem 0 1.4rem; }

.hero-big h1 { font-size: 3.4rem; line-height: 1.05; font-weight: 700; margin: 0 0 0.8rem; }

.hero-big p { color: var(--muted); font-size: 1.15rem; max-width: 56ch; margin: 0; font-family: 'Fraunces', serif;}

.section-label { color: var(--muted); font-size: 0.9rem; margin: 1.4rem 0 0.5rem; }



@media (prefers-reduced-motion: reduce) { * { transition: none !important; } }




</style>

""",

    unsafe_allow_html=True,

)

# ======================================================================

# DATA

# ======================================================================

TOPICS = {

    "Planets": [

        "Why is Mars red?",

        "Which planet has the most moons?",

        "Could humans ever live on Venus?",

    ],

    "Stars": [

        "How far away is the nearest star?",

        "What is a neutron star?",

        "How does the Sun produce energy?",

    ],

    "Black holes": [

        "What happens inside a black hole?",

        "How do black holes form?",

        "Can light escape a black hole?",

    ],

    "Galaxies": [

        "How big is the Milky Way?",

        "What will happen when Andromeda collides with us?",

        "How many galaxies are there?",

    ],

}



FOLLOW_UPS = [

    "Explain that more simply",

    "Give me a real-world example",

    "What should I learn next?",

]

# ======================================================================

# HELPERS

# ======================================================================

def page_header(title: str, subtitle: str) -> None:

    st.markdown(

        f'<div class="page-head"><h1>{title}</h1><p>{subtitle}</p></div>',

        unsafe_allow_html=True,

    )

def ask_model(model: str, question: str, history=None) -> str:

    fn = ask_gemini if model == "Gemini" else ask_ollama

    try:

        return fn(question, history) if history is not None else fn(question)

    except Exception as e:  # noqa: BLE001

        return f"Could not get a response from {model}. Details: {e}"

def transcript_text() -> str:

    lines = []

    for m in st.session_state.messages:

        who = "You" if m["role"] == "user" else "AstroAI"

        lines.append(f"{who}: {m['content']}\n")

    return "\n".join(lines)

def archive_current_chat() -> None:

    msgs = st.session_state.messages

    if not msgs:

        return

    title = msgs[0]["content"][:40]

    st.session_state.archive.insert(0, {"title": title, "messages": list(msgs)})

    st.session_state.archive = st.session_state.archive[:8]



# ======================================================================

# SESSION STATE

# ======================================================================

st.session_state.setdefault("messages", [])

st.session_state.setdefault("pending", None)

st.session_state.setdefault("compare_result", None)

st.session_state.setdefault("archive", [])

st.session_state.setdefault("topic", "Planets")

# ======================================================================

# SIDEBAR

# ======================================================================

with st.sidebar:

    st.markdown(

        '<div class="brand">🌌 AstroAI</div>'

        '<div class="brand-sub">Your personal space assistant</div>',

        unsafe_allow_html=True,

    )

    st.divider()

    page = st.radio("Navigation", ["Chat", "Compare models", "About"],

                    label_visibility="collapsed")

    st.divider()

    st.markdown('<div class="side-label">Model</div>', unsafe_allow_html=True)

    model = st.selectbox(

        "Model", ["Gemini", "Ollama"], label_visibility="collapsed",

        help="Gemini runs in the cloud. Ollama runs on your computer.",

    )

    st.caption(

        "Cloud model, fast and detailed."

        if model == "Gemini" else "Local model, private and works offline."

    )

    st.divider()

    st.markdown(
        '<div class="side-label">Chat Mode</div>',
        unsafe_allow_html=True,
    )

    chat_mode = st.radio(
        "Choose chat mode",
        ["Normal Chat", "Knowledge Mode"],
        horizontal=False,
        label_visibility="collapsed",
        help=(
            "Normal Chat uses Gemini or Ollama. "
            "Knowledge Mode answers using your space knowledge file."
        ),
    )

    if chat_mode == "Knowledge Mode":
        st.caption("📚 Answers grounded in your space knowledge.")
    else:
        st.caption("✨ Ask general astronomy questions.")

    st.divider()

    if st.button("New chat", icon=":material/add_comment:", use_container_width=True):

        archive_current_chat()

        st.session_state.messages = []

        st.session_state.pending = None

        st.rerun()

    if st.session_state.messages:

        st.download_button(

            "Save conversation", data=transcript_text(),

            file_name=f"astroai-chat-{datetime.now():%Y%m%d-%H%M}.txt",

            icon=":material/download:", use_container_width=True,

        )

    if st.session_state.archive:

        st.divider()

        st.markdown('<div class="side-label">Recent chats</div>', unsafe_allow_html=True)

        for i, chat in enumerate(st.session_state.archive):

            if st.button(chat["title"], key=f"recent_{i}", use_container_width=True):

                archive_current_chat()

                st.session_state.messages = list(chat["messages"])

                st.rerun()

    st.divider()

    st.caption(f"{len(st.session_state.messages)} messages in this chat")

    st.caption("Built with Python and Streamlit")

# ======================================================================

# CHAT PAGE  (conversation + info panel)

# ======================================================================

if page == "Chat":

    main_col = st.container()

    with main_col:

        if not st.session_state.messages:

            st.markdown(

                '<div class="hero-big"><h1>Ask the universe<br>anything.</h1>'

                "<p>Clear, beginner-friendly answers about planets, stars, galaxies "

                "and black holes. Pick a topic to start, or type your own question below.</p></div>",

                unsafe_allow_html=True,

            )

            st.markdown('<div class="section-label">Choose a topic</div>', unsafe_allow_html=True)

            tcols = st.columns(len(TOPICS))

            for col, name in zip(tcols, TOPICS):

                is_active = st.session_state.topic == name

                if col.button(name, key=f"topic_{name}", use_container_width=True,

                              type="primary" if is_active else "secondary"):

                    st.session_state.topic = name

                    st.rerun()

            st.markdown('<div class="section-label">Popular questions</div>', unsafe_allow_html=True)

            for i, q in enumerate(TOPICS[st.session_state.topic]):

                if st.button(q, key=f"start_{i}", use_container_width=True):

                    st.session_state.pending = q

                    st.rerun()

        else:

            st.markdown(f'<span class="model-tag live">● {model}</span>', unsafe_allow_html=True)

            st.write("")

        for m in st.session_state.messages:

            avatar = "🧑‍🚀" if m["role"] == "user" else "🪐"

            with st.chat_message(m["role"], avatar=avatar):

                st.markdown(m["content"])

                if m.get("meta"):

                    st.markdown(f'<div class="msg-meta">{m["meta"]}</div>', unsafe_allow_html=True)

        typed = st.chat_input("Ask anything about space...")

        question = typed or st.session_state.pending

        st.session_state.pending = None

        if question and question.strip():

            history = [{"role": m["role"], "content": m["content"]}

                       for m in st.session_state.messages]

            st.session_state.messages.append({"role": "user", "content": question})

            with st.chat_message("user", avatar="🧑‍🚀"):

                st.markdown(question)

            with st.chat_message("assistant", avatar="🪐"):

                start = time.time()

                with st.spinner(
                    "Searching space knowledge..." 
                    if chat_mode == "Knowledge Mode"
                    else f"{model} is thinking..."
                ):
                    if chat_mode == "Knowledge Mode":
                        answer = ask_knowledge(question)
                    else:
                        answer = ask_model(model, question, history)

                mode_name = "Space Knowledge (RAG)" if chat_mode == "Knowledge Mode" else model
                meta = f"{mode_name} · {time.time() - start:.1f}s"

                st.markdown(answer)

                st.markdown(f'<div class="msg-meta">{meta}</div>', unsafe_allow_html=True)

            st.session_state.messages.append(

                {"role": "assistant", "content": answer, "meta": meta}

            )

        # Follow-up suggestions after the latest answer

        if st.session_state.messages and st.session_state.messages[-1]["role"] == "assistant":

            st.markdown('<div class="section-label">Keep going</div>', unsafe_allow_html=True)

            fcols = st.columns(len(FOLLOW_UPS))

            for i, (col, f) in enumerate(zip(fcols, FOLLOW_UPS)):

                if col.button(f, key=f"fu_{len(st.session_state.messages)}_{i}",

                              use_container_width=True):

                    st.session_state.pending = f

                    st.rerun()

# ======================================================================

# COMPARE PAGE

# ======================================================================

elif page == "Compare models":

    page_header("Compare models", "Ask one question and read both answers side by side.")

    with st.container(border=True):

        in_col, btn_col = st.columns([4, 1], gap="medium", vertical_alignment="bottom")

        with in_col:

            compare_question = st.text_input(

                "Your question", key="compare_question",

                placeholder="Example: Why is Mars red?",

            )

        with btn_col:

            run = st.button("Compare answers", type="primary",

                            icon=":material/compare_arrows:", use_container_width=True)

    if run:

        if not compare_question.strip():

            st.warning("Enter a question first.")

        else:

            results = {}

            for name in ("Gemini", "Ollama"):

                start = time.time()

                with st.spinner(f"{name} is thinking..."):

                    text = ask_model(name, compare_question)

                results[name] = (text, time.time() - start)

            st.session_state.compare_result = {"question": compare_question, "results": results}

    res = st.session_state.compare_result

    if res:

        st.write("")

        st.caption(f"Question: {res['question']}")

        col1, col2 = st.columns(2, gap="large")

        for col, name, kind in ((col1, "Gemini", "Cloud"), (col2, "Ollama", "Local")):

            text, secs = res["results"][name]

            with col:

                with st.container(border=True):

                    st.markdown(f"### {name}")

                    st.markdown(

                        f'<span class="model-tag">{kind}</span> '

                        f'<span class="model-tag">{secs:.1f}s</span>',

                        unsafe_allow_html=True,

                    )

                    st.write("")

                    st.markdown(text)

    else:

        st.info("Results appear here after you compare.")

# ======================================================================

# ABOUT PAGE

# ======================================================================

elif page == "About":

    page_header("About AstroAI",

                "An astronomy assistant that explains space in plain, beginner-friendly language.")

    left, right = st.columns([3, 2], gap="large")

    with left:

        with st.container(border=True):

            st.markdown("### What you can do")

            st.markdown(

                """

- Ask astronomy questions and get simple explanations

- Follow up, since AstroAI remembers the conversation

- Switch between Gemini (cloud) and Ollama (local)

- Compare both models on the same question

- Reopen recent chats and save any conversation as a text file

"""

            )

    with right:

        with st.container(border=True):

            st.markdown("### Built with")

            st.markdown(

                """

- **Python** for the app logic

- **Streamlit** for the interface

- **Google Gemini API** for cloud answers

- **Ollama** for local answers

- **Session state** for chat memory

"""

            )

