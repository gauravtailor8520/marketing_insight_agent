# Marketing Insight Agent 🚀

A sophisticated AI-powered marketing analytics platform that combines machine learning, knowledge graphs, and large language models to provide actionable marketing insights from campaign data.

## 🌟 Features

- **Intelligent CSV Processing**: Automated cleaning and normalization of marketing campaign data
- **Knowledge Graph Integration**: Neo4j-powered graph database for campaign relationships and insights
- **Hybrid Retrieval System**: Combines semantic search with graph-based concept filtering
- **AI-Powered Insights**: Gemini 2.0 Flash model for generating data-driven marketing recommendations
- **Self-Refining Analysis**: AI critiques and improves its own insights for better quality
- **Blog Content Integration**: Indexes marketing best practices from blog content
- **RESTful API**: FastAPI-based web service for easy integration
- **Performance Testing**: Built-in evaluation metrics and benchmarking

## 🏗️ Architecture

```
marketing_insight_agent/
├── agents/                 # Core AI agents and processing logic
│   ├── csv_loader.py      # CSV cleaning and normalization
│   ├── insight_generator.py # Main LangGraph pipeline
│   ├── kg_ingest.py       # Neo4j knowledge graph ingestion
│   ├── retriever.py       # Hybrid retrieval (Graph + Vector)
│   └── self_refine.py     # Self-improvement feedback loop
├── apps/                  # FastAPI application
│   ├── config.py          # Configuration management
│   ├── main.py            # API endpoints
│   └── schemas.py         # Pydantic models
├── blogs/                 # Blog content processing
│   ├── fetch_blogs.py     # Blog content fetching
│   ├── index_blogs.py     # ChromaDB vector indexing
│   └── chroma_index/      # Vector database storage
├── evals/                 # Evaluation and testing
│   ├── eval_metric.py     # Custom evaluation metrics
│   ├── test_ragas.py      # RAGAS evaluation
│   ├── test_rouge.py      # ROUGE scoring
│   └── test_speed.py      # Performance benchmarking
├── knowledge/             # Knowledge graph initialization
│   └── init_neo4j.py      # Neo4j schema setup
└── tmp/                   # Temporary file storage
    └── csvs/              # Uploaded CSV files
```

## 🛠️ Technology Stack

- **Backend**: FastAPI, Python 3.11+
- **AI/ML**: LangChain, LangGraph, Google Gemini 2.0 Flash
- **Databases**: 
  - Neo4j (Knowledge Graph)
  - ChromaDB (Vector Database)
- **Data Processing**: Pandas, NumPy
- **Testing**: Pytest, RAGAS, ROUGE
- **Deployment**: Docker, Uvicorn

## 📋 Prerequisites

- Python 3.11 or higher
- Neo4j database instance
- Google Cloud API key for Gemini
- Docker (optional, for containerized deployment)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd marketing_insight_agent
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Setup

Create a `.env` file in the root directory:

```env
# Google AI API
GOOGLE_API_KEY=your_gemini_api_key_here

# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=your_neo4j_password
```

### 4. Initialize Knowledge Graph

```bash
python knowledge/init_neo4j.py
```

### 5. Index Blog Content

```bash
python blogs/fetch_blogs.py
python blogs/index_blogs.py
```

### 6. Start the API Server

```bash
python apps/main.py
```

The API will be available at `http://localhost:8000`

## 📊 API Usage

### Upload CSV Data

```bash
curl -X POST "http://localhost:8000/upload-csv" \
  -F "file=@your_marketing_data.csv"
```

### Get Marketing Insights

```bash
curl -X POST "http://localhost:8000/run-agent" \
  -F "question=What are the top performing campaigns?" \
  -F "file_name=your_marketing_data.csv"
```

### API Documentation

Visit `http://localhost:8000/docs` for interactive Swagger documentation.

## 📈 CSV Data Format

The system expects marketing campaign CSV files with the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| `campaign_id` | Unique campaign identifier | "CAMP_001" |
| `company` | Company/brand name | "TechCorp" |
| `campaign_type` | Type of campaign | "Search", "Display", "Social" |
| `target_audience` | Target demographic | "25-34 Tech Workers" |
| `channel_used` | Marketing channel | "Google Ads", "Facebook" |
| `date` | Campaign date | "2024-01-15" |
| `acquisition_cost` | Cost per acquisition | "$25.50" |
| `clicks` | Number of clicks | 1250 |
| `impressions` | Number of impressions | 50000 |
| `conversion_rate` | Conversion percentage | 0.025 |
| `roi` | Return on investment | 2.5 |
| `engagement_score` | Engagement metric | 0.85 |

## 🧪 Testing and Evaluation

### Run Performance Tests

```bash
pytest evals/test_speed.py -v
```

### Evaluate with RAGAS

```bash
python evals/test_ragas.py
```

### ROUGE Score Analysis

```bash
python evals/test_rouge.py
```

## 🐳 Docker Deployment

### Build and Run

```bash
docker build -t marketing-insight-agent .
docker run -p 8000:8000 --env-file .env marketing-insight-agent
```

### Docker Compose (with Neo4j)

```yaml
version: '3.8'
services:
  neo4j:
    image: neo4j:latest
    ports:
      - "7474:7474"
      - "7687:7687"
    environment:
      NEO4J_AUTH: neo4j/password
    
  app:
    build: .
    ports:
      - "8000:8000"
    depends_on:
      - neo4j
    env_file:
      - .env
```

## 🔧 Configuration

### Key Configuration Options

- **Model Settings**: Adjust temperature and token limits in `agents/insight_generator.py`
- **Retrieval Parameters**: Modify search limits in `agents/retriever.py`
- **Data Processing**: Customize column mappings in `agents/csv_loader.py`
- **Embedding Model**: Change embedding model in `blogs/index_blogs.py`

## 📚 Key Components

### CSV Loader (`agents/csv_loader.py`)
- Standardizes column names
- Cleans monetary values
- Handles missing data
- Computes derived metrics (CTR)

### Insight Generator (`agents/insight_generator.py`)
- Main LangGraph pipeline
- Integrates CSV analysis with blog insights
- Uses Gemini 2.0 Flash for reasoning

### Knowledge Graph Ingestion (`agents/kg_ingest.py`)
- Creates campaign and metric nodes
- Establishes relationships
- Enables graph-based queries

### Hybrid Retriever (`agents/retriever.py`)
- Combines graph traversal with semantic search
- Filters relevant blog content
- Provides context for insights

### Self-Refine (`agents/self_refine.py`)
- Critiques initial responses
- Improves clarity and actionability
- Ensures data-grounded insights

## 🎯 Use Cases

1. **Campaign Performance Analysis**: Identify top-performing campaigns and optimization opportunities
2. **Audience Insights**: Discover which audiences respond best to different campaign types
3. **Channel Optimization**: Compare performance across marketing channels
4. **ROI Analysis**: Calculate and improve return on investment
5. **Trend Detection**: Identify seasonal patterns and trends
6. **Creative Performance**: Analyze which creative elements drive engagement

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

For questions, issues, or contributions:

- Open an issue on GitHub
- Check the [documentation](http://localhost:8000/docs) when running locally
- Review the evaluation results in the `evals/` directory

## 🔮 Roadmap

- [ ] Real-time campaign monitoring
- [ ] Advanced visualization dashboard
- [ ] Multi-language support
- [ ] Integration with popular marketing platforms
- [ ] Advanced anomaly detection
- [ ] Automated report generation
- [ ] A/B testing recommendations

---

Built with ❤️ using LangChain, Gemini AI, and modern Python technologies.
