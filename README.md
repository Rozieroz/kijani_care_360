# KijaniCare360 🌳

**Building a Greener Kenya, One Tree at a Time**

A comprehensive tree conservation platform for Kenya featuring AI-powered tree expertise, community engagement, gamification, and real-time analytics. The platform combines modern web technologies with environmental science to promote sustainable forestry practices across Kenya.

##  Features

### Core Features
- **Tree Planting Streaks** - Track and maintain tree planting/watering streaks
- **AI Tree Expert** - LangChain + Groq powered chatbot for tree species advice
- **Community Forum** - Discussions, topics, and knowledge sharing
- **Analytics Dashboard** - Kenya forest coverage data and trends
- **Smart Notifications** - Watering reminders and community updates

###  Advanced Features
- **Gamification System** - Achievements, points, and leaderboards
- **Regional Recommendations** - Location-based tree species suggestions
- **Environmental Impact** - CO2 absorption and oxygen production calculations
- **User Growth Tracking** - Engagement metrics and community stats
- **Multilingual Support** - English and Swahili content

### User Experience
- **Modern React Frontend** - Responsive design with Tailwind CSS
- **Real-time Updates** - Live notifications and data synchronization
- **Interactive Charts** - Visual analytics with Chart.js
- **Mobile Optimized** - Progressive Web App capabilities
- **Smooth Animations** - Enhanced UX with Framer Motion

## Quick Start

### Prerequisites
- **Backend:** Python 3.8+, PostgreSQL 12+, Redis
- **Frontend:** Node.js 16+, npm/yarn

### Installation

#### 1. Clone Repository
```bash
git clone <repository-url>
cd kijanicare360
```

#### 2. Backend Setup
```bash
cd kijani360_backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Database setup
createdb kijanicare360

# Environment configuration
cp .env.example .env
# Edit .env with your settings

# Start backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### 3. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

### 🌐 Access Points
- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

## 🔧 Configuration

### Backend Environment Variables
```env
# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/kijanicare360

# Security
SECRET_KEY=your-super-secret-key-change-in-production

# AI/LLM
GROQ_API_KEY=your-groq-api-key-from-console.groq.com

# Optional
REDIS_URL=redis://localhost:6379/0
ENABLE_PUSH_NOTIFICATIONS=true
```

### Frontend Configuration
The frontend automatically connects to the backend API. Update the API base URL in the frontend configuration if needed.

## Tree Species Database

The platform includes comprehensive data for 8+ Kenyan tree species:

| Species | Common Name | Region | Use Case |
|---------|-------------|---------|----------|
| Grevillea robusta | Silky Oak | Central Kenya | Coffee intercropping |
| Melia volkensii | Mukau | Arid areas | Drought-resistant |
| Croton megalocarpus | - | Highlands | Biodiesel production |
| Markhamia lutea | Siala | Widespread | Agroforestry |
| Acacia species | - | Dry areas | Nitrogen-fixing |
| Prunus africana | - | Highlands | Medicinal |
| Terminalia brownii | - | Dry areas | Multipurpose |
| Casuarina equisetifolia | - | Coastal | Windbreak |

## Regional Coverage

- **Central Kenya** (Nairobi, Kiambu, Murang'a)
- **Western Kenya** (Kakamega, Bungoma, Vihiga)
- **Eastern Kenya** (Machakos, Kitui, Embu)
- **Rift Valley** (Nakuru, Eldoret, Narok)
- **Coast** (Mombasa, Kilifi, Kwale)
- **Nyanza** (Kisumu, Siaya, Migori)
- **Northern Kenya** (Turkana, Marsabit, Isiolo)

## Architecture

### Project Structure
```
kijanicare360/
├── frontend/                 # React frontend application
│   ├── src/
│   │   ├── components/       # Reusable UI components
│   │   ├── pages/           # Page components
│   │   ├── contexts/        # React contexts
│   │   └── utils/           # Utility functions
│   ├── public/              # Static assets
│   └── package.json
├── kijani360_backend/       # FastAPI backend application
│   ├── app/
│   │   ├── api/v1/endpoints/ # API route handlers
│   │   ├── core/            # Configuration & security
│   │   ├── database/        # Database connection
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Business logic
│   │   ├── agents/          # AI agents
│   │   └── utils/           # Utilities
│   ├── static/              # Static files
│   └── requirements.txt
└── README.md
```

### Technology Stack

#### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - Database ORM
- **PostgreSQL** - Primary database
- **Redis** - Caching and background tasks
- **LangChain** - AI agent framework
- **Groq** - LLM API for AI chatbot
- **Pydantic** - Data validation

#### Frontend
- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **Chart.js** - Data visualization
- **Framer Motion** - Animations
- **Lucide React** - Icon library

## API Endpoints

### Core Endpoints
```
GET  /api/v1/health                    # Health check
GET  /api/v1/analytics/tree-coverage   # Kenya forest data
POST /api/v1/chatbot/query            # AI tree expert
GET  /api/v1/forum/topics             # Community discussions
```

### Advanced Endpoints
```
GET  /api/v1/analytics/environmental-impact  # Environmental calculations
GET  /api/v1/forum/leaderboard              # Community rankings
POST /api/v1/notifications/                 # Smart notifications
GET  /api/v1/chatbot/recommendations        # Personalized suggestions
```

## Development

### Running Tests
```bash
# Backend tests
cd kijani360_backend
pytest

# Frontend tests (if configured)
cd frontend
npm test
```

### Code Formatting
```bash
# Backend
black app/
isort app/

# Frontend
npm run lint
npm run format
```

### Database Migrations
```bash
cd kijani360_backend
alembic revision --autogenerate -m "Description"
alembic upgrade head
```

## Production Deployment

### Docker Deployment
```dockerfile
# Backend Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

```dockerfile
# Frontend Dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
FROM nginx:alpine
COPY --from=0 /app/dist /usr/share/nginx/html
```

### Environment Setup
- Use strong SECRET_KEY in production
- Configure proper CORS origins
- Set up Redis for background tasks
- Configure push notification services
- Set up monitoring and logging
- Use environment-specific database URLs

### Build Commands
```bash
# Frontend production build
cd frontend
npm run build

# Backend production setup
cd kijani360_backend
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

### Development Guidelines
- Follow PEP 8 for Python code
- Use ESLint and Prettier for JavaScript/React code
- Write tests for new features
- Update documentation for API changes
- Ensure responsive design for frontend changes

## License

MIT License - see LICENSE file for details.

## Support & Contact  

 **Issues:** GitHub Issues


<!-- -  **Email:** support@kijanicare360.com
-  **Documentation:** /docs endpoint
-  **Website:** https://kijanicare360.com

<!-- ## 🙏 Acknowledgments -->

- Kenya Forest Service for forest coverage data
- Groq for AI/LLM capabilities
- Open source community for amazing tools and libraries
- Environmental conservation organizations in Kenya -->

---

**Made with ❤️ for Kenya's Environment** 🌳🇰🇪

*Join us in building a sustainable future through technology and community engagement.*