import streamlit as st
import groq
import os

# Set up Groq API client
client = groq.Client(api_key=os.getenv("GROQ_API_KEY"))

# Streamlit UI styling
st.markdown(
    """
    <style>
    body {
        background-color: #f0f2f6;
    }
    .title {
        text-align: center;
        color: #4CAF50;
        font-size: 36px;
        font-weight: bold;
    }
    .chat-container {
        max-width: 700px;
        margin: auto;
    }
    .user-message {
        background-color: #DCF8C6;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        text-align: right;
    }
    .assistant-message {
        background-color: #E1E1E1;
        padding: 10px;
        border-radius: 10px;
        margin: 5px 0;
        text-align: left;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<h1 class='title'>Inkspire AI 🖋️💡</h1>", unsafe_allow_html=True)

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [
         {"role": "system", "content": ''' You are an advanced AI content creator with expertise in writing engaging, informative, and well-structured content.  
Your primary goal is to generate **high-quality, human-like content** that is engaging, SEO-friendly, and tailored for the target audience.  

🔹 **Tone & Style:**  
- Adapt the tone based on the context (formal, conversational, persuasive, or storytelling).  
- Use natural, engaging language with smooth transitions.  
- Keep readability high and avoid robotic or repetitive phrasing.  

🔹 **Content Types You Can Create:**  
- Blog posts, articles, and essays.  
- Social media posts and ad copies.  
- Product descriptions and reviews.  
- Email marketing content.  
- Video scripts, podcast transcripts, and captions.  
- Website content, including landing pages and "About Us" sections.  

🔹 **Key Writing Strategies:**  
- Hook the reader within the first two sentences.  
- Use storytelling techniques to enhance engagement.  
- Implement SEO best practices, including keywords, headings, and meta descriptions.  
- Keep paragraphs short and use bullet points where needed.  
- Provide actionable insights and well-researched information.  

🔹 **Editing & Refinement:**  
- Self-edit for grammar, clarity, and readability.  
- Ensure content is factually correct and provides value.  
- Avoid filler content or unnecessary complexity.  

Now, generate high-quality content based on the user’s request!'''
}
    ]

for msg in st.session_state["messages"]:
    if msg["role"] == "system":  # Ignore system messages in UI
        continue  
    elif msg["role"] == "user":
        st.markdown(f"<div class='user-message'>{msg['content']}</div>", unsafe_allow_html=True)
    else:
        st.markdown(f"<div class='assistant-message'>{msg['content']}</div>", unsafe_allow_html=True)

# **Input box at the bottom**
prompt = st.chat_input("Type your message...")
if prompt:
    # Add user message to history
    st.session_state["messages"] += [{"role": "user", "content": prompt}]

    # Display user message
    st.markdown(f"<div class='user-message'>{prompt}</div>", unsafe_allow_html=True)

    # Send request to Groq API
    response = client.chat.completions.create(
        model="llama3-8b-8192",  # Ensure this is a valid model name
        messages=[{"role": "system", "content": "You are a helpful AI assistant."}] + 
                 st.session_state["messages"]
    ).choices[0].message.content

    # Add assistant message to history
    st.session_state["messages"] += [{"role": "assistant", "content": response}]

    # Display assistant message
    st.markdown(f"<div class='assistant-message'>{response}</div>", unsafe_allow_html=True)
