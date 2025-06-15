import gradio as gr
import base64
import os
from openai import OpenAI  # Assuming Gemini is using OpenAI-compatible SDK

with open("gemini_api_kay", "r") as file:
    api_key_gem = file.read().strip()

os.environ["API_KEY_GEM"] = api_key_gem

# Gemini Client Initialization
client = OpenAI(
    api_key=os.environ["API_KEY_GEM"],
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Convert image to base64 string
def image_to_base64(image):
    buffered = image.convert("RGB")
    with open("temp.png", "wb") as f:
        buffered.save(f, format="PNG")
    with open("temp.png", "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

# Compare images using Gemini
def compare_dashboards(before_img, after_img):
    if before_img is None or after_img is None:
        return "Please upload both BEFORE and AFTER images."

    before_b64 = image_to_base64(before_img)
    after_b64 = image_to_base64(after_img)

    messages = [
        {
            "role": "system",
            "content": """You are an expert data analyst assistant.
Analyze the two provided images of a data analyst dashboard.
The first image is the 'BEFORE' version.
The second image is the 'AFTER' version.

Please carefully compare them and provide a detailed, itemized list of the changes. Focus on:
1. Changes in chart types, data displayed within charts (e.g., bar heights, line trends, pie slice proportions, new data series, changes in axis scales).
2. Modifications to Key Performance Indicator (KPI) values or any other numerical data presented. If a number changed, state the old and new value if discernible.
3. Added, removed, or repositioned visual elements (e.g., charts, tables, text boxes, filters, legends, buttons).
4. Alterations in titles, labels, or annotations.
5. Significant changes in color schemes or overall styling if they impact readability or meaning.
6. Changes in dashboard layout or structure.
7. Determine if there are any filters present like slicers, pull downs and drill throughs and provide valuable opinions whether the change may or may not be affected because of them

Be as specific and factual as possible."""
        },
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "There are two images before and after of a power bi dashboard, help me identify the changes"},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{before_b64}"}},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{after_b64}"}}
            ]
        }
    ]

    response = client.chat.completions.create(
        model="gemini-2.5-flash-preview-05-20",
        reasoning_effort="high",
        messages=messages
    )

    return response.choices[0].message.content

# Gradio UI
gr.Interface(
    fn=compare_dashboards,
    inputs=[
        gr.Image(type="pil", label="BEFORE Dashboard"),
        gr.Image(type="pil", label="AFTER Dashboard")
    ],
    outputs=gr.Textbox(label="Gemini Analysis Output"),
    title="Power BI Dashboard Change Detector",
    description="Upload BEFORE and AFTER dashboard screenshots to get a detailed comparison using Gemini LLM."
).launch()
