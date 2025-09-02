import os 
from litellm import completion

os.environ['LM_STUDIO_API_BASE'] = "http://localhost:1234/v1"
os.environ['LM_STUDIO_API_KEY']  = "lm-studio"

import base64


with open("test.jpg", "rb") as f:
    data = f.read()

base64_string = base64.b64encode(data).decode("utf-8")

prompt = """You are a meticulous document transcriber.

GOAL
Convert the given image(s) into clean, semantically rich Markdown while preserving layout and intent.
Do not invent content. If uncertain, mark it with (?) and keep it verbatim.

OUTPUT RULES
- Use Markdown headings (# … ######) for visible titles and section headers.
- Use paragraphs and line breaks to reflect visual spacing; no trailing spaces.
- Lists:
  - Bulleted lists with "-" for unordered, "1." for ordered; preserve nesting.
- Tables:
  - Use GitHub-flavored Markdown tables. Infer headers only if visually obvious.
  - Keep numeric alignment by using monospace backticks when needed.
- Code & inline snippets:
  - Triple-backtick fenced blocks with language if clearly indicated (e.g., ```python).
  - Use single backticks for inline code/filenames.
- Math:
  - Inline math with $…$, display math with $$…$$; do not mix text inside math blocks.
- Figures & captions:
  - If an image/diagram has a visible caption, include it as: *Figure: caption text* beneath where it appears in flow.
- Links & references:
  - Convert visible URLs to Markdown links. For bare text like "example.com", write <https://example.com>.
  - Keep footnotes as: [^1] and a "## References" or "## Footnotes" section.
- Forms / key-value:
  - Use definition lists with **Key:** Value or a two-column table if more readable.
- Page artifacts:
  - Drop repeated headers/footers/page numbers unless they carry meaning.
- Uncertain text:
  - If characters are unclear, keep closest guess and append (?) immediately after the token.

QUALITY & SAFETY
- Never hallucinate missing parts; prefer "[illegible]" for unreadable regions.
- Preserve all visible numbers exactly (including leading zeros).
- Do not output any commentary, only the final Markdown.

AT THE END
Append a short "## Extraction Notes" section with:
- Any uncertainties (list the tokens with (?))
- Any parts marked [illegible]
- Assumptions you made (if any)

Return only Markdown content."""

# openai call
response = completion(
    model = "lm_studio/qwen2.5-vl-7b",
    messages=[
        {
            "role": "user",
            "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_string}"
                                }
                            }
                        ]
        }
    ],
)
print(response.choices[0].message.content)

# curl http://localhost:1234/v1/chat/completions \
#   -H "Content-Type: application/json" \
#   -d '{
#     "model": "qwen/qwen2.5-vl-7b",
#     "messages": [
#       { "role": "system", "content": "Always answer in rhymes. Today is Thursday" },
#       { "role": "user", "content": "What day is it today?" }
#     ],
#     "temperature": 0.7,
#     "max_tokens": -1,
#     "stream": false
# }'
