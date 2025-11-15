# 📄 ArXiv Paper Extractor

A Streamlit application that extracts and analyzes key insights from academic research papers using AI. Simply provide an arXiv link or upload a PDF to get a structured analysis of the paper.

## Features

- 📥 **Multiple Input Methods**:
  - Download papers directly from arXiv using URL or ID
  - Upload PDF files from your local system

- 🤖 **AI-Powered Analysis**:
  - Uses Anthropic Claude to extract structured insights
  - Analyzes papers across 7 key dimensions

- 📊 **Structured Output**:
  - Background of the study
  - Research objectives and hypothesis
  - Methodology
  - Results and findings
  - Discussion and interpretation
  - Contributions to the field
  - Achievements and significance

- 💾 **Export Functionality**:
  - Download analysis results as JSON
  - Timestamped exports for record-keeping

## Installation

### Prerequisites

- Python 3.8 or higher
- Anthropic API key ([Get one here](https://console.anthropic.com/))

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd arxiv-extractor
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure your API key:

Create a `.env` file in the project root:
```bash
cp .env.example .env
```

Edit `.env` and add your API key:
```
ANTHROPIC_API_KEY=your_api_key_here
```

Alternatively, you can enter the API key directly in the app's sidebar.

## Usage

1. Start the Streamlit app:
```bash
streamlit run app.py
```

2. The app will open in your browser (usually at `http://localhost:8501`)

3. Choose your input method:
   - **ArXiv URL**: Enter an arXiv URL (e.g., `https://arxiv.org/abs/2301.00001`) or just the ID (e.g., `2301.00001`)
   - **Upload PDF**: Upload a PDF file from your computer

4. Click "Extract Insights" to analyze the paper

5. Review the structured analysis and download as JSON if needed

## Example ArXiv Papers to Try

- `2301.00001` - Machine Learning paper
- `https://arxiv.org/abs/2212.08073` - ChatGPT paper
- `https://arxiv.org/abs/2303.08774` - GPT-4 paper

## Project Structure

```
arxiv-extractor/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env.example        # Example environment configuration
├── .env               # Your API keys (create this, not tracked in git)
└── README.md          # This file
```

## How It Works

1. **PDF Acquisition**: Downloads PDF from arXiv or accepts uploaded file
2. **Text Extraction**: Extracts text content using PyPDF2
3. **AI Analysis**: Sends text to Anthropic Claude with structured prompt
4. **Result Display**: Parses and displays the analysis in organized sections
5. **Export**: Allows downloading complete analysis as JSON

## Configuration

### API Key Options

You can provide your Anthropic API key in two ways:

1. **Environment Variable** (recommended):
   - Add `ANTHROPIC_API_KEY` to your `.env` file
   - The app will load it automatically

2. **Sidebar Input**:
   - Enter your API key in the sidebar when running the app
   - Useful for testing or temporary usage

### Model Configuration

The app uses `claude-3-5-sonnet-20241022` by default. To use a different model, edit the `model` parameter in `app.py`:

```python
message = client.messages.create(
    model="claude-3-5-sonnet-20241022",  # Change this
    max_tokens=4096,
    messages=[...]
)
```

## Troubleshooting

### PDF Download Fails
- Check your internet connection
- Verify the arXiv ID is correct
- Some papers may have access restrictions

### Text Extraction Issues
- Some PDFs may have formatting that makes extraction difficult
- Try downloading the PDF manually and uploading it
- Ensure the PDF is not password-protected

### API Errors
- Verify your API key is valid
- Check your API usage limits
- Ensure you have sufficient credits

### JSON Export Issues
- Check browser download settings
- Ensure pop-ups are not blocked
- Try a different browser if issues persist

## Dependencies

- **streamlit**: Web application framework
- **PyPDF2**: PDF text extraction
- **requests**: HTTP requests for downloading papers
- **anthropic**: Anthropic Claude API client
- **python-dotenv**: Environment variable management

## Limitations

- Text extraction quality depends on PDF formatting
- Analysis limited by AI model token limits (~50,000 characters)
- Some complex equations or figures may not be captured in text extraction

## Future Enhancements

- [ ] Support for multiple AI providers (OpenAI, Google, etc.)
- [ ] Batch processing of multiple papers
- [ ] Citation network visualization
- [ ] Export to other formats (Markdown, Word, PDF)
- [ ] Save analysis history
- [ ] Compare multiple papers

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

MIT License - feel free to use this project for your research and development needs.

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Built with Streamlit • Powered by Anthropic Claude**
