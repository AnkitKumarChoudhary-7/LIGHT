from skills.base import Skill
import commands  # TEMPORARY (explained below)

class VolumeSkill(Skill):

    def can_handle(self, query: str) -> bool:
        q = query.lower()
        return "volume" in q or "mute" in q

    def execute(self, query: str):
        q = query.lower()

        if "up" in q or "increase" in q:
            commands.volume_up()
        elif "down" in q or "decrease" in q:
            commands.volume_down()
        elif "mute" in q:
            commands.mute_volume()
