
import base64
from io import BytesIO

import pyautogui

from Vision.Vbrain import vision_brain


def analyze_screen(question: str) -> tuple[bool, str]:
    """
    Capture the desktop and ask the vision model a question.

    The screenshot is sent to the external vision service only when
    this function is called. It is not saved to a local image file.
    """
    try:
        screenshot = pyautogui.screenshot()

        image_buffer = BytesIO()
        screenshot.save(image_buffer, format="PNG")

        encoded_image = base64.b64encode(
            image_buffer.getvalue()
        ).decode("utf-8")

        answer = vision_brain(
            encoded_image,
            question=question,
            image_format="png",
        )

        if not answer:
            return False, (
                "I couldn't analyze your screen. "
                "The vision service may be unavailable."
            )

        if answer.startswith(
            "Screen analysis is unavailable because"
        ):
            return False, answer

        return True, answer

    except Exception as e:
        print(f"Screen intelligence error: {e}")
        return False, "I couldn't capture or analyze your screen."
