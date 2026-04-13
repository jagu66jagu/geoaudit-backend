from typing import Any
import anthropic
from app.core.config import settings

# Maps action_type to a system prompt
SYSTEM_PROMPTS: dict[str, str] = {
    "generate_wikidata_draft": (
        "You are a structured data expert. Generate a Wikidata-ready JSON draft "
        "for the given brand. Include required fields (P31, P856, P17, P452), "
        "list missing fields, and add review notes. Respond in Turkish."
    ),
    "generate_entity_page": (
        "You are a GEO content strategist. Generate a brand entity page draft "
        "that AI systems can easily parse. Include page structure, required sections, "
        "Organization schema, and improvement notes. Respond in Turkish."
    ),
    "generate_faq_block": (
        "You are a GEO content expert. Generate a FAQ block with 5 questions and answers "
        "optimized for AI citation. Include FAQPage schema markup. Respond in Turkish."
    ),
    "generate_schema_suggestion": (
        "You are a structured data expert. Generate JSON-LD schema markup suggestions "
        "for the given page. Include Organization, relevant type schema, and FAQPage. "
        "Respond in Turkish."
    ),
    "generate_internal_link_plan": (
        "You are an SEO strategist. Generate an internal linking plan for the given "
        "orphan pages. Include source page, anchor text, placement hint, and priority. "
        "Respond in Turkish."
    ),
    "generate_cms_draft": (
        "You are a content strategist. Generate a CMS-ready page draft with title, "
        "meta description, H1, and main content sections. Respond in Turkish."
    ),
    "create_task_payload": (
        "You are a project manager. Generate a structured task payload for the given "
        "finding. Include title, description, priority, effort, and acceptance criteria. "
        "Respond in Turkish."
    ),
}

def build_user_prompt(action_type: str, context_data: dict[str, Any]) -> str:
    brand = context_data.get("brandName", "Marka")
    domain = context_data.get("domain", "")
    industry = context_data.get("industry", "")
    issues = context_data.get("detectedIssues", [])

    base = f"Marka: {brand}\nDomain: {domain}\nSektör: {industry}\n"

    if issues:
        base += f"Tespit edilen sorunlar:\n"
        for issue in issues:
            base += f"- {issue}\n"

    # Add any extra context fields
    for k, v in context_data.items():
        if k not in ("brandName", "domain", "industry", "detectedIssues"):
            base += f"{k}: {v}\n"

    return base

async def run_action(
    action_type: str,
    finding_id: str,
    context_data: dict[str, Any],
) -> dict[str, Any]:

    system_prompt = SYSTEM_PROMPTS.get(action_type)
    if not system_prompt:
        raise ValueError(f"Unknown action type: {action_type}")

    user_prompt = build_user_prompt(action_type, context_data)

    client = anthropic.Anthropic(api_key=settings.anthropic_api_key)

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        messages=[{"role": "user", "content": user_prompt}],
        system=system_prompt,
    )

    content = message.content[0].text

    return {
        "action_type": action_type,
        "finding_id": finding_id,
        "format": "markdown",
        "title": f"{action_type.replace('_', ' ').title()} — {context_data.get('brandName', '')}",
        "preview": content[:300] + "..." if len(content) > 300 else content,
        "full_content": content,
        "metadata": {
            "model": "claude-sonnet-4-6",
            "input_tokens": message.usage.input_tokens,
            "output_tokens": message.usage.output_tokens,
            "confidence": 85,
            "missing_fields": [],
            "review_notes": [
                "AI tarafından üretilmiştir — inceleme yapınız",
                "Yayınlamadan önce doğrulayınız",
            ],
        },
        "export_options": ["copy", "json", "task"],
    }
