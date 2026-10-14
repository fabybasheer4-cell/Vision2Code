import google.generativeai as genai
from PIL import Image

# Step 1: Configure your Gemini API Key
genai.configure(api_key="AIzaSyAqTwYwseX8CHyMhlFizAhmPXWY-sX6S4A")

# Step 2: Load input image
image_path = "lg.jpeg"  # Replace with your form drawing
img = Image.open(image_path)

# Step 3: Initialize Gemini 1.5 Flash model
model = genai.GenerativeModel('gemini-1.5-flash')

# Step 4: Prepare the prompt
prompt = (
    "This is a drawing of a form UI. Generate a complete standalone HTML page "
    "with full structure: <!DOCTYPE html>, <html>, <head>, <title>, <style>, and <body>. "
    "Inside the body, include ONLY the form layout based on the image. "
    "The <form> tag must include action='/submit' and method='post'. "
    "Use clean internal CSS. Do not include explanations or Markdown formatting like ```html."
)

# Step 5: Get Gemini response
response = model.generate_content([img, prompt])
html_code = response.text.strip()

# Step 6: Remove Markdown-style backticks if present
if html_code.startswith("```html"):
    html_code = html_code.replace("```html", "").replace("```", "").strip()

# Step 7: Save to .html file
output_file = "generated_lg_page.html"
with open(output_file, "w", encoding="utf-8") as file:
    file.write(html_code)

print(f"✅ Full HTML form page saved to: {output_file}")