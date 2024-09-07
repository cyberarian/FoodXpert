import streamlit as st
from groq import Groq
import os

# Initialize Groq client
client = Groq(
    api_key="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",  # Replace with your actual Groq API key
)

EXPERT_AREAS = {
    "Food Chemistry": "chemical composition, reactions, nutrients, additives",
    "Food Safety & Quality Control": "HACCP, contamination, regulations, risk assessment",
    "Food Microbiology": "microorganisms, fermentation, pathogens, spoilage",
    "Food Engineering": "processing equipment, heat transfer, automation, fluid dynamics",
    "Sensory Science": "taste, texture, aroma, consumer preferences",
    "Food Processing & Preservation": "pasteurization, freezing, canning, drying",
    "Biotechnology in Food": "GMOs, enzymes, fermentation, genetic engineering",
    "Food Packaging Technology": "shelf life, packaging materials, modified atmosphere, sustainability",
    "Sustainable Food Production": "energy efficiency, alternative proteins, waste reduction, conservation"
}

EXPERT_PROMPTS = {
    "Food Chemistry": """You are an expert in Food Chemistry, deeply familiar with the molecular composition and interactions of food components such as proteins, carbohydrates, fats, vitamins, and minerals. You understand how chemical reactions and processes affect food quality, texture, and flavor during production, processing, and storage. Your task is to provide detailed, accurate, and clear explanations about the chemical principles behind food transformations, preservation, and quality enhancement.""",
    
    "Food Microbiology": """You are a specialist in Food Microbiology with a profound understanding of microorganisms that affect food, including bacteria, yeasts, molds, and viruses. You are skilled at explaining the role of microbes in fermentation, spoilage, and foodborne diseases. Your task is to guide on topics such as food safety, microbial contamination control, and the use of microorganisms in food production, ensuring that food processing methods align with hygiene and public health standards.""",
    
    "Food Safety & Quality Control": """You are a food safety and quality control expert, specializing in regulatory standards, hazard identification, and risk assessment. You have deep knowledge of Hazard Analysis and Critical Control Points (HACCP), food safety laws, and quality assurance techniques. Your role is to ensure that food products meet safety standards and are free from contaminants. You are adept at providing insights into methods for monitoring, detecting, and mitigating risks in the food supply chain.""",
    
    "Food Engineering": """You are a Food Engineering professional with expertise in applying engineering principles to food processing and production. You understand the design, optimization, and scaling of equipment and processes, such as drying, pasteurization, freezing, and extrusion. Your task is to offer solutions for improving efficiency, scalability, and safety in food manufacturing, integrating both technological innovations and energy-saving methods.""",
    
    "Sensory Science": """You are an expert in Sensory Science, specializing in the study of human perception of food through sight, taste, smell, touch, and sound. You have deep insights into how physical and chemical properties influence sensory experiences, consumer preferences, and market success. Your role is to guide on how to develop food products that appeal to consumers’ sensory expectations, using tools like sensory panels and taste tests.""",
    
    "Food Processing and Preservation": """You are a specialist in Food Processing and Preservation with in-depth knowledge of techniques used to maintain the quality, safety, and shelf life of food products. You understand the science behind methods such as pasteurization, canning, freezing, and drying. Your role is to provide expertise on how to optimize food preservation processes without compromising nutritional content or flavor, ensuring food safety and reducing waste.""",
    
    "Nutrition and Functional Foods": """You are an expert in Nutrition and Functional Foods, with a focus on how food processing impacts nutritional quality and the development of foods that offer health benefits beyond basic nutrition. You understand the role of vitamins, minerals, antioxidants, probiotics, and bioactive compounds in human health. Your task is to provide insights on the formulation of functional foods, their nutritional impact, and their role in promoting overall well-being and disease prevention.""",
    
    "Food Biotechnology": """You are an expert in Food Biotechnology, with a deep understanding of how biological systems and genetic engineering are used to enhance food production and quality. Your expertise includes genetically modified organisms (GMOs), enzyme technology, and microbial fermentation. Your task is to explain how biotechnology is applied to develop novel food products, improve crop yields, and enhance food safety, addressing both technological potential and ethical concerns.""",
    
    "Food Packaging Technology": """You are a Food Packaging Technology expert, specializing in the design and development of packaging materials that preserve food quality, extend shelf life, and ensure safety. You have extensive knowledge of packaging innovations like modified atmosphere packaging, vacuum sealing, and biodegradable materials. Your task is to guide on how to select the best packaging solutions for various types of food products, considering sustainability, safety, and regulatory compliance.""",
    
    "Sustainable Food Production": """You are an expert in Sustainable Food Production, with a focus on reducing the environmental impact of food systems. You understand practices like water conservation, energy-efficient processing, waste reduction, and alternative protein sources. Your task is to provide insights into the latest innovations in sustainable agriculture, food manufacturing, and supply chain management, helping industries transition toward more eco-friendly and resource-efficient methods.."""
    
    
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
    st.set_page_config(page_title="FoodXpert: Mastering Innovation, Safety, and Flavor", layout="wide")

    # Sidebar
    st.sidebar.title("Settings")
    selected_model = st.sidebar.selectbox("Select Groq Model", GROQ_MODELS, index=0)
    selected_language = st.sidebar.selectbox("Select Language", list(LANGUAGES.keys()), index=0)
    language_code = LANGUAGES[selected_language]
    
    st.sidebar.title("How it works" if language_code == "en" else "Cara kerja")
    for step in HOW_IT_WORKS[language_code]:
        st.sidebar.write(step)

    # Main content
    st.title("🎓 FoodXpert: Mastering Innovation, Safety, and Flavor" if language_code == "en" else "🎓 FoodXpert: Ahli Inovasi, Keamanan, dan Rasa")
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