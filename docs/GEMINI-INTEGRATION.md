# Google Gemini Integration for Agent3D DDD Framework

This document explains how to use Google Gemini instead of Anthropic Claude for running the Agent3D Documentation-Driven Development (DDD) framework.

## Overview

The Agent3D framework now supports **Google Gemini** as an alternative to Anthropic Claude for powering the SWE-bench agent and orchestrator. This provides:

- **Cost-effective alternative**: Gemini often has more competitive pricing
- **High performance**: Gemini 1.5 Pro offers excellent code generation capabilities
- **Large context window**: Gemini 1.5 Pro supports up to 2M tokens context
- **Automatic fallback**: System automatically falls back to Claude if Gemini is unavailable

## Setup Instructions

### 1. Get Google AI API Key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key

### 2. Set Environment Variable

```bash
# Set the Google API key
export GOOGLE_API_KEY="your_google_api_key_here"

# Verify it's set
echo $GOOGLE_API_KEY
```

### 3. Install Dependencies

The Google AI package should already be installed, but if needed:

```bash
cd ~/.agent3d
source venv/bin/activate
pip install google-generativeai
```

## Usage

### Running Full DDD Pass with Gemini

Once you have the `GOOGLE_API_KEY` set, you can run the DDD pass normally:

```bash
cd ~/.agent3d

# Using the shell script (recommended)
./ddd-pass.sh --task "Execute comprehensive DDD pass" --mode complete --verbose

# Or using Python directly
python run_full_ddd_pass.py --task "Execute comprehensive DDD pass" --mode complete --verbose
```

### API Provider Priority

The system automatically selects the LLM provider in this order:

1. **Google Gemini** (if `GOOGLE_API_KEY` is set)
2. **Anthropic Claude** (if `ANTHROPIC_API_KEY` is set)
3. **Error** (if neither is available)

### Checking Which Provider is Being Used

The system will log which provider it's using:

```
✅ Using Google Gemini for SWE-bench agent
```

or

```
✅ Using Anthropic Claude for SWE-bench agent
```

## Gemini Models Supported

The integration currently uses:

- **Default**: `gemini-1.5-pro` - Best balance of performance and cost
- **Alternative**: `gemini-1.5-flash` - Faster and cheaper for simpler tasks

To change the model, modify the `model_name` parameter in `agents/orchestrator/tools.py`:

```python
llm_client = GeminiDirectClient(
    model_name="gemini-1.5-flash",  # Change this
    max_retries=2
)
```

## Features and Limitations

### ✅ Supported Features

- **Text generation**: Full support for code generation and analysis
- **System prompts**: Converted to conversation format
- **Multi-turn conversations**: Full conversation history support
- **Error handling**: Automatic retries with exponential backoff
- **Token counting**: Input/output token tracking for cost monitoring

### ⚠️ Limitations

- **Tool calling**: Not yet implemented (planned for future release)
- **Thinking tokens**: Not supported (Gemini doesn't have this feature)
- **Caching**: No prompt caching equivalent to Claude's system

### 🔄 Automatic Fallbacks

If Gemini fails or is unavailable, the system will:

1. Log the failure reason
2. Attempt to use Anthropic Claude if available
3. Use mock execution if no LLM is available

## Cost Comparison

Approximate costs (as of 2024):

| Provider | Model | Input (per 1M tokens) | Output (per 1M tokens) |
|----------|-------|----------------------|------------------------|
| Google | Gemini 1.5 Pro | $1.25 | $5.00 |
| Google | Gemini 1.5 Flash | $0.075 | $0.30 |
| Anthropic | Claude 3.5 Sonnet | $3.00 | $15.00 |

*Note: Prices may vary. Check current pricing on respective provider websites.*

## Troubleshooting

### Common Issues

1. **"GOOGLE_API_KEY not found"**
   ```bash
   export GOOGLE_API_KEY="your_api_key_here"
   ```

2. **"google-generativeai package required"**
   ```bash
   pip install google-generativeai
   ```

3. **API quota exceeded**
   - Check your Google AI Studio quota limits
   - Consider upgrading to paid tier if needed

4. **Import errors**
   ```bash
   # Reinstall the package
   pip uninstall google-generativeai
   pip install google-generativeai
   ```

### Debug Mode

Run with verbose logging to see detailed information:

```bash
./ddd-pass.sh --verbose
```

This will show:
- Which LLM provider is being used
- Token usage statistics
- API call details
- Error messages with full stack traces

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Google AI API key | Yes (for Gemini) |
| `ANTHROPIC_API_KEY` | Anthropic API key | No (fallback) |

### Model Configuration

Edit `agents/orchestrator/tools.py` to customize:

```python
# Gemini configuration
llm_client = GeminiDirectClient(
    model_name="gemini-1.5-pro",  # or "gemini-1.5-flash"
    max_retries=2
)
```

## Integration Details

### Architecture

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   DDD Pass      │───▶│   Orchestrator   │───▶│  SWE-bench      │
│   Script        │    │                  │    │  Agent          │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │                        │
                                ▼                        ▼
                       ┌──────────────────┐    ┌─────────────────┐
                       │  LLM Provider    │    │  Gemini Client  │
                       │  Selection       │───▶│                 │
                       └──────────────────┘    └─────────────────┘
```

### Code Locations

- **Gemini Client**: `agents/swebench/utils/llm_client.py` (GeminiDirectClient class)
- **Provider Selection**: `agents/orchestrator/tools.py` (SWEBenchTool._initialize_agent)
- **Configuration**: `run_full_ddd_pass.py` and `ddd-pass.sh`

## Next Steps

1. **Set up your Google API key** following the instructions above
2. **Run a test DDD pass** to verify everything works
3. **Monitor token usage** to optimize costs
4. **Provide feedback** on performance compared to Claude

For questions or issues, check the troubleshooting section or review the logs in `.agent3d-tmp/logs/`.
