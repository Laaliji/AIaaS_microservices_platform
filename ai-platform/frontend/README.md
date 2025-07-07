# AIaaS Platform Dashboard

A modern, responsive React dashboard for the AI-as-a-Service Microservices Platform. This dashboard provides a user-friendly interface to manage and monitor AI services, RAG workflows, and platform analytics.

## Features

- **Modern UI/UX**: Built with React, TypeScript, and TailwindCSS for a clean and responsive design
- **Dark/Light Mode**: Full support for both dark and light themes
- **Interactive Dashboard**: Real-time metrics and visualizations
- **AI Services Management**: Monitor and manage AI microservices
- **RAG Workflows**: Create and monitor RAG (Retrieval-Augmented Generation) workflows
- **Analytics**: Comprehensive analytics and reporting
- **Settings**: Configure platform settings and preferences

## Tech Stack

- **React 18** with TypeScript
- **Vite** for fast development and optimized builds
- **TailwindCSS** for utility-first styling
- **React Router** for navigation
- **Framer Motion** for smooth animations
- **Headless UI** for accessible UI components
- **React Hook Form** with Zod for form validation
- **Chart.js** for data visualization
- **Heroicons** for beautiful icons

## Getting Started

### Prerequisites

- Node.js (v14+)
- npm or yarn

### Installation

1. Navigate to the frontend directory:
   ```
   cd ai-platform/frontend
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm run dev
   ```

4. Open your browser and navigate to `http://localhost:5173`

## Building for Production

```
npm run build
```

The build artifacts will be stored in the `dist/` directory.

## Project Structure

```
frontend/
├── public/
├── src/
│   ├── assets/         # Static assets
│   ├── components/     # Reusable components
│   │   ├── dashboard/  # Dashboard-specific components
│   │   ├── layout/     # Layout components
│   │   └── ui/         # UI components
│   ├── hooks/          # Custom React hooks
│   ├── lib/            # Utility functions
│   ├── pages/          # Page components
│   ├── services/       # API services
│   ├── App.tsx         # Main App component
│   ├── index.css       # Global styles
│   └── main.tsx        # Entry point
├── index.html
├── package.json
├── tailwind.config.js
└── tsconfig.json
```

## License

MIT
