import os
import base64

import requests
import cv2


def capture_image_and_save(image_path="captured_image.png"):
    """Capture one frame from the webcam and save it."""
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Could not open camera.")
        return False

    try:
        ret, frame = cap.read()

        if ret:
            cv2.imwrite(image_path, frame)
            print(f"Image captured and saved as {image_path}")
            return True

        print("Error: Could not capture image.")
        return False

    finally:
        cap.release()
        cv2.destroyAllWindows()


def encode_image_to_base64(image_path):
    """Encode an image file as a Base64 string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def vision_brain(
    encoded_image,
    question="What is written in this image?",
    image_format="png",
):
    """Send an image and question to DeepInfra's vision model."""
    api_key = os.environ.get("DEEPINFRA_API_KEY")

    if not api_key:
        print(
            "Vision API error: DEEPINFRA_API_KEY is not configured "
            "in this terminal."
        )
        return None

    url = "https://api.deepinfra.com/v1/openai/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    image_format = image_format.lower()
    mime_type = (
        "image/jpeg"
        if image_format in ("jpg", "jpeg")
        else "image/png"
    )

    payload = {
        "model": "Qwen/Qwen3-VL-30B-A3B-Instruct",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{encoded_image}"
                        },
                    },
                    {
                        "type": "text",
                        "text": question,
                    },
                ],
            }
        ],
    }

    try:
        response = requests.post(
            url,
            headers=headers,
            json=payload,
            timeout=45,
        )
        response.raise_for_status()

        data = response.json()
        return data["choices"][0]["message"]["content"]

    except requests.HTTPError as e:
        if e.response is not None:
            status = e.response.status_code

            if status == 402:
                print(
                    "Vision API unavailable: DeepInfra account has "
                    "no available inference balance."
                )
                return (
                    "Screen analysis is unavailable because the configured "
                    "vision service has no available inference credits."
                )

            print(f"Vision API HTTP error: {status}")
            print("Server response:", e.response.text[:1000])
        else:
            print(f"Vision API HTTP error: {e}")

        return None

    except requests.RequestException as e:
        print(f"Vision API request failed: {e}")
        return None

    except (ValueError, KeyError, IndexError, TypeError) as e:
        print(f"Unexpected vision API response: {e}")
        return None
