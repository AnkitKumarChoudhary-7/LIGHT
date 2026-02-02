from skills.base import Skill
import core


class BrightnessSkill(Skill):

    def can_handle(self, query: str) -> bool:
        q = query.lower()
        return any(word in q for word in [
            "brightness", "screen", "display"
        ])

    def execute(self, query: str):
        q = query.lower()

        # Check for decrease commands first
        if any(word in q for word in ["down", "decrease", "dim", "lower", "reduce"]):
            core.decrease_brightness()

        # Check for increase commands
        elif any(word in q for word in ["up", "increase", "raise", "max", "higher"]):
            core.increase_brightness()

        # Check for set commands
        elif any(word in q for word in ["set", "to"]):
            # Try to extract a number from the query
            import re
            numbers = re.findall(r'\d+', q)
            if numbers:
                percent = int(numbers[0])
                core.set_brightness(percent)
            else:
                core.say("What brightness level would you like, sir?")
        
        else:
            core.say("What would you like me to do with the brightness, sir?")
