from skills.base import Skill
import commands
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
            commands.lock_pc()
            return

        # DANGEROUS COMMANDS → confirmation required
        if "shutdown" in q:
            self.confirm_and_execute(
                "shutdown", commands.shutdown_system
            )

        elif "restart" in q:
            self.confirm_and_execute(
                "restart", commands.restart_system
            )

        elif "sleep" in q:
            self.confirm_and_execute(
                "sleep", commands.sleep_system
            )

        elif "sign out" in q:
            self.confirm_and_execute(
                "sign out", commands.sign_out
            )

    def confirm_and_execute(self, action_name, action_func):
        core.say(f"Are you sure you want to {action_name}, sir?")
        answer = core.takeCommand()

        if answer and answer.lower() in ["yes", "yeah", "sure", "do it"]:
            core.say(f"Proceeding to {action_name}, sir.")
            action_func()
        else:
            core.say("Cancelled, sir.")
