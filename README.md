# Data Analysis Dashboard

A Streamlit-based dashboard for data analysis and visualization using LangChain and DeepSeek.

## Setup

1. Clone the repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your API keys:
     ```
     DEEPSEEK_API_KEY=your_deepseek_api_key_here
     LANGCHAIN_API_KEY=your_langchain_api_key_here
     ```

4. Run the application:
```bash
streamlit run data_analysis_streamlit_app.py
```

## Features

- Upload and analyze CSV files
- Interactive chat interface for data analysis
- Debug view for intermediate outputs
- Automatic data visualization
- Basic statistics and data preview

## Directory Structure

```
.
├── Pages/
│   ├── components/         # UI components
│   ├── services/          # Business logic services
│   ├── graph/             # LangChain graph components
│   └── prompts/           # System prompts
├── uploads/               # Uploaded files directory
├── .env                   # Environment variables (create from .env.example)
├── .env.example          # Environment variables template
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## Environment Variables

The following environment variables are required:

- `DEEPSEEK_API_KEY`: Your DeepSeek API key
- `LANGCHAIN_API_KEY`: Your LangChain API key

Optional environment variables:

- `LANGCHAIN_TRACING_V2`: Enable LangChain tracing (default: true)
- `LANGCHAIN_PROJECT`: LangChain project name (default: SANITY_ANALYSIS)
- `STREAMLIT_SERVER_MAX_UPLOAD_SIZE`: Maximum upload size in MB (default: 2000)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 