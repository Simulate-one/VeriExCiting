import streamlit as st
from veriexcite import (
    extract_bibliography_section,
    split_references,
    search_title,
    set_openrouter_api_key,
    set_google_api_key,  # Keep for backward compatibility
    ReferenceStatus,  # new import
)
import io
import pandas as pd
import PyPDF2


def extract_text_from_pdf(pdf_file: st.runtime.uploaded_file_manager.UploadedFile) -> str:
    """Validates if the file is a PDF, then extract text."""
    if not pdf_file.name.lower().endswith(".pdf"):
        raise ValueError("Uploaded file is not a PDF.")
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.read()))
    pdf_content = ""
    for page in pdf_reader.pages:
        page_text = page.extract_text()
        if page_text:
            pdf_content += page_text + "\n"
    return pdf_content


def process_and_verify(bib_text: str, keywords=["Reference", "Bibliography", "Works Cited"]) -> pd.DataFrame:
    """Extracts, processes, and verifies references."""
    # Create containers in the main area
    progress_text = st.empty()
    placeholder = st.empty()
    progress_text.text("Extracting bibliography ...")

    try:
        references = split_references(bib_text)
        if not references:
            st.warning("No references were extracted from the bibliography section. This could be due to:")
            st.write("- The bibliography section was not found or is empty")
            st.write("- The API failed to parse the references")
            st.write("- The text format is not recognizable")
            return pd.DataFrame(columns=[
                "Index", "First Author", "Year", "Title", "Type", "DOI", "URL", "Raw Text", "Status", "Explanation"
            ])
    except Exception as e:
        st.error(f"Error processing references: {str(e)}")
        st.write("This could be due to:")
        st.write("- Invalid API key")
        st.write("- API service unavailable")
        st.write("- Network connectivity issues")
        return pd.DataFrame(columns=[
            "Index", "First Author", "Year", "Title", "Type", "DOI", "URL", "Raw Text", "Status", "Explanation"
        ])

    ref_type_dict = {"journal_article": "Journal Article", "preprint": "Preprint", "conference_paper": "Conference Paper",
                     "book": "Book", "book_chapter": "Book Chapter", "non_academic_website": "Website"}
    status_emoji = {
        "validated": "✅Validated",
        "invalid": "❌Invalid",
        "not_found": "⚠️Not Found",
        "Pending": "⏳Pending"
    }

    results = []
    for idx, ref in enumerate(references):
        results.append({
            "Index": idx,
            "First Author": ref.author,
            "Year": str(ref.year),
            "Title": ref.title,
            "Type": ref_type_dict.get(ref.type, ref.type),
            "DOI": ref.DOI,
            "URL": ref.URL,
            "Raw Text": ref.bib,
            "Status": "Pending",
            "Explanation": "Pending"
        })

    # Create DataFrame with default columns if results is empty
    if not results:
        df = pd.DataFrame(columns=[
            "Index", "First Author", "Year", "Title", "Type", "DOI", "URL", "Raw Text", "Status", "Explanation"
        ])
    else:
        df = pd.DataFrame(results)
        
        # if URL is empty, and DOI is not empty: if DOI start with https://, fill url with doi. Else, fill url with doi.org link
        df['URL'] = df.apply(
            lambda x: x['DOI'] if pd.notna(x['DOI']) and x['DOI'] != '' and (pd.isna(x['URL']) or x['URL'] == '') and x[
                'DOI'].startswith('https://') else f'https://doi.org/{x["DOI"]}' if pd.notna(x['DOI']) and x[
                'DOI'] != '' and (pd.isna(x['URL']) or x['URL'] == '') else x['URL'], axis=1)

    column_config = {
        "First Author": st.column_config.TextColumn(
            help="First Author's last name, or organization"),
        "Year": st.column_config.TextColumn(width="small"),
        "URL": st.column_config.LinkColumn(width="medium"),
        "Raw Text": st.column_config.TextColumn(
            "Raw Reference Text",  # Display name
            help="Hover for full text",  # Tooltip message
            width="medium",  # Width of the column
        ),
        "Status": st.column_config.TextColumn(
            help="Reference validation status"
        ),
        "Explanation": st.column_config.TextColumn(
            help="Explanation of the validation result"
        )
    }

    df_display = df[[
        'First Author', 'Year', 'Title', 'Type', 'URL', 'Raw Text', 'Status', 'Explanation']]
    placeholder.dataframe(df_display, use_container_width=True, column_config=column_config)

    verified_count = 0
    warning_count = 0
    progress_text.text(f"Validated: {verified_count} | Invalid/Not Found: {warning_count}")

    for index, row in df.iterrows():
        result = search_title(references[index])
        df.loc[index, "Status"] = status_emoji.get(result.status.value, result.status.value)
        df.loc[index, "Explanation"] = result.explanation
        if result.status == ReferenceStatus.VALIDATED:
            verified_count += 1
        else:
            warning_count += 1
        df_display = df[[
            'First Author', 'Year', 'Title', 'Type', 'URL', 'Raw Text', 'Status', 'Explanation']]
        placeholder.dataframe(df_display, use_container_width=True, column_config=column_config)
        progress_text.text(f"Validated: {verified_count} | Invalid/Not Found: {warning_count}")

    return df


def main():
    st.set_page_config(page_title="VeriExCite", page_icon="🔍", layout="wide", initial_sidebar_state="expanded",
                       menu_items={
                           "About": "This is a tool to verify citations in academic papers. View the source code on [GitHub](https://github.com/ykangw/VeriExCiting)."})

    st.title("VeriExCite: Verify Existing Citations")
    st.write(
        "This tool helps verify the existence of citations in academic papers (PDF format). "
        "It extracts the bibliography, parses references, and checks their validity."
    )

    with st.sidebar:
        st.header("Input")
        pdf_files = st.file_uploader("Upload one or more PDF files", type="pdf", accept_multiple_files=True)

        st.write("**API Configuration**")
        api_provider = st.radio(
            "Choose API provider:",
            ["OpenRouter", "Google Gemini"],
            help="OpenRouter provides access to multiple AI models including Claude, GPT-4, and others."
        )
        
        if api_provider == "OpenRouter":
            st.write(
                "Get your OpenRouter API key at [OpenRouter](https://openrouter.ai/) - supports Claude 3.5 Sonnet, GPT-4, and many other models.")
            
            # Model selection
            model_options = {
                "Claude 3.5 Sonnet": "anthropic/claude-3.5-sonnet",
                "Claude 3 Haiku": "anthropic/claude-3-haiku",
                "GPT-4o": "openai/gpt-4o",
                "GPT-4o Mini": "openai/gpt-4o-mini",
                "GPT-4 Turbo": "openai/gpt-4-turbo",
                "Gemma 2 27B": "google/gemma-2-27b-it",
                "LLaMA 3.1 8B": "meta-llama/llama-3.1-8b-instruct",
            }
            
            selected_model_name = st.selectbox(
                "Select Model:",
                options=list(model_options.keys()),
                help="Different models have different strengths and costs"
            )
            selected_model = model_options[selected_model_name]
            
            use_dev_key = st.checkbox("Use developer's OpenRouter key for a trial (limited uses)")
            if use_dev_key:
                api_key = st.secrets.get("OPENROUTER_API_KEY", "")
                if not api_key:
                    st.warning("Developer key not available. Please enter your own API key.")
            else:
                api_key = st.text_input("Enter your OpenRouter API key:", type="password")
        else:
            st.write(
                "You can apply for a Gemini API key at [Google AI Studio](https://ai.google.dev/aistudio) with 1500 requests per day for FREE.")
            selected_model = "gemini-2.5-flash"  # Default Gemini model
            use_dev_key = st.checkbox("Use developer's Gemini key for a trial (limited uses)")
            if use_dev_key:
                api_key = st.secrets.get("GOOGLE_API_KEY", "")
                if not api_key:
                    st.warning("Developer key not available. Please enter your own API key.")
            else:
                api_key = st.text_input("Enter your Google Gemini API key:", type="password")

    if st.sidebar.button("Start Verification"):
        if not pdf_files:
            st.warning("Please upload at least one PDF file.")
            return

        if not api_key:
            provider_name = "OpenRouter" if api_provider == "OpenRouter" else "Google Gemini"
            st.warning(f"Please enter a {provider_name} API key or select 'Use developer's API key'.")
            return

        try:
            if api_provider == "OpenRouter":
                set_openrouter_api_key(api_key, selected_model)
                st.success(f"✅ Using {selected_model_name} via OpenRouter")
            else:
                set_google_api_key(api_key)
                st.success("✅ Using Google Gemini")
            all_results = []

            for pdf_file in pdf_files:
                subheader = st.subheader(f"Processing: {pdf_file.name}")
                bib_text = extract_bibliography_section(extract_text_from_pdf(pdf_file))

                # Display extracted bibliography text with expander
                with st.expander(f"Extracted Bibliography Text for {pdf_file.name}"):
                    st.text_area("Extracted Text", bib_text, height=200, label_visibility="hidden")

                results_df = process_and_verify(bib_text)
                results_df['Source File'] = pdf_file.name
                all_results.append(results_df)
                subheader.subheader(f"Completed: {pdf_file.name}")

            if all_results:
                combined_results = pd.concat(all_results, ignore_index=True)
                csv = combined_results.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="Download All Results as CSV",
                    data=csv,
                    file_name='VeriCite_results.csv',
                    mime='text/csv',
                )

        except ValueError as ve:
            st.error(str(ve))
        except Exception as e:
            st.error(f"An error occurred: {e}")


if __name__ == "__main__":
    main()