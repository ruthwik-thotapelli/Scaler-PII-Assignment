import streamlit as st
import io
from redact_pii import redact_docx
import redact_pii

# Set page layout and aesthetics
st.set_page_config(
    page_title="PII Redaction Engine",
    page_icon="🛡️",
    layout="centered"
)

# Custom header styling
st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #2563eb; margin-bottom: 10px;">🛡️ Enterprise PII Redaction Engine</h1>
        <p style="color: #64748b; font-size: 1.1em;">Automatically detect, redact, and anonymize sensitive information inside Microsoft Word (.docx) documents.</p>
    </div>
""", unsafe_allow_html=True)

st.write("---")

# File uploader
uploaded_file = st.file_uploader("Upload Word Document (.docx)", type="docx")

if uploaded_file is not None:
    # Read files in-memory using BytesIO stream
    input_stream = io.BytesIO(uploaded_file.read())
    output_stream = io.BytesIO()

    with st.spinner("Analyzing document structure & neutralizing sensitive data..."):
        # Reset the global mapping cache to prevent cross-user leakages
        redact_pii.ENTITY_MAP.clear()
        
        # Run core redaction engine using the stream
        redact_docx(input_stream, output_stream)
        
        # Rewind pointer to read from beginning
        output_stream.seek(0)

    st.success("Redaction Complete & Secured! 🎉")

    # Download Button
    st.download_button(
        label="Download Redacted Document (.docx)",
        data=output_stream,
        file_name=f"redacted_{uploaded_file.name}",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )

    # Show Mapping Details
    if redact_pii.ENTITY_MAP:
        st.write("---")
        st.subheader("📊 Anonymization Map")
        st.write("The engine resolved and replaced the following detected items consistently:")
        
        # Convert dictionary to lists for displaying
        mapping_table = [{"Original PII": k, "Synthetic Alternative": v} for k, v in redact_pii.ENTITY_MAP.items()]
        st.table(mapping_table)
else:
    st.info("Please upload a .docx file to begin the redaction process.")
