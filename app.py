import streamlit as st
from groq import Groq
import os

# Initialize Groq client
client = Groq(
    api_key="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",  # Replace with your actual Groq API key
)

EXPERT_AREAS = {
    "Computer Science": "algorithms, programming languages, software engineering, artificial intelligence",
    "Library and Information Science": "information organization, digital libraries, metadata management, information retrieval",
    "Archival Studies": "records management, digital preservation, archival description, historical research",
    "Data Science": "data analysis, machine learning, statistical modeling, data visualization"
}

EXPERT_PROMPTS = {
    "Computer Science": """You are a Computer Science expert with deep expertise in algorithms, programming languages, software engineering, and artificial intelligence. Your responses must demonstrate a comprehensive understanding of computational theory, software development practices, and the latest advancements in emerging technologies, particularly AI. When answering questions, consider both theoretical principles and practical applications, offering clear, precise, and insightful explanations. Additionally, reflect on the current and future impact of AI, addressing how it transforms industries, influences technological trends, and shapes the future of software development and computational theory. If a query falls outside your area of expertise, respond politely, indicating that the request is beyond your specialized knowledge.""",
    
    "Library and Information Science": """You are an expert in Library and Information Science, specializing in information organization, digital libraries, metadata management, and information retrieval, and the latest advancements in emerging technologies, particularly AI. Your knowledge encompasses both traditional library practices and modern digital information systems. When responding, consider the evolving landscape of information access and management in the digital age, offering clear, precise, and insightful explanations. Additionally, reflect on how digital transformation impacts libraries, metadata standards, and information retrieval practices. If a query falls outside your area of expertise, respond politely, indicating that the request is beyond your specialized knowledge.""",
    
    "Archival Studies": """You are an expert in Archival Studies with extensive knowledge of records management, digital preservation, archival description, historical research methods, and the latest advancements in emerging technologies, particularly AI. Your expertise covers both traditional archival practices and modern digital archiving techniques. When answering questions, consider the importance of preserving and providing access to historical and cultural heritage, offering clear, precise, and insightful explanations. Additionally, reflect on the challenges and advancements in digital preservation and access strategies in the context of evolving archival standards. If a query falls outside your area of expertise, respond politely, indicating that the request is beyond your specialized knowledge.""",
    
    "Data Science": """You are an expert in Data Science, proficient in data analysis, machine learning, statistical modeling, data visualization, and the latest advancements in emerging technologies, particularly AI. Your knowledge spans various analytical techniques and tools used to extract insights from complex datasets. When responding, consider both the technical aspects of data manipulation and the strategic implications of data-driven decision making, offering clear, precise, and insightful explanations. Additionally, address the challenges and opportunities in applying data science methodologies to real-world problems. If a query falls outside your area of expertise, respond politely, indicating that the request is beyond your specialized knowledge."""
}

GROQ_MODELS = [
    "gemma2-9b-it",
    "gemma-7b-it",
    "llama-3.1-8b-instant",
    "llama3-groq-70b-8192-tool-use-preview",
    "llama3-groq-8b-8192-tool-use-preview",
    "llama3-70b-8192",
    "llama3-70b-4096",
    "mixtral-8x7b-32768",    
]

LANGUAGES = {
    "English": "en",
    "Bahasa Indonesia": "id"
}

HOW_IT_WORKS = {
    "en": [
        "1. Select an area of expertise for your question.",
        "2. Enter your question or topic (up to 50 words).",
        "3. Click 'Get Expert Answer' to receive a response.",
        "4. The system analyzes the question and generates an answer based on the selected expertise.",
        "5. Enjoy your personalized expert response!"
    ],
    "id": [
        "1. Pilih bidang keahlian untuk pertanyaan Anda.",
        "2. Masukkan pertanyaan atau topik Anda (maksimal 50 kata).",
        "3. Klik 'Dapatkan Jawaban Ahli' untuk menerima respons.",
        "4. Sistem menganalisis pertanyaan dan menghasilkan jawaban berdasarkan keahlian yang dipilih.",
        "5. Nikmati respons ahli personal Anda!"
    ]
}

def generate_response_with_groq(question, expert_area, model, language):
    system_prompt = EXPERT_PROMPTS[expert_area]
    system_prompt += f"\n\nYour task is to generate a comprehensive answer to the given question, embodying the expertise and knowledge of a {expert_area} specialist. The answer should be only in {'Indonesian (Bahasa Indonesia)' if language == 'id' else 'English'}."

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": f"Answer the following question as an expert in {expert_area}: {question}"
            }
        ],
        model=model,
        temperature=0.3,
        max_tokens=500,
        top_p=1,
        stream=False,
    )
    return chat_completion.choices[0].message.content

def generate_expert_info(expert_area, model, language):
    system_prompt = "You are a knowledgeable expert with a deep understanding of various academic fields. Provide concise, informative responses about different areas of expertise."
    user_prompt = f"Generate a single, concise sentence about the field of {expert_area}, focusing on its significance and key areas of study. The sentence should be informative and suitable for a brief introduction. Respond only in {'Indonesian' if language == 'id' else 'English'}."

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        model=model,
        temperature=0.3,
        max_tokens=500,
        top_p=1,
        stream=False,
    )
    return chat_completion.choices[0].message.content.strip()

def word_count(text):
    return len(text.split())

def main():
    st.set_page_config(page_title="ExpertChat, Your Academic Companion", layout="wide")

    # Sidebar
    st.sidebar.title("Settings")
    selected_model = st.sidebar.selectbox("Select Groq Model", GROQ_MODELS, index=0)
    selected_language = st.sidebar.selectbox("Select Language", list(LANGUAGES.keys()), index=0)
    language_code = LANGUAGES[selected_language]
    
    st.sidebar.title("How it works" if language_code == "en" else "Cara kerja")
    for step in HOW_IT_WORKS[language_code]:
        st.sidebar.write(step)

    # Main content
    st.title("🎓 XpertChat, Your Academic Companion" if language_code == "en" else "🎓 XpertChat, Teman Akademis Anda")
    st.markdown("Get expert answers to your academic questions across various fields." if language_code == "en" else "Dapatkan jawaban ahli untuk pertanyaan akademis Anda di berbagai bidang.")

    col1, col2 = st.columns([2, 1])

    with col1:
        expert_area = st.selectbox("Choose an area of expertise:" if language_code == "en" else "Pilih bidang keahlian:", list(EXPERT_AREAS.keys()))
        question = st.text_area("Enter your question (up to 50 words):" if language_code == "en" else "Masukkan pertanyaan Anda (maksimal 50 kata):", height=100, max_chars=500, help="Provide a clear and specific question related to the chosen field of expertise (max 50 words)." if language_code == "en" else "Berikan pertanyaan yang jelas dan spesifik terkait bidang keahlian yang dipilih (maksimal 50 kata).")
        word_count_question = word_count(question)
        st.write(f"Word count: {word_count_question}/50" if language_code == "en" else f"Jumlah kata: {word_count_question}/50")

    with col2:
        st.markdown("### About the Expertise" if language_code == "en" else "### Tentang Keahlian")
        expert_info = generate_expert_info(expert_area, selected_model, language_code)
        st.info(expert_info)

    if st.button("Get Expert Answer" if language_code == "en" else "Dapatkan Jawaban Ahli", type="primary"):
        if not question:
            st.warning("Please enter a question." if language_code == "en" else "Mohon masukkan pertanyaan.")
        elif word_count_question > 50:
            st.warning("Please limit your question to 50 words or less." if language_code == "en" else "Mohon batasi pertanyaan Anda hingga 50 kata atau kurang.")
        else:
            with st.spinner("Generating expert response..." if language_code == "en" else "Menghasilkan respons ahli..."):
                response = generate_response_with_groq(question, expert_area, selected_model, language_code)
                st.success("Expert response ready!" if language_code == "en" else "Respons ahli siap!")
                st.markdown("### Expert Answer" if language_code == "en" else "### Jawaban Ahli")
                st.markdown(response)

    # Footer
    st.markdown("---")
    st.markdown("Built with :orange_heart: thanks to Claude.ai, Groq, Github, Streamlit. :scroll: support my works at https://saweria.co/adnuri", help="cyberariani@gmail.com")

if __name__ == "__main__":
    main()