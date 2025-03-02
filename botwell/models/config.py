"""
Model configuration and definitions for the Botwell test framework.
"""

# Model configurations - customize as needed
# Only models verified to work with OpenRouter are included
MODELS = [
    # Original models
    {"name": "GPT-4o", "model_id": "openai/gpt-4o"},
    {"name": "Claude-3-Opus", "model_id": "anthropic/claude-3-opus"},
    {"name": "Claude-3-Sonnet", "model_id": "anthropic/claude-3-sonnet"},
    {"name": "Claude-3.7-Sonnet", "model_id": "anthropic/claude-3.7-sonnet"},
    {"name": "Claude-3.7-Sonnet-thinking", "model_id": "anthropic/claude-3.7-sonnet:thinking"},
    {"name": "GPT-4o-mini", "model_id": "openai/gpt-4o-mini"},
    {"name": "Llama-3-8B", "model_id": "meta-llama/llama-3-8b-instruct"},
    {"name": "GPT-3.5-Turbo", "model_id": "openai/gpt-3.5-turbo"},
    {"name": "o3-mini-high", "model_id": "openai/o3-mini-high"},
    {"name": "o1", "model_id": "openai/o1"},
    {"name": "o1-mini", "model_id": "openai/o1-mini"},
    {"name": "DeepSeek-R1-Full", "model_id": "deepseek/deepseek-r1"},
    {"name": "DeepSeek-Distill-Qwen-32b", "model_id": "deepseek/deepseek-r1-distill-qwen-32b"},
    {"name": "grok2-1212", "model_id": "x-ai/grok-2-1212"},
    {"name": "grok-beta", "model_id": "x-ai/grok-beta"},
    {"name": "Qwen-Plus", "model_id": "qwen/qwen-plus"},
    {"name": "Qwen-Turbo", "model_id": "qwen/qwen-turbo"},
    {"name": "Qwen-Max", "model_id": "qwen/qwen-max"},
    {"name": "Perplexity: Llama 3.1 Sonar 70B", "model_id": "perplexity/llama-3.1-sonar-large-128k-chat"},
    {"name": "Perplexity: Llama 3.1 Sonar 8B Online", "model_id": "perplexity/llama-3.1-sonar-small-128k-online"},
    {"name": "Gemini Flash 2.0", "model_id": "google/gemini-2.0-flash-001"},
    {"name": "Gemini Pro 1.5", "model_id": "google/gemini-pro-1.5"},
    
    # New free models
    {"name": "Moonshot AI: Moonlight 16b A3b Instruct (free)", "model_id": "moonshotai/moonlight-16b-a3b-instruct:free"},
    {"name": "Nous: DeepHermes 3 Llama 3 8B Preview (free)", "model_id": "nousresearch/deephermes-3-llama-3-8b-preview:free"},
    {"name": "Google: Gemini Flash Lite 2.0 Preview (free)", "model_id": "google/gemini-2.0-flash-lite-preview-02-05:free"},
    {"name": "Google: Gemini Pro 2.0 Experimental (free)", "model_id": "google/gemini-2.0-pro-exp-02-05:free"},
    {"name": "Dolphin3.0 R1 Mistral 24B (free)", "model_id": "cognitivecomputations/dolphin3.0-r1-mistral-24b:free"},
    {"name": "DeepSeek: R1 (free)", "model_id": "deepseek/deepseek-r1:free"},
    {"name": "Mistral: Mistral Small 3 (free)", "model_id": "mistralai/mistral-small-24b-instruct-2501:free"},
    {"name": "Meta: Llama 3.1 8B Instruct (free)", "model_id": "meta-llama/llama-3.1-8b-instruct:free"},
    {"name": "Meta: Llama 3.3 70B Instruct (free)", "model_id": "meta-llama/llama-3.3-70b-instruct:free"},
    {"name": "NVIDIA: Llama 3.1 Nemotron 70B Instruct (free)", "model_id": "nvidia/llama-3.1-nemotron-70b-instruct:free"},
    {"name": "Mistral: Mistral Nemo (free)", "model_id": "mistralai/mistral-nemo:free"},
    {"name": "Meta: Llama 3.2 1B Instruct (free)", "model_id": "meta-llama/llama-3.2-1b-instruct:free"}
]


# Define a list of free/widely accessible models for use with the --free flag
FREE_MODELS = [
    # Original free models
    "GPT-4o-mini",
    "Llama-3-8B",
    "GPT-3.5-Turbo",
    "DeepSeek-Distill-Qwen-32b",
    "Qwen-Plus",
    "Qwen-Turbo",
    "Perplexity: Llama 3.1 Sonar 8B Online",
    "Gemini Flash 2.0",
    
    # Newer free models
    "Moonshot AI: Moonlight 16b A3b Instruct (free)",
    "Nous: DeepHermes 3 Llama 3 8B Preview (free)",
    "Google: Gemini Flash Lite 2.0 Preview (free)",
    "Google: Gemini Pro 2.0 Experimental (free)",
    "Dolphin3.0 R1 Mistral 24B (free)",
    "DeepSeek: R1 (free)",
    "Mistral: Mistral Small 3 (free)",
    "Meta: Llama 3.1 8B Instruct (free)",
    "Meta: Llama 3.3 70B Instruct (free)",
    "NVIDIA: Llama 3.1 Nemotron 70B Instruct (free)",
    "Mistral: Mistral Nemo (free)",
    "Meta: Llama 3.2 1B Instruct (free)"
]

# Define models to skip when using --free flag (premium models)
PREMIUM_MODELS = [
    "Claude-3-Opus",
    "Claude-3-Sonnet",
    "Claude-3.7-Sonnet",
    "Claude-3.7-Sonnet-thinking",
    "GPT-4o",
    "o3-mini-high",
    "o1",
    "o1-mini",
    "DeepSeek-R1-Full",
    "grok2-1212",
    "grok-beta",
    "Qwen-Max",
    "Perplexity: Llama 3.1 Sonar 405B Online",
    "Perplexity: Llama 3.1 Sonar 70B",
    "Gemini Pro 1.5"
]