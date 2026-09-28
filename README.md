# Kling Video API Examples

Compare Kling text-to-video, image-to-video, and motion-control workflows through Muapi's unified API. This repository documents Muapi's Kling endpoints; it is not an official Kuaishou/Kling SDK or a direct connection to Kling's own API.

## Related Projects

- [Open-Generative-AI](https://github.com/Anil-matcha/Open-Generative-AI) — an open-source generative media application with multi-model workflows.
- [Kling-4-API](https://github.com/Anil-matcha/Kling-4-API) — examples for the Kling 4 video model family.
- [AI-Video-API](https://github.com/Anil-matcha/AI-Video-API) — cross-provider video generation API examples.

## Overview

- Kling API landing page: [Kling Video API on Muapi](https://muapi.ai/kling-api)
- API documentation: [Muapi API docs](https://muapi.ai/docs)
- Create an API key: [Muapi access keys](https://muapi.ai/access-keys)
- Website: [muapi.ai](https://muapi.ai)
- Kling 3.0 Pro text-to-video: [playground and API reference](https://muapi.ai/playground/kling-v3.0-pro-text-to-video/api)
- Kling 3.0 Pro image-to-video: [playground and API reference](https://muapi.ai/playground/kling-v3.0-pro-image-to-video/api)
- Kling 3.0 Pro motion control: [playground and API reference](https://muapi.ai/playground/kling-v3.0-pro-motion-control/api)
- Kling 3.0 Omni Pro text-to-video: [playground and API reference](https://muapi.ai/playground/kling-v3.0-omni-pro-text-to-video/api)

Muapi exposes these models through authenticated REST endpoints. Submit a generation request, retain its `request_id`, then poll the prediction result endpoint. Output and accepted request fields depend on the selected model. Use the linked model reference for the current schema and pricing before integrating.

## Endpoint comparison

| Workflow | Muapi endpoint | Use it for | Pricing |
|---|---|---|---|
| Text-to-video | `POST /api/v1/kling-v3.0-pro-text-to-video` | Generate a clip from a text prompt | Check the live model page |
| Image-to-video | `POST /api/v1/kling-v3.0-pro-image-to-video` | Animate a supplied image with a prompt | Check the live model page |
| Motion control | `POST /api/v1/kling-v3.0-pro-motion-control` | Motion-transfer workflows | Check the live model page |
| Omni text-to-video | `POST /api/v1/kling-v3.0-omni-pro-text-to-video` | Kling Omni video generation | Check the live model page |

The endpoints above are listed as live in Muapi's current Kling catalog. This README intentionally avoids fixed prices: model rates and options can change, and billing can depend on generation settings. Compare the current model pages for supported controls, output quality, latency, and cost using the same prompt and target format.

## Quickstart

Install the small example dependency and provide your own key in the environment:

```bash
python -m pip install -r requirements.txt
export MUAPI_API_KEY="your-api-key"
python examples/kling_video.py t2v
```

Do not commit API keys. The script supports `t2v`, `i2v`, and `motion` submission payloads. Replace the example image URL with an image URL accessible to the service for image-conditioned workflows. Confirm the current model page for required fields; payload schemas are endpoint-specific.

## cURL example

Submit a text-to-video job:

```bash
curl -X POST https://api.muapi.ai/api/v1/kling-v3.0-pro-text-to-video \
  -H "x-api-key: $MUAPI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"prompt":"A samurai walking through rainy Tokyo at night","duration":5,"aspect_ratio":"16:9"}'
```

The submission response contains a `request_id`. Poll for status and outputs:

```bash
curl "https://api.muapi.ai/api/v1/predictions/REQUEST_ID/result" \
  -H "x-api-key: $MUAPI_API_KEY"
```

## Request and response flow

All requests use `https://api.muapi.ai/api/v1` and authenticate with the `x-api-key` header. A successful submission returns a request identifier, typically as `request_id`. Poll `GET /predictions/{request_id}/result`; completed results include output URLs, while failed jobs return failure information. The example handles both terminal states and reports unexpected HTTP errors. Generation is asynchronous, so polling intervals and overall timeouts should suit your application.

The text-to-video sample sends `prompt`, `duration`, and `aspect_ratio`; the current schema also supports `generate_audio`. Image-to-video requires `prompt` and `image_url`, with optional `last_image`, `duration`, and `generate_audio`. Motion control requires both `image_url` and `video_url`, and accepts `character_orientation` (`image` or `video`) and `keep_original_sound`; the optional prompt describes desired motion. The Python example payloads follow the current Muapi schema examples. Review the endpoint references above before production use because schemas can change.

## Comparison checklist

When choosing among Kling workflows, compare:

1. **Input type:** prompt-only generation, a source image, or motion-driving inputs.
2. **Controls:** duration, aspect ratio, resolution, and any endpoint-specific reference inputs.
3. **Motion and consistency:** test camera movement, subject action, and identity consistency on representative prompts.
4. **Operational behavior:** submission latency, completion time, failures, and result retention in your application.
5. **Current cost:** verify each model's live Muapi pricing and options instead of assuming one fixed rate across tiers.

## Example

[`examples/kling_video.py`](examples/kling_video.py) is a Python submit-and-poll example for text-to-video, image-to-video, and motion control. It uses `requests`, reads the key from `MUAPI_API_KEY`, and does not download generated assets.
