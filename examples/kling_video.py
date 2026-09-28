"""Submit and poll Kling video jobs through Muapi.

Usage: MUAPI_API_KEY=... python examples/kling_video.py [t2v|i2v|motion]
"""

import os
import sys
import time

import requests

BASE_URL = "https://api.muapi.ai/api/v1"
REQUESTS = {
    "t2v": (
        "kling-v3.0-pro-text-to-video",
        {"prompt": "A samurai walking through rainy Tokyo at night", "duration": 5, "aspect_ratio": "16:9"},
    ),
    "i2v": (
        "kling-v3.0-pro-image-to-video",
        {
            "prompt": "The camera slowly pushes in as the leaves move in the breeze",
            "image_url": "https://d3adwkbyhxyrtq.cloudfront.net/webassets/videomodels/kling-v3.0-pro-image-to-video1.jpg",
            "duration": 5,
            "aspect_ratio": "16:9",
        },
    ),
    "motion": (
        "kling-v3.0-pro-motion-control",
        {
            "prompt": "A performer follows the supplied motion reference",
            "image_url": "https://d3adwkbyhxyrtq.cloudfront.net/webassets/videomodels/kling-v3.0-pro-motion-control.png",
            "video_url": "https://d3adwkbyhxyrtq.cloudfront.net/webassets/videomodels/kling-v3.0-pro-motion-control-in.mp4",
            "character_orientation": "image",
            "keep_original_sound": True,
        },
    ),
}


def main():
    api_key = os.environ.get("MUAPI_API_KEY")
    if not api_key:
        raise SystemExit("Set MUAPI_API_KEY in your environment.")
    kind = sys.argv[1] if len(sys.argv) > 1 else "t2v"
    if kind not in REQUESTS:
        raise SystemExit(f"Choose one of: {', '.join(REQUESTS)}")

    endpoint, payload = REQUESTS[kind]
    headers = {"x-api-key": api_key}
    response = requests.post(f"{BASE_URL}/{endpoint}", headers=headers, json=payload, timeout=60)
    response.raise_for_status()
    submitted = response.json()
    request_id = submitted.get("request_id")
    if not request_id:
        raise SystemExit(f"Submission response did not include request_id: {submitted}")
    print(f"Submitted {endpoint}; request_id={request_id}")

    while True:
        result_response = requests.get(
            f"{BASE_URL}/predictions/{request_id}/result", headers=headers, timeout=60
        )
        result_response.raise_for_status()
        result = result_response.json()
        status = str(result.get("status", "")).lower()
        print(f"Status: {status or 'unknown'}")
        if status == "completed":
            print("Outputs:", result.get("outputs", result))
            return
        if status in {"failed", "error", "cancelled"}:
            print("Generation did not complete:", result)
            return
        time.sleep(5)


if __name__ == "__main__":
    main()
