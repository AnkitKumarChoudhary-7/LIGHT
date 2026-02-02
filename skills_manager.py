from skills.volume import VolumeSkill
from skills.media import MediaSkill
from skills.system import SystemSkill
from skills.brightness import BrightnessSkill

class SkillManager:
    def __init__(self):
        self.skills = [
            VolumeSkill(),
            MediaSkill(),
            SystemSkill(),
            BrightnessSkill(),
        ]
    
    def handle(self, query: str) -> bool:
        """Try to handle query with available skills. Return True if handled."""
        for skill in self.skills:
            if skill.can_handle(query):
                skill.execute(query)
                return True
        return False
