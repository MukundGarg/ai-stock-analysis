# StockSense AI - Frontend Project

A modern, AI-powered stock market learning platform built with Next.js, TailwindCSS, and TypeScript.

## Project Overview

StockSense AI is an educational platform designed to teach beginners how the stock market works. Stage 1 focuses on building the complete frontend structure and UI layout using modern web technologies.

## Features

### 5 AI-Powered Learning Tools:

1. **📄 PDF Financial Report Explainer** - Upload and analyze financial documents with AI-powered explanations
2. **📊 Chart Pattern Analyzer** - Learn technical analysis with pattern recognition
3. **📈 Market Sentiment AI** - Track real-time market sentiment and investor psychology
4. **🎮 AI Trade Simulator** - Practice trading with virtual capital, risk-free
5. **🔍 Stock Movement Analysis** - Understand why stocks are moving

## Tech Stack

- **Frontend Framework**: Next.js 16.2.3 (App Router)
- **Styling**: TailwindCSS
- **Language**: TypeScript
- **Package Manager**: npm
- **UI Components**: Custom components (shadcn/ui ready)

## Project Structure

```
stocksense-ai/
├── app/
│   ├── layout.tsx                 # Root layout with Navbar & Footer
│   ├── page.tsx                  # Home page (/)
│   ├── globals.css               # Global styles
│   ├── features/
│   │   └── page.tsx              # Features page (/features)
│   └── dashboard/
│       ├── page.tsx              # Dashboard main page (/dashboard)
│       ├── pdf/
│       │   └── page.tsx          # PDF analyzer tool (/dashboard/pdf)
│       ├── chart/
│       │   └── page.tsx          # Chart analyzer tool (/dashboard/chart)
│       ├── sentiment/
│       │   └── page.tsx          # Sentiment analyzer tool (/dashboard/sentiment)
│       ├── simulator/
│       │   └── page.tsx          # Trade simulator tool (/dashboard/simulator)
│       └── movement/
│           └── page.tsx          # Movement analysis tool (/dashboard/movement)
├── components/
│   ├── Navbar.tsx                # Navigation bar with mobile menu
│   ├── Footer.tsx                # Footer with links and disclaimer
│   ├── FeatureCard.tsx           # Reusable feature card component
│   └── ToolCard.tsx              # Reusable tool card component
├── public/                        # Static assets
├── package.json                   # Dependencies
├── tailwind.config.ts             # TailwindCSS configuration
├── tsconfig.json                  # TypeScript configuration
└── next.config.ts                 # Next.js configuration
```

## Getting Started

### Installation

1. **Navigate to the project directory**:
   ```bash
   cd "/Users/mukundgarg/Desktop/Stock Market Ai/stocksense-ai"
   ```

2. **Install dependencies** (already installed):
   ```bash
   npm install
   ```

### Development

**Start the development server**:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

### Build for Production

**Create an optimized production build**:
```bash
npm run build
```

**Start the production server**:
```bash
npm start
```

### Other Commands

```bash
# Run linter
npm run lint

# Run TypeScript type checking
npm run type-check
```

## Pages Overview

### Home Page (`/`)
- Hero section with compelling headline
- Feature highlights preview
- Quick statistics
- Call-to-action buttons
- Modern gradient background

### Features Page (`/features`)
- Detailed explanation of all 5 tools
- Feature cards with icons and descriptions
- How each tool works section
- Learning methodology
- Call-to-action

### Dashboard Page (`/dashboard`)
- Main user workspace
- Five tool cards linking to individual tools
- Getting started guide
- Learning tips
- Learning resources section
- Educational content links

### Tool Pages

#### PDF Analyzer (`/dashboard/pdf`)
- File upload area
- Feature showcase
- Pro tips sidebar
- Supported documents list

#### Chart Analyzer (`/dashboard/chart`)
- Stock symbol input
- Chart visualization area
- Common pattern explanations
- Timeframe selection
- Pattern learning guide

#### Market Sentiment (`/dashboard/sentiment`)
- Overall sentiment indicator
- Fear & Greed index
- Sector-wise sentiment
- Key sentiment drivers
- Bullish/Bearish indicators

#### Trade Simulator (`/dashboard/simulator`)
- Portfolio overview
- Trading execution panel
- Holdings display
- Performance metrics
- AI recommendations
- Trading rules guide

#### Stock Movement Analysis (`/dashboard/movement`)
- Stock search functionality
- Price chart display
- Key catalysts listing
- Impact assessment
- AI forecast
- Historical context

## Design Features

### Modern Fintech UI
- Clean, minimal design aesthetic
- Dark/Light mode support
- Professional color scheme (Blue & Purple gradients)
- Card-based layouts
- Responsive grid system
- Smooth transitions and hover effects

### Components

**Navbar**
- Sticky navigation bar
- Logo with gradient background
- Mobile hamburger menu
- Active page highlighting
- Dashboard CTA button

**Footer**
- Multi-column link structure
- Important disclaimer section
- Social media links
- Copyright information
- Dark mode support

**FeatureCard**
- Icon display
- Title and description
- Hover effects
- Border transitions

**ToolCard**
- Large icon display
- Title, description, benefits
- "Open Tool" button
- Flexible card layout

## Customization

### Colors

Edit the TailwindCSS color scheme in `tailwind.config.ts`:
- Primary: Blue (`from-blue-600` to `to-blue-700`)
- Secondary: Purple (`from-purple-600` to `to-purple-700`)
- Backgrounds: White/Black with gray variants

### Typography

All fonts use Next.js default fonts (Geist Sans and Geist Mono).

### Spacing & Layout

- Max-width: 7xl (1280px) for content containers
- Padding: Standard TailwindCSS scale
- Grid gaps: 6-8px
- Border radius: lg (8px) and xl (12px)

## Browser Support

- Modern browsers (Chrome, Firefox, Safari, Edge)
- Mobile responsive design
- Touch-friendly interface

## Future Enhancements (Stage 2+)

- Backend API integration with Python FastAPI
- Real-time stock data fetching
- PDF upload and processing
- AI-powered analysis integration
- User authentication system
- Data persistence
- WebSocket for real-time updates
- Chart.js or similar for interactive charts

## Disclaimer

This platform provides educational insights only and does not constitute financial advice. Users should consult with qualified financial advisors before making investment decisions.

## Performance

- Optimized builds with Next.js Turbopack
- Fast TypeScript compilation
- Pre-rendered static pages
- Optimized CSS with TailwindCSS

## Development Workflow

1. Pages are in the `app/` directory following Next.js App Router conventions
2. Reusable components are in the `components/` directory
3. Each page is a separate route
4. Global styles are in `app/globals.css`
5. TailwindCSS provides all styling utilities

## Next Steps

1. **Backend Integration** - Connect to FastAPI backend for AI features
2. **API Integration** - Integrate stock data APIs (Alpha Vantage, IEX Cloud, etc.)
3. **Authentication** - Add user login/signup system
4. **Database** - Set up PostgreSQL for user data
5. **Real-time Updates** - Implement WebSocket for live feeds
6. **PDF Processing** - Set up document processing pipeline
7. **Chart Integration** - Add interactive charting libraries

## Important Notes

- No AI logic is implemented in Stage 1 - it's UI/structure only
- All pages are placeholder components ready for backend integration
- Database connections are not yet implemented
- Authentication system is not included in Stage 1
- All external links are placeholder links

## Deployment

Deployment options for production:
- **Vercel** (Recommended for Next.js)
- **AWS Amplify**
- **Netlify**
- **Docker** (any cloud provider)
- **Traditional VPS/Server**

## Support

For issues or questions about the codebase, refer to:
- Next.js Documentation: https://nextjs.org/docs
- TailwindCSS Documentation: https://tailwindcss.com/docs
- TypeScript Documentation: https://www.typescriptlang.org/docs

---

**Project Status**: Stage 1 Complete - Frontend UI/Structure
**Last Updated**: 2024
**Version**: 1.0.0
