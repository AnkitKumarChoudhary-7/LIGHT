from skills.volume import VolumeSkill
from skills.media import MediaSkill
from skills.system import SystemSkill   # ADD THIS

class SkillManager:
    def __init__(self):
        self.skills = [
            VolumeSkill(),
            MediaSkill(),
            SystemSkill(),   # ADD THIS
        ]
