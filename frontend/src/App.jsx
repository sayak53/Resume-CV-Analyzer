import { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [jd, setJd] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);

    setResult(null);

    const formData = new FormData();

    formData.append("resume", file);
    formData.append("job_description", jd);

    const response = await fetch("http://127.0.0.1:8000/analyze/", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    setTimeout(() => {
      setResult(data);

      setLoading(false);
    }, 1000);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-slate-900 to-black flex items-center justify-center px-4 py-10">
      <div className="w-full max-w-2xl bg-slate-950 border border-slate-800 rounded-3xl p-8 shadow-2xl">
        <h1 className="text-5xl font-bold text-white text-center mb-8">
          Resume Analyzer
        </h1>

        <div className="space-y-6">
          <label className="border-2 border-dashed border-slate-700 rounded-2xl p-8 flex flex-col items-center justify-center cursor-pointer hover:border-blue-500 transition-all duration-300 bg-slate-900">
            <input
              type="file"
              className="hidden"
              onChange={(e) => setFile(e.target.files[0])}
            />

            <p className="text-white text-lg font-semibold mb-2">
              Upload Resume
            </p>

            <p className="text-slate-400 text-sm">PDF files only</p>

            {file && (
              <p className="mt-4 text-blue-400 font-medium">{file.name}</p>
            )}
          </label>

          <textarea
            placeholder="Paste Job Description..."
            value={jd}
            onChange={(e) => setJd(e.target.value)}
            className="w-full h-40 bg-slate-900 border border-slate-700 rounded-2xl p-4 text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
          />

          <button
            onClick={handleSubmit}
            className="w-full bg-blue-600 hover:bg-blue-700 transition-all duration-300 text-white py-4 rounded-2xl text-lg font-semibold shadow-lg"
          >
            {loading ? "Analyzing..." : "Analyze Resume"}
          </button>
        </div>

        {result && (
          <div className="mt-10 bg-slate-900 border border-slate-700 rounded-2xl p-6">
            <h2 className="text-3xl font-bold text-white mb-4 text-center">
              Analysis Result
            </h2>

            <div className="text-center mb-8">
              <p className="text-slate-400 mb-2">Match Score</p>

              <h3
                className={`text-6xl font-bold ${
                  result.score >= 70
                    ? "text-green-400"
                    : result.score >= 40
                      ? "text-yellow-400"
                      : "text-red-400"
                }`}
              >
                {result.score}%
              </h3>
            </div>

            <div className="mb-6">
              <p className="text-slate-400 mb-3">Missing Keywords</p>

              <div className="flex flex-wrap gap-3">
                {result.missing_keywords.map((keyword, index) => (
                  <span
                    key={index}
                    className="bg-red-500/20 text-red-300 px-4 py-2 rounded-full border border-red-500/30"
                  >
                    {keyword}
                  </span>
                ))}
              </div>
            </div>

            <div>
              <p className="text-slate-400 mb-2">Resume Preview</p>

              <div className="bg-black border border-slate-800 rounded-xl p-4 text-slate-300 max-h-60 overflow-y-auto leading-7">
                {result.resume_preview}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
