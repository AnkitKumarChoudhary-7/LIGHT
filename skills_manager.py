from skills.volume import VolumeSkill
from skills.media import MediaSkill

class SkillManager:

    def __init__(self):
        self.skills = [
            VolumeSkill(),
            MediaSkill(),
        ]

    def handle(self, query: str) -> bool:
        for skill in self.skills:
            if skill.can_handle(query):
                skill.execute(query)
                return True
        return False
