import streamlit as st
import requests
import json
import os
from datetime import datetime
from dotenv import load_dotenv
import PyPDF2
from io import BytesIO
import re
from anthropic import Anthropic

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="ArXiv Paper Extractor",
    page_icon="📄",
    layout="wide"
)

# Title and description
st.title("📄 ArXiv Paper Extractor")
st.markdown("""
Extract structured insights from academic research papers using AI.
Upload a PDF or provide an arXiv link to get started.
""")

def extract_arxiv_id(url):
    """Extract arXiv ID from URL"""
    patterns = [
        r'arxiv.org/abs/(\d+\.\d+)',
        r'arxiv.org/pdf/(\d+\.\d+)',
        r'^(\d+\.\d+)$'
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def download_arxiv_pdf(arxiv_id):
    """Download PDF from arXiv"""
    pdf_url = f"https://arxiv.org/pdf/{arxiv_id}.pdf"

    try:
        response = requests.get(pdf_url, timeout=30)
        response.raise_for_status()
        return BytesIO(response.content)
    except Exception as e:
        st.error(f"Error downloading PDF: {str(e)}")
        return None

def extract_text_from_pdf(pdf_file):
    """Extract text from PDF file"""
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""

        # Extract text from all pages
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"

        return text
    except Exception as e:
        st.error(f"Error extracting text from PDF: {str(e)}")
        return None

def analyze_paper_with_ai(paper_text, api_key):
    """Analyze paper using Anthropic Claude API"""

    prompt = f"""You are an expert academic research analyst. Analyze the following research paper and extract key information in a structured format.

Research Paper Text:
{paper_text[:50000]}  # Limit to avoid token limits

Please provide a comprehensive analysis with the following sections:

1. Background of the study: Summarize the motivation behind the research, its relevance, and the problem it aims to address.
2. Research objectives and hypothesis: Clearly outline the main goal of the study and the hypothesis the authors are testing.
3. Methodology: Describe how the authors conducted their research, including experimental design, datasets, and evaluation methods.
4. Results and findings: Summarize the key outcomes of the study, highlighting improvements or novel discoveries.
5. Discussion and interpretation: Explain the broader implications of the findings and how they compare to existing approaches.
6. Contributions to the field: Highlight the unique contributions of the study and its significance.
7. Achievements and significance: Conclude with the practical impact and potential real-world applications of the research.

Format your response as a JSON object with the following structure:
{{
    "background": "...",
    "objectives_and_hypothesis": "...",
    "methodology": "...",
    "results_and_findings": "...",
    "discussion_and_interpretation": "...",
    "contributions": "...",
    "achievements_and_significance": "..."
}}

Ensure the output is concise, well-structured, and preserves core technical details."""

    try:
        client = Anthropic(api_key=api_key)

        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=4096,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )

        response_text = message.content[0].text

        # Try to extract JSON from response
        try:
            # Look for JSON in the response
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                result = json.loads(json_match.group())
            else:
                # If no JSON found, structure it manually
                result = {"raw_analysis": response_text}
        except json.JSONDecodeError:
            result = {"raw_analysis": response_text}

        return result

    except Exception as e:
        st.error(f"Error analyzing paper: {str(e)}")
        return None

def display_analysis(analysis):
    """Display analysis results in structured format"""

    sections = [
        ("📚 Background of the Study", "background"),
        ("🎯 Research Objectives and Hypothesis", "objectives_and_hypothesis"),
        ("🔬 Methodology", "methodology"),
        ("📊 Results and Findings", "results_and_findings"),
        ("💡 Discussion and Interpretation", "discussion_and_interpretation"),
        ("✨ Contributions to the Field", "contributions"),
        ("🏆 Achievements and Significance", "achievements_and_significance")
    ]

    for title, key in sections:
        st.subheader(title)
        if key in analysis:
            st.write(analysis[key])
        else:
            st.write("_Not available_")
        st.divider()

# Sidebar for API configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    api_key = st.text_input(
        "Anthropic API Key",
        type="password",
        value=os.getenv("ANTHROPIC_API_KEY", ""),
        help="Enter your Anthropic API key"
    )

    st.divider()
    st.markdown("""
    ### How to use:
    1. Enter your API key
    2. Choose input method:
       - ArXiv URL
       - Upload PDF
    3. Click 'Extract Insights'
    4. Download results as JSON
    """)

# Main content area
tab1, tab2 = st.tabs(["ArXiv URL", "Upload PDF"])

pdf_file = None
source_info = ""

with tab1:
    st.subheader("Extract from ArXiv")
    arxiv_input = st.text_input(
        "Enter ArXiv URL or ID",
        placeholder="https://arxiv.org/abs/2301.00001 or 2301.00001"
    )

    if st.button("Download and Extract", key="arxiv_btn"):
        if not arxiv_input:
            st.warning("Please enter an ArXiv URL or ID")
        else:
            arxiv_id = extract_arxiv_id(arxiv_input)
            if arxiv_id:
                st.info(f"Downloading paper: {arxiv_id}")
                pdf_file = download_arxiv_pdf(arxiv_id)
                source_info = f"ArXiv ID: {arxiv_id}"

                if pdf_file:
                    st.session_state['pdf_file'] = pdf_file
                    st.session_state['source_info'] = source_info
                    st.success("✅ PDF downloaded successfully!")
            else:
                st.error("Invalid ArXiv URL or ID")

with tab2:
    st.subheader("Upload PDF File")
    uploaded_file = st.file_uploader(
        "Choose a PDF file",
        type=['pdf']
    )

    if uploaded_file is not None:
        st.session_state['pdf_file'] = uploaded_file
        st.session_state['source_info'] = f"Uploaded: {uploaded_file.name}"
        st.success("✅ PDF uploaded successfully!")

# Extract insights button
st.divider()

if 'pdf_file' in st.session_state and st.session_state['pdf_file'] is not None:
    st.info(f"📄 {st.session_state['source_info']}")

    if st.button("🚀 Extract Insights", type="primary", use_container_width=True):
        if not api_key:
            st.error("⚠️ Please provide an Anthropic API key in the sidebar")
        else:
            with st.spinner("Extracting text from PDF..."):
                paper_text = extract_text_from_pdf(st.session_state['pdf_file'])

            if paper_text:
                st.success(f"✅ Extracted {len(paper_text)} characters from PDF")

                with st.spinner("🤖 Analyzing paper with AI... This may take a minute..."):
                    analysis = analyze_paper_with_ai(paper_text, api_key)

                if analysis:
                    st.session_state['analysis'] = analysis
                    st.session_state['analysis_timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    st.success("✅ Analysis complete!")

# Display results
if 'analysis' in st.session_state:
    st.divider()
    st.header("📋 Analysis Results")
    st.caption(f"Generated on: {st.session_state.get('analysis_timestamp', 'N/A')}")

    display_analysis(st.session_state['analysis'])

    # Download button
    st.divider()
    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        # Prepare JSON download
        download_data = {
            "source": st.session_state.get('source_info', 'Unknown'),
            "timestamp": st.session_state.get('analysis_timestamp', 'N/A'),
            "analysis": st.session_state['analysis']
        }

        json_str = json.dumps(download_data, indent=2)

        st.download_button(
            label="📥 Download as JSON",
            data=json_str,
            file_name=f"paper_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            use_container_width=True
        )

# Footer
st.divider()
st.caption("Built with Streamlit • Powered by Anthropic Claude")
