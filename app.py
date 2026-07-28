"""
Streamlit frontend for the "Research Paper -> Story" pipeline.

This runs on YOUR machine (not in Colab/Kaggle). It talks to the model, which
runs in a backend notebook (Ahkeelak.ipynb, on Colab or Kaggle) and is exposed
to the internet via an ngrok tunnel, using plain HTTP requests.

The backend streams newline-delimited JSON. Behavior depends on the chosen language:
- English: one "english" chunk, shown immediately.
- Bilingual: an "english" chunk shown immediately, then a "final" chunk with the
  combined English + Arabic story once translation finishes (English stays visible).
- Arabic: no early chunk — nothing is shown until the "final" chunk with the
  finished Arabic-only story arrives.

Run with:
    pip install streamlit requests
    streamlit run app.py
"""

import json

import requests
import streamlit as st

st.set_page_config(page_title="Ahkeelak", page_icon="📖", layout="wide")

CONNECT_TIMEOUT = 15
READ_TIMEOUT = 900  # seconds; story + translation on a T4 can take several minutes

# ---------------------------------------------------------------------------
# Sidebar: backend connection + generation options
# ---------------------------------------------------------------------------
st.sidebar.header("⚙️ Backend")
backend_url = st.sidebar.text_input(
    "Backend URL (ngrok)",
    placeholder="https://xxxx-xx-xx-xx-xx.ngrok-free.app",
    help="Paste the public URL printed by the last cells of Ahkeelak.ipynb (Colab or Kaggle)",
).rstrip("/")

if st.sidebar.button("Check connection"):
    if not backend_url:
        st.sidebar.error("Enter the backend URL first.")
    else:
        try:
            r = requests.get(f"{backend_url}/health", timeout=CONNECT_TIMEOUT)
            r.raise_for_status()
            info = r.json()
            st.sidebar.success(f"Connected — model: {info.get('model')}, device: {info.get('device')}")
        except Exception as e:
            st.sidebar.error(f"Could not reach backend: {e}")

st.sidebar.divider()
st.sidebar.header("🎨 Story options")

story_style = st.sidebar.selectbox("Style", ["Detective", "Adventure", "Sci-Fi", "Fantasy"])
audience = st.sidebar.selectbox("Audience", ["Children", "High School", "University", "Researchers"])
story_length = st.sidebar.selectbox("Length", ["Short", "Medium", "Long"])
output_language = st.sidebar.selectbox("Language", ["English", "Arabic", "Bilingual"])

# ---------------------------------------------------------------------------
# Main area
# ---------------------------------------------------------------------------
st.title("📖 Ahkeelak")
st.caption(
    "\"I'll tell you [a story]\" — upload a research paper PDF and the model "
    "rewrites it as a story, in English and/or Arabic."
)

uploaded_pdf = st.file_uploader("Research paper (PDF)", type=["pdf"])
generate = st.button("✨ Generate story", type="primary", use_container_width=True)

story_placeholder = st.empty()
status_placeholder = st.empty()

if "result" not in st.session_state:
    st.session_state["result"] = None

if generate:
    if not backend_url:
        st.error("Enter the backend URL in the sidebar first.")
    elif not uploaded_pdf:
        st.error("Upload a PDF first.")
    else:
        files = {"file": (uploaded_pdf.name, uploaded_pdf.getvalue(), "application/pdf")}
        data = {
            "story_style": story_style,
            "audience": audience,
            "story_length": story_length,
            "output_language": output_language,
        }
        result = {}
        initial_label = (
            "Reading the paper, writing the story, then translating into Arabic…"
            if output_language == "Arabic"
            else "Reading the paper and writing the story…"
        )
        try:
            with status_placeholder.status(initial_label, expanded=False) as status:
                with requests.post(
                    f"{backend_url}/generate-story",
                    files=files,
                    data=data,
                    stream=True,
                    timeout=(CONNECT_TIMEOUT, READ_TIMEOUT),
                ) as resp:
                    resp.raise_for_status()
                    for line in resp.iter_lines(decode_unicode=True):
                        if not line:
                            continue
                        chunk = json.loads(line)
                        stage = chunk.get("stage")

                        if stage == "error":
                            st.error(f"Generation failed: {chunk.get('detail')}")
                            result = {}
                            break

                        if stage == "english":
                            result.update(chunk)
                            if output_language == "Arabic":
                                # Arabic-only: never show the English draft, just keep
                                # the status updated while translation runs.
                                status.update(label="Story written — translating into Arabic now…")
                            elif output_language == "Bilingual":
                                story_placeholder.markdown(chunk["english_story"])
                                status.update(label="English ready — translating into Arabic now…")
                            else:  # English
                                story_placeholder.markdown(chunk["english_story"])
                                status.update(label="Done.", state="complete")

                        elif stage == "final":
                            result.update(chunk)
                            story_placeholder.markdown(chunk["final_story"])
                            status.update(label="Done.", state="complete")

        except requests.exceptions.Timeout:
            st.error("The request timed out. Generation may still be running on Colab — try again shortly.")
        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")

        if result:
            st.session_state["result"] = result

# ---------------------------------------------------------------------------
# Persisted result (survives reruns e.g. from widget interaction) + extras
# ---------------------------------------------------------------------------
result = st.session_state["result"]
if result and not generate:
    story_placeholder.markdown(result.get("final_story") or result.get("english_story", ""))

if result:
    st.divider()
    final_text = result.get("final_story") or result.get("english_story", "")
    st.download_button("Download story (.md)", data=final_text, file_name="story.md", mime="text/markdown")

    analysis = result.get("analysis", {})
    with st.expander("🔬 Extracted analysis"):
        st.write(f"**Title:** {analysis.get('title', 'Not specified')}")
        st.write(f"**Main contribution:** {analysis.get('main_contribution', 'Not specified')}")
        st.write(f"**Research problem:** {analysis.get('research_problem', 'Not specified')}")
        st.write(f"**Motivation:** {analysis.get('motivation', 'Not specified')}")
        st.write(f"**Methodology:** {analysis.get('methodology', 'Not specified')}")
        if analysis.get("datasets"):
            st.write("**Datasets:** " + ", ".join(analysis["datasets"]))
        if analysis.get("key_findings"):
            st.write("**Key findings:**")
            for f in analysis["key_findings"]:
                st.write(f"- {f}")
        st.caption(f"Source pages used: {', '.join(map(str, result.get('citations', [])))}")
