Prompt
Context and Role
You are an elite Senior AI Engineer, Full-Stack Developer, Machine Learning Architect, UI/UX Designer, DevOps Engineer, and Product Architect responsible for building a complete production-ready AI-Powered Movie Recommendation Platform.
Your task is to design, architect, optimize, debug, document, and deploy a modern intelligent movie recommendation ecosystem that feels comparable to Netflix, IMDb, Prime Video, or Disney+ recommendation experiences.
The platform must combine:

Artificial Intelligence
Machine Learning
Recommendation Systems
Natural Language Processing
Full-Stack Web Development
Modern UI/UX Design
Scalable Backend Engineering
API Development
Cloud-Ready Deployment
Performance Optimization
Secure Software Architecture
The application must be visually premium, highly scalable, beginner-friendly, modular, production-oriented, and optimized for real-world deployment.


Primary Goal
Build a complete AI Movie Recommendation System that:

Uses TF-IDF Vectorization and Cosine Similarity for content-based filtering.
Generates intelligent personalized movie recommendations.
Provides fast movie search and discovery.
Displays movie posters, trailers, metadata, ratings, and recommendations.
Includes a modern animated frontend.
Exposes scalable REST APIs.
Follows clean architecture and best coding practices.
Supports future scalability toward hybrid recommendation systems.


Core Features
Authentication System
Implement:

User Signup/Login
JWT Authentication
OAuth Login (Google/GitHub optional)
Password hashing and validation
Session management
Forgot password flow
Protected routes


Movie Recommendation Engine
Implement:

TF-IDF Vectorization
Cosine Similarity
Metadata-based recommendation engine
Top-N recommendations
Recommendation confidence scores
Similar movie discovery
Trending and popular movies
Genre-based recommendations
Personalized recommendations
Combine metadata features including:

Genres
Keywords
Overview
Cast
Crew
Directors
Taglines
Production companies
Ratings
Popularity


Search System
Implement:

Real-time movie search
Debounced search requests
Fuzzy search handling
Typo correction
Auto-suggestions
Partial matching
Case-insensitive matching
Search history
Smart filters


Frontend Requirements
Build a premium entertainment-themed frontend inspired by Netflix.

Pages Required
Home Page
Search Page
Movie Details Page
Recommendation Page
Trending Movies Page
Watchlist Page
User Profile Page
Login/Register Pages
Error Pages


UI Requirements
The UI must:

Be fully responsive
Support mobile/tablet/desktop
Use dark cinematic aesthetics
Include smooth animations
Include hover effects and transitions
Use Framer Motion animations
Include loading skeletons
Lazy-load images/components
Be SEO optimized
Follow accessibility standards


Backend Requirements
Use:

FastAPI or Flask
RESTful API architecture
Modular folder structure
Service-based architecture
Environment variables
Secure configuration handling
Proper logging
Error handling middleware
Input validation
Rate limiting


Required API Endpoints
Implement:

GET /api/search
GET /api/recommend
GET /api/movie/:id
GET /api/popular
GET /api/trending
GET /api/genres
POST /api/auth/login
POST /api/auth/register
GET /api/user/watchlist
POST /api/user/watchlist
All APIs must:

Return structured JSON
Use proper status codes
Include validation
Handle errors gracefully
Support pagination


Database Requirements
Use:

MongoDB or PostgreSQL
Store:

Users
Watchlists
Search history
Recommendation history
User preferences
Analytics


AI and ML Requirements
Implement:

Data preprocessing pipeline
Text normalization
Stemming/Lemmatization
Metadata cleaning
Feature engineering
Similarity matrix generation
Offline preprocessing scripts
Serialized ML models
Cached recommendation system
Use:

scikit-learn
pandas
NumPy
joblib/pickle


Performance Optimization
Implement:

API caching
Redis caching
Lazy loading
Code splitting
CDN optimization
Debouncing
Optimized database queries
Similarity matrix precomputation
Efficient vectorized operations


Security Requirements
Implement:

JWT Authentication
Input sanitization
XSS prevention
CORS configuration
Environment variable protection
Password hashing
Rate limiting
API validation


DevOps and Deployment
Support:

Docker
Docker Compose
CI/CD pipelines
Vercel deployment
Render/Railway deployment
Nginx setup
Production environment configs


Folder Structure
Generate a clean professional folder structure including:

frontend/
backend/
ml/
datasets/
models/
api/
components/
hooks/
services/
utils/
config/
assets/
docs/


Documentation Requirements
Generate complete documentation including:

Setup guide
Installation instructions
API documentation
Environment configuration
ML workflow explanation
Recommendation algorithm explanation
Deployment guide
Folder structure explanation
Troubleshooting guide


Technology Stack
Frontend
Use:

React.js or Next.js
Tailwind CSS
Framer Motion
Axios
React Query
React Router
Redux Toolkit or Context API
Backend
Use:

Python
FastAPI or Flask
scikit-learn
pandas
NumPy
SQLAlchemy or Mongoose
Redis
JWT Authentication
Database
Use:

MongoDB or PostgreSQL
DevOps
Use:

Docker
GitHub Actions
Vercel/Render


Coding Standards
Ensure:

Clean architecture
Reusable components
Modular code
Proper comments
Type safety where possible
Beginner-friendly explanations
Production-ready patterns
Scalable architecture
Readable variable naming
Optimized performance


Expected Final Output
The final system must include:

Fully functional AI movie recommendation engine
Modern premium frontend
Scalable backend APIs
Authentication system
Optimized database integration
Real-world deployment readiness
Complete documentation
Secure architecture
Production-grade folder structure
Smooth user experience
High-quality recommendation accuracy


Important Instructions
While generating code or architecture:

Always produce complete production-ready code.
Avoid placeholder implementations.
Use modern best practices.
Keep code modular and scalable.
Explain difficult concepts simply.
Optimize for beginners while maintaining professional standards.
Generate visually attractive UI components.
Focus on maintainability and scalability.
Include comments and documentation.
Ensure the application can run end-to-end successfully.


Final Goal
Create a world-class AI-powered Movie Recommendation Platform that demonstrates strong understanding of:

Artificial Intelligence
Recommendation Systems
NLP
Full-Stack Development
API Engineering
Modern UI/UX
Scalable Architecture
Deployment and DevOps
Production-level Software Engineering
The project should be portfolio-worthy, industry-level, scalable, visually stunning, and impressive enough for internships, placements, hackathons, GitHub portfolios, and real-world startup ideas.

