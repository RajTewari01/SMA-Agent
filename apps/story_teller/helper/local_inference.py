"""
local_inference.py — Story Teller
================================

FEATURES:
    >>> Generates high-quality stories or poems by dynamically adjusting parameters based on user input.

    >>> If the genre or theme is not provided, it automatically retrieves suitable options
        from a JSON file or database and generates coherent content.

    >>> Ensures structured output formatting using Pydantic models and GBNF schemas
        for reliable JSON generation.

    >>> Optimized for low-end systems (e.g., GTX 1650) with efficient inference settings.

NOTES:
    - Replace the local model path with a higher-parameter model for improved quality.
    - Output quality depends heavily on the model used and parameter tuning.
    - GBNF is used to enforce strict output structure (especially useful for JSON consistency).
    - Designed for balance between performance and quality on limited hardware.
"""
