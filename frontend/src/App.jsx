import { useState, useRef } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const resultRef = useRef(null);

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
      const response = await fetch(
        "https://resume-analyzer-backend-osg2.onrender.com/analyze/",
        {
          method: "POST",
          body: formData,
        },
      );

      const data = await response.json();

      await new Promise((resolve) => setTimeout(resolve, 1000));

      setResult(data);

      setTimeout(() => {
        resultRef.current?.scrollIntoView({
          behavior: "smooth",
        });
      }, 100);
    } catch (error) {
      console.log(error);
      alert("Something went wrong");
    }

    setLoading(false);
  }

  return (
    <div className="min-h-screen bg-[#020617] flex justify-center items-start py-6 px-4">
      <div className="w-full max-w-4xl bg-[#07122b] border border-slate-800 rounded-3xl p-8 shadow-2xl">
        <h1 className="text-6xl font-bold text-white text-center mb-8">
          Resume Analyzer
        </h1>

        <div className="mb-6">
          <label
            htmlFor="resumeUpload"
            className="border-2 border-dashed border-slate-600 rounded-3xl py-12 px-6 flex flex-col items-center justify-center cursor-pointer bg-[#0b1736] hover:border-blue-500 transition"
          >
            <p className="text-white text-2xl font-semibold mb-2">
              Upload Resume
            </p>

            <p className="text-slate-400 text-lg mb-4">PDF files only</p>

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
          className="w-full h-40 bg-[#0b1736] border border-slate-700 rounded-3xl p-6 text-white text-xl outline-none resize-none mb-6"
        />

        <button
          onClick={handleAnalyze}
          disabled={loading}
          className="w-full bg-blue-600 hover:bg-blue-700 transition text-white text-2xl font-bold py-5 rounded-3xl mb-8 flex items-center justify-center gap-3 disabled:opacity-70"
        >
          {loading ? (
            <>
              <div className="w-7 h-7 border-4 border-white border-t-transparent rounded-full animate-spin"></div>
              <span>Analyzing Resume...</span>
            </>
          ) : (
            "Analyze Resume"
          )}
        </button>

        {result && (
          <div
            ref={resultRef}
            className="bg-[#0b1736] border border-slate-700 rounded-3xl p-8"
          >
            <h2 className="text-5xl font-bold text-white text-center mb-6">
              Analysis Result
            </h2>

            <h3 className="text-slate-400 text-2xl text-center mb-6">
              Match Score
            </h3>

            <div className="flex justify-center mb-8">
              <div className="relative w-56 h-56">
                <svg className="w-56 h-56 -rotate-90">
                  <circle
                    cx="112"
                    cy="112"
                    r="82"
                    stroke="#1e293b"
                    strokeWidth="16"
                    fill="transparent"
                  />

                  <circle
                    cx="112"
                    cy="112"
                    r="82"
                    stroke={
                      result.score >= 70
                        ? "#00e676"
                        : result.score >= 40
                          ? "#ffcc00"
                          : "#ff5c5c"
                    }
                    strokeWidth="16"
                    fill="transparent"
                    strokeLinecap="round"
                    strokeDasharray={515}
                    strokeDashoffset={515 - (515 * result.score) / 100}
                  />
                </svg>

                <div className="absolute inset-0 flex items-center justify-center">
                  <span
                    className={`text-5xl font-bold ${
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

            <p className="text-slate-300 text-xl text-center mb-10">
              Experience:{" "}
              <span className="text-white font-semibold">
                {result.experience} Years
              </span>
            </p>

            <div className="mb-10">
              <h3 className="text-slate-400 text-3xl mb-5">
                AI Resume Feedback
              </h3>
              <div className="bg-gradient-to-r from-blue-900/40 to-slate-900 border border-blue-700 rounded-3xl p-6">
                <p className="text-slate-200 text-xl leading-10">
                  {result.summary}
                </p>
              </div>
            </div>

            <div className="mb-10">
              <h3 className="text-slate-400 text-3xl mb-5">Resume Sections</h3>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div
                  className={`p-4 rounded-2xl border ${
                    result.resume_sections.skills
                      ? "border-green-500 bg-green-900/20"
                      : "border-red-500 bg-red-900/20"
                  }`}
                >
                  <p className="text-xl font-semibold text-white">
                    {result.resume_sections.skills ? "✅" : "❌"} Skills
                  </p>
                </div>

                <div
                  className={`p-4 rounded-2xl border ${
                    result.resume_sections.projects
                      ? "border-green-500 bg-green-900/20"
                      : "border-red-500 bg-red-900/20"
                  }`}
                >
                  <p className="text-xl font-semibold text-white">
                    {result.resume_sections.projects ? "✅" : "❌"} Projects
                  </p>
                </div>

                <div
                  className={`p-4 rounded-2xl border ${
                    result.resume_sections.education
                      ? "border-green-500 bg-green-900/20"
                      : "border-red-500 bg-red-900/20"
                  }`}
                >
                  <p className="text-xl font-semibold text-white">
                    {result.resume_sections.education ? "✅" : "❌"} Education
                  </p>
                </div>

                <div
                  className={`p-4 rounded-2xl border ${
                    result.resume_sections.experience
                      ? "border-green-500 bg-green-900/20"
                      : "border-red-500 bg-red-900/20"
                  }`}
                >
                  <p className="text-xl font-semibold text-white">
                    {result.resume_sections.experience ? "✅" : "❌"} Experience
                  </p>
                </div>

                <div
                  className={`p-4 rounded-2xl border ${
                    result.resume_sections.certifications
                      ? "border-green-500 bg-green-900/20"
                      : "border-red-500 bg-red-900/20"
                  }`}
                >
                  <p className="text-xl font-semibold text-white">
                    {result.resume_sections.certifications ? "✅" : "❌"}{" "}
                    Certifications
                  </p>
                </div>
              </div>
            </div>

            <div className="mb-10">
              <h3 className="text-red-400 text-3xl mb-6">
                Missing Skills by Category
              </h3>

              {Object.keys(result.categorized_missing_skills).length > 0 ? (
                <div className="space-y-6">
                  {Object.entries(result.categorized_missing_skills).map(
                    ([category, skills]) => (
                      <div
                        key={category}
                        className="bg-red-900/10 border border-red-700 rounded-3xl p-5"
                      >
                        <h4 className="text-red-300 text-2xl font-bold mb-4">
                          {category}
                        </h4>

                        <div className="flex flex-wrap gap-4">
                          {skills.map((skill, index) => (
                            <span
                              key={index}
                              className="bg-red-900/40 border border-red-600 text-red-300 px-5 py-2 rounded-full text-lg"
                            >
                              {skill}
                            </span>
                          ))}
                        </div>
                      </div>
                    ),
                  )}
                </div>
              ) : (
                <p className="text-green-400 text-2xl font-semibold">
                  No missing skills 🎉
                </p>
              )}
            </div>

            <div className="mb-10">
              <h3 className="text-green-400 text-3xl mb-6">
                Matched Skills by Category
              </h3>

              {Object.keys(result.categorized_matched_skills).length > 0 ? (
                <div className="space-y-6">
                  {Object.entries(result.categorized_matched_skills).map(
                    ([category, skills]) => (
                      <div
                        key={category}
                        className="bg-green-900/10 border border-green-700 rounded-3xl p-5"
                      >
                        <h4 className="text-green-300 text-2xl font-bold mb-4">
                          {category}
                        </h4>

                        <div className="flex flex-wrap gap-4">
                          {skills.map((skill, index) => (
                            <span
                              key={index}
                              className="bg-green-900/30 border border-green-600 text-green-300 px-5 py-2 rounded-full text-lg"
                            >
                              {skill}
                            </span>
                          ))}
                        </div>
                      </div>
                    ),
                  )}
                </div>
              ) : (
                <p className="text-red-400 text-xl">No matched skills found</p>
              )}
            </div>

            {result.suggestions && result.suggestions.length > 0 && (
              <div className="mb-10">
                <h3 className="text-yellow-400 text-3xl mb-6">Suggestions</h3>

                <div className="space-y-4">
                  {result.suggestions.map((suggestion, index) => (
                    <div
                      key={index}
                      className="bg-yellow-500/10 border border-yellow-500/30 text-yellow-200 px-5 py-4 rounded-2xl text-lg"
                    >
                      ⚠ {suggestion}
                    </div>
                  ))}
                </div>
              </div>
            )}

            <div>
              <h3 className="text-slate-400 text-3xl mb-5">Resume Preview</h3>

              <div className="bg-black rounded-3xl p-6 max-h-72 overflow-y-auto">
                <p className="text-white text-lg leading-10 whitespace-pre-wrap">
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
