import streamlit as st
from backend import generate_blog
from pathlib import Path
from datetime import datetime

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="Blog Generator",
    page_icon="✍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------
st.markdown("""
<style>

/* Main background */
.stApp {
    background: linear-gradient(135deg, #0f172a, #111827);
    color: white;
}

/* Remove Streamlit default spacing */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* Title */
.main-title {
    font-size: 3rem;
    font-weight: 800;
    color: white;
    margin-bottom: 0;
}

.gradient-text {
    background: linear-gradient(90deg, #38bdf8, #818cf8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Subtitle */
.subtitle {
    color: #cbd5e1;
    font-size: 1.1rem;
    margin-bottom: 2rem;
}

/* Card */
.custom-card {
    background: rgba(255,255,255,0.05);
    padding: 1.5rem;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
    margin-bottom: 1rem;
}

/* Text area */
textarea {
    background-color: #111827 !important;
    color: white !important;
    border-radius: 15px !important;
    border: 1px solid #334155 !important;
    font-size: 16px !important;
}

/* Buttons */
.stButton > button {
    width: 100%;
    height: 55px;
    border-radius: 14px;
    border: none;
    background: linear-gradient(90deg, #2563eb, #7c3aed);
    color: white;
    font-size: 18px;
    font-weight: 700;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.02);
    background: linear-gradient(90deg, #1d4ed8, #6d28d9);
}

/* Download button */
.stDownloadButton > button {
    width: 100%;
    border-radius: 14px;
    height: 50px;
    font-weight: 700;
}

/* Markdown content */
.blog-content {
    background: rgba(255,255,255,0.04);
    padding: 2rem;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.08);
}

/* Footer */
.footer {
    text-align: center;
    margin-top: 50px;
    color: #94a3b8;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
# ---------------------------------------------------
# PREVIOUS BLOGS
# ---------------------------------------------------

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------
with st.sidebar:

    st.markdown("## ⚡ Blog Generator")

    st.markdown("""
    ### Features
    - Blog Writing
    - Research Powered
    - Markdown Export
    - Technical Blogging
    - LangGraph Workflow
    """)

    st.markdown("---")

    st.markdown("### 👨‍💻 Author")
    st.markdown("## SHUBAIB")

    st.markdown("---")

    st.markdown(
        f"""
        **Today**  
        {datetime.now().strftime("%d %B %Y")}
        """
    )

    # 👇👇 ADD THIS INSIDE SIDEBAR ONLY

  
# ---------------------------------------------------
# LOAD PREVIOUS BLOG
# ---------------------------------------------------

# ---------------------------------------------------
# HERO SECTION
# ---------------------------------------------------
st.markdown("""
<div class="custom-card">

<h1 class="main-title">
<span class="gradient-text">AI Blog Generator</span>
</h1>

<p class="subtitle">
Generate high-quality technical blogs using LangGraph, LLMs, Research Agents, and AI orchestration.
</p>

</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# INPUT SECTION
# ---------------------------------------------------
st.markdown("### 📝 Enter Your Blog Topic")

topic = st.text_area(
    "",
    placeholder="Example: Open Source LLMs vs Proprietary LLMs in 2026",
    height=160
)

# ---------------------------------------------------
# GENERATE BUTTON
# ---------------------------------------------------
if st.button("🚀 Generate Blog"):

    if not topic.strip():
        st.warning("Please enter a blog topic.")
    else:

        with st.spinner("Generating your blog..."):

            try:
                result = generate_blog(topic)

                st.success("✅ Blog generated successfully!")

                # ---------------------------------------------------
                # TITLE CARD
                # ---------------------------------------------------
                st.markdown(f"""
                <div class="custom-card">
                    <h2>{result['title']}</h2>
                    <p>✍️ Author: <b>SHUBAIB</b></p>
                </div>
                """, unsafe_allow_html=True)

                # ---------------------------------------------------
                # BLOG CONTENT
                # ---------------------------------------------------
                st.markdown('<div class="blog-content">', unsafe_allow_html=True)

                st.markdown(result["content"])

                st.markdown('</div>', unsafe_allow_html=True)

                # ---------------------------------------------------
                # INFO ROW
                # ---------------------------------------------------
                col1, col2 = st.columns(2)

                with col1:
                    st.info(f"📁 Saved at: {result['saved_path']}")

                with col2:
                    word_count = len(result["content"].split())
                    st.info(f"📝 Word Count: {word_count}")

                # ---------------------------------------------------
                # DOWNLOAD BUTTON
                # ---------------------------------------------------
                st.download_button(
                    label="⬇ Download Markdown File",
                    data=result["content"],
                    file_name=f"{result['title']}.md",
                    mime="text/markdown"
                )

            except Exception as e:
                st.error(f"❌ Error: {e}")

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("")

st.markdown("---")
st.markdown("### 📚 Previous Blogs")

output_dir = Path("outputs")
output_dir.mkdir(exist_ok=True)

blog_files = sorted(
    output_dir.glob("*.md"),
    key=lambda x: x.stat().st_mtime,
    reverse=True
)

selected_blog = None

if blog_files:

    for file in blog_files:

        blog_name = file.stem.replace("_", " ")

        # short title
        short_name = (
            blog_name[:35] + "..."
            if len(blog_name) > 35
            else blog_name
        )

        if st.button(
            f"📝 {short_name}",
            key=file.name,
            use_container_width=True
        ):
            selected_blog = file.stem

            st.session_state["selected_blog"] = selected_blog

else:
    st.caption("No previous blogs found.")


st.markdown("")

selected_blog = st.session_state.get("selected_blog")

if selected_blog:

    selected_path = output_dir / f"{selected_blog}.md"

    if selected_path.exists():

        previous_content = selected_path.read_text(encoding="utf-8")

        with st.expander("📖 View Previous Blog", expanded=False):

            st.markdown(f"""
            <div class="custom-card">
                <h2>{selected_blog.replace("_", " ").title()}</h2>
                <p>👨‍💻 Author: <b>SHUBAIB</b></p>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(previous_content)

            st.download_button(
                label="⬇ Download Previous Blog",
                data=previous_content,
                file_name=f"{selected_blog}.md",
                mime="text/markdown",
                key="previous_blog_download"
            )


st.markdown("""
<div class="footer">


👨‍💻 Author: <b>SHUBAIB</b>

</div>
""", unsafe_allow_html=True)
