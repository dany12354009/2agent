const startButton = document.getElementById("start");
const specField = document.getElementById("spec");
const logContainer = document.getElementById("log");
const downloadLink = document.getElementById("download");
const statusBox = document.getElementById("status");

function appendLog(agent, message, type) {
  const entry = document.createElement("article");
  entry.className = `message ${type || "info"}`;

  const meta = document.createElement("div");
  meta.className = "meta";
  meta.textContent = `${(type || "event").toUpperCase()} · ${agent || "System"}`;
  entry.appendChild(meta);

  const body = document.createElement("pre");
  body.textContent = message;
  entry.appendChild(body);

  logContainer.appendChild(entry);
  logContainer.scrollTop = logContainer.scrollHeight;
}

function setStatus(text, variant = "info") {
  statusBox.textContent = text;
  statusBox.dataset.variant = variant;
}

async function createSession() {
  const response = await fetch("/api/sessions", { method: "POST" });
  if (!response.ok) {
    throw new Error(`Failed to create session (${response.status})`);
  }
  return response.json();
}

function isMalicious(spec) {
  const lower = spec.toLowerCase();
  return ["malware", "virus", "ransomware", "credential", "phishing", "botnet"].some((k) =>
    lower.includes(k),
  );
}

async function startBuild() {
  const spec = specField.value.trim();
  if (!spec) {
    setStatus("Please provide a build specification.", "error");
    return;
  }

  if (isMalicious(spec)) {
    setStatus("Request rejected: specification appears malicious.", "error");
    return;
  }

  startButton.disabled = true;
  downloadLink.classList.add("hidden");
  logContainer.innerHTML = "";
  setStatus("Requesting session...");

  try {
    const { session_id } = await createSession();
    await openSocket(session_id, spec);
  } catch (error) {
    console.error(error);
    setStatus(`Failed to start session: ${error.message}`, "error");
    startButton.disabled = false;
  }
}

async function openSocket(sessionId, spec) {
  setStatus("Connecting to DuoForge...");
  const protocol = window.location.protocol === "https:" ? "wss" : "ws";
  const socket = new WebSocket(`${protocol}://${window.location.host}/ws/${sessionId}`);

  socket.addEventListener("open", () => {
    setStatus("Agents are collaborating on your request...");
    socket.send(JSON.stringify({ prompt: spec }));
  });

  socket.addEventListener("message", (event) => {
    try {
      const payload = JSON.parse(event.data);
      handleEvent(payload);
      if (payload.type === "error") {
        socket.close();
      }
    } catch (err) {
      console.error("Failed to parse event", err);
    }
  });

  socket.addEventListener("close", () => {
    setStatus("Session finished. You can launch another build.");
    startButton.disabled = false;
  });

  socket.addEventListener("error", () => {
    setStatus("Connection error.", "error");
    startButton.disabled = false;
  });
}

function handleEvent(event) {
  switch (event.type) {
    case "plan":
    case "diff":
    case "review":
      appendLog(event.from_agent, event.content, event.type);
      break;
    case "zip_ready":
      downloadLink.href = event.url;
      downloadLink.classList.remove("hidden");
      setStatus("Build complete! Download is ready.");
      appendLog("System", "Workspace archive prepared.", "info");
      break;
    case "error":
      appendLog("System", event.content || "An error occurred.", event.type);
      setStatus(event.content || "An error occurred.", "error");
      break;
    default:
      appendLog("System", JSON.stringify(event, null, 2), event.type || "info");
  }
}

startButton.addEventListener("click", startBuild);
