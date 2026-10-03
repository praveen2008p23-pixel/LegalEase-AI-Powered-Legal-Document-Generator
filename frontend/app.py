from __future__ import annotations

import os
from datetime import date

import requests
import streamlit as st

from dotenv import load_dotenv

from utils.document_formatter import (
    format_docx,
    format_html_preview,
    format_pdf,
    sanitize_text
)


load_dotenv()


BACKEND_URL = os.getenv(
    "BACKEND_URL",
    "http://127.0.0.1:8000"
).rstrip("/")


st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    .hero {

        padding: 1.2rem 1.4rem;

        border-radius: 18px;

        background:
            linear-gradient(
                135deg,
                #101828,
                #1d2939
            );

        color: white;

        margin-bottom: 1rem;
    }

    .hero h1 {

        margin: 0;

        font-size: 2.1rem;
    }

    .hero p {

        margin: .4rem 0 0;

        color: #d0d5dd;
    }

    .preview {

        background: #0b1220;

        color: #f8fafc;

        border: 1px solid #344054;

        border-radius: 14px;

        padding: 24px;

        max-height: 650px;

        overflow-y: auto;

        line-height: 1.65;
    }

    .preview h3 {

        color: #ffffff;

        margin-top: 18px;
    }

    .preview p {

        color: #e4e7ec;
    }

    .preview .bullet {

        margin:
            4px 0
            4px 12px;
    }

    .doc-spacer {

        height: 8px;
    }

    .disclaimer {

        padding: 10px 14px;

        border-left:
            4px solid
            #98a2b3;

        background: #f2f4f7;

        border-radius: 6px;

        color: #344054;

        font-size: .9rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Header
# --------------------------------------------------

st.markdown(
    """
    <div class="hero">

        <h1>⚖️ LegalEase</h1>

        <p>
            AI-powered legal document
            drafting, editing and export.
        </p>

    </div>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# Disclaimer
# --------------------------------------------------

st.markdown(
    """
    <div class="disclaimer">

        <b>Important:</b>

        LegalEase creates AI-generated
        drafts/templates for informational
        and drafting purposes.

        It is not a substitute for advice
        from a qualified legal professional.

        Review the document for your
        jurisdiction and circumstances
        before using it.

    </div>
    """,
    unsafe_allow_html=True
)


st.write("")


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.subheader(
        "Backend Connection"
    )

    st.code(
        BACKEND_URL,
        language="text"
    )

    if st.button(
        "Check Backend",
        use_container_width=True
    ):

        try:

            response = requests.get(
                f"{BACKEND_URL}/health",
                timeout=5
            )

            response.raise_for_status()

            st.success(
                "Backend is running."
            )

        except requests.RequestException as error:

            st.error(
                f"Backend unavailable: {error}"
            )

    st.divider()

    st.caption(
        "LegalEase project based on "
        "the supplied documentation."
    )


# --------------------------------------------------
# Layout
# --------------------------------------------------

left_column, right_column = st.columns(
    [1, 1]
)


# --------------------------------------------------
# INPUT SECTION
# --------------------------------------------------

with left_column:

    st.subheader(
        "Document Details"
    )

    document_type = st.text_input(
        "Document Type",
        placeholder=(
            "Freelance Work Contract"
        )
    )

    parties = st.text_area(
        "Parties Involved",
        placeholder=(
            "Jane Doe (Service Provider), "
            "TechNova Inc. (Client)"
        ),
        height=120
    )

    terms = st.text_area(
        "Terms & Conditions",
        placeholder=(
            "Payment within 30 days of invoice; "
            "Confidentiality must be maintained; "
            "Either party may terminate with 15 days notice"
        ),
        height=180,
        help=(
            "Separate individual terms "
            "with semicolons (;)."
        )
    )

    dates = st.text_input(
        "Effective Date / Dates",
        value=date.today().strftime(
            "%B %d, %Y"
        )
    )

    generate_button = st.button(
        "✨ Generate Document",
        type="primary",
        use_container_width=True
    )


# --------------------------------------------------
# GENERATE
# --------------------------------------------------

if generate_button:

    missing_fields = []

    if not document_type.strip():

        missing_fields.append(
            "Document Type"
        )

    if not parties.strip():

        missing_fields.append(
            "Parties Involved"
        )

    if not terms.strip():

        missing_fields.append(
            "Terms & Conditions"
        )

    if not dates.strip():

        missing_fields.append(
            "Effective Date / Dates"
        )

    if missing_fields:

        st.error(
            "Please complete: "
            + ", ".join(missing_fields)
        )

    else:

        payload = {

            "document_type":
                document_type.strip(),

            "parties":
                parties.strip(),

            "terms":
                terms.strip(),

            "dates":
                dates.strip()
        }

        with st.spinner(
            "Generating document with Gemini..."
        ):

            try:

                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json=payload,
                    timeout=120
                )

                response.raise_for_status()

                data = response.json()

                st.session_state[
                    "document"
                ] = data["document"]

                st.session_state[
                    "document_type"
                ] = document_type.strip()

                st.session_state[
                    "terms"
                ] = terms.strip()

                st.session_state[
                    "model"
                ] = data.get(
                    "model",
                    "Gemini"
                )

                st.success(
                    "Document generated successfully."
                )

            except requests.RequestException as error:

                detail = ""

                if (
                    getattr(
                        error,
                        "response",
                        None
                    )
                    is not None
                ):

                    try:

                        detail = (
                            error
                            .response
                            .json()
                            .get(
                                "detail",
                                ""
                            )
                        )

                    except Exception:

                        detail = (
                            error
                            .response
                            .text
                        )

                st.error(
                    "Generation failed. "
                    + (
                        detail
                        or str(error)
                    )
                )


# --------------------------------------------------
# PREVIEW SECTION
# --------------------------------------------------

with right_column:

    st.subheader(
        "Preview & Edit"
    )

    if "document" not in st.session_state:

        st.info(
            "Your generated document "
            "will appear here."
        )

    else:

        st.caption(
            "Model: "
            + st.session_state.get(
                "model",
                "Gemini"
            )
        )

        edited_document = st.text_area(
            "Edit the generated document",
            value=st.session_state[
                "document"
            ],
            height=430
        )

        st.session_state[
            "document"
        ] = edited_document

        st.markdown(
            "**Styled Preview**"
        )

        preview = format_html_preview(
            edited_document
        )

        st.markdown(
            f"""
            <div class="preview">
                {preview}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("")

        safe_type = "".join(
            character
            if character.isalnum()
            else "_"
            for character
            in document_type.lower()
        ).strip("_")

        if not safe_type:

            safe_type = (
                "legal_document"
            )

        clean_text = sanitize_text(
            edited_document
        )

        # ------------------------------------------
        # TXT
        # ------------------------------------------

        txt_column, docx_column, pdf_column = (
            st.columns(3)
        )

        with txt_column:

            st.download_button(
                "⬇️ Download TXT",

                data=clean_text.encode(
                    "utf-8"
                ),

                file_name=(
                    f"{safe_type}.txt"
                ),

                mime="text/plain",

                use_container_width=True
            )

        # ------------------------------------------
        # DOCX
        # ------------------------------------------

        docx_bytes = format_docx(
            clean_text,

            st.session_state.get(
                "document_type",
                "Legal Document"
            ),

            st.session_state.get(
                "terms",
                ""
            )
        )

        with docx_column:

            st.download_button(
                "⬇️ Download DOCX",

                data=docx_bytes,

                file_name=(
                    f"{safe_type}.docx"
                ),

                mime=(
                    "application/"
                    "vnd.openxmlformats-officedocument."
                    "wordprocessingml.document"
                ),

                use_container_width=True
            )

        # ------------------------------------------
        # PDF
        # ------------------------------------------

        pdf_bytes = format_pdf(
            clean_text,

            st.session_state.get(
                "document_type",
                "Legal Document"
            ),

            st.session_state.get(
                "terms",
                ""
            )
        )

        with pdf_column:

            st.download_button(
                "⬇️ Download PDF",

                data=pdf_bytes,

                file_name=(
                    f"{safe_type}.pdf"
                ),

                mime="application/pdf",

                use_container_width=True
            )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "LegalEase • Streamlit Frontend • "
    "FastAPI Backend • Gemini AI"
)