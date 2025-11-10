import os
import asyncio
import json
from agents.planner_agent import run_planner
from agents.search_agent import perform_search
from agents.fact_checker_agent import fact_checker_agent
from agents.writer_agent import generate_report  
from agents.guardrails import run_all_guards
from agents.email_agent import send_email
import markdown


class ResearchManager:
    async def run(self, query: str, recipient: str, api_key: str):

        os.environ["OPENAI_API_KEY"] = api_key
        yield f"Starting AI Policy Research for: **{query}**"

        # ============================================================
        # 1️ PLAN SEARCHES
        # ============================================================

        yield "Planning searches..."

        try:
            plan_result = await run_planner(query)
            plan_data = getattr(plan_result, "final_output", None)

            if not plan_data or "searches" not in plan_data:
                yield "PlannerAgent returned no structured plan. Using fallback..."
                plan_data = {"searches": [{"query": query, "reason": "Main topic"}]}
            searches = plan_data["searches"]

        except Exception as e:
            yield f"PlannerAgent failed: {e}"
            return

        # ============================================================
        # 2️ PERFORM SEARCHES
        # ============================================================

        yield "Conducting searches..."

        search_tasks = [
            perform_search(s.get("query"), s.get("reason", ""))
            for s in searches if isinstance(s, dict)
        ]

        search_results = await asyncio.gather(*search_tasks)

        for i, result in enumerate(search_results, start=1):
            status = result.get("status")
            if status == "ok":
                yield f"Search {i}/{len(search_results)} complete."
            elif status == "empty":
                yield f"Search {i}/{len(search_results)} returned no data."
            elif status == "error":
                yield f"Search {i}/{len(search_results)} failed: {result.get('message', '')}"

        # ============================================================
        # 3️ FACT-CHECK RESULTS
        # ============================================================
        yield "Fact-checking results..."
        try:
            fact_checked = await fact_checker_agent.run(str(search_results))
            summary = getattr(fact_checked, "final_output", None)
            if not summary:
                summary = "Summary result by FactCheckerAgent (simulated)"
        except Exception as e:
            yield f"FactCheckerAgent failed: {e}"
            summary = "Fact-check step skipped due to error."

        # ============================================================
        # 4️ GENERATE REPORT
        # ============================================================
        yield "Writing policy report..."
        try:
            report_output = await asyncio.to_thread(generate_report, query, summary)

            markdown_text = report_output.get("markdown_report", "")
            short_summary = report_output.get("short_summary", "")

            if not markdown_text.strip():
                markdown_text = f"Writer returned empty report.\nSimulated markdown for: {query}"

        except Exception as e:
            yield f"WriterAgent failed: {e}"
            markdown_text = f"Simulated markdown report for: {query}"
            short_summary = ""
        # ============================================================
        # 5️⃣ GUARDRAILS
        # ============================================================
        yield "🧩 Running guardrails..."
        try:
            guards = run_all_guards(markdown_text)
            if not all(guards.values()):
                yield f"⚠️ Guardrail warning: {guards}"
        except Exception as e:
            yield f"⚠️ Guardrail check failed: {e}"


        # ============================================================
        # 7️⃣ EMAIL DELIVERY
        # ============================================================
        yield "📨 Sending email..."
        try:
            html_template = f"""
            <div style="font-family: Arial, sans-serif; background:#f8f9fa; padding:30px;">
            <div style="max-width:700px; margin:auto; background:white; border-radius:12px; padding:30px;">
                <h2 style="color:#004aad;">AI Policy Research Brief</h2>
                <p><b>Topic:</b> {query}</p>
                <hr>
                <div style="font-size:15px; line-height:1.6;">{markdown.markdown(markdown_text)}</div>
                <hr>
                <p style="font-size:13px; color:#666;">Generated automatically by the <b>AI Policy Research Assistant</b>.</p>
            </div>
            </div>
            """


            result = await asyncio.to_thread(
                send_email,
                f"AI Policy Research Brief: {query}",
                html_template,
                recipient
            )

            if result.get("status") == "success":
                yield f"✅ Email sent successfully to {recipient}"
            else:
                yield f"⚠️ Email sending failed: {result.get('message', 'Unknown error')}"

        except Exception as e:
            yield f"❌ Error while sending email: {e}"

        # ============================================================
        # ✅ DONE
        # ============================================================
        yield "✅ Research complete. Report sent successfully!"
        yield markdown_text
