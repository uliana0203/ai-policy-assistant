import gradio as gr
from core.research_manager import ResearchManager

# =========================================================
# Gradio Interface for AI Policy Research Assistant
# =========================================================

async def run_research(query: str, user_email: str, user_api_key: str):
    if not query:
        yield "Please enter a research question.", ""
        return
    if not user_email or "@" not in user_email:
        yield "Please provide a valid email address.", ""
        return
    if not user_api_key or not user_api_key.startswith("sk-"):
        yield "Please enter a valid OpenAI API key (starts with 'sk-').", ""
        return

    yield f"Starting AI Policy Research for query: **{query}**", ""

    manager = ResearchManager()
    final_report = ""

    try:
        async for update in manager.run(query, user_email, user_api_key):
            if update.strip().startswith("##") or "Executive Summary" in update:
                final_report = update
                yield "Research complete. See full report below", final_report
            elif "Simulated markdown report" in update:
                final_report = update
                yield "WriterAgent returned simulated markdown.", final_report
            else:
                yield update, final_report

        if not final_report:
            yield "No final report found.", ""

    except Exception as e:
        yield f"Error occurred: {str(e)}", ""


# =========================================================
# Gradio UI
# =========================================================

with gr.Blocks(theme=gr.themes.Soft(primary_hue="blue")) as app:
 
    gr.HTML(
        """
        <style>
        #report_box {
            background: white;
            padding: 24px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            line-height: 1.6;
            margin-top: 10px;
        }
        </style>
        """
    )

    gr.Markdown(
        """
        #  AI Policy Research Assistant  
        This assistant conducts **multi-agent policy analysis** using OpenAI models.  
        It plans, searches, fact-checks, writes, visualizes, and emails a policy report to you.
        """
    )

    with gr.Row():
        query_box = gr.Textbox(
            label="Research Topic",
            placeholder="e.g. Compare EU AI Act and U.S. AI Bill of Rights in algorithmic transparency",
            lines=3,
        )

    with gr.Row():
        email_input = gr.Textbox(label="Your Email", placeholder="example@email.com")
        api_input = gr.Textbox(
            label="OpenAI API Key",
            placeholder="sk-...",
            type="password",
        )

    with gr.Row():
        run_btn = gr.Button("Start Research", variant="primary")

    with gr.Row():
        progress_box = gr.Markdown(label="Progress")


    with gr.Row():
        report_box = gr.Markdown(
            label="Generated Report",
            value="",
            elem_id="report_box",
        )

    run_btn.click(
        fn=run_research,
        inputs=[query_box, email_input, api_input],
        outputs=[progress_box, report_box],
        api_name="run_research",
        queue=True,
    )

    gr.Markdown(
        """
        ---
        **Tips:**
        - Your API key is used only temporarily and not stored.
        - Reports are automatically fact-checked and filtered for ethics.
        - Email delivery uses SendGrid (100 free messages/day).
        """
    )

app.queue()
app.launch(server_name="127.0.0.1", server_port=7860, share=True)



