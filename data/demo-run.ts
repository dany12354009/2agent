import type { FileNode } from "@/types/files";

export type AgentRole = "Architect" | "Coder" | "Reviewer";

export interface DemoEvent {
  id: string;
  type: "plan" | "code" | "review" | "approve" | "diff" | "zip_ready";
  role: AgentRole;
  message: string;
  timestamp: string;
  diff?: string;
  file?: string;
}

export interface DemoFile {
  path: string;
  language: string;
  content: string;
}

export const demoEvents: DemoEvent[] = [
  {
    id: "1",
    type: "plan",
    role: "Architect",
    timestamp: "09:41",
    message:
      "Plan: Build a minimal Express server with a /health route and Jest test. Steps: scaffold server.ts, package.json scripts, health test, run tests, summarize.",
  },
  {
    id: "2",
    type: "code",
    role: "Coder",
    timestamp: "09:42",
    message:
      "Implementing Express server with typed handler, enabling CORS, and exporting app for testing. Adding npm scripts for dev/test.",
    diff: String.raw`diff --git a/src/server.ts b/src/server.ts
new file mode 100644
index 0000000..0ca4aa1
--- /dev/null
+++ b/src/server.ts
@@
+import express from "express";
+import cors from "cors";
+
+const app = express();
+app.use(cors());
+
+app.get("/health", (_req, res) => {
+  res.json({ status: "ok" });
+});
+
+if (require.main === module) {
+  const port = process.env.PORT || 3000;
+  app.listen(port, () => {
+    console.log("Server listening on", port);
+  });
+}
+
+export default app;
`,
    file: "src/server.ts",
  },
  {
    id: "3",
    type: "code",
    role: "Coder",
    timestamp: "09:43",
    message:
      "Adding Jest configuration and first test to assert /health returns status ok.",
    diff: String.raw`diff --git a/test/server.test.ts b/test/server.test.ts
new file mode 100644
index 0000000..c5ff12d
--- /dev/null
+++ b/test/server.test.ts
@@
+import request from "supertest";
+import app from "../src/server";
+
+describe("GET /health", () => {
+  it("returns ok", async () => {
+    const response = await request(app).get("/health");
+    expect(response.status).toBe(200);
+    expect(response.body).toEqual({ status: "ok" });
+  });
+});
`,
    file: "test/server.test.ts",
  },
  {
    id: "4",
    type: "review",
    role: "Reviewer",
    timestamp: "09:44",
    message:
      "Tests pass locally. Consider exporting the server for reuse and logging only when run directly. No issues found.",
  },
  {
    id: "5",
    type: "approve",
    role: "Architect",
    timestamp: "09:45",
    message:
      "Ship it. Generating README and packaging ZIP with project skeleton.",
  },
  {
    id: "6",
    type: "zip_ready",
    role: "Reviewer",
    timestamp: "09:46",
    message: "Bundle ready with README.md and src/test directories.",
  },
];

export const demoFiles: DemoFile[] = [
  {
    path: "src/server.ts",
    language: "ts",
    content: String.raw`import express from "express";
import cors from "cors";

const app = express();
app.use(cors());

app.get("/health", (_req, res) => {
  res.json({ status: "ok" });
});

if (require.main === module) {
  const port = process.env.PORT || 3000;
  app.listen(port, () => {
    console.log("Server listening on", port);
  });
}

export default app;
`,
  },
  {
    path: "test/server.test.ts",
    language: "ts",
    content: String.raw`import request from "supertest";
import app from "../src/server";

describe("GET /health", () => {
  it("returns ok", async () => {
    const response = await request(app).get("/health");
    expect(response.status).toBe(200);
    expect(response.body).toEqual({ status: "ok" });
  });
});
`,
  },
  {
    path: "package.json",
    language: "json",
    content: String.raw`{
  "name": "express-health-check",
  "version": "1.0.0",
  "private": true,
  "scripts": {
    "dev": "tsx src/server.ts",
    "test": "jest"
  },
  "dependencies": {
    "cors": "^2.8.5",
    "express": "^4.18.2"
  },
  "devDependencies": {
    "@types/express": "^4.17.17",
    "@types/jest": "^29.5.11",
    "@types/supertest": "^2.0.16",
    "jest": "^29.7.0",
    "supertest": "^6.3.3",
    "tsx": "^4.7.0"
  }
}
`,
  },
];

export const demoReadme = String.raw`# Express Health Check\n\nThis demo project showcases how 2Agent plans, codes, reviews, and ships an Express service with a simple health route.\n\n## Quick start\n\n\`\`\`bash\nnpm install\nnpm run dev\n\`\`\`\n\n## Tests\n\n\`\`\`bash\nnpm test\n\`\`\`\n`;

export const demoFileTree: FileNode[] = [
  {
    name: "src",
    path: "src",
    type: "folder",
    children: [
      {
        name: "server.ts",
        path: "src/server.ts",
        type: "file",
      },
    ],
  },
  {
    name: "test",
    path: "test",
    type: "folder",
    children: [
      {
        name: "server.test.ts",
        path: "test/server.test.ts",
        type: "file",
      },
    ],
  },
  {
    name: "package.json",
    path: "package.json",
    type: "file",
  },
];
