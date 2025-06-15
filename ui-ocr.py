import gradio as gr
import base64
import os
from openai import OpenAI  # Assuming Gemini is using OpenAI-compatible SDK
import pytesseract

with open("gemini_api_kay", "r") as file:
    api_key_gem = file.read().strip()

os.environ["API_KEY_GEM"] = api_key_gem

# Gemini Client Initialization
client = OpenAI(
    api_key=os.environ["API_KEY_GEM"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# image to ocr
def image_to_ocr(image):
    try:
        if not isinstance(image, Image.Image):
            return "Invalid image format"
        return pytesseract.image_to_string(image)
    except Exception as e:
        return f"Error extracting text: {str(e)}"
    

# Compare images using Gemini
client=OpenAI(
    api_key=os.environ["API_KEY_GEM"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)
model = "gemini-2.5-flash-preview-05-20"

def compare_dashboards_ocr_only(before_img, after_img):
    if before_img is None or after_img is None:
        return "❗ Please upload both BEFORE and AFTER dashboard images."
    
    before_text = image_to_ocr(before_img)
    after_text = image_to_ocr(after_img)
    
    messeges = [
        {
            "role": "system",
            "content": """You are an expert data analyst assistant.
Analyze the two provided OCR data of images of a data analyst dashboard.
The first OCR image text is the 'BEFORE' version.
The second OCR image text is the 'AFTER' version.

Please carefully compare them and provide a detailed, itemized list of the changes. Focus on:
1. Changes in chart types, data displayed within charts (e.g., bar heights, line trends, pie slice proportions, new data series, changes in axis scales).
2. Modifications to Key Performance Indicator (KPI) values or any other numerical data presented. If a number changed, state the old and new value if discernible.
3. Added, removed, or repositioned visual elements (e.g., charts, tables, text boxes, filters, legends, buttons).
4. Alterations in titles, labels, or annotations.
5. Significant changes in color schemes or overall styling if they impact readability or meaning.
6. Changes in dashboard layout or structure.
7. Determine if there are any filters present like slicers, pull downs and drill throughs and provide valuable opinions whether the change may or may not be affected because of them.
8. Pay close attention to subtle changes in granularity (e.g., drill-down or drill-up actions in charts). This can appear as changes in axis labels (e.g., year vs. quarter), data grouping, or breadcrumb navigations at the top of charts.


Be as specific and factual as possible."""
        },
        {"role":"user",
         "content":[
             {"type":"text","text": f"Before Dashboard Text{before_text}"},
             {"type":"text","text": f"After Dashboard Text{after_text}"}
             ]
             }
         ]
    
    responces = client.chat.completions.create(
    model= model,
    reasoning_effort="high",
    messages= messeges
    )

    return responces.choices[0].message.content


# Gradio UI
gr.Interface(
    fn=compare_dashboards_ocr_only,
    inputs=[
        gr.Image(type="pil", label="BEFORE Dashboard"),
        gr.Image(type="pil", label="AFTER Dashboard")
    ],
    outputs=gr.Textbox(label="Gemini Analysis Output"),
    title="Power BI Dashboard Change Detector",
    description="Upload BEFORE and AFTER dashboard screenshots to get a detailed comparison using Gemini LLM."
).launch()