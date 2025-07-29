# VeriExCite with OpenRouter Support

## 🔗 Original Project Attribution

This project is a fork of [**VeriExCiting**](https://github.com/ykangw/VeriExCiting) by [@ykangw](https://github.com/ykangw).

**Original Project**: https://github.com/ykangw/VeriExCiting  
**Original Web App**: https://veriexcite.streamlit.app/  
**License**: AGPL-3.0

## 🆕 Added Features

This fork adds **OpenRouter API support** to the original VeriExCiting tool, providing access to multiple AI models:

### New Features Added:
- ✅ **OpenRouter Integration**: Support for multiple AI models via [OpenRouter](https://openrouter.ai/)
- ✅ **Model Selection**: Choose from Claude 3.5 Sonnet, GPT-4o, GPT-4o Mini, and more
- ✅ **Dual API Support**: Keep original Google Gemini support alongside OpenRouter
- ✅ **Improved JSON Parsing**: Better handling of different API response formats
- ✅ **Enhanced UI**: Updated interface for API provider and model selection
- ✅ **Better Error Handling**: More detailed error messages and debugging information

### Supported Models (via OpenRouter):
- **Claude 3.5 Sonnet** (anthropic/claude-3.5-sonnet)
- **Claude 3 Haiku** (anthropic/claude-3-haiku)  
- **GPT-4o** (openai/gpt-4o)
- **GPT-4o Mini** (openai/gpt-4o-mini)
- **GPT-4 Turbo** (openai/gpt-4-turbo)
- **Gemma 2 27B** (google/gemma-2-27b-it)
- **LLaMA 3.1 8B** (meta-llama/llama-3.1-8b-instruct)

## 🚀 Quick Start

### Prerequisites
- Python 3.13+ (recommended)
- Conda or virtual environment

### Installation

1. **Clone this repository**:
```bash
git clone <your-repo-url>
cd VeriExCiting-OpenRouter
```

2. **Create and activate environment**:
```bash
conda create -n veriexciting python=3.13 -y
conda activate veriexciting
```

3. **Install dependencies**:
```bash
pip install .
```

4. **Run the application**:
```bash
streamlit run streamlit_app.py
```

## 🔑 API Keys

### Option 1: OpenRouter (Recommended)
- Get your API key at [OpenRouter](https://openrouter.ai/)
- Supports multiple models with competitive pricing
- More reliable and flexible than single-provider APIs

### Option 2: Google Gemini (Original)
- Get your API key at [Google AI Studio](https://ai.google.dev/aistudio)
- Free tier: 1500 requests per day
- Original functionality from the base project

## 📖 How to Use

1. **Choose API Provider**: Select between OpenRouter or Google Gemini
2. **Select Model** (if using OpenRouter): Pick your preferred AI model
3. **Enter API Key**: Input your API key or use developer key for trial
4. **Upload PDF**: Upload one or more academic papers
5. **Start Verification**: Click to begin citation verification process

## 🎯 What This Tool Does

**VeriExCite** helps detect AI-generated fake citations in academic papers by:

- **Extracting** bibliography sections from PDF documents
- **Parsing** references using AI (now with multiple model options)
- **Verifying** citations against:
  - Crossref database
  - Google Scholar
  - ArXiv
  - Direct URL checking
- **Reporting** validation status with detailed explanations

## 📊 Understanding Results

- ✅ **Validated**: Citation found and verified in academic databases
- ❌ **Invalid**: Citation has errors (e.g., DOI mismatch)
- ⚠️ **Not Found**: Citation could not be verified (manual check recommended)

## 🤝 Contributing

This is a community fork focused on adding OpenRouter support. For core functionality improvements, please consider contributing to the [original project](https://github.com/ykangw/VeriExCiting).

For OpenRouter-specific features or bugs:
1. Fork this repository
2. Create a feature branch
3. Submit a pull request

## 📜 License

This fork maintains the same **AGPL-3.0 license** as the original project.

## 🙏 Acknowledgments

- **Original Author**: [@ykangw](https://github.com/ykangw) for creating VeriExCiting
- **Original Project**: [VeriExCiting](https://github.com/ykangw/VeriExCiting)
- **OpenRouter**: For providing multi-model API access
- **Community**: For testing and feedback

## 🔗 Links

- **Original Project**: https://github.com/ykangw/VeriExCiting
- **Original Web App**: https://veriexcite.streamlit.app/
- **OpenRouter**: https://openrouter.ai/
- **Google AI Studio**: https://ai.google.dev/aistudio

---

> **Note**: This fork focuses on adding OpenRouter support while maintaining all original functionality. For the most up-to-date core features, please check the [original repository](https://github.com/ykangw/VeriExCiting).