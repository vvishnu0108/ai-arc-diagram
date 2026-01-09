# Architecture Diagram Generator - Backend

**Current State**:
This is a simple implementation of an Architecture Diagram Generation Agent. It accepts natural language input and generates architecture diagrams using an agentic feedback loop with Meta's Llama 3.3 70B Instruct Model. The generated diagrams can be exported in multiple formats (PNG, DOT, Draw.io XML) and edited in an embedded Draw.io interface.

> **Note**: Currently utilizes NVIDIA APIs. **Refrain from uploading any Confidential Data as Input**. This is for demonstration purposes only.

**Future State/End State**:
Accept natural language prompts or IaC code uploads to generate live, editable diagrams with embedded Draw.io interface for real-time manual editing or AI-assisted modifications.

## Tech Stack
- **Framework**: Flask
- **Language**: Python 3.8+
- **LLM**: NVIDIA-hosted Meta Llama 3.3 70B Instruct (via LangChain)
- **Diagram Generation**: Python `diagrams` library
- **Diagram Export**: `graphviz2drawio` for Draw.io format conversion
- **API Communication**: REST API with JSON payloads

## Steps to Run

### Pre-requisites
- Git installed
- Python 3.8+ installed
- Python venv installed
- NVIDIA API key (for LLM access)
- Linux/WSL environment (for Graphviz support)

### Setup Instructions

1. **Clone the repository**
    ```bash
    git clone <repository-url>
    cd diagram-ui/backend
    ```

2. **Create and activate Python virtual environment**
    ```bash
    python3 -m venv venv
    
    # For Linux/macOS
    source venv/bin/activate
    
    # For Windows (Git Bash/WSL)
    source venv/Scripts/activate
    ```

3. **Install Python dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4. **Install system dependencies (Linux/WSL)**
    ```bash
    sudo apt update -y 
    sudo apt install -y graphviz graphviz-dev
    pip install graphviz2drawio
    ```

5. **Set up environment variables**
    ```bash
    export NVIDIA_API_KEY="your-nvidia-api-key-here"
    ```
    
    Or create a `.env` file in the backend directory:
    ```
    NVIDIA_API_KEY=your-nvidia-api-key-here
    ```

6. **Run the Flask server**
    ```bash
    python3 app.py
    ```
    
    The API will be available at `http://localhost:5000`

## API Endpoints

### Generate Diagram
**POST** `/api/generate`

Generate a new architecture diagram from a natural language prompt.

**Request:**
```json
{
  "prompt": "create a 2 tier architecture with load balancer and database"
}
```

**Response:**
```json
{
  "status": "success",
  "image_url": "/api/diagram/png",
  "drawio_url": "/api/diagram/drawio"
}
```

### Get PNG
**GET** `/api/diagram/png`

Retrieve the generated diagram as PNG image.

### Get Draw.io XML
**GET** `/api/diagram/drawio/xml`

Retrieve the generated diagram in Draw.io XML format for import into Draw.io desktop or web editor.

### Get Draw.io File
**GET** `/api/diagram/drawio`

Download the Draw.io file directly.

## Project Structure

```
backend/
├── app.py                      # Flask application
├── orchestrator.py             # Main pipeline orchestration
├── diagram_generator.py        # Diagram generation logic
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── detectors/
│   └── architecture_detector.py   # Architecture type detection
├── executors/
│   ├── code_executor.py        # Execute generated Python code
│   ├── diagram_runner.py       # Run diagram generation
│   └── drawio_exporter.py      # Export to Draw.io format
├── llm/
│   ├── client.py               # NVIDIA LLM integration
│   └── prompts/
│       └── sys_prompt.md       # System prompt for LLM
└── outputs/
    ├── diagram.py              # Generated Python code
    ├── diagram.dot             # Generated Graphviz DOT file
    ├── diagram.png             # Generated PNG image
    └── diagram.drawio          # Generated Draw.io XML
```

## How It Works

1. **Input**: User provides a natural language description of an architecture
2. **Detection**: System detects the architecture type (AWS, Azure, GCP, On-prem)
3. **Code Generation**: LLM generates Python code using the `diagrams` library
4. **Execution**: Generated code is executed to create PNG and DOT files
5. **Export**: DOT file is converted to Draw.io XML format
6. **Output**: User can download PNG, Draw.io file, or view in the web interface

## Error Handling

The backend includes comprehensive logging for debugging:
- API request/response logging
- Pipeline execution status
- File generation verification
- LLM retry logic for failed diagrams

Check the terminal output when running `python3 app.py` for detailed logs.

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `NVIDIA_API_KEY` | API key for NVIDIA-hosted LLM | Yes |

## Dependencies

Key Python packages:
- `flask` - Web framework
- `flask-cors` - CORS support
- `langchain` - LLM integration
- `langchain-nvidia-ai-endpoints` - NVIDIA API integration
- `diagrams` - Architecture diagram generation
- `graphviz2drawio` - Graphviz to Draw.io conversion

See `requirements.txt` for complete list.

## Troubleshooting

### "Invalid file" error when opening in DrawIO Desktop
- Ensure you're downloading from the `/api/diagram/drawio/xml` endpoint
- The file should open directly in DrawIO desktop

### Graphviz not found
- Ensure Graphviz is installed: `sudo apt install graphviz graphviz-dev`
- Verify with: `dot -V`

### NVIDIA API errors
- Check that `NVIDIA_API_KEY` is set correctly
- Verify API key is valid and has sufficient credits

### Diagrams library import errors
- Regenerate the diagram (the LLM will self-correct)
- Check the backend logs for the actual error

## Contributing

When making changes:
1. Keep all outputs in the `outputs/` directory
2. Maintain comprehensive logging for debugging
3. Test API endpoints before committing
4. Update this README with any new features

## License

See LICENSE file in the root repository.
