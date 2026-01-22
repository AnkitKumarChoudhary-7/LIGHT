from skills.base import Skill
import commands


class MediaSkill(Skill):

    def can_handle(self, query: str) -> bool:
        q = query.lower()
        return any(
            word in q
            for word in ["play", "music", "song", "youtube"]
        )

    def execute(self, query: str):
        q = query.lower()

        if "youtube" in q:
            commands.play_youtube_song()
        else:
            commands.playMusic()
