
import React, { useState } from "react";
import axios from "axios";

function SchemaEditor({ fetchSchemas }) {
  const [name, setName] = useState("");
  const [version, setVersion] = useState("");

  const addSchema = () => {
    axios.post("http://127.0.0.1:8000/schemas", {
      id: Date.now().toString(),
      name,
      version,
      content: {}
    }).then(() => {
      fetchSchemas();
      setName("");
      setVersion("");
    });
  };

  return (
    <div style={{ marginBottom: "20px" }}>
      <h3>Add New Schema:</h3>
      <input
        placeholder="Schema Name"
        value={name}
        onChange={e => setName(e.target.value)}
      />
      <input
        placeholder="Version"
        value={version}
        onChange={e => setVersion(e.target.value)}
      />
      <button onClick={addSchema}>Add Schema</button>
    </div>
  );
}

export default SchemaEditor;
