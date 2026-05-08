import { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleAnalyze() {
    if (!file || !jobDescription) {
      alert("Please upload resume and add job description");
      return;
    }

    setLoading(true);

    const formData = new FormData();

    formData.append("resume", file);
    formData.append("job_description", jobDescription);

    try {
      const response = await fetch("http://127.0.0.1:8000/analyze/", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      await new Promise((resolve) => setTimeout(resolve, 1000));

      setResult(data);
    } catch (error) {
      console.log(error);
      alert("Something went wrong");
    }

    setLoading(false);
  }

  return (
    <div className="min-h-screen bg-[#020617] flex justify-center items-center p-8">
      <div className="w-full max-w-4xl bg-[#07122b] border border-slate-800 rounded-3xl p-8 shadow-2xl">
        <h1 className="text-6xl font-bold text-white text-center mb-10">
          Resume Analyzer
        </h1>

        <div className="mb-8">
          <label
            htmlFor="resumeUpload"
            className="border-2 border-dashed border-slate-600 rounded-3xl p-12 flex flex-col items-center justify-center cursor-pointer bg-[#0b1736] hover:border-blue-500 transition"
          >
            <p className="text-white text-2xl font-semibold mb-3">
              Upload Resume
            </p>

            <p className="text-slate-400 mb-5">PDF files only</p>

            {file && (
              <p className="text-blue-400 font-semibold text-xl">{file.name}</p>
            )}
          </label>

          <input
            id="resumeUpload"
            type="file"
            accept=".pdf"
            onChange={(e) => setFile(e.target.files[0])}
            className="hidden"
          />
        </div>

        <textarea
          placeholder="Paste Job Description Here..."
          value={jobDescription}
          onChange={(e) => setJobDescription(e.target.value)}
          className="w-full h-52 bg-[#0b1736] border border-slate-700 rounded-3xl p-6 text-white text-2xl outline-none resize-none mb-8"
        />

        <button
          onClick={handleAnalyze}
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-700 transition text-white text-2xl font-bold py-6 rounded-3xl mb-10"
        >
          {loading ? "Analyzing..." : "Analyze Resume"}
        </button>

        {result && (
          <div className="bg-[#0b1736] border border-slate-700 rounded-3xl p-10">
            <h2 className="text-5xl font-bold text-white text-center mb-8">
              Analysis Result
            </h2>

            <h3 className="text-slate-400 text-xl text-center mb-6">
              Match Score
            </h3>

            <div className="flex justify-center mb-8">
              <div className="relative w-64 h-64">
                <svg className="w-64 h-64 rotate-[-90deg]">
                  <circle
                    cx="128"
                    cy="128"
                    r="90"
                    stroke="#1e293b"
                    strokeWidth="18"
                    fill="transparent"
                  />

                  <circle
                    cx="128"
                    cy="128"
                    r="90"
                    stroke={
                      result.score >= 70
                        ? "#00e676"
                        : result.score >= 40
                          ? "#ffcc00"
                          : "#ff5c5c"
                    }
                    strokeWidth="18"
                    fill="transparent"
                    strokeLinecap="round"
                    strokeDasharray={565}
                    strokeDashoffset={565 - (565 * result.score) / 100}
                  />
                </svg>

                <div className="absolute inset-0 flex items-center justify-center">
                  <span
                    className={`text-6xl font-bold ${
                      result.score >= 70
                        ? "text-green-400"
                        : result.score >= 40
                          ? "text-yellow-400"
                          : "text-red-400"
                    }`}
                  >
                    {result.score}%
                  </span>
                </div>
              </div>
            </div>

            <p className="text-slate-300 text-lg text-center mb-10">
              Experience:{" "}
              <span className="text-white font-semibold">
                {result.experience} Years
              </span>
            </p>

            <div className="mb-10">
              <h3 className="text-slate-400 text-2xl mb-5">Missing Keywords</h3>

              <div className="flex flex-wrap gap-4">
                {result.missing_keywords.length > 0 ? (
                  result.missing_keywords.map((keyword, index) => (
                    <span
                      key={index}
                      className="bg-red-900/40 border border-red-600 text-red-300 px-6 py-3 rounded-full text-xl"
                    >
                      {keyword}
                    </span>
                  ))
                ) : (
                  <p className="text-green-400 text-2xl font-semibold">
                    No missing keywords 🎉
                  </p>
                )}
              </div>
            </div>

            <div className="mb-10">
              <h3 className="text-slate-400 text-2xl mb-5">Matched Skills</h3>

              <div className="flex flex-wrap gap-4">
                {result.matched_skills.length > 0 ? (
                  result.matched_skills.map((skill, index) => (
                    <span
                      key={index}
                      className="bg-green-900/30 border border-green-600 text-green-300 px-6 py-3 rounded-full text-xl"
                    >
                      {skill}
                    </span>
                  ))
                ) : (
                  <p className="text-red-400 text-xl">
                    No matched skills found
                  </p>
                )}
              </div>
            </div>

            <div>
              <h3 className="text-slate-400 text-2xl mb-5">Resume Preview</h3>

              <div className="bg-black rounded-3xl p-6 max-h-72 overflow-y-auto">
                <p className="text-white text-xl leading-10 whitespace-pre-wrap">
                  {result.resume_preview}
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
