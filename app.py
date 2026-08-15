import streamlit as st
from transformers import pipeline

# Set up page configurations for an academic project style
st.set_page_config(page_title="AI Writing Assistant", layout="centered")

st.title("📝 AI Writing Assistant: A Mini Grammarly")
st.caption("Course Project Prototype: Automatic Grammar Correction & Next-Word Prediction")

# --- Step A: Model Loading (Updated for newer transformers versions) ---
@st.cache_resource
def load_models():
    # Causal LM (Decoder-Only Transformer) for next-word options
    predictor = pipeline("text-generation", model="distilgpt2", pad_token_id=50256)
    
    # Updated: Changed task from "text2text-generation" to "text-generation"
    corrector = pipeline("text-generation", model="pszemraj/flan-t5-large-grammar-synthesis")
    
    return predictor, corrector


with st.spinner("Loading Transformer models into memory..."):
    word_predictor, grammar_corrector = load_models()

# --- Step B: Initialize App Session State Variables ---
# Necessary for interactive "Accept Change" buttons to inject text
if "text_input" not in st.session_state:
    st.session_state.text_input = ""

# Callback function to handle multi-word suggestion insertions
def insert_predicted_word(word):
    st.session_state.text_input = st.session_state.text_input.strip() + " " + word + " "

# Callback function to accept full grammatical text updates
def accept_grammar_correction(new_text):
    st.session_state.text_input = new_text + " "

# --- Step C: Build the Suggestion Interface Layout ---
# Textbox tied directly to session state
user_text = st.text_area(
    "Enter text to analyze:", 
    key="text_input", 
    placeholder="Type something here (e.g., I has a car and I am goin to school.)",
    height=150
)

# Run pipeline logic only if text is provided by the student user
if user_text.strip():
    # 1. Sequence Inference: Grammar & Spelling Corrections
    with st.spinner("Analyzing grammar..."):
        correction_output = grammar_corrector(user_text, max_length=128)
        # Note: Depending on version, it might return a list or dict. 
        # This safe extraction handles both.
        if isinstance(correction_output, list):
            corrected_sentence = correction_output[0]['generated_text']
        else:
            corrected_sentence = correction_output['generated_text']


    # 2. Sequence Inference: Distinct Multi Next-Word Options
    with st.spinner("Predicting next tokens..."):
        prediction_outputs = word_predictor(
            user_text, 
            max_new_tokens=2, 
            num_return_sequences=4, 
            do_sample=True, 
            top_k=40
        )
        
        predictions = []
        for output in prediction_outputs:
            generated = output['generated_text']
            new_tokens = generated[len(user_text):].strip()
            first_word = new_tokens.split()[0] if new_tokens.split() else ""
            clean_word = first_word.strip(".,!?\"'")
            if clean_word and clean_word.lower() not in [p.lower() for p in predictions]:
                predictions.append(clean_word)

    # Display Requirement 2 & 3: Error Analysis Section
    st.subheader("🔍 Review & Suggestions")
    
    # Check if changes were recommended by the encoder network
    if corrected_sentence.lower().strip() != user_text.lower().strip():
        st.error(f"**Original Text:** {user_text}")
        st.success(f"**Suggested Correction:** {corrected_sentence}")
        
        # Requirement 5 Met: Dynamic interactive acceptance mechanism
        st.button(
            "Accept Correction", 
            type="primary", 
            on_click=accept_grammar_correction, 
            args=(corrected_sentence,)
        )
    else:
        st.info("Grammar check complete: No distinct mistakes isolated.")

    # Display Bonus Requirement: Multiple Next-Word Tokens
    st.subheader("💡 Predictive Completion Options")
    st.write("Click any predicted token option to append it to your input block:")
    
    if predictions:
        # Create columns to display word choices horizontally as inline pills
        cols = st.columns(len(predictions[:3]))
        for idx, word in enumerate(predictions[:3]):
            with cols[idx]:
                st.button(
                    f"➕ {word}", 
                    key=f"pred_{idx}_{word}", 
                    on_click=insert_predicted_word, 
                    args=(word,)
                )
    else:
        st.text("No predictive tokens matched current structural context.")
else:
    st.info("Awaiting structural input sequence. Type a phrase to see evaluations.")
