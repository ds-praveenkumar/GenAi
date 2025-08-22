#===============================================================================
#  File Name    : tts.py
#  Project Name : Project Name
#  Description  : 
#    Description of this file

#  Author       : Praveen Kumar
#  Created On   : 2025-08-22
#  Last Updated : 2025-08-22
#  Version      : v1.0.0

#  Language     : Python
#  File name    : tts.py
#  Dependencies : 
#    - Dependency 1
#    - Dependency 2

#  Inputs       : Expected inputs
#  Outputs      : Expected outputs
#  Usage        : 
#    Example usage

#  Notes        : 
#    - Notes or TODOs
#===============================================================================
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import os
from abc import ABC, abstractmethod
from dotenv import load_dotenv

load_dotenv(".env")


class TextToSpeechBaseTool(ABC):
    def __init__(self) -> None:
        self.elevenlabs = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
        self.voice_id="JBFqnCBsd6RMkjVDRZzb"
        self.model_id="eleven_multilingual_v2"
        self.output_format="mp3_44100_128"

    def convert_text_to_speech(self, text):
        return self.elevenlabs.text_to_speech.convert(
            text=text,
            voice_id=self.voice_id,
            model_id=self.model_id,
            output_format=self.output_format,
        )
    
    def speak(self, text):
        audio = self.convert_text_to_speech(text)
        play(audio)

class AgentSpeaker(TextToSpeechBaseTool):
    def __init__(self):
        super().__init__()
        self.voice_id="JBFqnCBsd6RMkjVDRZzb"

    def convert_text_to_speech(self, text):
        return self.elevenlabs.text_to_speech.convert(
            text=text,
            voice_id=self.voice_id,
            model_id=self.model_id,
            output_format=self.output_format,
        )

class HumanSpeaker(TextToSpeechBaseTool):
    def __init__(self) -> None:
        super().__init__()
        self.voice_id = "broqrJkktxd1CclKTudW"

if __name__ == "__main__":
    text="The first move is what sets everything in motion."
    tts = AgentSpeaker()
    tts.speak(text)
    hs = HumanSpeaker()
    hs.speak(text)