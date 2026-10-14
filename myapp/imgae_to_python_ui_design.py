import google.generativeai as genai
from PIL import Image

# ======= USER CONFIG ========
API_KEY = "AIzaSyAqTwYwseX8CHyMhlFizAhmPXWY-sX6S4A"       # Replace this with your Gemini API key
image_path = "lg.jpeg"       # Your form sketch or wireframe image
output_file = "generated_gui.py"      # Output Python file
# ============================

# Step 1: Setup Gemini API
genai.configure(api_key=API_KEY)

# Step 2: Load the image
img = Image.open(image_path)

# Step 3: Prompt Gemini to generate Tkinter code
prompt = (
    "This is a hand-drawn form UI. Generate complete Python Tkinter code "
    "to build this GUI. Include appropriate labels, entry fields, and buttons. "
    "Use clean layout with grid or pack. Return only the code without any explanation or markdown formatting."
)

# Step 4: Generate response from Gemini
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content([img, prompt])
tkinter_code = response.text.strip()

# Step 5: Clean markdown-style formatting (e.g., ```python)
if tkinter_code.startswith("```"):
    tkinter_code = tkinter_code.split("```")[1] if "```" in tkinter_code else tkinter_code
    tkinter_code = tkinter_code.strip()

# Step 6: Save generated code to a Python file
with open(output_file, "w", encoding="utf-8") as f:
    f.write(tkinter_code)

print(f"✅ Tkinter Python GUI code saved to: {output_file}")