import { createRoot } from "react-dom/client";
import App from "./App";
import "./index.css";

// Add meta tags for SEO and viewport
const updateMetaTags = () => {
  // Set page title
  document.title = "Trial Junkies - No Rehab, Just Free Trials";

  // Set favicon
  const link = document.createElement('link');
  link.rel = 'icon';
  link.href = '/favicon.ico';
  document.head.appendChild(link);

  // Add additional meta tags
  const meta = document.createElement('meta');
  meta.name = 'description';
  meta.content = 'Get hooked on the ultimate subscription hack. Our AI-powered bots automate free trials across hundreds of services so you never pay again.';
  document.head.appendChild(meta);

  // Add font imports
  const fontImport = document.createElement('link');
  fontImport.rel = 'stylesheet';
  fontImport.href = 'https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Roboto:wght@300;400;500;700&display=swap';
  document.head.appendChild(fontImport);

  // Add font awesome
  const fontAwesome = document.createElement('link');
  fontAwesome.rel = 'stylesheet';
  fontAwesome.href = 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css';
  document.head.appendChild(fontAwesome);
};

updateMetaTags();
createRoot(document.getElementById("root")!).render(<App />);
