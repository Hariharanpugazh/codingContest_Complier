import React from 'react';
import MonacoEditor from '@monaco-editor/react';

// src/components/CodeEditor.js
function CodeEditor({ language, code, setCode, setLanguage }) {
  return (
    <div>
      <label className="text-lg font-semibold">Select Programming Language</label>
      <select
        className="w-full mt-2 mb-4 p-2 border rounded"
        value={language}
        onChange={(e) => {
          setLanguage(e.target.value);
          setCode(""); // Reset the code to an empty string
        }}
      >
        <option value="python">Python</option>
        <option value="javascript">JavaScript</option>
        <option value="java">Java</option>
        <option value="cpp">C++</option>
      </select>
      <MonacoEditor
        language={language}
        value={code}
        onChange={(value) => setCode(value)}
        theme="vs-dark"
        height="300px"
      />
    </div>
  );
}



export default CodeEditor;