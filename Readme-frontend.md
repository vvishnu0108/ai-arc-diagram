# Architecture Diagram Generator - Frontend

**Current State**:
This is a React-based web interface for the Architecture Diagram Generator. It provides a user-friendly interface to input natural language prompts, visualize generated diagrams in an embedded Draw.io editor, and download/export diagrams in multiple formats.

The frontend communicates with a Flask backend API to generate architecture diagrams using an LLM-powered agentic approach.

> **Note**: This frontend requires the backend API running at `http://localhost:5000`. Ensure the backend is started before running the frontend.

**Key Features**:
- Natural language input for architecture description
- Real-time diagram visualization with embedded Draw.io
- Download diagrams as PNG images
- Export diagrams as Draw.io files for further editing
- Responsive UI with status indicators
- Comprehensive console logging for debugging

## Tech Stack
- **Framework**: React 18+ with Vite
- **Styling**: CSS3
- **HTTP Client**: Fetch API
- **Editor Integration**: Embedded Draw.io (diagrams.net)
- **Package Manager**: npm or yarn
- **Build Tool**: Vite

## Steps to Run

### Pre-requisites
- Node.js 16+ installed
- npm or yarn installed
- Git installed
- Backend API running on `http://localhost:5000`

### Setup Instructions

1. **Clone the repository** (if not already done)
    ```bash
    git clone <repository-url>
    cd diagram-ui/frontend
    ```

2. **Install Node dependencies**
    ```bash
    npm install
    ```

3. **Start the development server**
    ```bash
    npm run dev
    ```
    
    The frontend will be available at `http://localhost:5173` (or another port if 5173 is in use)

4. **Build for production**
    ```bash
    npm run build
    ```

5. **Preview production build**
    ```bash
    npm run preview
    ```

## Project Structure

```
frontend/
├── index.html                          # Entry HTML file
├── package.json                        # Node dependencies
├── vite.config.js                      # Vite configuration
├── eslint.config.js                    # ESLint configuration
├── README.md                           # This file
├── public/                             # Static assets
├── src/
│   ├── main.jsx                        # React entry point
│   ├── App.jsx                         # Main App component
│   ├── assets/
│   │   ├── components/
│   │   │   ├── DrawioFrame.jsx        # Draw.io iframe wrapper
│   │   │   ├── PromptPanel.jsx        # Input prompt panel
│   │   │   └── Toolbar.jsx            # Top toolbar with actions
│   │   └── services/
│   │       └── drawioBridge.js        # Draw.io communication bridge
│   └── styles/
│       └── App.css                    # Application styles
└── .gitignore                          # Git ignore rules
```

## Component Architecture

### App.jsx
Main application component that orchestrates the flow:
- Manages diagram generation state
- Handles API calls to backend
- Manages DrawIO iframe reference
- Coordinates between PromptPanel and DrawioFrame

### DrawioFrame.jsx
Embedded Draw.io editor wrapper:
- Manages iframe initialization and readiness
- Handles diagram loading into the editor
- Queues pending diagrams if iframe not ready
- Exports diagrams on save

### PromptPanel.jsx
User input interface:
- Text area for natural language prompts
- Generate button with loading states
- Status messages (loading, success, error)

### Toolbar.jsx
Top navigation and actions:
- Brand/title display
- View PNG button (opens in new tab)
- Download Draw.io File button (downloads XML)

### drawioBridge.js
Service for communication with Draw.io iframe:
- Sends messages to embedded Draw.io
- Loads diagrams into the editor
- Clears old diagrams before loading new ones
- Initiates exports

## API Integration

The frontend communicates with the backend API at `http://localhost:5000`:

### Generate Diagram Flow
1. User enters prompt in PromptPanel
2. App sends POST request to `/api/generate`
3. Backend processes and returns `{ status: "success" }`
4. App fetches XML from `/api/diagram/drawio/xml`
5. XML is loaded into DrawioFrame
6. User sees diagram in embedded editor

### Download Options
- **View PNG**: Opens `/api/diagram/png` in new tab
- **Download Draw.io**: Fetches from `/api/diagram/drawio/xml` and downloads as `.drawio` file

## Console Logging

The frontend includes detailed console logging for debugging. Open DevTools (F12) and check the Console tab to see:
- Prompt received
- API call status
- XML fetch completion
- DrawIO initialization
- Diagram loading status

Example console output:
```
Prompt received: create a 2 tier architecture
Sending API call to /api/generate with prompt...
Response received from /api/generate: {status: "success"}
Fetching XML from /api/diagram/drawio/xml...
XML received from backend, length: 122712
Loading XML into DrawIO iframe...
Diagram loaded successfully!
```

## Available Scripts

```bash
# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run ESLint
npm run lint

# Format code
npm run format
```

## Browser Support

- Chrome/Chromium 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## Configuration

### Backend API URL
The frontend is configured to connect to the backend at `http://localhost:5000`. To change this:

Edit `src/App.jsx` and update the fetch URLs:
```javascript
const res = await fetch("http://localhost:5000/api/generate", {
```

### Draw.io Embed Options
The Draw.io embed parameters can be modified in `src/assets/components/DrawioFrame.jsx`:

Current URL: `https://embed.diagrams.net/?embed=1&proto=json&spin=1&ui=min&save=1`

Parameters:
- `embed=1` - Enable embedded mode
- `proto=json` - Use JSON protocol for communication
- `spin=1` - Show loading spinner
- `ui=min` - Minimal UI
- `save=1` - Enable save button

## Error Handling

The application handles errors gracefully:
- API call failures show error message
- DrawIO loading failures queue diagrams for retry
- Network errors display user-friendly alerts

Check console logs for detailed error messages.

## State Management

Uses React hooks for state management:
- `status` - Current operation status (idle, loading, success, error)
- `drawioRef` - Reference to DrawioFrame component

Status flow:
```
idle → loading → success/error
```

## Performance Considerations

- DrawioFrame is lazy-loaded when the component mounts
- XML data is cleared before loading new diagrams
- Pending diagrams are queued if iframe initialization is slow
- File downloads use blob URLs for efficiency

## Development Workflow

1. Start backend: `cd backend && python3 app.py`
2. Start frontend: `cd frontend && npm run dev`
3. Open browser to `http://localhost:5173`
4. Make changes and see hot-reload (Vite HMR)
5. Check console (F12) for logs and errors

## Troubleshooting

### Blank page or not loading
- Check if backend is running at `http://localhost:5000`
- Check browser console for errors (F12)
- Clear browser cache and reload

### DrawIO not loading
- Check if iframe can access `https://embed.diagrams.net`
- Verify no CORS issues in console
- Check network tab in DevTools

### API calls failing
- Ensure backend is running: `python3 app.py` in backend directory
- Check backend console for errors
- Verify CORS is enabled in Flask (should be by default)

### Files not downloading
- Check browser download folder
- Verify PopUp not blocked by browser
- Check browser console for errors

### DrawIO save button not working
- Ensure you're using the Toolbar's "Download Draw.io File" button instead
- The embedded Draw.io save button requires different configuration

## Contributing

When making changes:
1. Follow React best practices
2. Use functional components with hooks
3. Add console logging for debugging
4. Test with backend running
5. Update this README with new features

## Dependencies

See `package.json` for complete list. Key packages:
- `react` - UI library
- `react-dom` - React DOM rendering
- `vite` - Build tool and dev server
- `eslint` - Code linting

## License

See LICENSE file in the root repository.

      const data = await res.json();
      if (data.status !== "success") throw new Error();

      const xmlRes = await fetch(
        "http://localhost:5000/api/diagram/drawio/xml"
      );
      const xmlData = await xmlRes.json();

      drawioRef.current.load(xmlData.xml);
      setStatus("success");

    } catch (err) {
      console.error(err);
      setStatus("error");
    }
  };

  return (
    <div className="app-container">
      <Toolbar drawioRef={drawioRef} />

      <div className="main-content">
        <PromptPanel
          collapsed={collapsed}
          onGenerate={handleGenerate}
          status={status}
        />

        <button
          className={`collapse-toggle ${collapsed ? "collapsed" : ""}`}
          onClick={() => setCollapsed(!collapsed)}
        >
          {collapsed ? "›" : "‹"}
        </button>

        <DrawioFrame ref={drawioRef} />
      </div>
    </div>
  );
}

