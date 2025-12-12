
import React, { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";
import ThemeSwitcher from "./components/ThemeSwitcher";
import SchemaEditor from "./components/SchemaEditor";

function App() {
  const [schemas, setSchemas] = useState([]);
  const [theme, setTheme] = useState("theme-light");
  const API_URL = "http://127.0.0.1:8000/schemas";

  const fetchSchemas = () => {
    axios.get(API_URL).then(res => setSchemas(res.data));
  };

  useEffect(() => {
    fetchSchemas();
  }, []);

  return (
    <div className={`app-container ${theme}`}>
      <h1>JSONED - Schema Manager</h1>
      <ThemeSwitcher setTheme={setTheme} />
      <SchemaEditor fetchSchemas={fetchSchemas} />
      <div className="schema-list">
        {schemas.map(schema => (
          <div key={schema._id} className="schema-card">
            <h3>{schema.name}</h3>
            <p>Version: {schema.version}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
