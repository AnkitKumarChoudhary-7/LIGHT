from skills_manager import SkillManager
import core


skill_manager = SkillManager()


def handle_query(query: str):
    if not query:
        return "ok"

    q = query.lower()

    # EXIT stays here
    if "exit" in q or "quit" in q or "goodbye" in q or "bye light" in q:
        core.say("Goodbye sir. Shutting down.")
        return "exit"

    # 🔥 NEW: delegate to skills
    handled = skill_manager.handle(q)
    if handled:
        return "ok"

    print("No skill matched for:", q)

    # fallback AI (unchanged)
    core.say("Let me think about that, sir.")
    answer = core.ai(q)
    core.say(answer)

    return "ok"
