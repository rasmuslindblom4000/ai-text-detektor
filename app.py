import streamlit as st
import re
from collections import Counter

def ai_text_detector(text):
    sentences = re.split(r'[.!?]\s+', text.strip())
    words = re.findall(r'\w+', text)
    word_count = len(words)
    sentence_count = len(sentences)
    avg_sentence_length = word_count / sentence_count if sentence_count else 0

    word_freq = Counter(words)
    most_common_words = word_freq.most_common(10)
    repetitiveness_score = sum(freq for _, freq in most_common_words) / word_count if word_count else 0

    bullet_points = len(re.findall(r'\d+-|[a-z]\.', text))
    qa_detected = bool(re.search(r'(?i)(fråga|svar|\?)', text))

    score = 0
    reasoning = []

    if bullet_points > 10:
        score += 0.3
        reasoning.append("Många punktlistor och strukturerade definitioner")
    if avg_sentence_length < 12:
        score += 0.2
        reasoning.append("Korta, enkla meningar")
    if repetitiveness_score > 0.15:
        score += 0.2
        reasoning.append("Hög repetitivitet i ordval")
    if qa_detected:
        score += 0.1
        reasoning.append("Q&A-format upptäckt")

    score += 0.1
    probability = min(score, 1.0) * 100

    return {
        "antal_ord": word_count,
        "antal_meningar": sentence_count,
        "genomsnittlig_meningslängd": round(avg_sentence_length, 2),
        "vanligaste_ord": most_common_words,
        "repetitivitet": round(repetitiveness_score, 2),
        "punktlistor": bullet_points,
        "qa_format": qa_detected,
        "sannolikhet_AI": round(probability, 1),
        "orsaker": reasoning
    }

st.title("AI Textdetektor")
text_input = st.text_area("Klistra in din text här:", height=300)

if st.button("Analysera"):
    if text_input.strip():
        result = ai_text_detector(text_input)
        st.subheader(f"Sannolikhet att texten är AI-genererad: {result['sannolikhet_AI']}%")
        st.write("**Detaljer:**")
        st.write(f"Antal ord: {result['antal_ord']}")
        st.write(f"Antal meningar: {result['antal_meningar']}")
        st.write(f"Genomsnittlig meningslängd: {result['genomsnittlig_meningslängd']}")
        st.write(f"Punktlistor: {result['punktlistor']}")
        st.write(f"Q&A-format: {'Ja' if result['qa_format'] else 'Nej'}")
        st.write(f"Vanligaste ord: {result['vanligaste_ord']}")
        st.write(f"Orsaker: {', '.join(result['orsaker'])}")
