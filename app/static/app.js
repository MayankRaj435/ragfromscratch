const questionInput = document.querySelector("#question");
const askForm = document.querySelector("#ask-form");
const askButton = document.querySelector("#ask-button");
const formMessage = document.querySelector("#form-message");
const answerHeading = document.querySelector("#answer-heading");
const answerContent = document.querySelector("#answer-content");
const answerTag = document.querySelector("#answer-tag");
const sources = document.querySelector("#sources");
const charCount = document.querySelector("#char-count");
const runTestsButton = document.querySelector("#run-tests");
const testResults = document.querySelector("#test-results");

questionInput.addEventListener("input", () => {
  charCount.textContent = questionInput.value.length;
});

function showError(message) {
  answerHeading.textContent = "Something needs attention";
  answerTag.textContent = "ERROR";
  answerTag.classList.add("error");
  answerContent.className = "answer-content";
  answerContent.textContent = message;
  sources.hidden = true;
}

function showAnswer(data) {
  answerHeading.textContent = "Grounded response";
  answerTag.textContent = "READY";
  answerTag.classList.remove("error");
  answerContent.className = "answer-content";
  answerContent.textContent = data.answer;
  sources.hidden = false;
  sources.innerHTML = '<div class="source-title">Retrieved sources</div>' +
    (data.sources || []).map((source, index) => `
      <article class="source">
        <span class="source-meta">SOURCE ${String(index + 1).padStart(2, "0")} · SIMILARITY ${source.score}</span>
        ${escapeHtml(source.text)}
      </article>`).join("");
}

function escapeHtml(value) {
  return String(value).replace(/[&<>"']/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#039;"
  }[character]));
}

askForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  askButton.disabled = true;
  askButton.querySelector("span").textContent = "Thinking...";
  formMessage.textContent = "Retrieving context and generating an answer...";
  try {
    const response = await fetch("/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: questionInput.value })
    });
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || "The request could not be completed.");
    showAnswer(data);
    formMessage.textContent = "Answer grounded in the retrieved policy context.";
  } catch (error) {
    showError(error.message);
    formMessage.textContent = "The request was not completed. Check the message above.";
  } finally {
    askButton.disabled = false;
    askButton.querySelector("span").textContent = "Ask question";
  }
});

async function runCheck(name, request, assertion) {
  const started = performance.now();
  try {
    const response = await request();
    const contentType = response.headers.get("content-type") || "";
    const data = contentType.includes("application/json") ? await response.json() : null;
    const passed = assertion(response, data);
    return { name, passed, detail: `${response.status} · ${Math.round(performance.now() - started)}ms` };
  } catch (error) {
    return { name, passed: false, detail: error.message };
  }
}

runTestsButton.addEventListener("click", async () => {
  runTestsButton.disabled = true;
  runTestsButton.firstChild.textContent = "Running... ";
  testResults.innerHTML = "";
  const checks = await Promise.all([
    runCheck("Frontend route", () => fetch("/"), (response) => response.ok),
    runCheck("Health endpoint", () => fetch("/health"), (response, data) => response.ok && data.status === "healthy"),
    runCheck("Empty-question guardrail", () => fetch("/ask", {
      method: "POST", headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question: "" })
    }), (response, data) => response.status === 400 && Boolean(data.detail))
  ]);
  testResults.innerHTML = checks.map((check) => `
    <div class="test-result ${check.passed ? "pass" : "fail"}">
      <span>${check.name}</span><strong>${check.passed ? "PASS" : "FAIL"}</strong><small>${check.detail}</small>
    </div>`).join("");
  runTestsButton.disabled = false;
  runTestsButton.firstChild.textContent = "Run checks ";
});
