from skills.base import Skill
import core


class VolumeSkill(Skill):

    def can_handle(self, query: str) -> bool:
        q = query.lower()
        return any(word in q for word in [
            "volume", "sound", "audio", "mute", "loud", "quiet"
        ])

    def execute(self, query: str):
        q = query.lower()

        if any(word in q for word in ["up", "increase", "loud", "max"]):
            core.volume_up()

        elif any(word in q for word in ["down", "decrease", "quiet", "low"]):
            core.volume_down()

        elif "unmute" in q:
            core.unmute_volume()

        elif "mute" in q:
            core.mute_volume()

        else:
            core.say("What would you like me to do with the volume, sir?")
