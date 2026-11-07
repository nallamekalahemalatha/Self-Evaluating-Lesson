# Loom Video Walkthrough Script & Demo Guide (15–20 Minutes)

**Role**: GenAI Engineer — Content Systems  
**Project**: Self-Evaluating RAG Lesson Content Generator  
**Topic**: Introduction to RAG (Retrieval-Augmented Generation)  
**Target Audience**: 12th-grade graduate from India, limited English vocabulary, non-English-medium background  

---

## 🎥 Recording Setup & Instructions
- **Tool**: Loom (or OBS / Screen Recorder with face-visible webcam bubble).
- **Camera**: Keep your face clearly visible in the bottom-left or bottom-right corner throughout the video.
- **Screen Layout**:
  - Browser tab: Streamlit dashboard (`http://localhost:8501`).
  - Terminal tab: PowerShell running CLI (`python run.py --provider mock --inject-flaw jargon`).
  - Code Editor: VS Code displaying project structure, `core/evaluator.py`, and `core/pipeline.py`.
- **Target Duration**: 16 to 19 minutes.

---

## ⏱️ Minute-by-Minute Presentation Timeline

| Segment | Timestamp | Focus Area | On-Screen Asset |
|---|---|---|---|
| **Part 1** | 0:00 – 3:00 | Intro, Role Context & Learner Persona | Face-Cam + Slide / Title Screen |
| **Part 2** | 3:00 – 7:00 | System Architecture & 6-Point Hard Rubric | Architecture Diagram + VS Code (`rubric.py`) |
| **Part 3** | 7:00 – 11:00 | End-to-End Live Workflow Demo | Streamlit Web UI (Baseline Passing Run) |
| **Part 4** | 11:00 – 15:00 | Live Deliberate Flaw Injection & Evaluator Catch | Streamlit UI (Flaw Injection & Rejection Log) |
| **Part 5** | 15:00 – 18:30 | Self-Evolution, Memory & Design Trade-offs | SQLite Viewer / Evolution Tab + Terminal |
| **Part 6** | 18:30 – 20:00 | Summary, Takeaways & Conclusion | Face-Cam Wrap-Up |

---

## Detailed Transcript & Talking Points

---

### Part 1: Introduction, Role Context & Learner Persona (0:00 – 3:00)
**[Face-Cam Visible]**

> *"Hello everyone! My name is [Your Name], and this is my submission for the GenAI Engineer - Content Systems role.
>
> Today, I'm presenting the **Self-Evaluating Lesson Content Generator** — an autonomous closed-loop agentic engine that does not just generate learning material, but rigorously evaluates its own quality against a strict pass/fail rubric and self-heals before any human learner ever sees it.
>
> As emphasized in the prompt: this role is **not** about writing one clever prompt. Anyone can prompt ChatGPT to produce generic text. Our job as Content Systems Engineers is to build production pipelines that guarantee pedagogical quality, brand safety, readability, and factual accuracy at scale.
>
> ### Who are we building for?
> Our target learner is very specific and profoundly important:
> - An **Indian 12th-grade student who completed schooling in a regional, non-English-medium language** (like Hindi, Telugu, Tamil, Marathi, or Bengali medium).
> - They have limited English vocabulary and feel easily intimidated by heavy academic jargon or long, nested English sentences.
> - But they are ambitious, curious, and want to kickstart a high-paying career in Artificial Intelligence!
>
> If our AI outputs a phrase like *'non-parametric memory via high-dimensional latent vector spaces'*, this student will feel discouraged and give up. But if we explain RAG as an **Open-Book Exam vs a Closed-Book Exam**, or like using a **Google Maps pin**, they immediately get it! That pedagogical empathy is hard-coded into our system."*

---

### Part 2: Architecture & Evaluator Design (3:00 – 7:00)
**[Switch Screen to Architecture Diagram in README or VS Code]**

> *"Let’s look at the system architecture.
>
> Rather than a linear script, we built a **Stateful Agentic Graph Loop** with four core components:
> 1. **Content Generator Agent**: Hydrated with the target persona, cultural anchors (school exams, railway timetables, college circulars), and dynamic guardrails fetched from memory.
> 2. **Two-Tier Evaluator Engine**: Combines deterministic algorithmic scanners with an LLM-as-a-judge binary evaluator.
> 3. **Regenerator Agent**: Synthesizes structured diagnostic feedback from failed checks and executes surgical revisions.
> 4. **Persistent Memory & Self-Evolution Layer**: Uses SQLite and JSON to remember failures across runs and evolve dynamic guardrails over time.
>
> ### Why Hard Pass/Fail Checkpoints? (No Partial Credit!)
> In real production, 'partial credit' is a dangerous trap. If a medical or financial lesson scores 85%, but the 15% missing is factual truth, that content cannot ship!
> 
> We designed **6 Hard Checkpoints** where every check is strictly **1 (Pass)** or **0 (Fail)**:
> - **CP1: ACCURACY_AND_GROUNDED**: Accurately describes RAG as context augmentation. Strictly fails if it claims RAG retrains model weights or alters neural parameters.
> - **CP2: BEGINNER_FRIENDLY_LANGUAGE**: Tested via Flesch-Kincaid Grade Level (<= 7.5) and average sentence length (<= 18 words).
> - **CP3: TEACHES_BY_EXAMPLE**: Mandatory everyday student analogy (Open-Book Exam) plus a concrete query walkthrough.
> - **CP4: NO_UNEXPLAINED_JARGON**: Regex scanner and semantic judge verify that terms like 'Vector', 'Embedding', 'LLM', or 'Hallucination' are immediately demystified with plain English analogies.
> - **CP5: COVERS_KEY_POINTS**: Explains why AI lies (hallucination), what R-A-G stands for, the 3-step mechanics, and career value.
> - **CP6: COHERENT_TEACHING_FLOW**: Logical progression from Hook -> Analogy -> Steps -> Example -> 'Check Your Understanding' mini-quiz.
>
> If even **one** of these 6 checkpoints fails, the draft is rejected."*

---

### Part 3: Live End-to-End Workflow Demonstration (7:00 – 11:00)
**[Switch Screen to Streamlit Web Dashboard: `http://localhost:8501`]**

> *"Now, let's see the system in action!
>
> Here is our interactive web dashboard. On the left sidebar, we have our controls: topic input, model provider selection (`mock`, `gemini`, `openai`), max retry limits, and our deliberate error injection harness.
>
> Let's start with a **clean baseline production run** for our topic: *'Introduction to RAG (Retrieval-Augmented Generation)'*.
>
> I'll click **'Run Agentic Pipeline'**.
>
> Watch the live status indicator:
> 1. It fetches active evolved guardrails from SQLite memory.
> 2. The Generator Agent produces Iteration 1.
> 3. The Evaluator scans readability metrics and checks all 6 dimensions.
> 4. Result: **APPROVED on Iteration 1!**
>
> Let's look at the generated lesson:
> - **Title & Tone**: Warm, welcoming: *'Namaste! If you have just passed your 12th class...'*
> - **Section 1 (The Problem)**: The student sitting in a closed-book exam who doesn't know today's syllabus and starts guessing — explaining **Hallucination** in simple terms.
> - **Section 2 (The Breakthrough)**: Explains RAG as an **Open-Book Exam**. It breaks down R (Retrieval = Search), A (Augmented = Attached), G (Generation = Writing the answer).
> - **Section 3 (Query Walkthrough)**: Concrete example of a student asking about Delhi University hostel fees.
> - **Section 4 (Jargon Demystified)**: Explaining 'Vector Embeddings' as GPS pins on Google Maps!
> - **Section 6 (Active Quiz)**: 3 interactive questions with celebratory answers.
>
> Now, let's click on **Tab 2: Checkpoint Rubric Matrix**.
> Look at the cards: All 6 checkpoints are green (Score: 1/1). Flesch-Kincaid grade is 6.8, and average sentence length is 14.8 words — perfectly hitting our beginner constraints!"*

---

### Part 4: Deliberate Error Injection & Live Evaluator Catch (11:00 – 15:00)
**[Highlight Sidebar in Streamlit Dashboard]**

> *"Now, let's address the most exciting requirement of this assessment: **deliberately injecting a flaw and showing the evaluator catch it live**.
>
> In the sidebar under **'Video Demo Harness'**, I'm going to select:
> 👉 **'Dense Academic Jargon (Fails CP2 & CP4)'**.
>
> This forces the generator to inject dense academic terms like *'non-parametric memory'*, *'orthogonal paradigms shift'*, and *'cosine distance metrics over HNSW indices'* with long, complex sentences.
>
> Let's click **'Run Agentic Pipeline'**!
>
> Look at what happened:
> 1. Iteration 1 was generated with the deliberate flaw.
> 2. The Evaluator immediately stepped in: **Draft Iteration 1 REJECTED!**
> 3. It diagnosed the failure, formulated targeted critique, fed it to the Regenerator Agent, and produced Iteration 2.
> 4. Iteration 2 was re-evaluated and **PASSED 6/6!**
>
> ### Let's Inspect the Rejection Audit Log (Tab 3)
> Look at the exact audit trail:
> - **Rejected Checkpoints**: `CP2` (Beginner-Friendly Language) and `CP4` (No Unexplained Jargon).
> - **Algorithmic Scanner**: Flesch-Kincaid jumped to **17.8** (post-graduate level), and average sentence length was **26.4 words**.
> - **Offending Snippets Flagged**: 
>   * 'orthogonal paradigms shift in probabilistic autoregressive transformer architectures'
>   * 'epistemic uncertainty precipitates stochastic hallucinations'
> - **Targeted Feedback Given to Regenerator**:
>   *'Break long sentences down to under 16 words. Never mention technical terms without an immediate plain-English analogy.'*
> - **Action Taken on Retry**: The regenerator replaced academic phrasing with the Open-Book Exam analogy, dropped sentence length to 14.8 words, and demystified embeddings as Google Maps pins.
>
> This demonstrates the self-healing power of our agentic loop. Before a human ever saw the draft, the bad content was caught and fixed!"*

---

### Part 5: Self-Evolution, Memory & Production Trade-offs (15:00 – 18:30)
**[Switch to Tab 4: Memory & Self-Evolution]**

> *"Now, let's look under the hood at how the system evolves across runs.
>
> Click on **Tab 4: Memory & Self-Evolution**.
>
> ### 1. Persistent Memory Layer (`core/memory.py`)
> We maintain an embedded SQLite database (`data/memory/engine_history.db`).
> Every run stores:
> - The prompt and generation parameters.
> - Each intermediate draft.
> - The full evaluation rubric scores and offending snippets.
> - Latency, token usage, and approval status.
>
> ### 2. The Self-Evolution Engine (`core/evolution.py`)
> When rejections occur, our system doesn't just throw them away. The evolution module inspects the rejection log, extracts the root cause, and synthesizes **'Evolved Guardrails'** stored in `evolved_guardrails.json`.
>
> Look at the active guardrails list on screen:
> - *'Strict Fact-Check Rule: State explicitly that RAG does not retrain weights, but provides real-time reference notes.'*
> - *'Jargon Ban Rule: Ensure terms like Embeddings are accompanied by GPS pin analogies.'*
>
> On all subsequent runs, the pipeline hydrates these guardrails into the system prompt. In other words, **the system gets smarter with every failure**!
>
> ### Key Architectural Trade-offs:
> 1. **Two-Tier Evaluator (Algorithmic + LLM)**:
>    *Trade-off*: Why not just use an LLM prompt? Because LLMs are susceptible to prompt drift, inconsistency, and forgiving leniency. By running deterministic regex scanners and Flesch-Kincaid calculations first, we catch objective violations with zero latency and zero token cost!
> 2. **Max 1–2 Retries Bound**:
>    *Trade-off*: An unconstrained agentic loop can loop infinitely, accumulating massive API bills. Setting a hard cap of 2 retries guarantees termination and predictable latency.
> 3. **Zero-Key Mock Engine**:
>    *Trade-off*: We built a high-fidelity simulation provider so anyone reviewing this repo can clone it and run unit tests or launch the UI instantly without needing an API key."*

---

### Part 6: Summary & Conclusion (18:30 – 20:00)
**[Full Face-Cam Visible]**

> *"To summarize what we've built:
> 1. We built a complete closed-loop agentic content system with zero reliance on manual prompting.
> 2. We designed an unyielding 6-dimension pass/fail rubric tailored for an Indian 12th-grade beginner.
> 3. We proved that the evaluator catches deliberate errors (jargon, hallucinations, missing analogies) and self-heals via targeted regeneration.
> 4. We implemented persistent SQLite memory and dynamic prompt evolution.
> 5. Everything is open-source, tested with 100% pytest pass rate, and ready to run via CLI or interactive Streamlit UI.
>
> Thank you so much for watching, and I look forward to discussing how I can bring this engineering rigor to the Content Systems team!"*

---

## 📋 Pre-Recording Checklist
1. Launch Streamlit: `streamlit run app.py`.
2. Confirm audio/video sync on Loom.
3. Keep this script open on a second monitor or side-by-side window.
4. Practice the flaw injection transition once before recording.
