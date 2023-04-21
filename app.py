import json
import os
import requests
import gradio

def generate_image(text_prompt, init_image):
    engine_id = "stable-diffusion-v1-5"
    api_host = os.getenv('API_HOST', 'https://api.stability.ai')
    url = f"{api_host}/v1alpha/generation/{engine_id}/image-to-image"

    api_key = 'sk-pJ2hAocegVJCVgRYHvhleFaOP6AVTwSrhzsWYucwmrFi8XKS'
    if api_key is None:
        raise Exception("Missing Stability API key.")

    options = json.dumps(
        {
            "text_prompts": [
                {
                    "text": text_prompt,
                    "weight": 2
                }
            ],
        }
    )

    headers = {
        'accept': 'image/png',
        'Authorization': api_key,
    }

    files = {
        'init_image': open(init_image, 'rb'),
        'options': (None, options),
    }

    response = requests.post(url, headers=headers, files=files)

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    with open("output.png", "wb") as f:
        f.write(response.content)

    return "output.png"


# Gradio


inputs = [
    gr.inputs.Textbox(label="Text"),
    gr.inputs.Image(label="Image")
]

outputs = gr.outputs.Image(label="Generated Image")

gr.Interface(fn=generate_image, inputs=inputs, outputs=outputs).launch(debug=True)
