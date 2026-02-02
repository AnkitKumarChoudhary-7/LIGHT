from skills.base import Skill
import core

class SystemSkill(Skill):

    def can_handle(self, query: str) -> bool:
        q = query.lower()
        return any(word in q for word in [
            "shutdown", "restart", "lock", "sleep", "sign out"
        ])

    def execute(self, query: str):
        q = query.lower()

        # SAFE COMMAND (no confirmation)
        if "lock" in q:
            core.lock_pc()
            return

        # DANGEROUS COMMANDS → confirmation required
        if "shutdown" in q:
            self.confirm_and_execute(
                "shutdown", core.shutdown_system
            )

        elif "restart" in q:
            self.confirm_and_execute(
                "restart", core.restart_system
            )

        elif "sleep" in q:
            self.confirm_and_execute(
                "sleep", core.sleep_system
            )

        elif "sign out" in q:
            self.confirm_and_execute(
                "sign out", core.sign_out
            )

    def confirm_and_execute(self, action_name, action_func):
        core.say(f"Are you sure you want to {action_name}, sir?")
        # Use voice input for confirmation (more natural for voice assistant)
        answer = core.takeCommand()
        
        if answer and answer.lower() in ["yes", "yeah", "sure", "do it", "confirm", "ok"]:
            core.say(f"Proceeding to {action_name}, sir.")
            action_func()
        else:
            core.say("Cancelled, sir.")
