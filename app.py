import os
import time
import gradio as gr
import plotly.graph_objects as go
from datetime import datetime
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

load_dotenv()

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

report_history = []

def generate_smart_chart(topic):
    charts = []
    colors = ["#c084fc", "#e879f9", "#f0abfc", "#a855f7", "#ec4899", "#db2777"]
    topic_lower = topic.lower()

    if any(w in topic_lower for w in ["ai", "artificial intelligence", "machine learning"]):
        fig1 = go.Figure(go.Bar(x=["Healthcare", "Finance", "Retail", "Manufacturing", "Transport"], y=[80, 70, 60, 50, 40], marker_color=colors))
        fig1.update_layout(title="🤖 AI Adoption by Industry (%)")
        charts.append(fig1)
        fig2 = go.Figure(go.Scatter(x=["2020", "2021", "2022", "2023", "2024", "2025"], y=[50, 70, 100, 140, 170, 190], mode="lines+markers", line=dict(color="#c084fc", width=3), fill="tozeroy"))
        fig2.update_layout(title="📈 Global AI Market Growth (Billion $)")
        charts.append(fig2)
    elif any(w in topic_lower for w in ["bitcoin", "crypto", "blockchain"]):
        fig1 = go.Figure(go.Scatter(x=["2020", "2021", "2022", "2023", "2024", "2025"], y=[10000, 40000, 30000, 25000, 45000, 60000], mode="lines+markers", line=dict(color="#e879f9", width=3), fill="tozeroy"))
        fig1.update_layout(title="₿ Bitcoin Price Trend ($)")
        charts.append(fig1)
    elif any(w in topic_lower for w in ["expense", "budget", "finance", "money"]):
        fig1 = go.Figure(go.Pie(labels=["Food", "Transport", "Entertainment", "Bills", "Shopping", "Health"], values=[30, 15, 10, 25, 12, 8], marker=dict(colors=colors)))
        fig1.update_layout(title="💸 Expense Distribution (%)")
        charts.append(fig1)
    else:
        fig1 = go.Figure(go.Bar(x=["Research", "Development", "Impact", "Growth", "Future"], y=[85, 72, 90, 78, 88], marker_color=colors))
        fig1.update_layout(title=f"📊 {topic.title()} - Key Metrics")
        charts.append(fig1)

    for fig in charts:
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0.95)",
            plot_bgcolor="rgba(0,0,0,0.5)",
            font=dict(color="#f0abfc", family="Inter"),
            title_font=dict(size=16, color="#e879f9"),
            margin=dict(l=40, r=40, t=60, b=40)
        )
    return charts


def get_history_html():
    if not report_history:
        return "<div style='text-align:center;padding:20px;color:#333;font-size:0.8em;'>🪼 No reports yet</div>"
    html = ""
    for item in report_history:
        preview = item['report'][:80] + "..."
        html += f"""
        <div style="background:rgba(192,132,252,0.06);border:1px solid rgba(192,132,252,0.2);
                    border-radius:12px;padding:10px 12px;margin-bottom:8px;">
            <div style="color:#c084fc;font-weight:700;font-size:0.82em;">🪼 {item['topic'].title()}</div>
            <div style="color:#444;font-size:0.68em;margin-top:2px;">🕐 {item['time']}</div>
            <div style="color:#666;font-size:0.75em;margin-top:4px;">{preview}</div>
        </div>"""
    return html


def run_crew(topic):
    global report_history
    if not topic.strip():
        return "⚠️ Please enter a topic first!", None, None, get_history_html()

    researcher = Agent(role="Research Analyst", goal=f"Research key information about {topic}", backstory="Expert researcher who finds real data.", llm=llm, verbose=True)
    writer = Agent(role="Content Writer", goal=f"Write professional report about {topic}.", backstory="Skilled writer who creates detailed reports.", llm=llm, verbose=True)
    reviewer = Agent(role="Quality Reviewer", goal="Review and polish the report.", backstory="Strict reviewer ensuring professional quality.", llm=llm, verbose=True)

    research_task = Task(description=f"Research {topic}. Find 5 real data points. No image links.", expected_output="Research findings with statistics.", agent=researcher)
    write_task = Task(description=f"Write professional report about {topic}. No image links.", expected_output="Well structured report.", agent=writer)
    review_task = Task(description="Review and polish the report.", expected_output="Final polished report.", agent=reviewer)

    crew = Crew(agents=[researcher, writer, reviewer], tasks=[research_task, write_task, review_task], verbose=True, max_rpm=3)

    time.sleep(5)
    result = crew.kickoff()
    report_text = str(result)

    report_history.insert(0, {"topic": topic, "report": report_text, "time": datetime.now().strftime("%d %b, %I:%M %p")})
    report_history[:] = report_history[:10]

    chart_keywords = ["chart", "graph", "visual", "plot", "compare", "statistics", "stats", "data"]
    wants_chart = any(word in topic.lower() for word in chart_keywords)

    if wants_chart:
        charts = generate_smart_chart(topic)
        c1 = charts[0] if len(charts) > 0 else None
        c2 = charts[1] if len(charts) > 1 else None
    else:
        c1, c2 = None, None

    return report_text, c1, c2, get_history_html()


voice_js = """
async () => {
    try {
        const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
        recognition.lang = 'en-US';
        recognition.interimResults = false;
        recognition.start();
        return new Promise((resolve) => {
            recognition.onresult = (e) => resolve(e.results[0][0].transcript);
            recognition.onerror = () => resolve("");
        });
    } catch(e) { return ""; }
}
"""

with gr.Blocks(title="Multi Agent AI Research System") as app:

    gr.HTML("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@400;600&display=swap');

    body, .gradio-container {
        background: #000000 !important;
        font-family: 'Inter', sans-serif !important;
    }
    .gradio-container {
        max-width: 880px !important;
        margin: auto !important;
        position: relative;
        z-index: 1;
    }

    /* Jellyfish canvas */
    #jelly-canvas {
        position: fixed;
        top: 0; left: 0;
        width: 100%; height: 100%;
        z-index: 0;
        pointer-events: none;
    }

    /* Animations */
    @keyframes gradientShift {
        0%   { background-position: 0% 50%; }
        50%  { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    @keyframes floatJelly {
        0%, 100% { transform: translateY(0) scaleX(1); }
        25%       { transform: translateY(-18px) scaleX(1.04); }
        75%       { transform: translateY(-8px) scaleX(0.97); }
    }
    @keyframes wave {
        0%, 100% { transform: translateY(0) rotate(0deg); }
        25%      { transform: translateY(-12px) rotate(-6deg); }
        75%      { transform: translateY(-6px) rotate(6deg); }
    }
    @keyframes floatY {
        0%, 100% { transform: translateY(0); }
        50%      { transform: translateY(-14px); }
    }
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50%      { opacity: 0.4; }
    }
    @keyframes jellyGlow {
        0%, 100% { box-shadow: 0 0 20px rgba(192,132,252,0.4), 0 0 60px rgba(192,132,252,0.15); }
        50%      { box-shadow: 0 0 40px rgba(232,121,249,0.7), 0 0 100px rgba(232,121,249,0.3); }
    }
    @keyframes tentacleWave {
        0%, 100% { transform: skewX(0deg); }
        50%      { transform: skewX(3deg); }
    }

    /* Title */
    .main-title {
        font-family: 'Orbitron', sans-serif;
        font-size: 2.2em;
        font-weight: 900;
        text-align: center;
        background: linear-gradient(90deg, #c084fc, #e879f9, #f0abfc, #ec4899, #c084fc);
        background-size: 300%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        animation: gradientShift 4s ease infinite;
        letter-spacing: 1px;
        margin-bottom: 4px;
        filter: drop-shadow(0 0 20px rgba(192,132,252,0.5));
    }
    .subtitle {
        text-align: center;
        color: #7c3aed;
        font-size: 0.85em;
        opacity: 0.8;
    }

    /* Stars */
    .stars { display:flex; justify-content:center; gap:6px; margin: 8px 0; }
    .star  { font-size:0.85em; animation: pulse 2s ease-in-out infinite; }
    .star:nth-child(2) { animation-delay:.35s; }
    .star:nth-child(3) { animation-delay:.7s; }

    /* Robot row */
    .robots-container {
        display: flex;
        justify-content: center;
        gap: 44px;
        margin: 14px 0 22px;
        padding: 20px 24px;
        background: rgba(192,132,252,0.04);
        border: 1px solid rgba(192,132,252,0.15);
        border-radius: 30px;
        backdrop-filter: blur(10px);
        animation: jellyGlow 4s ease-in-out infinite;
    }
    .robot-wrapper { display:flex; flex-direction:column; align-items:center; gap:8px; }
    .robot { font-size:2.6em; filter: drop-shadow(0 0 15px rgba(232,121,249,0.8)); }
    .robot-1 { animation: floatJelly 2s ease-in-out infinite; }
    .robot-2 { animation: wave      2.4s ease-in-out infinite; animation-delay:.4s; }
    .robot-3 { animation: floatY    2.8s ease-in-out infinite; animation-delay:.8s; }
    .robot-label {
        font-size:.64em; color:#c084fc; font-weight:600;
        background: rgba(192,132,252,0.1);
        padding: 3px 12px; border-radius:20px;
        border: 1px solid rgba(192,132,252,0.3);
    }

   /* Input */
    .input-row textarea {
        background: linear-gradient(135deg, rgba(124,58,237,0.08), rgba(192,132,252,0.05)) !important;
        border: 2px solid transparent !important;
        border-radius: 20px !important;
        color: #f0abfc !important;
        font-size: 1.05em !important;
        padding: 14px 18px !important;
        caret-color: #e879f9 !important;
        transition: all .3s !important;
        font-family: 'Inter', sans-serif !important;
        outline: 2px solid rgba(168,85,247,0.4) !important;
        box-shadow: 0 0 20px rgba(168,85,247,0.15), inset 0 0 20px rgba(192,132,252,0.05) !important;
    }
    .input-row textarea:focus {
        outline: 2px solid #e879f9 !important;
        box-shadow: 0 0 35px rgba(232,121,249,0.3), inset 0 0 25px rgba(192,132,252,0.08) !important;
        background: linear-gradient(135deg, rgba(124,58,237,0.12), rgba(192,132,252,0.08)) !important;
    }
    .input-row textarea::placeholder { color: #6b21a8 !important; }
    .input-row label {
        color: #e879f9 !important;
        font-weight: 700 !important;
        font-size: 1em !important;
        text-shadow: 0 0 10px rgba(232,121,249,0.5) !important;
    }
    
#voice-btn button {
        background: linear-gradient(135deg, #7c3aed, #a855f7, #c084fc) !important;
        border: 2px solid #c084fc !important;
        border-radius: 20px !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1em !important;
        height: 52px !important;
        transition: all .25s !important;
        box-shadow: 0 0 15px rgba(168,85,247,0.6),
                    0 0 35px rgba(168,85,247,0.3),
                    0 0 60px rgba(168,85,247,0.15) !important;
    }
    #voice-btn button:hover {
        box-shadow: 0 0 25px rgba(168,85,247,0.9),
                    0 0 60px rgba(168,85,247,0.5),
                    0 0 100px rgba(168,85,247,0.2) !important;
        transform: scale(1.06) !important;
    }

    #generate-btn button {
        background: linear-gradient(135deg, #ec4899, #c084fc, #e879f9) !important;
        border: 2px solid #f0abfc !important;
        border-radius: 20px !important;
        color: #000 !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 0.88em !important;
        font-weight: 900 !important;
        height: 52px !important;
        letter-spacing: 1px !important;
        box-shadow: 0 0 15px rgba(232,121,249,0.6),
                    0 0 35px rgba(232,121,249,0.3),
                    0 0 60px rgba(236,72,153,0.15) !important;
        animation: jellyGlow 3s ease-in-out infinite !important;
        transition: transform .2s !important;
    }
    #generate-btn button:hover {
        box-shadow: 0 0 25px rgba(232,121,249,0.9),
                    0 0 60px rgba(232,121,249,0.5),
                    0 0 100px rgba(236,72,153,0.25) !important;
        transform: scale(1.06) !important;
    }
            
    /* Clear button */
    #clear-btn button {
        background: transparent !important;
        border: 1px solid rgba(236,72,153,0.35) !important;
        border-radius: 16px !important;
        color: #ec4899 !important;
        font-weight: 600 !important;
        transition: all .25s !important;
    }
    #clear-btn button:hover {
        background: rgba(236,72,153,0.1) !important;
        box-shadow: 0 0 14px rgba(236,72,153,0.3) !important;
    }

    /* Output */
    #output-box textarea {
        background: rgba(192,132,252,0.03) !important;
        border: 1px solid rgba(192,132,252,0.18) !important;
        border-radius: 20px !important;
        color: #e9d5ff !important;
        font-size: .93em !important;
        line-height: 1.85 !important;
        padding: 20px !important;
    }

    /* Floating history */
    #history-float-box {
        position: fixed;
        top: 15px; right: 15px;
        width: 250px;
        max-height: 88vh;
        overflow-y: auto;
        background: rgba(0,0,0,0.97);
        border: 1px solid rgba(192,132,252,0.22);
        border-radius: 24px;
        padding: 14px;
        z-index: 9999;
        backdrop-filter: blur(20px);
        box-shadow: 0 0 40px rgba(192,132,252,0.1), inset 0 0 30px rgba(192,132,252,0.02);
    }
    #history-float-box::-webkit-scrollbar { width:3px; }
    #history-float-box::-webkit-scrollbar-thumb { background:rgba(192,132,252,0.3); border-radius:3px; }

    .gr-markdown h3 { color: #c084fc !important; }
    .footer-txt { text-align:center; color:#1a0a2e; font-size:.78em; margin-top:22px; }
    </style>

    <!-- Jellyfish Canvas -->
    <canvas id="jelly-canvas"></canvas>
    <script>
    (function(){
        const canvas = document.getElementById('jelly-canvas');
        const ctx = canvas.getContext('2d');
        let W, H;

        function resize(){ W = canvas.width = window.innerWidth; H = canvas.height = window.innerHeight; }
        window.addEventListener('resize', resize);
        resize();

        // Jellyfish class
        class Jellyfish {
            constructor(){
                this.reset();
            }
            reset(){
                this.x = Math.random() * W;
                this.y = H + 150;
                this.size = Math.random() * 40 + 20;
                this.speed = Math.random() * 0.5 + 0.2;
                this.wobble = Math.random() * Math.PI * 2;
                this.wobbleSpeed = Math.random() * 0.03 + 0.01;
                this.alpha = Math.random() * 0.4 + 0.15;
                const r = Math.random();
                if(r < 0.5){
                    this.color1 = 'rgba(192,132,252,';
                    this.color2 = 'rgba(232,121,249,';
                    this.tentacleColor = 'rgba(216,180,254,';
                } else {
                    this.color1 = 'rgba(236,72,153,';
                    this.color2 = 'rgba(192,132,252,';
                    this.tentacleColor = 'rgba(249,168,212,';
                }
                this.tentacles = [];
                const numT = Math.floor(Math.random() * 5 + 5);
                for(let i=0; i<numT; i++){
                    this.tentacles.push({
                        offset: (i / numT - 0.5) * this.size * 1.8,
                        length: Math.random() * this.size * 2 + this.size,
                        wave: Math.random() * Math.PI * 2,
                        waveSpeed: Math.random() * 0.04 + 0.01,
                        segments: Math.floor(Math.random() * 6 + 6)
                    });
                }
            }

            draw(){
                this.wobble += this.wobbleSpeed;
                this.y -= this.speed;
                this.x += Math.sin(this.wobble * 0.5) * 0.5;

                const wobbleX = Math.sin(this.wobble) * 3;
                const a = this.alpha;
                const s = this.size;

                ctx.save();
                ctx.translate(this.x + wobbleX, this.y);

                // Tentacles
                this.tentacles.forEach(t => {
                    t.wave += t.waveSpeed;
                    ctx.beginPath();
                    ctx.moveTo(t.offset, s * 0.4);
                    const segH = t.length / t.segments;
                    for(let i=0; i<=t.segments; i++){
                        const ty = s * 0.4 + i * segH;
                        const tx = t.offset + Math.sin(t.wave + i * 0.5) * (8 + i * 1.5);
                        if(i === 0) ctx.moveTo(tx, ty);
                        else ctx.lineTo(tx, ty);
                    }
                    ctx.strokeStyle = this.tentacleColor + (a * 0.6) + ')';
                    ctx.lineWidth = 1;
                    ctx.stroke();
                });

                // Bell body
                const grad = ctx.createRadialGradient(0, -s*0.2, 0, 0, 0, s);
                grad.addColorStop(0, this.color1 + (a * 0.8) + ')');
                grad.addColorStop(0.6, this.color2 + (a * 0.4) + ')');
                grad.addColorStop(1, this.color1 + '0)');

                ctx.beginPath();
                ctx.ellipse(0, 0, s, s * 0.7, 0, Math.PI, 0);
                ctx.fillStyle = grad;
                ctx.fill();

                // Inner glow
                const innerGrad = ctx.createRadialGradient(0, -s*0.1, 0, 0, -s*0.1, s*0.5);
                innerGrad.addColorStop(0, this.color1 + (a * 0.6) + ')');
                innerGrad.addColorStop(1, this.color1 + '0)');
                ctx.beginPath();
                ctx.ellipse(0, -s*0.1, s*0.5, s*0.35, 0, Math.PI, 0);
                ctx.fillStyle = innerGrad;
                ctx.fill();

                // Rim glow
                ctx.beginPath();
                ctx.ellipse(0, 0, s, s*0.7, 0, Math.PI, 0);
                ctx.strokeStyle = this.color2 + (a * 0.8) + ')';
                ctx.lineWidth = 1.5;
                ctx.stroke();

                ctx.restore();

                if(this.y < -200) this.reset();
            }
        }

        // Bubbles
        class Bubble {
            constructor(){
                this.reset();
            }
            reset(){
                this.x = Math.random() * W;
                this.y = H + 10;
                this.r = Math.random() * 3 + 1;
                this.speed = Math.random() * 0.8 + 0.3;
                this.wobble = Math.random() * Math.PI * 2;
                this.alpha = Math.random() * 0.3 + 0.05;
            }
            draw(){
                this.wobble += 0.03;
                this.y -= this.speed;
                this.x += Math.sin(this.wobble) * 0.5;
                ctx.beginPath();
                ctx.arc(this.x, this.y, this.r, 0, Math.PI*2);
                ctx.strokeStyle = `rgba(192,132,252,${this.alpha})`;
                ctx.lineWidth = 0.8;
                ctx.stroke();
                if(this.y < -10) this.reset();
            }
        }

        const jellies = Array.from({length: 8}, () => {
            const j = new Jellyfish();
            j.y = Math.random() * H;
            return j;
        });
        const bubbles = Array.from({length: 40}, () => {
            const b = new Bubble();
            b.y = Math.random() * H;
            return b;
        });

        function draw(){
            ctx.clearRect(0,0,W,H);
            bubbles.forEach(b => b.draw());
            jellies.forEach(j => j.draw());
            requestAnimationFrame(draw);
        }
        draw();
    })();
    </script>
    """)

    # Header
    gr.HTML("""
    <div class="main-title">🪼 Multi-Agent AI Research System 🪼</div>
    <div class="subtitle">Powered by CrewAI + Groq LLaMA 3.3 • 3 Agents Collaborating</div>
    <div class="stars">
        <span class="star">🪼</span>
        <span class="star">✨</span>
        <span class="star">🪼</span>
    </div>
    <div class="robots-container">
        <div class="robot-wrapper">
            <div class="robot robot-1">🤖</div>
            <div class="robot-label">🔍 Researcher</div>
        </div>
        <div class="robot-wrapper">
            <div class="robot robot-2">🦾</div>
            <div class="robot-label">✍️ Writer</div>
        </div>
        <div class="robot-wrapper">
            <div class="robot robot-3">🧠</div>
            <div class="robot-label">✅ Reviewer</div>
        </div>
    </div>
    """)

    # Input
    with gr.Row(elem_classes=["input-row"]):
        topic_input = gr.Textbox(
            label="🔎 Research Topic",
            placeholder="e.g. Artificial Intelligence, Bitcoin, Climate Change...",
            lines=2,
            scale=8
        )

    with gr.Row():
        voice_btn  = gr.Button("🎤 Speak",          elem_id="voice-btn",   scale=1)
        submit_btn = gr.Button("🪼 Generate Report", elem_id="generate-btn", scale=3)

    output = gr.Textbox(
        label="📋 Generated Report",
        lines=22,
        placeholder="🪼 Your AI-generated research report will float up here...",
        elem_id="output-box"
    )

    with gr.Column():
        gr.Markdown("### 📊 Data Visualizations")
        charts_output  = gr.Plot(label="Chart 1", visible=False)
        charts_output2 = gr.Plot(label="Chart 2", visible=False)

    clear_btn = gr.Button("🗑️ Clear All", elem_id="clear-btn")

    history_display = gr.HTML(value="""
        <div id='history-float-box'>
            <div style='color:#c084fc;font-weight:700;font-size:.88em;
                        border-bottom:1px solid rgba(192,132,252,0.2);
                        padding-bottom:8px;margin-bottom:10px;'>
                🪼 Report History
            </div>
            <div id='history-inner'>
                <div style='text-align:center;padding:15px;color:#333;font-size:.8em;'>
                    🪼 No reports yet
                </div>
            </div>
        </div>
    """)

    gr.HTML("<div class='footer-txt'>Built with 🪼 using CrewAI | Groq | Gradio | Plotly</div>")

    def run_and_display(topic):
        report, c1, c2, history_html = run_crew(topic)
        updated = f"""
        <div id='history-float-box'>
            <div style='color:#c084fc;font-weight:700;font-size:.88em;
                        border-bottom:1px solid rgba(192,132,252,0.2);
                        padding-bottom:8px;margin-bottom:10px;'>
                🪼 Report History
            </div>
            <div id='history-inner'>{history_html}</div>
        </div>"""
        return (
            report,
            gr.update(value=c1, visible=c1 is not None),
            gr.update(value=c2, visible=c2 is not None),
            updated
        )

    def clear_all_fn():
        return "", gr.update(value=None, visible=False), gr.update(value=None, visible=False)

    voice_btn.click(fn=None, inputs=[], outputs=[topic_input], js=voice_js)
    submit_btn.click(fn=run_and_display, inputs=topic_input, outputs=[output, charts_output, charts_output2, history_display])
    clear_btn.click(fn=clear_all_fn, outputs=[output, charts_output, charts_output2])

app.launch()