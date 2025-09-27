"use client";

import * as React from "react";
import JSZip from "jszip";
import { FileTree } from "@/components/file-tree";
import { ChatBubble } from "@/components/chat-bubble";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { CodeViewer } from "@/components/code-viewer";
import { DiffViewer } from "@/components/diff-viewer";
import { Badge } from "@/components/ui/badge";
import { useToast } from "@/components/toaster";
import { demoEvents, demoFiles, demoReadme, demoFileTree, type DemoEvent } from "@/data/demo-run";
import { formatTimestamp, sleep } from "@/lib/utils";
import { Download, Play, Sparkles } from "lucide-react";

const presets = [
  "Build a health-check microservice in TypeScript with tests",
  "Create a CLI that formats markdown tables",
  "Prototype a Next.js landing page with CTA"
];

const guardrailKeywords = ["exploit", "malware", "ransomware", "ddos"];

const tabs = ["chat", "files", "diffs", "readme"] as const;

type DemoTab = (typeof tabs)[number];

type Status = "idle" | "planning" | "coding" | "reviewing" | "approved";

export function DemoWorkbench() {
  const [prompt, setPrompt] = React.useState(presets[0]);
  const [events, setEvents] = React.useState<DemoEvent[]>([]);
  const [activeTab, setActiveTab] = React.useState<DemoTab>("chat");
  const [activeFilePath, setActiveFilePath] = React.useState<string>(demoFiles[0].path);
  const [activeDiffIndex, setActiveDiffIndex] = React.useState(0);
  const [diffEvents, setDiffEvents] = React.useState<DemoEvent[]>([]);
  const [isRunning, setIsRunning] = React.useState(false);
  const [status, setStatus] = React.useState<Status>("idle");
  const [guardrail, setGuardrail] = React.useState<string | null>(null);
  const [zipReady, setZipReady] = React.useState(false);
  const { publish } = useToast();

  const activeFile = React.useMemo(
    () => demoFiles.find((file) => file.path === activeFilePath) ?? demoFiles[0],
    [activeFilePath]
  );

  const activeDiff = diffEvents[activeDiffIndex];

  const runDemo = React.useCallback(async () => {
    if (isRunning) return;
    const lower = prompt.toLowerCase();
    const hit = guardrailKeywords.find((word) => lower.includes(word));
    if (hit) {
      setGuardrail(`Guardrail: We can\'t help with ${hit}-related tooling. Try another build.`);
      publish({
        title: "Guardrail triggered",
        description: "This request violates our allowed use policy.",
        variant: "error",
      });
      return;
    }

    setGuardrail(null);
    setEvents([]);
    setDiffEvents([]);
    setZipReady(false);
    setActiveDiffIndex(0);
    setActiveTab("chat");
    setActiveFilePath(demoFiles[0].path);
    setStatus("planning");
    setIsRunning(true);
    publish({ title: "Starting build", description: "Architect is planning." });

    for (const event of demoEvents) {
      await sleep(520);
      setEvents((prev) => [...prev, event]);

      if (event.type === "plan") {
        setStatus("planning");
        publish({ title: "Planning", description: event.message });
      }
      if (event.type === "code") {
        setStatus("coding");
        publish({ title: "Coding", description: `${event.role} committed a change.` });
        if (event.diff) {
          setDiffEvents((prev) => {
            const next = [...prev, event];
            setActiveDiffIndex(next.length - 1);
            return next;
          });
        }
        if (event.file) {
          setActiveFilePath(event.file);
          setActiveTab("files");
        }
      }
      if (event.type === "review") {
        setStatus("reviewing");
        publish({ title: "Reviewing", description: event.message });
      }
      if (event.type === "approve") {
        setStatus("approved");
        publish({ title: "Approved", description: event.message, variant: "success" });
      }
      if (event.type === "zip_ready") {
        setZipReady(true);
        publish({ title: "Bundle ready", description: "Download ZIP + README", variant: "success" });
      }
    }

    setIsRunning(false);
  }, [isRunning, prompt, publish]);

  React.useEffect(() => {
    const handleKey = (event: KeyboardEvent) => {
      const isRun = (event.metaKey || event.ctrlKey) && event.key === "Enter";
      if (isRun) {
        event.preventDefault();
        runDemo();
      }
      if (event.key === "[" || event.key === "]") {
        event.preventDefault();
        setActiveTab((current) => {
          const currentIndex = tabs.indexOf(current);
          const delta = event.key === "[" ? -1 : 1;
          const nextIndex = (currentIndex + delta + tabs.length) % tabs.length;
          return tabs[nextIndex];
        });
      }
    };
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, [runDemo]);

  const downloadZip = async () => {
    const zip = new JSZip();
    demoFiles.forEach((file) => {
      zip.file(file.path, file.content);
    });
    zip.file("README.md", demoReadme);
    const blob = await zip.generateAsync({ type: "blob" });
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = "2agent-demo.zip";
    anchor.click();
    URL.revokeObjectURL(url);
    publish({ title: "Exported", description: "Demo ZIP downloaded." });
  };

  return (
    <div className="grid gap-6 lg:grid-cols-[340px_1fr]">
      <section className="space-y-6">
        <div className="rounded-3xl border border-border/70 bg-surface/80 p-6 shadow-glass">
          <div className="flex items-center justify-between">
            <h3 className="text-lg font-semibold text-text">Prompt</h3>
            <Badge className="bg-accent/15 text-accent">Cmd/Ctrl+Enter to run</Badge>
          </div>
          <Textarea
            value={prompt}
            onChange={(event) => setPrompt(event.target.value)}
            placeholder="Describe what you want the agents to build"
            className="mt-4 min-h-[180px]"
          />
          <div className="mt-4 flex flex-wrap gap-2">
            {presets.map((preset) => (
              <Button
                key={preset}
                type="button"
                variant={preset === prompt ? "primary" : "ghost"}
                size="sm"
                onClick={() => setPrompt(preset)}
              >
                <Sparkles className="h-4 w-4" /> {preset}
              </Button>
            ))}
          </div>
          <Button
            type="button"
            onClick={runDemo}
            disabled={isRunning}
            className="mt-6 w-full"
          >
            <Play className="h-4 w-4" /> {isRunning ? "Running..." : "Run demo"}
          </Button>
          {guardrail && (
            <div className="mt-4 rounded-2xl border border-red-500/40 bg-red-500/10 p-4 text-sm text-red-200">
              {guardrail}
            </div>
          )}
        </div>
        <div className="rounded-3xl border border-border/70 bg-surface/80 p-6 shadow-glass">
          <h3 className="text-lg font-semibold text-text">Status</h3>
          <p className="mt-2 text-sm text-text-muted">
            {status === "idle" && "Waiting to start"}
            {status === "planning" && "Architect drafting the plan"}
            {status === "coding" && "Coder applying diffs"}
            {status === "reviewing" && "Reviewer running checks"}
            {status === "approved" && "Build approved"}
          </p>
          <div className="mt-4 flex flex-col gap-2 text-xs uppercase tracking-wide text-text-muted/80">
            <StatusStep label="Plan" active={status !== "idle"} done={events.some((e) => e.type === "plan")} />
            <StatusStep label="Code" active={status === "coding" || status === "reviewing" || status === "approved"} done={diffEvents.length > 0} />
            <StatusStep label="Review" active={status === "reviewing" || status === "approved"} done={events.some((e) => e.type === "review")} />
            <StatusStep label="Ship" active={status === "approved"} done={zipReady} />
          </div>
        </div>
        <div className="rounded-3xl border border-border/70 bg-surface/80 p-6 shadow-glass">
          <h3 className="text-lg font-semibold text-text">Export</h3>
          <p className="mt-2 text-sm text-text-muted">
            Download the artifact bundle with README.
          </p>
          <Button
            type="button"
            onClick={downloadZip}
            variant="secondary"
            className="mt-4 w-full"
            disabled={!zipReady}
          >
            <Download className="h-4 w-4" /> Download ZIP
          </Button>
          {!zipReady && (
            <p className="mt-2 text-xs text-text-muted">Run the demo to generate a bundle.</p>
          )}
        </div>
      </section>
      <section className="rounded-3xl border border-border/70 bg-surface/80 p-6 shadow-glass">
        <Tabs value={activeTab} onValueChange={(value) => setActiveTab(value as DemoTab)}>
          <TabsList>
            <TabsTrigger value="chat">Debate</TabsTrigger>
            <TabsTrigger value="files">Files</TabsTrigger>
            <TabsTrigger value="diffs">Diffs</TabsTrigger>
            <TabsTrigger value="readme">README</TabsTrigger>
          </TabsList>
          <TabsContent value="chat" className="space-y-4">
            <div className="space-y-4">
              {events.length === 0 && (
                <p className="text-sm text-text-muted">Run the demo to stream the multi-agent debate.</p>
              )}
              {events.map((event) => (
                <ChatBubble
                  key={event.id}
                  role={event.role}
                  message={event.message}
                  timestamp={formatTimestamp(new Date(`2020-01-01T${event.timestamp}:00`))}
                />
              ))}
            </div>
          </TabsContent>
          <TabsContent value="files">
            <div className="grid gap-4 lg:grid-cols-[240px_1fr]">
              <div className="rounded-2xl border border-border/70 bg-background/40 p-3">
                <FileTree
                  nodes={demoFileTree}
                  activePath={activeFilePath}
                  onSelect={(node) => node.type === "file" && setActiveFilePath(node.path)}
                />
              </div>
              <CodeViewer code={activeFile.content} language={activeFile.language} />
            </div>
          </TabsContent>
          <TabsContent value="diffs">
            {diffEvents.length === 0 ? (
              <p className="text-sm text-text-muted">Run the demo to inspect diffs.</p>
            ) : (
              <div className="space-y-4">
                <div className="flex flex-wrap gap-2">
                  {diffEvents.map((diffEvent, index) => (
                    <Button
                      key={diffEvent.id}
                      type="button"
                      variant={activeDiffIndex === index ? "primary" : "ghost"}
                      size="sm"
                      onClick={() => setActiveDiffIndex(index)}
                    >
                      {diffEvent.file}
                    </Button>
                  ))}
                </div>
                {activeDiff && activeDiff.diff ? (
                  <DiffViewer diff={activeDiff.diff} />
                ) : (
                  <p className="text-sm text-text-muted">Select a diff to view changes.</p>
                )}
              </div>
            )}
          </TabsContent>
          <TabsContent value="readme">
            <div className="rounded-2xl border border-border/70 bg-background/40 p-4">
              <pre className="whitespace-pre-wrap font-mono text-sm text-text-muted">{demoReadme}</pre>
            </div>
          </TabsContent>
        </Tabs>
      </section>
    </div>
  );
}

function StatusStep({ label, active, done }: { label: string; active: boolean; done: boolean }) {
  return (
    <div className="flex items-center gap-3">
      <span
        className={"h-3 w-3 rounded-full"}
        style={{
          backgroundColor: done ? "#15C2B8" : active ? "#9FB2BF" : "rgba(159,178,191,0.3)",
        }}
      />
      <span className="text-sm text-text">{label}</span>
    </div>
  );
}
