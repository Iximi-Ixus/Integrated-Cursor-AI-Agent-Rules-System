# Cursor AI Agent Rules System - Examples

This document provides real-world examples of how to customize the Cursor AI Agent Rules System for different project types, technologies, and team scenarios.

## 📋 Table of Contents

- [Quick Setup Examples](#quick-setup-examples)
- [Technology Stack Examples](#technology-stack-examples)
- [Project Type Examples](#project-type-examples)
- [Team Configuration Examples](#team-configuration-examples)
- [Advanced Customization Examples](#advanced-customization-examples)

## Quick Setup Examples

### Example 1: React TypeScript Web App

**Project Context:**
- Frontend web application using React + TypeScript
- Team of 3 developers
- Uses Jest for testing, ESLint for linting
- Deploys to Vercel

**Key File Customizations:**

**010-cursor_general_rules.mdc:**
```yaml
[PROJECT_NAME] → "TaskManager WebApp"
[PROJECT_COMMAND_QUALITY] → "npm test && npm run lint && tsc --noEmit"
[MAIN_LANGUAGE] → "TypeScript"
```

**011-cursor_project_rules.mdc:**
```yaml
[TECH_STACK] → "React, TypeScript, Vercel"
[FRAMEWORK] → "React 18"
[MIN_VERSION] → "Node 18+"
[PACKAGE_MANAGER] → "npm"
```

**020-task_list.mdc sample tasks:**
```yaml
🔴 CRITICAL: User authentication system
🔴 CRITICAL: Task creation and management UI
🟡 HIGH: Responsive design implementation
🟡 HIGH: API integration for data persistence
🟢 MEDIUM: Testing suite setup
🟢 MEDIUM: Performance optimization
🔵 LOW: Dark mode theme
🔵 LOW: Mobile PWA features
```

### Example 2: Python FastAPI Backend

**Project Context:**
- REST API using Python + FastAPI
- Solo developer
- Uses pytest, black, mypy for quality
- Deploys to AWS Lambda

**Key File Customizations:**

**010-cursor_general_rules.mdc:**
```yaml
[PROJECT_NAME] → "E-commerce API"
[PROJECT_COMMAND_QUALITY] → "pytest && black --check . && mypy ."
[MAIN_LANGUAGE] → "Python"
```

**011-cursor_project_rules.mdc:**
```yaml
[TECH_STACK] → "FastAPI, PostgreSQL, AWS Lambda"
[FRAMEWORK] → "FastAPI"
[MIN_VERSION] → "Python 3.9+"
[PACKAGE_MANAGER] → "pip"
```

**020-task_list.mdc sample tasks:**
```yaml
🔴 CRITICAL: User authentication endpoints
🔴 CRITICAL: Product catalog API
🟡 HIGH: Order management system
🟡 HIGH: Payment processing integration
🟢 MEDIUM: API documentation with Swagger
🟢 MEDIUM: Database optimization
🔵 LOW: Admin dashboard API
🔵 LOW: Analytics endpoints
```

## Technology Stack Examples

### Python + Django

**011-cursor_project_rules.mdc customization:**
```python
# Core Technical Stack (Immutable)
Language: Python 3.9+
Framework: Django 4.2
Package Manager: pip
Testing: pytest, django-test-utils
Linting: flake8, pylint
Formatting: black
Type Checking: mypy
Dependencies: requirements.txt, requirements-dev.txt

# Quality Commands
pytest --cov=src/
black src/ --check
flake8 src/
mypy src/
python manage.py check

# Project Architecture
project_name/
├── apps/                      # Django applications
│   ├── users/                 # User management app
│   ├── core/                  # Core functionality
│   └── api/                   # API endpoints
├── config/                    # Django settings
├── static/                    # Static files
├── templates/                 # Django templates
└── requirements.txt           # Dependencies
```

### Node.js + Express + PostgreSQL

**011-cursor_project_rules.mdc customization:**
```javascript
# Core Technical Stack (Immutable)
Language: JavaScript (Node.js 18+)
Framework: Express.js
Database: PostgreSQL
Package Manager: npm
Testing: Jest, Supertest
Linting: ESLint
Formatting: Prettier
Dependencies: package.json

# Quality Commands
npm test
npm run lint
npm run format:check
npm audit

# Project Architecture
project_name/
├── src/
│   ├── controllers/           # Request handlers
│   ├── models/                # Database models
│   ├── routes/                # API routes
│   ├── middleware/            # Custom middleware
│   ├── services/              # Business logic
│   └── utils/                 # Utility functions
├── tests/                     # Test files
├── docs/                      # API documentation
└── package.json               # Dependencies and scripts
```

### Flutter Mobile App

**011-cursor_project_rules.mdc customization:**
```dart
# Core Technical Stack (Immutable)
Language: Dart 3.0+
Framework: Flutter 3.10+
Package Manager: pub
Testing: flutter_test, integration_test
Linting: dart analyze
Formatting: dart format
Dependencies: pubspec.yaml

# Quality Commands
flutter test
flutter analyze
dart format --output=none --set-exit-if-changed .
flutter build apk --debug

# Project Architecture
project_name/
├── lib/
│   ├── screens/               # App screens
│   ├── widgets/               # Reusable widgets
│   ├── models/                # Data models
│   ├── services/              # API and services
│   ├── utils/                 # Utility functions
│   └── main.dart              # App entry point
├── test/                      # Unit tests
├── integration_test/          # Integration tests
└── pubspec.yaml               # Dependencies
```

## Project Type Examples

### SaaS Application

**020-task_list.mdc example:**
```yaml
Strategic Vision Summary:
Primary Focus: Multi-tenant SaaS platform for project management
Core Strength: Real-time collaboration with intelligent automation
Target Audience: Small to medium businesses and development teams
Growth Strategy: Freemium model with enterprise features

🔴 CRITICAL PRIORITY - Immediate Development Focus
- User authentication and multi-tenancy
- Core project management features
- Real-time collaboration system
- Subscription and billing integration

🟡 HIGH PRIORITY - Core Enhancement
- Advanced project analytics
- Team permission management
- API for third-party integrations
- Mobile-responsive design

🟢 MEDIUM PRIORITY - Advanced Features
- Automated workflow triggers
- Time tracking and reporting
- Document management system
- White-label customization

🔵 LOW PRIORITY - Future Development
- Mobile native applications
- Advanced enterprise features
- Marketplace for extensions
- AI-powered project insights
```

### E-commerce Platform

**020-task_list.mdc example:**
```yaml
Strategic Vision Summary:
Primary Focus: Modern e-commerce platform with seamless checkout
Core Strength: Performance optimization and user experience
Target Audience: Online retailers and marketplace vendors
Growth Strategy: Commission-based revenue with premium features

🔴 CRITICAL PRIORITY - Immediate Development Focus
- Product catalog management
- Shopping cart and checkout flow
- Payment processing integration
- Order management system

🟡 HIGH PRIORITY - Core Enhancement
- User account management
- Inventory tracking system
- Shipping and fulfillment
- Admin dashboard for vendors

🟢 MEDIUM PRIORITY - Advanced Features
- Product recommendation engine
- Customer reviews and ratings
- Discount and promotion system
- Analytics and reporting

🔵 LOW PRIORITY - Future Development
- Mobile application
- Multi-vendor marketplace features
- International shipping and currency
- Advanced SEO optimization
```

### Data Science Platform

**020-task_list.mdc example:**
```yaml
Strategic Vision Summary:
Primary Focus: Self-service data analytics platform
Core Strength: Automated machine learning and visualization
Target Audience: Data analysts and business intelligence teams
Growth Strategy: Usage-based pricing with collaborative features

🔴 CRITICAL PRIORITY - Immediate Development Focus
- Data ingestion and cleaning pipeline
- Interactive data visualization
- Basic statistical analysis tools
- User workspace management

🟡 HIGH PRIORITY - Core Enhancement
- Automated machine learning workflows
- Collaborative analysis sharing
- Data source connectors
- Export and reporting system

🟢 MEDIUM PRIORITY - Advanced Features
- Advanced ML model deployment
- Real-time data streaming
- Custom visualization builders
- API for programmatic access

🔵 LOW PRIORITY - Future Development
- Enterprise security features
- Advanced model monitoring
- Data marketplace integration
- White-label deployment options
```

## Team Configuration Examples

### Solo Developer

**030-cursor_task_rules.mdc customization:**
```yaml
# Simplified workflow for individual developers
Task Completion Workflow:
- Implementation → "Ready for Review" (self-review)
- Personal verification → Mark "Completed"
- Immediate archival to completed tasks

Quality Gates:
- Automated testing and linting
- Personal code review checklist
- Documentation updates

Git Workflow:
- Feature branches for significant changes
- Direct commits for minor updates
- Release branches for version management
```

### Small Team (2-5 developers)

**030-cursor_task_rules.mdc customization:**
```yaml
# Collaborative workflow with peer review
Task Completion Workflow:
- Implementation → "Ready for Review"
- Peer review and approval
- Team lead marks "Completed"
- Weekly archival process

Quality Gates:
- Automated CI/CD pipeline
- Mandatory peer code review
- Integration testing
- Documentation review

Git Workflow:
- Feature branches for all changes
- Pull request with team review
- Protected main branch
- Staged deployment process
```

### Large Team (10+ developers)

**030-cursor_task_rules.mdc customization:**
```yaml
# Enterprise workflow with formal processes
Task Completion Workflow:
- Implementation → "Ready for Review"
- Technical review by senior developer
- Product owner approval
- DevOps team handles deployment
- Monthly archival and retrospective

Quality Gates:
- Multi-stage CI/CD pipeline
- Mandatory code review with 2 approvals
- Comprehensive testing suite
- Security and compliance checks
- Documentation and API review

Git Workflow:
- GitFlow with feature/develop/release/hotfix branches
- Formal pull request process
- Automated deployment pipelines
- Release management with changelogs
```

## Advanced Customization Examples

### Microservices Architecture

**040-cursor_organization_rules.mdc customization:**
```yaml
# Microservices project structure
project_name/
├── services/                   # Individual microservices
│   ├── user-service/
│   │   ├── src/
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   └── package.json
│   ├── product-service/
│   │   ├── src/
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   └── package.json
│   └── order-service/
├── shared/                     # Shared libraries and utilities
│   ├── common/
│   ├── types/
│   └── utils/
├── infrastructure/             # Infrastructure as code
│   ├── docker-compose.yml
│   ├── kubernetes/
│   └── terraform/
├── docs/                       # Service documentation
│   ├── api/
│   ├── architecture/
│   └── deployment/
└── scripts/                    # Deployment and maintenance scripts
```

### Multi-Environment Configuration

**021-cursor_environment_rules.mdc customization:**
```yaml
# Enhanced environment detection
Environment Detection:
- local: Default development (branch: feature/*)
- dev: Development server (branch: develop)
- test: Testing environment (branch: test)
- staging: Pre-production (branch: staging)
- prod: Production (branch: main/master)

Environment-Specific Behavior:
LOCAL:
  - Permissive error handling
  - Verbose logging
  - Hot reloading enabled
  - Test data seeding

DEV:
  - Moderate error handling
  - Debug logging
  - Continuous deployment
  - Shared development database

TEST:
  - Strict error handling
  - Automated testing
  - Clean database per test
  - Performance monitoring

STAGING:
  - Production-like configuration
  - Limited test data
  - Security scanning
  - Load testing

PROD:
  - Maximum error handling
  - Minimal logging
  - Monitoring and alerting
  - Backup and recovery
```

### Custom Quality Gates

**032-cursor_quality_rules.mdc customization:**
```yaml
# Industry-specific quality requirements

Healthcare/HIPAA Compliance:
🔴 CRITICAL Triggers:
- Any patient data handling code
- Authentication or authorization changes
- Database schema modifications
- API endpoint changes
- Third-party integrations

Additional Validation:
- HIPAA compliance review
- Security vulnerability scan
- Data encryption verification
- Audit trail validation
- Privacy impact assessment

Financial Services/SOX Compliance:
🔴 CRITICAL Triggers:
- Financial calculation logic
- User permission changes
- Data access modifications
- Reporting and analytics code
- Audit log implementations

Additional Validation:
- Financial accuracy testing
- Audit trail verification
- Security penetration testing
- Compliance documentation review
- Change approval workflow

Gaming/Performance Critical:
🔴 CRITICAL Triggers:
- Rendering or graphics code
- Game logic modifications
- Network synchronization changes
- Performance-critical algorithms
- Memory management updates

Additional Validation:
- Performance benchmarking
- Memory leak testing
- Cross-platform compatibility
- Network latency testing
- User experience validation
```

## Usage Tips

### Getting Started
1. **Start with similar examples**: Find the closest match to your project type
2. **Copy and adapt**: Use examples as starting points, don't start from scratch
3. **Test iteratively**: Implement one section at a time and test with your AI assistant
4. **Document changes**: Keep track of customizations that work well for your team

### Troubleshooting
- **If rules aren't loading**: Check file paths and extensions in examples above
- **If behavior is inconsistent**: Ensure placeholder replacement is complete
- **If quality gates aren't triggering**: Verify your quality commands are properly configured

### Advanced Usage
- **Multi-project setups**: Create project-specific rule variations
- **Team standards**: Share successful customizations with your team
- **Continuous improvement**: Update rules based on development patterns and lessons learned 