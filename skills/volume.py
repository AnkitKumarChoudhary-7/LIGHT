from skills.base import Skill
import commands 


class VolumeSkill(Skill):

    def can_handle(self, query: str) -> bool:
        q = query.lower()
        return any(
            word in q
            for word in ["volume", "sound", "audio", "mute", "loud", "quiet"]
        )

    def execute(self, query: str):
        q = query.lower()

        if "up" in q or "increase" in q:
            commands.volume_up()
        elif "down" in q or "decrease" in q:
            commands.volume_down()
        elif "mute" in q:
            commands.mute_volume()
