# Resume-to-Job Fit Quick Scorer

An AI-powered recruitment tool that automates resume screening with on-device LLM processing for privacy and speed.

## Features

- **Resume Upload**: Support for PDF/DOC formats with OCR processing
- **Job Description Matching**: Paste or upload job descriptions for comparison
- **AI-Powered Scoring**: 0-100 fit score with top 3 reasoning points
- **Batch Processing**: Process up to 25 resumes simultaneously
- **Export Results**: CSV/PDF export for further analysis
- **Privacy-First**: On-device AI processing with Ollama
- **Mobile-Friendly**: React Native interface for on-the-go screening

## Tech Stack

- **Frontend**: React Native
- **Backend**: Python (Flask)
- **Database**: SQLite (development) / PostgreSQL (production)
- **AI/ML**: Ollama (on-device LLM)
- **OCR**: Tesseract with document preprocessing
- **Mobile**: React Native with native modules

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 14+
- React Native CLI
- Ollama (for AI features)
- Tesseract OCR

### Installation

1. Clone and setup:
```bash
cd resume-job-fit-scorer
npm run install-all
```

2. Install Ollama and model:
```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama2:1b
```

3. Install Tesseract:
```bash
# Ubuntu/Debian
sudo apt-get install tesseract-ocr

# macOS
brew install tesseract
```

4. Start development servers:
```bash
npm run dev
```

5. For mobile development:
```bash
# Android
npx react-native run-android

# iOS
npx react-native run-ios
```

## Project Structure

```
resume-job-fit-scorer/
├── backend/                # Python Flask API
│   ├── models/            # Database models
│   ├── routes/            # API endpoints
│   ├── services/          # Business logic
│   ├── utils/             # Utility functions
│   ├── uploads/           # Resume storage
│   └── exports/           # Export files
├── mobile/                # React Native app
│   ├── src/
│   │   ├── components/    # Reusable components
│   │   ├── screens/       # App screens
│   │   ├── services/      # API calls
│   │   └── utils/         # Helper functions
│   ├── android/           # Android specific
│   └── ios/               # iOS specific
└── shared/                # Shared utilities
```

## MVP Features

✅ **Upload resumes (PDF/DOC) and paste job descriptions**  
✅ **On-device LLM extracts skills, experience, keywords**  
✅ **Generates 0-100 fit score with top 3 reasoning points**  
✅ **Batch process up to 25 resumes**  
✅ **Export results as CSV/PDF**  

## Development Timeline

- **Week 1**: Backend API and database setup
- **Week 2**: Resume parsing and OCR integration
- **Week 3**: AI/LLM integration for scoring
- **Week 4**: React Native mobile interface
- **Week 5**: Batch processing and optimization
- **Week 6**: Export functionality and testing
- **Week 7**: UI/UX polish and performance
- **Week 8**: Deployment and documentation

## License

This project is licensed under the ISC License.
