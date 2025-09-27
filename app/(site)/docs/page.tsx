import { Badge } from "@/components/ui/badge";
import { CodeViewer } from "@/components/code-viewer";

const sections = [
  {
    title: "Quickstart",
    body: [
      "1. Create an API key in the dashboard.",
      "2. Initialize the SDK with your key.",
      "3. Stream WebSocket events to follow the debate and diffs.",
    ],
  },
  {
    title: "Agent roles & prompts",
    body: [
      "Architect plans tasks and sets guardrails.",
      "Coder executes plans, proposes diffs, re-runs tests.",
      "Reviewer blocks unsafe or failing changes before approval.",
    ],
  },
  {
    title: "Test runner & diffs",
    body: [
      "Every run includes lint, unit tests, and optional integration suites.",
      "Diffs are unified and chunked for quick rendering in your UI.",
    ],
  },
  {
    title: "Safety & Allowed Use",
    body: [
      "We refuse prompts involving malware, exploits, or unsafe automation.",
      "Guardrails extend to custom instructions via policy configuration.",
    ],
  },
];

const codeSamples = [
  {
    title: "cURL",
    language: "bash",
    code: `curl -X POST https://api.2agent.dev/v1/sessions \\
  -H "Authorization: Bearer $AGENT_KEY" \\
  -d '{"prompt": "Generate a health check endpoint"}'`,
  },
  {
    title: "JavaScript",
    language: "ts",
    code: `import { TwoAgent } from "@2agent/sdk";

const client = new TwoAgent({ apiKey: process.env.AGENT_KEY! });

const session = await client.sessions.create({
  prompt: "Ship a Next.js hero section",
});

for await (const event of session.stream()) {
  console.log(event.type, event.payload);
}`,
  },
  {
    title: "Python",
    language: "py",
    code: `from twoagent import Client

client = Client(api_key="AGENT_KEY")

for event in client.run(prompt="Bootstrap a FastAPI health check"):
    print(event.type, event.payload)`,
  },
];

export default function DocsPage() {
  return (
    <div className="mx-auto flex max-w-6xl flex-col gap-16 px-6 py-20">
      <section className="space-y-6">
        <Badge className="bg-accent/20 text-accent">Docs</Badge>
        <h1 className="text-4xl font-semibold text-text">Build with the 2Agent API</h1>
        <p className="max-w-3xl text-lg text-text-muted">
          Stream structured events, subscribe to debate updates, and orchestrate multi-agent builds directly from your CI or editor.
        </p>
      </section>

      <section className="grid gap-8 md:grid-cols-2">
        {sections.map((section) => (
          <div key={section.title} className="rounded-3xl border border-border/70 bg-surface/80 p-6 shadow-glass">
            <h2 className="text-2xl font-semibold text-text">{section.title}</h2>
            <ul className="mt-4 space-y-2 text-sm text-text-muted">
              {section.body.map((item) => (
                <li key={item} className="flex gap-2">
                  <span className="mt-1 h-1.5 w-1.5 rounded-full bg-accent" />
                  <span>{item}</span>
                </li>
              ))}
            </ul>
          </div>
        ))}
      </section>

      <section className="space-y-6">
        <h2 className="text-3xl font-semibold text-text">Code samples</h2>
        <div className="grid gap-8 md:grid-cols-3">
          {codeSamples.map((sample) => (
            <div key={sample.title} className="space-y-4">
              <h3 className="text-lg font-semibold text-text">{sample.title}</h3>
              <CodeViewer code={sample.code} language={sample.language} />
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
