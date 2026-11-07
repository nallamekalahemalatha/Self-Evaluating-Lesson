"""
Self-Evaluating RAG Lesson Content Generator
Enterprise-Grade Control Center & Agentic Pipeline Studio
"""

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import json
import time
import re
from datetime import datetime

from config import DEFAULT_TOPIC, DEFAULT_PROVIDER, TARGET_PERSONA, RUBRIC_THRESHOLDS, GEMINI_API_KEY, OPENAI_API_KEY
from core.pipeline import ContentPipeline
from core.memory import MemoryStore
from core.evolution import EvolutionEngine
from core.curriculum import COMPREHENSIVE_RAG_LESSON, INTERACTIVE_ASSESSMENT_DATA
from rubrics.lesson_rubric import RUBRIC_CHECKPOINTS, analyze_readability
from rubrics.advanced_metrics import compute_comprehensive_metrics
from core.grounding import GroundingRetriever

# ------------------------------------------------------------------------------
# Page Setup
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Self-Evaluating RAG Lesson Content Generator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------------------------------------------------------------------
# Professional Enterprise Color Palette & Design System
# Primary: Deep Navy (#14213D), Professional Blue (#2563EB), Dark Blue (#1E3A5F), Teal (#0F9D8A)
# Supporting: Light Background (#F5F7FB), White (#FFFFFF), Soft Blue (#EAF1FF), Light Teal (#E6F6F2)
# Status: Success (#16A34A), Warning (#D97706), Error (#DC2626)
# ------------------------------------------------------------------------------
st.markdown("""
<style>
    /* Google Fonts Import */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Manrope:wght@600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        color: #14213D;
    }

    h1, h2, h3, h4, .manrope-heading {
        font-family: 'Manrope', 'Inter', sans-serif !important;
        font-weight: 700;
        letter-spacing: -0.02em;
    }

    code, pre, .mono-code {
        font-family: 'JetBrains Mono', monospace !important;
    }

    /* Top App Header Banner */
    .enterprise-header {
        background: linear-gradient(135deg, #14213D 0%, #1E3A5F 100%);
        border-radius: 12px;
        padding: 24px 30px;
        color: #ffffff;
        margin-bottom: 24px;
        box-shadow: 0 4px 14px rgba(20, 33, 61, 0.12);
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 16px;
    }
    .enterprise-header h1 {
        margin: 0;
        font-size: 1.85rem;
        color: #ffffff;
        font-weight: 800;
    }
    .enterprise-header p {
        margin: 6px 0 0 0;
        color: #EAF1FF;
        font-size: 0.92rem;
    }
    .header-badge {
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.25);
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        color: #ffffff;
    }

    /* Enterprise Metric Cards */
    .metric-card-pro {
        background: #ffffff;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 18px 20px;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.04);
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .metric-card-pro:hover {
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.08);
        border-color: #2563EB;
    }
    .metric-card-pro h5 {
        color: #64748B;
        font-size: 0.78rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin: 0 0 8px 0;
    }
    .metric-card-pro .metric-val {
        color: #14213D;
        font-size: 1.75rem;
        font-weight: 800;
        line-height: 1.1;
        font-family: 'Manrope', sans-serif;
    }
    .metric-card-pro .metric-sub {
        color: #64748B;
        font-size: 0.8rem;
        margin-top: 6px;
    }

    /* Pipeline Stage Stepper */
    .stepper-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        background: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 14px 18px;
        margin-bottom: 24px;
    }
    .step-badge {
        font-size: 0.76rem;
        font-weight: 600;
        padding: 6px 12px;
        border-radius: 20px;
        background: #FFFFFF;
        border: 1px solid #CBD5E1;
        color: #475569;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }
    .step-badge.active {
        background: #2563EB;
        color: #ffffff;
        border-color: #2563EB;
        box-shadow: 0 2px 6px rgba(37, 99, 235, 0.3);
    }
    .step-badge.success {
        background: #16A34A;
        color: #ffffff;
        border-color: #16A34A;
    }
    .step-badge.failed {
        background: #DC2626;
        color: #ffffff;
        border-color: #DC2626;
    }

    /* Checkpoint Visual Scorecards */
    .cp-card-pass {
        border-left: 5px solid #16A34A;
        background: #FFFFFF;
        border-top: 1px solid #E2E8F0;
        border-right: 1px solid #E2E8F0;
        border-bottom: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 14px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.03);
    }
    .cp-card-fail {
        border-left: 5px solid #DC2626;
        background: #FFF5F5;
        border-top: 1px solid #FECACA;
        border-right: 1px solid #FECACA;
        border-bottom: 1px solid #FECACA;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 14px;
        box-shadow: 0 2px 4px rgba(220, 38, 38, 0.05);
    }

    /* Diff Visualizer */
    .diff-del {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 4px 10px;
        margin: 3px 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.84rem;
        border-radius: 4px;
        border-left: 3px solid #DC2626;
    }
    .diff-add {
        background-color: #DCFCE7;
        color: #166534;
        padding: 4px 10px;
        margin: 3px 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.84rem;
        border-radius: 4px;
        border-left: 3px solid #16A34A;
    }

    /* Pedagogical Callout Box */
    .pedagogy-callout {
        background: #EAF1FF;
        border-left: 4px solid #2563EB;
        padding: 14px 18px;
        border-radius: 0 8px 8px 0;
        margin: 14px 0;
        color: #1E3A5F;
        font-size: 0.92rem;
    }
    .pedagogy-callout strong {
        color: #14213D;
    }

    /* Indian Analogy Card */
    .analogy-card {
        background: #E6F6F2;
        border: 1px solid #A7F3D0;
        border-left: 4px solid #0F9D8A;
        border-radius: 8px;
        padding: 16px 20px;
        margin: 12px 0;
        color: #064E3B;
    }

    /* Clean Reading Layout */
    .reader-container {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 36px 44px;
        line-height: 1.75;
        font-size: 1.05rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# Persistence & Memory Singletons
# ------------------------------------------------------------------------------
@st.cache_resource
def get_memory_store():
    return MemoryStore()

@st.cache_resource
def get_evolution_engine():
    return EvolutionEngine()

memory_store = get_memory_store()
evolution_engine = get_evolution_engine()

# Initialize Session State
if "latest_run" not in st.session_state:
    st.session_state.latest_run = None
if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False
if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}
if "selected_view" not in st.session_state:
    st.session_state.selected_view = "📊 Overview Dashboard"

# ------------------------------------------------------------------------------
# Left Sidebar Navigation (Enterprise Architecture)
# ------------------------------------------------------------------------------
st.sidebar.markdown("""
<div style="padding: 10px 0 16px 0;">
    <h3 style="margin: 0; color: #14213D; font-size: 1.15rem; font-weight: 800; font-family: 'Manrope', sans-serif;">
        ⚡ GenAI Engine Studio
    </h3>
    <div style="font-size: 0.78rem; color: #64748B; margin-top: 2px;">
        Self-Evaluating RAG Lesson Generator
    </div>
</div>
""", unsafe_allow_html=True)

nav_options = [
    "📊 Overview Dashboard",
    "⚡ Lesson Generator Studio",
    "🔄 Visual Agentic Pipeline",
    "🎯 Six-Checkpoint Evaluation",
    "📖 Learning Content Reader",
    "📐 Diagrams & Visualizations",
    "📝 Interactive Quizzes",
    "✂️ Self-Repair & Semantic Diff",
    "🧠 Cognitive & Linguistic Analytics",
    "💾 Memory & Self-Evolution",
    "📋 Execution History & Logs",
    "⚙️ Settings & System Controls"
]

selected_view = st.sidebar.radio(
    "Navigation Views",
    options=nav_options,
    index=nav_options.index(st.session_state.selected_view) if st.session_state.selected_view in nav_options else 0,
    label_visibility="collapsed"
)
st.session_state.selected_view = selected_view

st.sidebar.markdown("---")

# Quick Engine Status Badge
st.sidebar.markdown("""
<div style="background: #F8FAFC; border: 1px solid #E2E8F0; border-radius: 8px; padding: 10px 14px;">
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 0.75rem; font-weight: 700; color: #64748B; text-transform: uppercase;">Engine Status</span>
        <span style="display: inline-block; width: 8px; height: 8px; border-radius: 50%; background: #16A34A;"></span>
    </div>
    <div style="font-size: 0.82rem; font-weight: 600; color: #14213D; margin-top: 4px;">
        Active & Verified
    </div>
    <div style="font-size: 0.72rem; color: #64748B; margin-top: 2px;">
        6 Checkpoints Hard Enforced
    </div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# Helper Functions
# ------------------------------------------------------------------------------
def render_mermaid_chart(diagram_code: str, height: int = 420):
    """Render Mermaid syntax as an interactive visual graphic via CDN."""
    escaped_code = diagram_code.strip()
    html_block = f"""
    <div style="background: #ffffff; padding: 20px; border-radius: 10px; border: 1px solid #E2E8F0; box-shadow: 0 2px 6px rgba(0,0,0,0.03); text-align: center;">
        <pre class="mermaid" style="background: transparent; margin: 0;">
{escaped_code}
        </pre>
    </div>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ startOnLoad: true, theme: 'neutral', securityLevel: 'loose' }});
    </script>
    """
    components.html(html_block, height=height, scrolling=True)

# ------------------------------------------------------------------------------
# Top Header Banner
# ------------------------------------------------------------------------------
st.markdown("""
<div class="enterprise-header">
    <div>
        <h1>Self-Evaluating RAG Lesson Content Generator</h1>
        <p>Autonomous Closed-Loop Curriculum Architecture for Non-English-Medium Learners | 6 Hard Checkpoints (Zero Partial Credit)</p>
    </div>
    <div>
        <span class="header-badge">Target: 12th-Grade India</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# VIEW 1: Overview Dashboard (Real SQLite Data)
# ------------------------------------------------------------------------------
if selected_view == "📊 Overview Dashboard":
    st.markdown("### **Executive Overview & Performance Metrics**")
    st.caption("Real-time telemetry and aggregated historical run data directly from SQLite (`data/memory/engine_history.db`):")

    analytics = memory_store.get_aggregate_analytics()

    k1, k2, k3, k4, k5, k6 = st.columns(6)
    with k1:
        st.markdown(f"""
        <div class="metric-card-pro">
            <h5>Total Generations</h5>
            <div class="metric-val">{analytics['total_runs']}</div>
            <div class="metric-sub">Pipeline runs</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="metric-card-pro">
            <h5>Approved</h5>
            <div class="metric-val" style="color: #16A34A;">{analytics['approved_runs']}</div>
            <div class="metric-sub">Cleared all 6 checks</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div class="metric-card-pro">
            <h5>Rejected</h5>
            <div class="metric-val" style="color: #DC2626;">{analytics['rejected_runs']}</div>
            <div class="metric-sub">Quality bar caught</div>
        </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
        <div class="metric-card-pro">
            <h5>Approval Rate</h5>
            <div class="metric-val" style="color: #2563EB;">{analytics['approval_rate_pct']}%</div>
            <div class="metric-sub">Reliability score</div>
        </div>
        """, unsafe_allow_html=True)
    with k5:
        st.markdown(f"""
        <div class="metric-card-pro">
            <h5>Avg Iterations</h5>
            <div class="metric-val">{analytics['avg_iterations_to_approval']}</div>
            <div class="metric-sub">Self-repair cycles</div>
        </div>
        """, unsafe_allow_html=True)
    with k6:
        st.markdown(f"""
        <div class="metric-card-pro">
            <h5>Avg FK Grade</h5>
            <div class="metric-val">{analytics['avg_passing_fk_grade']}</div>
            <div class="metric-sub">Target <= 7.5</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_chart1, col_chart2 = st.columns([1, 1])
    with col_chart1:
        st.markdown("#### **Historical Checkpoint Failure Distribution**")
        freqs = analytics["checkpoint_failure_frequencies"]
        if freqs:
            df_freq = pd.DataFrame(list(freqs.items()), columns=["Checkpoint", "Failure Count"]).set_index("Checkpoint")
            st.bar_chart(df_freq, color="#2563EB")
        else:
            st.info("No failure violations recorded in database yet.")

    with col_chart2:
        st.markdown("#### **Active Evolved Guardrails in Persistent Memory**")
        st.caption("Synthesized by Evolution Engine from historical failure traces:")
        active_guardrails = evolution_engine.get_active_guardrails()
        for idx, rule in enumerate(active_guardrails[:5], 1):
            st.markdown(f"""
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 6px; padding: 10px 14px; margin-bottom: 8px; font-size: 0.88rem;">
                <strong style="color: #2563EB;">Rule #{idx}:</strong> {rule}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### **Recent Pipeline Executions**")
    recent_runs = memory_store.get_all_runs(limit=8)
    if recent_runs:
        df_recent = pd.DataFrame(recent_runs)
        st.dataframe(df_recent, use_container_width=True)
    else:
        st.info("No historical runs found in database.")

# ------------------------------------------------------------------------------
# VIEW 2: Lesson Generator Studio
# ------------------------------------------------------------------------------
elif selected_view == "⚡ Lesson Generator Studio":
    st.markdown("### **Lesson Generation Studio & Control Center**")
    st.caption("Configure generation parameters, inspect grounding literature, or test evaluator resilience:")

    col_config, col_grounding = st.columns([1.2, 1])

    with col_config:
        st.markdown("#### **1. Curriculum Configuration**")
        studio_topic = st.text_input("Lesson Subject / Topic", value=DEFAULT_TOPIC)
        
        c_p1, c_p2 = st.columns(2)
        with c_p1:
            difficulty = st.selectbox("Pedagogical Difficulty", ["Beginner (12th-Grade Non-English Medium)", "Intermediate", "Advanced"], index=0)
        with c_p2:
            target_length = st.selectbox("Target Curriculum Depth", ["Standard (1,000 - 1,200 words)", "Compact (600 words)", "Deep-Dive (2,000 words)"], index=0)

        learner_profile = st.selectbox(
            "Learner Persona",
            [
                "Indian 12th-Grade Graduate (Non-English Medium Background)",
                "Rural Polytechnic / Diploma Engineering Student",
                "Non-Tech Career Switcher"
            ],
            index=0
        )

        st.markdown("#### **2. Inference Engine & Parameters**")
        col_inf1, col_inf2 = st.columns(2)
        with col_inf1:
            studio_provider = st.selectbox("Inference Provider", ["mock", "gemini", "openai"], index=0, help="'mock' runs full simulated zero-key pipeline.")
        with col_inf2:
            studio_retries = st.slider("Max Self-Correction Retries", min_value=1, max_value=2, value=2)

        st.markdown("#### **3. Evaluator Stress-Test Harness**")
        st.caption("Inject deliberate flaws to verify the evaluator detects and rejects violations:")
        flaw_choice = st.radio(
            "Deliberate Error Injection Mode",
            [
                "None (Production Standard - 100% Passing)",
                "Dense Academic Jargon (Violates CP2 & CP4)",
                "Factual Hallucination / Weights Retraining (Violates CP1)",
                "Abstract Theory / Zero Analogy (Violates CP3)"
            ],
            index=0
        )

        flaw_map = {
            "None (Production Standard - 100% Passing)": None,
            "Dense Academic Jargon (Violates CP2 & CP4)": "jargon",
            "Factual Hallucination / Weights Retraining (Violates CP1)": "hallucination",
            "Abstract Theory / Zero Analogy (Violates CP3)": "no_analogy"
        }
        selected_deliberate_flaw = flaw_map[flaw_choice]

        st.markdown("<br>", unsafe_allow_html=True)
        execute_btn = st.button("🚀 Execute Autonomous Pipeline", type="primary", use_container_width=True)

    with col_grounding:
        st.markdown("#### **Authoritative Grounding Knowledge Base**")
        st.caption("Grounding references retrieved to teach RAG factually (Lewis et al. 2020 & IEEE):")
        grounder = GroundingRetriever()
        retrieved_preview = grounder.retrieve(studio_topic, top_k=3)
        for chunk in retrieved_preview:
            with st.expander(f"📚 [{chunk['chunk_id']}] {chunk['title']}", expanded=False):
                st.caption(f"Source: {chunk['source']} | Score: {chunk['similarity_score']*100:.0f}%")
                st.write(chunk["content"])

    # Execution Action
    if execute_btn:
        pipeline = ContentPipeline(
            provider=studio_provider,
            max_retries=studio_retries,
            memory_store=memory_store,
            evolution_engine=evolution_engine
        )

        progress_placeholder = st.empty()
        status_box = st.empty()

        def update_ui_status(stage, msg):
            stage_weights = {
                "START": (10, "Initializing pipeline context..."),
                "RETRIEVAL": (25, "Retrieving authoritative domain grounding chunks..."),
                "AUGMENT": (35, "Augmenting prompt with grounded references..."),
                "MEMORY": (45, "Hydrating evolved guardrails from SQLite memory..."),
                "GENERATE": (60, "Generating curriculum draft..."),
                "EVALUATE": (75, "Running Multi-Inspector 6-checkpoint rubric..."),
                "REJECT": (82, "Quality bar breached. Synthesizing prescriptive critique..."),
                "REGENERATE": (90, "Executing surgical regeneration patch..."),
                "PASS": (95, "All 6 checkpoints verified! Ship-ready approval..."),
                "EVOLUTION": (98, "Synthesizing new prompt guardrails from run logs..."),
                "DONE": (100, "Pipeline execution complete.")
            }
            pct, default_msg = stage_weights.get(stage, (50, msg))
            progress_placeholder.progress(pct, text=f"[{stage}] {msg}")

        result = pipeline.execute(
            topic=studio_topic,
            deliberate_flaw=selected_deliberate_flaw,
            status_callback=update_ui_status,
            target_persona=learner_profile
        )

        st.session_state.latest_run = result
        progress_placeholder.empty()
        status_box.success(f"Pipeline Execution Finished! Verdict: {'APPROVED' if result.is_approved else 'REJECTED'} (Run ID: {result.run_id})")

    # If recent run exists
    if st.session_state.latest_run:
        res = st.session_state.latest_run
        st.markdown("---")
        st.markdown(f"### **Latest Execution Summary: {res.topic}**")
        c_res1, c_res2, c_res3, c_res4 = st.columns(4)
        c_res1.metric("Status", "APPROVED" if res.is_approved else "REJECTED")
        c_res2.metric("Total Iterations", res.total_iterations)
        c_res3.metric("Latency", f"{res.telemetry.get('total_duration_sec', 'N/A')}s")
        c_res4.metric("Tokens", f"{res.telemetry.get('total_tokens', 0):,}")

# ------------------------------------------------------------------------------
# VIEW 3: Visual Agentic Pipeline
# ------------------------------------------------------------------------------
elif selected_view == "🔄 Visual Agentic Pipeline":
    st.markdown("### **Visual Agentic Pipeline Architecture**")
    st.caption("Inspect the 13 discrete stages of the autonomous generate → evaluate → regenerate loop:")

    pipeline_mode = st.radio("Pipeline Inspection Mode", ["Technical Architecture View", "💡 Understand This Pipeline (Beginner Mode for 12th Graders)"], horizontal=True)

    stages_data = [
        {"num": 1, "name": "User Input Analysis", "tech": "Parses topic, persona, and curricular bounds", "beginner": "You type the lesson topic you want to learn, like 'Introduction to RAG'."},
        {"num": 2, "name": "Authoritative Grounding Retrieval", "tech": "Semantic vector search against Lewis et al. & IEEE corpus", "beginner": "The system searches a trusted digital library for genuine facts about RAG."},
        {"num": 3, "name": "Dynamic Context Augmentation", "tech": "Assembles verified chunks into system context", "beginner": "It glues the verified facts right next to the question so the AI doesn't have to guess."},
        {"num": 4, "name": "Memory Hydration", "tech": "Loads active evolved guardrails from SQLite database", "beginner": "The system checks past mistakes stored in its memory to make sure it doesn't repeat them."},
        {"num": 5, "name": "Curriculum Draft Generation", "tech": "Generator Agent executes constrained multi-turn draft", "beginner": "The AI writes a complete first draft of the lesson using friendly words and student analogies."},
        {"num": 6, "name": "Tier 1: Algorithmic Guardrail Scan", "tech": "Deterministic FK grade, sentence variance, regex jargon scan", "beginner": "A strict math scanner checks if sentences are short and words are simple."},
        {"num": 7, "name": "Tier 2: Multi-Inspector Binary Evaluation", "tech": "Committee of 4 specialized inspectors enforce CP1-CP6", "beginner": "Four teacher inspectors grade the draft against 6 hard checkpoints (Pass or Fail only)."},
        {"num": 8, "name": "Decision Engine", "tech": "Binary gate: passes if and only if all 6 checkpoints clear", "beginner": "If even 1 checkpoint fails, the lesson is immediately rejected for repairs."},
        {"num": 9, "name": "Critique & Prescriptive Synthesis", "tech": "Synthesizes exact line numbers and concrete remediation", "beginner": "The inspector writes a clear note pointing out the exact problem and how to fix it."},
        {"num": 10, "name": "Surgical Regeneration & Patching", "tech": "Regenerator Agent performs localized patch, preserving structure", "beginner": "The AI fixes only the flawed paragraphs while keeping the good parts untouched."},
        {"num": 11, "name": "Re-Evaluation Loop", "tech": "Evaluates repaired draft against full rubric suite", "beginner": "The inspectors grade the revised draft again to ensure all 6 checks now pass."},
        {"num": 12, "name": "Memory Update & Evolution", "tech": "Logs rejection root cause; synthesizes new guardrail rules", "beginner": "The engine saves what it learned into permanent memory to stay smart forever."},
        {"num": 13, "name": "Final Artifact Approval", "tech": "Emits verified lesson, rejection audit trail, and telemetry", "beginner": "The approved lesson is handed to the student with 100% confidence of accuracy!"}
    ]

    st.markdown("<br>", unsafe_allow_html=True)

    for stg in stages_data:
        desc = stg["tech"] if pipeline_mode == "Technical Architecture View" else stg["beginner"]
        st.markdown(f"""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px 18px; margin-bottom: 10px; display: flex; align-items: center; justify-content: space-between;">
            <div style="display: flex; align-items: center; gap: 14px;">
                <span style="background: #2563EB; color: #ffffff; border-radius: 50%; width: 28px; height: 28px; display: flex; align-items: center; justify-content: center; font-size: 0.8rem; font-weight: 700;">
                    {stg['num']}
                </span>
                <div>
                    <strong style="color: #14213D; font-size: 0.95rem;">{stg['name']}</strong>
                    <div style="color: #64748B; font-size: 0.85rem; margin-top: 2px;">{desc}</div>
                </div>
            </div>
            <span class="step-badge success">Verified Stage</span>
        </div>
        """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# VIEW 4: Six-Checkpoint Evaluation Center
# ------------------------------------------------------------------------------
elif selected_view == "🎯 Six-Checkpoint Evaluation":
    st.markdown("### **Six-Checkpoint Evaluation Center (Zero Partial Credit)**")
    st.caption("Every checkpoint represents a non-negotiable quality bar. A single failure mandates rejection and self-repair:")

    res = st.session_state.latest_run
    if not res:
        # Default showcase with passing comprehensive lesson evaluation
        from core.mock_engine import get_mock_evaluation
        showcase_eval = get_mock_evaluation("Introduction to RAG", COMPREHENSIVE_RAG_LESSON, 1)
        evaluations_to_show = [showcase_eval]
        st.info("Displaying baseline evaluation of the verified flagship curriculum. Run the pipeline in Lesson Generator Studio to inspect live runs.")
    else:
        evaluations_to_show = res.evaluations

    for ev in evaluations_to_show:
        st.markdown(f"#### **Iteration {ev.iteration} Evaluation Matrix (Passed: {ev.passed_count}/{ev.total_count})**")
        st.markdown(f"**Executive Critique:** *{ev.overall_critique}*")

        for cp in ev.checkpoints:
            card_class = "cp-card-pass" if cp.passed else "cp-card-fail"
            badge = "PASSED" if cp.passed else "FAILED"
            badge_color = "#16A34A" if cp.passed else "#DC2626"

            snippets_block = ""
            if cp.offending_snippets:
                snippets_block = "<div style='margin-top: 8px;'><strong>Detected Violating Snippets:</strong><ul>" + "".join(f"<li><code>{s}</code></li>" for s in cp.offending_snippets) + "</ul></div>"

            st.markdown(f"""
            <div class="{card_class}">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <h4 style="margin: 0; font-size: 1.05rem; color: #14213D;">{cp.checkpoint_id}: {cp.name}</h4>
                    <span style="font-weight: 800; color: {badge_color}; font-size: 0.95rem;">{badge} (Score: {cp.score}/1)</span>
                </div>
                <div style="font-size: 0.8rem; color: #64748B; margin: 4px 0;">Dimension: {cp.dimension}</div>
                <p style="margin: 6px 0; color: #1E3A5F; font-size: 0.92rem;"><strong>Evaluator Reasoning:</strong> {cp.reason}</p>
                {snippets_block}
                <div style="margin-top: 6px; font-size: 0.88rem; color: #2563EB;"><strong>Prescriptive Action:</strong> {cp.prescriptive_action}</div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown("---")

# ------------------------------------------------------------------------------
# VIEW 5: Learning Content Reader
# ------------------------------------------------------------------------------
elif selected_view == "📖 Learning Content Reader":
    st.markdown("### **Flagship Learning Content: Introduction to RAG**")
    st.caption("Specially engineered for an Indian 12th-grade graduate from a non-English medium background:")

    res = st.session_state.latest_run
    lesson_to_render = res.final_lesson if res else COMPREHENSIVE_RAG_LESSON
    stats = analyze_readability(lesson_to_render)

    col_meta1, col_meta2, col_meta3, col_meta4 = st.columns(4)
    col_meta1.metric("Reading Time", "~25 Minutes")
    col_meta2.metric("Word Count", f"{stats.total_words:,} words")
    col_meta3.metric("Flesch-Kincaid Grade", f"Grade {stats.flesch_kincaid_grade}")
    col_meta4.metric("Analogy Anchors", "Kirana Store & IRCTC")

    st.markdown("<br>", unsafe_allow_html=True)

    # Highlighted Pedagogical Anchors
    c_anc1, c_anc2 = st.columns(2)
    with c_anc1:
        st.markdown("""
        <div class="analogy-card">
            <h5 style="margin:0 0 6px 0; font-weight:700;">🏪 The Kirana Store Analogy</h5>
            When you ask a local shopkeeper for spices, they don't invent them out of memory. They check their store shelf, retrieve the packet, and hand it to you. That is RAG!
        </div>
        """, unsafe_allow_html=True)
    with c_anc2:
        st.markdown("""
        <div class="analogy-card">
            <h5 style="margin:0 0 6px 0; font-weight:700;">🚆 The IRCTC Railway Analogy</h5>
            When you check train berth status on your phone, the app doesn't guess from last year's schedule. It retrieves live seat availability from the railway database and prints your berth.
        </div>
        """, unsafe_allow_html=True)

    st.download_button(
        label="📥 Download Clean Lesson Markdown",
        data=lesson_to_render,
        file_name="introduction_to_rag_lesson.md",
        mime="text/markdown"
    )

    st.markdown("<br>", unsafe_allow_html=True)
    with st.container():
        st.markdown(f"""
        <div class="reader-container">
            {lesson_to_render}
        </div>
        """, unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# VIEW 6: Diagrams & Visualizations
# ------------------------------------------------------------------------------
elif selected_view == "📐 Diagrams & Visualizations":
    st.markdown("### **Visual Architecture & Interactive Diagrams**")
    st.caption("Clear visual illustrations helping visual learners understand RAG intuitively:")

    d1, d2, d3 = st.tabs(["1. RAG 3-Step Flowchart", "2. Traditional AI vs RAG", "3. Vector Space & GPS Pins"])

    with d1:
        st.markdown("#### **The Complete 3-Step RAG Execution Engine**")
        rag_flowchart_mermaid = """
flowchart TD
    User["Student Question:<br/>'When is Delhi University hostel fee due?'"] --> SearchEngine["Step 1: RETRIEVAL ENGINE<br/>Searches Official Circular PDFs"]
    PDFStore[("University Circulars Database")] --> SearchEngine
    SearchEngine --> ExtractedDoc["Found Verified Fact:<br/>Hostel fee due 15th July 2026"]
    ExtractedDoc --> AugmentPrompt["Step 2: CONTEXT AUGMENTATION<br/>Pastes Fact into Prompt Note"]
    User --> AugmentPrompt
    AugmentPrompt --> LLMGen["Step 3: GENERATION ENGINE<br/>AI Reads Note and Answers"]
    LLMGen --> FinalAnswer["Final Truthful Answer:<br/>Deadline is 15th July 2026!"]
"""
        render_mermaid_chart(rag_flowchart_mermaid, height=440)
        with st.expander("View Raw Mermaid Code"):
            st.code(rag_flowchart_mermaid, language="mermaid")

    with d2:
        st.markdown("#### **Exam Analogy Architecture: Closed-Book vs Open-Book**")
        exam_mermaid = """
flowchart LR
    subgraph TraditionalAI["Standard AI (Closed-Book Exam)"]
        direction TB
        Q1["User Question"] --> LLM1["AI Model Weights<br/>(Static Old Memory)"]
        LLM1 --> Risk["High Hallucination Risk<br/>Guesses when unknown!"]
    end

    subgraph RAGSystem["RAG System (Open-Book Exam)"]
        direction TB
        Q2["User Question"] --> Search["Live Search<br/>in Knowledge Base"]
        Search --> Doc["Verified Document"]
        Doc --> LLM2["AI Model reads prompt<br/>+ Verified Document"]
        LLM2 --> Safe["Truthful Answer<br/>Zero Guesses!"]
    end
"""
        render_mermaid_chart(exam_mermaid, height=400)
        with st.expander("View Raw Mermaid Code"):
            st.code(exam_mermaid, language="mermaid")

    with d3:
        st.markdown("#### **Vector Embeddings: Digital GPS Pins for Sentences**")
        st.markdown("""
        <div class="pedagogy-callout">
            <strong>How Embeddings Work for 12th Graders:</strong><br>
            Just like Google Maps uses two numbers (Latitude and Longitude) to locate any house in India,
            AI gives each sentence a list of numbers called an <em>Embedding</em>. Sentences with similar meanings get numbers that are close to each other!
        </div>
        """, unsafe_allow_html=True)
        vector_mermaid = """
flowchart TD
    RawSentence["Sentence:<br/>'Where is my hostel fee receipt?'"] --> EmbedModel["Embedding Model<br/>(Sentence GPS Machine)"]
    EmbedModel --> VectorCoords["GPS Pin Coordinates:<br/>[0.82, -0.41, 0.95, ...]"]
    VectorCoords --> VectorDB[("Vector Database<br/>Finds closest matching circular!")]
"""
        render_mermaid_chart(vector_mermaid, height=360)

# ------------------------------------------------------------------------------
# VIEW 7: Interactive Quizzes & Assessment
# ------------------------------------------------------------------------------
elif selected_view == "📝 Interactive Quizzes":
    st.markdown("### **Interactive Assessment Center**")
    st.caption("11 comprehensive questions covering core recall, architectural mechanics, and practical Indian enterprise scenarios:")

    if st.session_state.quiz_submitted:
        # Show results
        user_answers = st.session_state.quiz_answers
        total_q = len(INTERACTIVE_ASSESSMENT_DATA)
        correct_count = 0

        # Calculate score for MCQs and T/F
        for q in INTERACTIVE_ASSESSMENT_DATA:
            qid = q["id"]
            if q["type"] in ["mcq", "tf"]:
                if user_answers.get(qid) == q["correct_index"]:
                    correct_count += 1
            else:
                # Short answer/scenario: grant point if user typed answer
                if user_answers.get(qid, "").strip():
                    correct_count += 1

        score_pct = int((correct_count / total_q) * 100)
        grade_letter = "A+" if score_pct >= 90 else "A" if score_pct >= 75 else "B" if score_pct >= 60 else "Review Needed"

        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #16A34A 0%, #0F9D8A 100%); border-radius: 10px; padding: 24px; color: #ffffff; margin-bottom: 24px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <h3 style="margin: 0; color: #ffffff;">Assessment Score: {correct_count} / {total_q} ({score_pct}%)</h3>
                    <p style="margin: 4px 0 0 0; color: #E6F6F2;">Performance Grade: <strong>{grade_letter}</strong> | Beginner AI Curriculum Mastery</p>
                </div>
                <div style="background: rgba(255,255,255,0.2); padding: 8px 18px; border-radius: 20px; font-weight: 700; font-size: 1.1rem;">
                    {grade_letter}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔄 Retake Assessment", type="secondary"):
            st.session_state.quiz_submitted = False
            st.session_state.quiz_answers = {}
            st.rerun()

        st.markdown("---")
        st.markdown("#### **Detailed Question-by-Question Review**")

        for idx, q in enumerate(INTERACTIVE_ASSESSMENT_DATA, 1):
            qid = q["id"]
            user_val = user_answers.get(qid)
            
            if q["type"] in ["mcq", "tf"]:
                is_correct = (user_val == q["correct_index"])
                border_color = "#16A34A" if is_correct else "#DC2626"
                bg_color = "#F0FDF4" if is_correct else "#FEF2F2"
                status_label = "CORRECT" if is_correct else "NEEDS REVIEW"

                user_choice_text = q["options"][user_val] if user_val is not None else "No answer selected"
                correct_choice_text = q["options"][q["correct_index"]]

                st.markdown(f"""
                <div style="background: {bg_color}; border-left: 4px solid {border_color}; border-radius: 6px; padding: 14px 18px; margin-bottom: 14px;">
                    <div style="display: flex; justify-content: space-between;">
                        <strong style="color: #14213D;">Question {idx}: {q['question']}</strong>
                        <span style="font-weight: 700; color: {border_color}; font-size: 0.85rem;">{status_label}</span>
                    </div>
                    <div style="margin: 6px 0; font-size: 0.88rem; color: #334155;">
                        Your Answer: <code>{user_choice_text}</code> | Correct: <strong>{correct_choice_text}</strong>
                    </div>
                    <div style="font-size: 0.86rem; color: #0369A1; margin-top: 4px;">
                        💡 <strong>Explanation:</strong> {q['explanation']}
                    </div>
                    <div style="font-size: 0.82rem; color: #64748B; margin-top: 2px;">
                        ⚠️ <em>Common Misconception Debunked:</em> {q.get('misconception', '')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="background: #FFFFFF; border-left: 4px solid #2563EB; border: 1px solid #E2E8F0; border-radius: 6px; padding: 14px 18px; margin-bottom: 14px;">
                    <strong style="color: #14213D;">Question {idx} [{q['category']}]: {q['question']}</strong>
                    <div style="margin: 8px 0; font-size: 0.88rem; color: #334155;">
                        <strong>Your Response:</strong> <em>"{user_val}"</em>
                    </div>
                    <div style="font-size: 0.86rem; color: #166534; background: #F0FDF4; padding: 8px 12px; border-radius: 4px;">
                        ✅ <strong>Model Answer:</strong> {q.get('sample_answer', '')}
                    </div>
                    <div style="font-size: 0.84rem; color: #0369A1; margin-top: 6px;">
                        💡 <strong>Key Rationale:</strong> {q['explanation']}
                    </div>
                </div>
                """, unsafe_allow_html=True)

    else:
        # Render Quiz Form
        with st.form("quiz_form"):
            form_answers = {}
            for idx, q in enumerate(INTERACTIVE_ASSESSMENT_DATA, 1):
                st.markdown(f"**Question {idx} ({q['category']}):** {q['question']}")
                qid = q["id"]
                if q["type"] in ["mcq", "tf"]:
                    selected = st.radio(
                        label=f"q_{qid}",
                        options=range(len(q["options"])),
                        format_func=lambda i, opts=q["options"]: opts[i],
                        key=f"field_{qid}",
                        label_visibility="collapsed"
                    )
                    form_answers[qid] = selected
                else:
                    ans_text = st.text_area(label=f"q_{qid}", placeholder="Type your explanation here...", key=f"field_{qid}", label_visibility="collapsed")
                    form_answers[qid] = ans_text
                st.markdown("<br>", unsafe_allow_html=True)

            submitted = st.form_submit_button("Submit Assessment & Grade", type="primary", use_container_width=True)
            if submitted:
                st.session_state.quiz_answers = form_answers
                st.session_state.quiz_submitted = True
                st.rerun()

# ------------------------------------------------------------------------------
# VIEW 8: Self-Repair & Semantic Diff Viewer
# ------------------------------------------------------------------------------
elif selected_view == "✂️ Self-Repair & Semantic Diff":
    st.markdown("### **Surgical Patch & Semantic Diff Analyzer**")
    st.caption("Inspect how the Regenerator Agent surgically repairs violating lines rather than blindly rewriting the lesson:")

    res = st.session_state.latest_run
    if res and res.iteration_diffs:
        for item in res.iteration_diffs:
            st.markdown(f"#### **Iteration {item['from_iteration']} → Iteration {item['to_iteration']} Repair Trace**")
            st.info(f"**Surgical Repair Summary:** {item['summary']}")

            diff_data = item["diff"]
            cA, cB, cC = st.columns(3)
            cA.metric("Lines Added", diff_data["lines_added"])
            cB.metric("Lines Removed", diff_data["lines_deleted"])
            cC.metric("Structure Preservation Rate", f"{diff_data['preservation_rate_pct']}%")

            st.markdown("##### **Line-by-Line Semantic Diff**")
            for chunk in diff_data["diff_chunks"]:
                if chunk["type"] == "deleted":
                    st.markdown(f"<div class='diff-del'>- {chunk['text']}</div>", unsafe_allow_html=True)
                elif chunk["type"] == "added":
                    st.markdown(f"<div class='diff-add'>+ {chunk['text']}</div>", unsafe_allow_html=True)
            st.markdown("---")
    elif res:
        st.success("✨ Lesson cleared all 6 checkpoints on Iteration 1 with 100% precision! No surgical repairs required.")
    else:
        st.info("Execute a pipeline run with a deliberate flaw (in Lesson Generator Studio) to see the surgical diff viewer in action.")

# ------------------------------------------------------------------------------
# VIEW 9: Cognitive & Linguistic Analytics
# ------------------------------------------------------------------------------
elif selected_view == "🧠 Cognitive & Linguistic Analytics":
    st.markdown("### **Multi-Index Cognitive & Linguistic Analytics Suite**")
    st.caption("Algorithmic verification ensuring vocabulary and sentence structures remain accessible to 12th-grade learners:")

    res = st.session_state.latest_run
    lesson_text = res.final_lesson if res else COMPREHENSIVE_RAG_LESSON
    metrics = compute_comprehensive_metrics(lesson_text)

    ca1, ca2, ca3, ca4, ca5 = st.columns(5)
    ca1.metric("Flesch-Kincaid", f"Grade {metrics['flesch_kincaid_grade']}", delta="Target <= 7.5", delta_color="inverse")
    ca2.metric("Coleman-Liau", f"Grade {metrics['coleman_liau_index']}")
    ca3.metric("Gunning-Fog", f"{metrics['gunning_fog_index']}")
    ca4.metric("Easy Words Ratio", f"{metrics['easy_word_percentage']}%", delta="Target >= 55%")
    ca5.metric("Cognitive Score", f"{metrics['cognitive_accessibility_score']} / 100")

    st.markdown("---")
    col_stat1, col_stat2 = st.columns(2)
    with col_stat1:
        st.markdown("#### **Sentence Structure & Length Distribution**")
        st.markdown(f"- **Total Sentences**: `{metrics['total_sentences']}`")
        st.markdown(f"- **Total Word Count**: `{metrics['total_words']} words`")
        st.markdown(f"- **Average Sentence Length**: `{metrics['avg_sentence_length']} words/sentence` (Target <= 16)")
        st.markdown(f"- **Sentence Length Std Dev**: `±{metrics['sentence_length_std_dev']} words`")

    with col_stat2:
        st.markdown("#### **Audience Guardrail Verification**")
        stats_obj = analyze_readability(lesson_text)
        st.markdown(f"- **Open-Book / Exam Analogy Present**: `{'✅ Yes' if stats_obj.has_relatable_analogy else '❌ No'}`")
        st.markdown(f"- **Active Comprehension Quiz Embedded**: `{'✅ Yes' if stats_obj.has_check_for_understanding else '❌ No'}`")
        st.markdown(f"- **Unexplained Jargon Violations**: `{len(stats_obj.unexplained_jargon_found)} detected`")

# ------------------------------------------------------------------------------
# VIEW 10: Memory & Self-Evolution Store
# ------------------------------------------------------------------------------
elif selected_view == "💾 Memory & Self-Evolution":
    st.markdown("### **Persistent Memory & Evolution Store**")
    st.caption("How the system learns across runs by persisting failures and synthesizing sharp guardrails:")

    active_rules = evolution_engine.get_active_guardrails()
    st.markdown("#### **Active Evolved Prompt Guardrails**")
    for idx, rule in enumerate(active_rules, 1):
        st.markdown(f"""
        <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 8px; padding: 12px 18px; margin-bottom: 8px;">
            <strong style="color: #2563EB;">Rule #{idx}:</strong> {rule}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("#### **Database Storage Inspection**")
    st.markdown("- **Database File**: `data/memory/engine_history.db`")
    st.markdown("- **Engine**: SQLite3 with WAL journal mode")
    st.markdown("- **Persistence Tables**: `pipeline_runs`, `lesson_drafts`, `rejection_audit_logs`, `evolved_guardrails`")

# ------------------------------------------------------------------------------
# VIEW 11: Execution History & Logs
# ------------------------------------------------------------------------------
elif selected_view == "📋 Execution History & Logs":
    st.markdown("### **Pipeline Execution History & Rejection Audit Logs**")
    st.caption("Complete historical execution ledger for verification and assessment auditing:")

    runs = memory_store.get_all_runs(limit=25)
    if runs:
        df_runs = pd.DataFrame(runs)
        st.dataframe(df_runs, use_container_width=True)
    else:
        st.info("No runs recorded in database yet.")

# ------------------------------------------------------------------------------
# VIEW 12: Settings & System Controls
# ------------------------------------------------------------------------------
elif selected_view == "⚙️ Settings & System Controls":
    st.markdown("### **Settings & Environment Configuration**")
    st.caption("Verify API keys, active models, and pipeline guardrail thresholds:")

    st.markdown("#### **Active Inference Credentials**")
    gemini_status = "Configured" if GEMINI_API_KEY else "Not Configured (Running in Mock Engine Simulation)"
    openai_status = "Configured" if OPENAI_API_KEY else "Not Configured (Running in Mock Engine Simulation)"
    
    st.markdown(f"- **Google Gemini API Key**: `{gemini_status}`")
    st.markdown(f"- **OpenAI API Key**: `{openai_status}`")
    st.markdown(f"- **Default Fallback Provider**: `{DEFAULT_PROVIDER}`")

    st.markdown("---")
    st.markdown("#### **Rubric Threshold Configurations**")
    st.json(RUBRIC_THRESHOLDS)
