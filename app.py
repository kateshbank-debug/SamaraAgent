import streamlit as st
import os
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# Временная настройка ключей только для локального теста (удалите эти строки перед коммитом!)
os.environ["OPENAI_API_KEY"] = "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"
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["LANGCHAIN_PROJECT"] = "Samara-Agent"

prompt = ChatPromptTemplate.from_messages([
    ("system", """


Create a well-structured blog post from the provided Context.
The blog post should effectively capture the key points, insights, and information from the Context.
Focus on maintaining a coherent flow and using proper grammar and language.
Incorporate relevant headings, subheadings, and bullet points to organize the content.
Ensure that the tone of the blog post is {style} (e.g., formal/informal), engaging and informative, catering to {target_audience} audience.
Integrate the provided {keywords} naturally for SEO optimization, include a meta-description at the start, and end with a call to action.
Use this language: {language}.
Feel free to enhance the context by adding additional examples, explanations, and insights where necessary to make it unique and valuable.
The goal is to convert context into a polished, original written resource (length: {length} words) on the topic {topic}, while maintaining accuracy and coherence. Avoid plagiarism by rephrasing in your own words.
"""),
("human", "CONTEXT: {text}\nBLOG POST:")
])
llm = ChatOpenAI(model="gpt-4o", temperature=0.7)
chain = prompt | llm

st.title("Samara Agent: Генератор контента")
style = st.selectbox("Стиль (informal/formal):", ["informal", "formal"])
target_audience = st.selectbox("Целевая аудитория:", ["bloggers", "marketers", "SMM specialists", "small business owners"])
keywords = st.text_input("Ключевые слова (через запятую):", "AI content generation, LangChain")
language = st.selectbox("Язык:", ["English", "Russian"])
length = st.text_input("Длина (слов):", "1000")
topic = st.text_input("Тема:", "How AI Agents Revolutionize Content Creation")
text = st.text_area("Контекст:")

if st.button("Генерировать"):
    input_data = {
        "style": style,
        "target_audience": target_audience,
        "keywords": keywords,
        "language": language,
        "length": length,
        "topic": topic,
        "text": text
    }
    result = chain.invoke(input_data)
    st.write(result.content)
