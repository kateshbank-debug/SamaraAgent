import os
import asyncio
from dotenv import load_dotenv
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate 
from langchain_core.output_parsers import StrOutputParser
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

# Загрузка .env
load_dotenv()
os.environ["HTTP_PROXY"] = "http://user251520:nyq6at@5.252.71.14:7714"
os.environ["HTTPS_PROXY"] = "http://user251520:nyq6at@5.252.71.14:7714"
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "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"
ZAPIER_MCP_URL = os.getenv("ZAPIER_MCP_URL")

# Промпт из вашего файла
prompt = PromptTemplate(
    input_variables=["style", "target_audience", "keywords", "language", "length", "topic", "text"],
    template="""Create a well-structured blog post from the provided Context.
The blog post should effectively capture the key points, insights, and information from the Context.
Focus on maintaining a coherent flow and using proper grammar and language.
Incorporate relevant headings, subheadings, and bullet points to organize the content.
Ensure that the tone of the blog post is {style} (e.g., formal/informal), engaging and informative, catering to {target_audience} audience.
Integrate the provided {keywords} naturally for SEO optimization, include a meta-description at the start, and end with a call to action.
Use this language: {language}.
Feel free to enhance the context by adding additional examples, explanations, and insights where necessary to make it unique and valuable.
The goal is to convert context into a polished, original written resource (length: {length} words) on the topic {topic}, while maintaining accuracy and coherence. Avoid plagiarism by rephrasing in your own words.
CONTEXT: {text}
BLOG POST:"""
)

async def main():
    llm = ChatOpenAI(temperature=0.7)
    chain = prompt | llm | StrOutputParser()

    st.title("Samara AI Content Generator")
    topic = st.text_input("Тема:")
    keywords = st.text_input("Ключевые слова:")
    style = st.selectbox("Стиль:", ["formal", "informal"])
    target_audience = st.text_input("Целевая аудитория:", "маркетологи")
    language = st.selectbox("Язык:", ["EN", "RU"])
    length = st.number_input("Длина (слов):", min_value=500, max_value=2000)
    context = st.text_area("Контекст:")

    if st.button("Генерировать"):
        result = chain.invoke({"style": style, "target_audience": target_audience, "keywords": keywords, "language": language, "length": length, "topic": topic, "text": context})
        st.write(result)

        publish = st.checkbox("Опубликовать в Telegram?")
        if publish:
            async with MultiServerMCPClient({"zapier": {"url": ZAPIER_MCP_URL, "transport": "sse"}}) as client:
                tools = client.get_tools()
                tools = [t for t in tools if hasattr(t, "name") and hasattr(t, "run")]

            if not tools:
                st.error("Нет инструментов в Zapier MCP.")
                return

            agent = create_react_agent(llm, tools)
            user_prompt = f'Send a message to Telegram chat ID "{os.getenv("TELEGRAM_CHAT_ID")}" with text "{result}".'
            agent_input = {"messages": [{"role": "user", "content": user_prompt}]}
            agent_result = await agent.ainvoke(agent_input)
            final_answer = agent_result.get("final_answer") or agent_result.get("output")
            st.write("Результат публикации:", final_answer)

if __name__ == "__main__":
    asyncio.run(main())