import whisper
import os
import sys
import tqdm
from datetime import timedelta


def format_vtt_time(seconds):
    total_seconds = int(seconds)
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    milliseconds = int((seconds % 1) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"


def format_srt_time(seconds):
    return str(timedelta(seconds=seconds)).replace(".", ",")


class _CustomProgressBar(tqdm.tqdm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._current = self.n

    def update(self, n):
        super().update(n)
        self._current += n
        print("Progress: " + str(self._current) + "/" + str(self.total))


transcribe_module = sys.modules['whisper.transcribe']
transcribe_module.tqdm.tqdm = _CustomProgressBar


class WhisperTranscriber:
    def __init__(self, username, model_size='base', language='English', output_dir='output_test', beam_size=5,
                 temperature=0,
                 no_speech_threshold=0.6):
        self.username = username
        self.model_size = model_size
        self.language = language
        self.output_dir = output_dir
        self.beam_size = beam_size
        self.temperature = temperature
        self.no_speech_threshold = no_speech_threshold
        self.model = whisper.load_model(model_size)

    def transcribe(self, video_file):
        # Determine the base directory of the video file
        base_dir = os.path.dirname(video_file)
        # Create a specific output directory for this model size within the video's directory
        model_output_dir = os.path.join(base_dir, self.model_size)
        if not os.path.exists(model_output_dir):
            os.makedirs(model_output_dir)

        result = self.model.transcribe(
            video_file,
            beam_size=self.beam_size,
            temperature=self.temperature,
            language=self.language,
            no_speech_threshold=self.no_speech_threshold
        )

        base_filename = os.path.splitext(os.path.basename(video_file))[0]
        # Generate transcript files within the model-specific directory
        transcript_file_vtt = os.path.join(model_output_dir, f"{base_filename}.vtt")
        transcript_file_txt = os.path.join(model_output_dir, f"{base_filename}.txt")
        transcript_file_srt = os.path.join(model_output_dir, f"{base_filename}.srt")

        with open(transcript_file_vtt, 'w') as vtt_file, \
                open(transcript_file_txt, 'w') as txt_file, \
                open(transcript_file_srt, 'w') as srt_file:
            for indx, segment in enumerate(result['segments']):
                # Write to VTT
                vtt_file.write(f"{indx + 1}\n")
                vtt_file.write(format_vtt_time(segment['start']) + ' --> ' + format_vtt_time(segment['end']) + '\n')
                vtt_file.write(segment['text'].strip() + '\n\n')

                # Write to TXT
                txt_file.write(segment['text'].strip() + '\n')

                # Write to SRT
                srt_file.write(f"{indx + 1}\n")
                srt_file.write(format_srt_time(segment['start']) + ' --> ' + format_srt_time(segment['end']) + '\n')
                srt_file.write(segment['text'].strip() + '\n\n')

        return [transcript_file_vtt, transcript_file_txt, transcript_file_srt]
