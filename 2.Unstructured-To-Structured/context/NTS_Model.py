from pydantic import BaseModel, Field
from typing import Optional, List

class Participant(BaseModel):
  """
  Represents one of the participants of the audio recording
  """
  speaker_id: str = Field(...,description="SPEAKER number of the participant during the audio")
  name: str = Field(..., description="Nickname of the participant. Probably mentioned by other speaker or himself")
  role: str = Field(..., description="Role of the participant during the scenario. Mentioned by himself during the presentation")

# class Presentation(BaseModel):
#   """
#   Represents when a participant presents their role
#   """
#   speaker: Participant = Field(...,description="Participant")
#   start_timestamp: Optional[float] = Field(..., description="Start time when speaker starts presenting")
#   stop_timestamp: Optional[float] = Field(..., description="Stop time when participant finishes their sentence")


class Order(BaseModel):
  """
  Represents what a participant orders
  """
  leader: Participant = Field(...,description="Leader participant that orders the action")
  follower: Optional[Participant] = Field(...,description="Participant that does the action. It could be on his/her own or ordered by other participant")
  action: str = Field(..., description="Action ordered by leader")
  start_timestamp: Optional[float] = Field(..., description="Start time when leader ordered the action")
  stop_timestamp: Optional[float] = Field(..., description="Stop time when participant mentioned something about his/her action")

# class Action(BaseModel):
#   """
#   Represents what a participant is doing
#   """
#   speaker: Participant = Field(...,description="Participant does the action")
#   action: str = Field(..., description="Action taken by the participant")
#   start_timestamp: Optional[float] = Field(..., description="Start time when participant is doing something")
#   stop_timestamp: Optional[float] = Field(..., description="Stop time when participant finishes the action")

class Skill(BaseModel):
  """
  Represents a non-technical skill of a participant in a certain moment
  """
  speaker: Participant = Field(..., description= "Participant with a principle of skill")
  main_skill: str = Field(..., description = "Main Non-technical skill or principle that the participant is showing")
  sentence: str = Field(..., description = "Sentence that reflects the non-technical skill")
  skill_description: str = Field(..., description = "Additional information about Non-technical skill")
  start_timestamp: Optional[float] = Field(..., description="Start time when participant is showing a skill")
  stop_timestamp: Optional[float] = Field(..., description="Stop time when participant finishes the sentence that shows a skill")

class Orders(BaseModel):
    ordersTimeline: list[Order]

# class Scenario(BaseModel):
#     actionsTimeline: list[Action]

class CRMSkills(BaseModel):
    skillsTimeline: list[Skill]