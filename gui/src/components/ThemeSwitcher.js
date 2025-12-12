
import React from "react";

function ThemeSwitcher({ setTheme }) {
  return (
    <div style={{ marginBottom: "20px" }}>
      <h3>Choose Theme:</h3>
      <div style={{ display: "flex", gap: "10px", flexWrap: "wrap" }}>
        <button
          style={{ backgroundColor: "#fdfdfd", color: "#222", border: "1px solid #ccc" }}
          onClick={() => setTheme("theme-light")}
        >
          ☀ Light
        </button>
        <button
          style={{ backgroundColor: "#444", color: "#eaeaea" }}
          onClick={() => setTheme("theme-dark")}
        >
          🌙 Dark
        </button>
        <button
          style={{ backgroundColor: "#8b0000", color: "#f8d7da" }}
          onClick={() => setTheme("theme-vampire")}
        >
          ❤️ Vampire
        </button>
        <button
          style={{ backgroundColor: "#fdd835", color: "#333" }}
          onClick={() => setTheme("theme-yellow")}
        >
          ⭐ Yellow
        </button>
        <button
          style={{ backgroundColor: "#2575fc", color: "#fff" }}
          onClick={() => setTheme("theme-modern")}
        >
          🎨 Modern
        </button>
      </div>
    </div>
  );
}

export default ThemeSwitcher;
