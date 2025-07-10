import re 
from youtube_transcript_api import YouTubeTranscriptApi
from gemini_llm import GeminiLLM

class YTSummarizer:
    def __init__(self, video_link ) :
        self.video_link = video_link
        self.llm = GeminiLLM().get_chat_llm()
        
    def extract_video_id(self):
        pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11}).*"
        match = re.search( pattern, self.video_link )
        if match:
            return match.group(1)
        else:
            raise ValueError("Invalid YouTube URL")
    
    def get_video_transcript(self):
        video_id = self.extract_video_id()
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        text = " ".join([entry["text"] for entry in transcript])
        return text
    
    def chunk_text(self,  max_tokens=1500):
        text  = vts.get_video_transcript()
        words = text.split()
        chunks = []
        for i in range(0, len(words), max_tokens):
            chunk = " ".join(words[i:i + max_tokens])
            chunks.append(chunk)
        return chunks
    
    def summarize_chunk(self, chunk):
        prompt = f"""
            Please summarize the following YouTube transcript section in 3 bullet points:

            {chunk}
            """
        response = self.llm.invoke(prompt)
        return response.content.strip()

    def generate_summary(self):
        chunks = self.chunk_text()
        all_summaries = []
        for chunk in chunks:
            summary = self.summarize_chunk(chunk)
            all_summaries.append(summary)
        return "\n\n".join(all_summaries)
    
    def main(self):
        summary = self.generate_summary()
        return summary

if __name__ == '__main__':
    video_url = "https://www.youtube.com/watch?v=C9QSpl5nmrY"
    vts = YTSummarizer(video_url)
    summary  = vts.main()
    print( summary )
        
    