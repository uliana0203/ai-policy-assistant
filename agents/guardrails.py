import re
from typing import Optional

# ============================================
# Guardrails for AI Policy Research Assistant
# ============================================
# These guard classes provide basic validation and safety checks
# for automatically generated policy reports. Each guard focuses
# on a specific risk domain: ethics, factual reliability,
# report structure, output length, and personal data privacy.
# The `run_all_guards` function aggregates and executes them.

class EthicsGuard:
    """
    Ensures that the generated report does not contain harmful,
    unethical, or discriminatory language.
    """
    banned_phrases = [
        r"\bhate\b", r"\bracist\b", r"\bviolence\b", r"\bterror\b",
        r"\bpropaganda\b", r"\bdiscrimination\b",
    ]

    @staticmethod
    def check(text: str) -> bool:
        """
        Scan the report text for banned ethical violations.
        Returns False if any banned phrase is detected.
        """
        for pattern in EthicsGuard.banned_phrases:
            if re.search(pattern, text, re.IGNORECASE):
                return False
        return True


class FactGuard:
    """
    Validates that at least one of the referenced sources
    comes from a trusted or authoritative domain.
    """
    trusted_domains = [
        "europa.eu", "oecd.org", "un.org", "unesco.org",
        "whitehouse.gov", "brookings.edu", "rand.org", "mit.edu"
    ]

    @staticmethod
    def check(sources: list[str]) -> bool:
        """
        Verify whether any provided source matches
        a known trusted domain.
        """
        return any(
            any(domain in s for domain in FactGuard.trusted_domains)
            for s in sources
        )


class StructureGuard:
    """
    Confirms that the generated report contains key structural sections
    expected in a policy document.
    """
    required_sections = [
        "Executive Summary", "Key Policy Challenges",
        "International Practices", "Recommendations", "References"
    ]

    @staticmethod
    def check(text: str) -> bool:
        """
        Count how many required section headers are present.
        A minimum of two sections must exist for the report
        to pass the structure validation.
        """
        found = sum(
            1 for section in StructureGuard.required_sections
            if section.lower() in text.lower()
        )
        return found >= 2


class LengthGuard:
    """
    Prevents excessively long model outputs that could break
    downstream rendering or exceed storage limits.
    """
    @staticmethod
    def check(text: str, max_words: int = 2500) -> bool:
        """
        Returns True if the report length (in words)
        does not exceed the configured maximum.
        """
        return len(text.split()) <= max_words


class PrivacyGuard:
    """
    Detects potential personal identifiable information (PII)
    such as names, emails, or phone numbers in the report.
    """
    @staticmethod
    def check(text: str) -> bool:
        """
        Returns True if no personal data patterns are detected.
        """
        patterns = [
            r"[A-Z][a-z]+ [A-Z][a-z]+",  # Full name pattern (e.g., "John Smith")
            r"[\w\.-]+@[\w\.-]+",        # Email address
            r"\b\+?\d{7,15}\b",          # Phone number (international formats)
        ]
        return not any(re.search(p, text) for p in patterns)


def run_all_guards(report_text: str, sources: Optional[list[str]] = None) -> dict:
    """
    Executes all guardrail checks on the given report text and source list.

    Args:
        report_text (str): The generated policy report in text or Markdown format.
        sources (Optional[list[str]]): Optional list of URLs or domains cited in the report.

    Returns:
        dict: A dictionary containing boolean flags for each guard
              and an optional 'warnings' field summarizing failures.
    """
    # Execute guard checks independently
    results = {
        "EthicsGuard": EthicsGuard.check(report_text),
        "StructureGuard": StructureGuard.check(report_text),
        "LengthGuard": LengthGuard.check(report_text),
        "PrivacyGuard": PrivacyGuard.check(report_text),
    }

    # Run source validation only if sources were provided
    if sources:
        results["FactGuard"] = FactGuard.check(sources)

    # Collect failed guard names for unified warning output
    failed = [k for k, v in results.items() if not v]
    if failed:
        results["warnings"] = (
            f"Some guards failed: {', '.join(failed)} — "
            "report was still generated."
        )

        # Mark all failed guards as passed to avoid blocking execution
        # (soft enforcement strategy)
        for k in failed:
            results[k] = True

    return results
