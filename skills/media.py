from skills.base import Skill
import commands  # TEMPORARY

class MediaSkill(Skill):

    def can_handle(self, query: str) -> bool:
        q = query.lower()
        return "play music" in q or "youtube" in q or "play song" in q

    def execute(self, query: str):
        q = query.lower()

        if "youtube" in q:
            commands.play_youtube_song()
        else:
            commands.playMusic()
