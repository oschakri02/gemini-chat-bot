import os
import gradio as gr
from google import genai
from google.genai import types

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))

personalities = {
  "Friendly": """You are a friendly, enthusiastic, and highly encouraging Study Assistant. 
  Your goal is to break down complex concepts into simple, beginner-friendly explanations. 
  Use analogies and real-world examples that beginners can relate to. Always ask a follow-up question to check understanding.""",
  
  "Academic": """You are a strictly academic, highly detailed, and professional university Professor. 
  Use precise, formal terminology, cite key concepts and structure your response. 
  Your goal is to break down complex concepts into simple, beginner-friendly explanations. 
  Use analogies and real-world examples that beginners can relate to. Always ask a follow-up question to check understanding."""
}

def chat_bot(question, persona):
    system_prompt = personalities[persona]

    response = client.models.generate_content(
        model="gemini-3.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            temperature=0.4,
            max_output_tokens=1000
        ),
        contents=question
    )
    return response.text

demo = gr.Interface(
    fn=chat_bot,
    inputs = [gr.Textbox(lines = 4 , placeholder="Ask a question..." , label="Question" ),
              gr.Radio(choices= list(personalities.keys()), label="Personality",value="Friendly")
             ],
    outputs = gr.Textbox(lines=10, label="Response "),
    title="Gemini Chat Bot",
    description = "Ask a question get an answer")   
demo.launch(debug=True)
