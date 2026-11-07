with open('app.py', 'r', encoding='utf-8') as f:
    code = f.read()

# Upgraded CSS with Enterprise styling, radio-hiding, and widget cards
old_css_marker = '/* Enterprise Metric Cards */'
new_css = """    /* Hide Streamlit top header bar & reduce top margin */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    #MainMenu, footer {
        visibility: hidden !important;
    }
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2.5rem !important;
        padding-left: 2.5rem !important;
        padding-right: 2.5rem !important;
        max-width: 1440px !important;
    }

    /* Transform Sidebar Navigation - Hide default radio dots */
    div[data-testid="stSidebar"] {
        background-color: #F8FAFC !important;
        border-right: 1px solid #E2E8F0 !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] {
        gap: 3px !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label[data-baseweb="radio"] > div:first-child {
        display: none !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label {
        display: flex !important;
        align-items: center !important;
        padding: 9px 14px !important;
        border-radius: 8px !important;
        margin: 1px 0 !important;
        cursor: pointer !important;
        font-size: 0.88rem !important;
        font-weight: 500 !important;
        color: #334155 !important;
        background: transparent !important;
        border: 1px solid transparent !important;
        transition: all 0.15s ease !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label:hover {
        background-color: #F1F5F9 !important;
        color: #0F172A !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) {
        background-color: #EAF1FF !important;
        border: 1px solid #BFDBFE !important;
        border-left: 4px solid #2563EB !important;
        color: #2563EB !important;
        font-weight: 700 !important;
        box-shadow: 0 1px 3px rgba(37, 99, 235, 0.08) !important;
    }
    div[data-testid="stRadio"] div[role="radiogroup"] label:has(input:checked) p {
        color: #2563EB !important;
        font-weight: 700 !important;
    }

    /* SaaS Widget Cards */
    .saas-widget-card {
        background: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 22px 24px;
        box-shadow: 0 1px 4px rgba(0, 0, 0, 0.03);
        margin-bottom: 20px;
    }
    .saas-widget-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 1px solid #F1F5F9;
    }
    .saas-widget-title {
        font-size: 1.05rem;
        font-weight: 700;
        color: #14213D;
        margin: 0;
        font-family: 'Manrope', sans-serif;
    }
    .widget-badge {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        padding: 3px 10px;
        border-radius: 12px;
        background: #EAF1FF;
        color: #2563EB;
        border: 1px solid #BFDBFE;
    }

    /* Enterprise Metric Cards */"""

code = code.replace(old_css_marker, new_css, 1)

# Upgrade the KPI cards styling with top accent borders
old_kpi_start = """    k1, k2, k3, k4, k5, k6 = st.columns(6)
    with k1:
        st.markdown(f\"\"\"
        <div class="metric-card-pro">
            <h5>Total Generations</h5>
            <div class="metric-val">{analytics['total_runs']}</div>
            <div class="metric-sub">Pipeline runs</div>
        </div>
        \"\"\", unsafe_allow_html=True)
    with k2:
        st.markdown(f\"\"\"
        <div class="metric-card-pro">
            <h5>Approved</h5>
            <div class="metric-val" style="color: #16A34A;">{analytics['approved_runs']}</div>
            <div class="metric-sub">Cleared all 6 checks</div>
        </div>
        \"\"\", unsafe_allow_html=True)
    with k3:
        st.markdown(f\"\"\"
        <div class="metric-card-pro">
            <h5>Rejected</h5>
            <div class="metric-val" style="color: #DC2626;">{analytics['rejected_runs']}</div>
            <div class="metric-sub">Quality bar caught</div>
        </div>
        \"\"\", unsafe_allow_html=True)
    with k4:
        st.markdown(f\"\"\"
        <div class="metric-card-pro">
            <h5>Approval Rate</h5>
            <div class="metric-val" style="color: #2563EB;">{analytics['approval_rate_pct']}%</div>
            <div class="metric-sub">Reliability score</div>
        </div>
        \"\"\", unsafe_allow_html=True)
    with k5:
        st.markdown(f\"\"\"
        <div class="metric-card-pro">
            <h5>Avg Iterations</h5>
            <div class="metric-val">{analytics['avg_iterations_to_approval']}</div>
            <div class="metric-sub">Self-repair cycles</div>
        </div>
        \"\"\", unsafe_allow_html=True)
    with k6:
        st.markdown(f\"\"\"
        <div class="metric-card-pro">
            <h5>Avg FK Grade</h5>
            <div class="metric-val">{analytics['avg_passing_fk_grade']}</div>
            <div class="metric-sub">Target <= 7.5</div>
        </div>
        \"\"\", unsafe_allow_html=True)"""

new_kpi_code = """    k1, k2, k3, k4, k5, k6 = st.columns(6)
    with k1:
        st.markdown(f\"\"\"
        <div class="metric-card-pro" style="border-top: 3px solid #2563EB;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <h5 style="margin: 0;">Total Runs</h5>
                <span style="font-size: 0.68rem; font-weight: 700; background: #EAF1FF; color: #2563EB; padding: 2px 7px; border-radius: 10px;">SQLITE</span>
            </div>
            <div class="metric-val">{analytics['total_runs']}</div>
            <div class="metric-sub">Autonomous sessions</div>
        </div>
        \"\"\", unsafe_allow_html=True)
    with k2:
        st.markdown(f\"\"\"
        <div class="metric-card-pro" style="border-top: 3px solid #16A34A;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <h5 style="margin: 0;">Approved</h5>
                <span style="font-size: 0.68rem; font-weight: 700; background: #DCFCE7; color: #16A34A; padding: 2px 7px; border-radius: 10px;">READY</span>
            </div>
            <div class="metric-val" style="color: #16A34A;">{analytics['approved_runs']}</div>
            <div class="metric-sub">Cleared all 6 checks</div>
        </div>
        \"\"\", unsafe_allow_html=True)
    with k3:
        st.markdown(f\"\"\"
        <div class="metric-card-pro" style="border-top: 3px solid #DC2626;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <h5 style="margin: 0;">Rejected</h5>
                <span style="font-size: 0.68rem; font-weight: 700; background: #FEE2E2; color: #DC2626; padding: 2px 7px; border-radius: 10px;">GATED</span>
            </div>
            <div class="metric-val" style="color: #DC2626;">{analytics['rejected_runs']}</div>
            <div class="metric-sub">Quality bar caught</div>
        </div>
        \"\"\", unsafe_allow_html=True)
    with k4:
        st.markdown(f\"\"\"
        <div class="metric-card-pro" style="border-top: 3px solid #0F9D8A;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <h5 style="margin: 0;">Approval Rate</h5>
                <span style="font-size: 0.68rem; font-weight: 700; background: #E6F6F2; color: #0F9D8A; padding: 2px 7px; border-radius: 10px;">METRIC</span>
            </div>
            <div class="metric-val" style="color: #0F9D8A;">{analytics['approval_rate_pct']}%</div>
            <div class="metric-sub">Production reliability</div>
        </div>
        \"\"\", unsafe_allow_html=True)
    with k5:
        st.markdown(f\"\"\"
        <div class="metric-card-pro" style="border-top: 3px solid #F59E0B;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <h5 style="margin: 0;">Avg Retries</h5>
                <span style="font-size: 0.68rem; font-weight: 700; background: #FEF3C7; color: #B45309; padding: 2px 7px; border-radius: 10px;">BOUNDED</span>
            </div>
            <div class="metric-val">{analytics['avg_iterations_to_approval']}</div>
            <div class="metric-sub">Self-repair cycles</div>
        </div>
        \"\"\", unsafe_allow_html=True)
    with k6:
        st.markdown(f\"\"\"
        <div class="metric-card-pro" style="border-top: 3px solid #7C3AED;">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
                <h5 style="margin: 0;">Avg FK Grade</h5>
                <span style="font-size: 0.68rem; font-weight: 700; background: #F3E8FF; color: #7C3AED; padding: 2px 7px; border-radius: 10px;">AUDIENCE</span>
            </div>
            <div class="metric-val" style="color: #7C3AED;">{analytics['avg_passing_fk_grade']}</div>
            <div class="metric-sub">Target &le; 7.5 Grade</div>
        </div>
        \"\"\", unsafe_allow_html=True)"""

code = code.replace(old_kpi_start, new_kpi_code, 1)

# Upgrade the Chart & Active Rules section into clean SaaS widget cards
old_bottom_start = """    col_chart1, col_chart2 = st.columns([1, 1])
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
            st.markdown(f\"\"\"
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-radius: 6px; padding: 10px 14px; margin-bottom: 8px; font-size: 0.88rem;">
                <strong style="color: #2563EB;">Rule #{idx}:</strong> {rule}
            </div>
            \"\"\", unsafe_allow_html=True)"""

new_bottom_code = """    col_chart1, col_chart2 = st.columns([1.1, 1])
    with col_chart1:
        st.markdown(\"\"\"
        <div class="saas-widget-card">
            <div class="saas-widget-header">
                <div>
                    <h4 class="saas-widget-title">Historical Checkpoint Failure Distribution</h4>
                    <div style="font-size: 0.78rem; color: #64748B; margin-top: 2px;">Frequency of rubric gate triggers across runs</div>
                </div>
                <span class="widget-badge">LIVE SQLITE DATA</span>
            </div>
        </div>
        \"\"\", unsafe_allow_html=True)
        freqs = analytics["checkpoint_failure_frequencies"]
        if freqs:
            df_freq = pd.DataFrame(list(freqs.items()), columns=["Checkpoint", "Failure Count"]).set_index("Checkpoint")
            st.bar_chart(df_freq, color="#2563EB", height=240)
        else:
            st.info("No failure violations recorded in database yet.")

    with col_chart2:
        st.markdown(\"\"\"
        <div class="saas-widget-card">
            <div class="saas-widget-header">
                <div>
                    <h4 class="saas-widget-title">Active Evolved Guardrails in Memory</h4>
                    <div style="font-size: 0.78rem; color: #64748B; margin-top: 2px;">Synthesized by Evolution Engine from historical failure logs</div>
                </div>
                <span class="widget-badge">PERSISTED</span>
            </div>
        </div>
        \"\"\", unsafe_allow_html=True)
        active_guardrails = evolution_engine.get_active_guardrails()
        for idx, rule in enumerate(active_guardrails[:4], 1):
            st.markdown(f\"\"\"
            <div style="background: #FFFFFF; border: 1px solid #E2E8F0; border-left: 3px solid #2563EB; border-radius: 6px; padding: 10px 14px; margin-bottom: 8px; font-size: 0.86rem; box-shadow: 0 1px 2px rgba(0,0,0,0.02);">
                <strong style="color: #14213D;">Guardrail #{idx}:</strong> <span style="color: #475569;">{rule}</span>
            </div>
            \"\"\", unsafe_allow_html=True)"""

code = code.replace(old_bottom_start, new_bottom_code, 1)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(code)

print("SUCCESS: Upgraded app.py with sleek SaaS design system!")
