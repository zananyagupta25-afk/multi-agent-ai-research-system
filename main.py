import os
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, LLM

# Load the .env file
load_dotenv()

# Setting up the LLM (Groq)
llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

# ── AGENTS ──────────────────────────────────────────

researcher = Agent(
    role="Research Analyst",
    goal="Research and find key information about a given topic",
    backstory="You are an expert researcher with years of experience in finding and analyzing information.",
    llm=llm,
    verbose=True
)

writer = Agent(
    role="Content Writer",
    goal="Write a clear and engaging report based on research findings",
    backstory="You are a skilled writer who specializes in turning complex research into easy to understand reports.",
    llm=llm,
    verbose=True
)

reviewer = Agent(
    role="Quality Reviewer",
    goal="Review the written report and improve its quality",
    backstory="You are a strict reviewer who ensures reports are accurate, well structured and professional.",
    llm=llm,
    verbose=True
)

# ── TASKS ────────────────────────────────────────────

research_task = Task(
    description="Research the latest trends in Artificial Intelligence in 2025",
    expected_output="A detailed list of top 5 AI trends with key facts and examples",
    agent=researcher
)

write_task = Task(
    description="Using the research findings, write a professional report about AI trends in 2025",
    expected_output="A well structured report with introduction, 5 sections and conclusion",
    agent=writer
)

review_task = Task(
    description="Review the written report, fix any issues and make it more professional",
    expected_output="A polished final report ready for publication",
    agent=reviewer
)

# ── CREW ─────────────────────────────────────────────

crew = Crew(
    agents=[researcher, writer, reviewer],
    tasks=[research_task, write_task, review_task],
    verbose=True
)

# ── RUN ──────────────────────────────────────────────

result = crew.kickoff()
print("\n\n========================")
print("FINAL REPORT:")
print("========================")
print(result)