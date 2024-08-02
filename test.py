import cmd
from youtube_transcript_api import YouTubeTranscriptApi
import summarize


art = """
__   _________        __               
\ \ / /_   _\ \      / / __ __ _ _ __  
 \ V /  | |  \ \ /\ / / '__/ _` | '_ \ 
  | |   | |   \ V  V /| | | (_| | |_) |
  |_|   |_|    \_/\_/ |_|  \__,_| .__/ 
                                |_|    
"""


class YTWrap(cmd.Cmd):
    prompt = ">> "
    intro = "Welcome to YTWrap. " + art + "Type 'help' to view all commands" + "\n"

    def __init__(self):
        super().__init__()

    def do_summarize(self, link):
        try:
            link = link.split('https://www.youtube.com/watch?v=')
            video_id = link[1].split('&')[0]
            #transcript = YouTubeTranscriptApi.get_transcript(video_id)

            # Concatenate transcript texts
            #text = " ".join([entry['text'] for entry in transcript])

            text = """
            Natural language processing (NLP) is a field of artificial intelligence in which computers analyze, understand, and derive meaning from human language in a smart and useful way. NLP is used to apply algorithms to identify and extract the natural language rules such that the unstructured language data is converted into a form that computers can understand.

            When text data is cleaned and preprocessed, it can be utilized to create algorithms that help solve various problems. NLP is commonly used for text summarization, sentiment analysis, topic extraction, named entity recognition, and language translation. The aim is to fill the gap between human communication and computer understanding.

            NLP plays a crucial role in the development of artificial intelligence and is used in various applications such as search engines, translation services, chatbots, and more. As technology continues to evolve, the capabilities of NLP are expected to grow, making it an even more essential part of our interaction with machines.
            """

            summary = summarize.summarize(text)

            # Convert the summary into bullet points with timestamps
            bullet_points = "\n".join([f"- {sentence}" for sentence in summary])


            print("Summary:")
            print(summary)
            # print(bullet_points)

        except Exception as e:
            print(f"An error occurred: {e}")

    def format_time(self, seconds):
        """Format time in seconds to HH:MM:SS format."""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

    def do_quit(self, line):
        """Exit the CLI."""
        return True

    def postcmd(self, stop, line):
        print()  # Add an empty line for better readability
        return stop


if __name__ == '__main__':
    YTWrap().cmdloop()
