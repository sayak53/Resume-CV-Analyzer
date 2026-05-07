import { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [jd, setJd] = useState("");
  const [result, setResult] = useState(null);

  const handleSubmit = async () => {
    const formData = new FormData();

    formData.append("resume", file);
    formData.append("job_description", jd);

    const response = await fetch("http://127.0.0.1:8000/analyze/", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    setResult(data);
  };

  return (
    <div style={{ padding: "40px" }}>
      <h1>Resume Analyzer</h1>

      <input type="file" onChange={(e) => setFile(e.target.files[0])} />

      <br />
      <br />

      <textarea
        placeholder="Paste Job Description"
        value={jd}
        onChange={(e) => setJd(e.target.value)}
        style={{
          width: "300px",
          height: "100px",
        }}
      />

      <br />
      <br />

      <button onClick={handleSubmit}>Analyze</button>

      {result && (
        <div style={{ marginTop: "20px" }}>
          <h2>Result</h2>

          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
