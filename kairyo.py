import os
import subprocess
from pydub import AudioSegment
import librosa

# YouTubeから音声をダウンロード
def download_youtube_audio(youtube_url, output_path):
    try:
        command = [
            "yt-dlp",
            "-x",                   # 音声のみを抽出
            "--audio-format", "m4a", # 音声フォーマットをm4aに指定
            "-o", f"{output_path}/%(title)s.%(ext)s", # 出力パスの指定
            youtube_url             # YouTubeのURL
        ]

        subprocess.run(command, check=True)
        print(f"Downloaded audio to {output_path}")

    except Exception as e:
        print(f"An error occurred while downloading: {e}")

# M4Aファイルの読み込みとWAV形式への変換
def load_m4a_as_wav(m4a_filename):
    audio = AudioSegment.from_file(m4a_filename, format='m4a')
    wav_filename = m4a_filename.replace('.m4a', '.wav')
    audio.export(wav_filename, format='wav')
    return wav_filename

# 音のピークを検出し、音ごとに分割
def split_audio_by_notes(wav_filename, output_dir, silence_threshold=-17.0):
    y, sr = librosa.load(wav_filename, sr=None)
    envelope = librosa.onset.onset_strength(y=y, sr=sr)
    onset_frames = librosa.onset.onset_detect(onset_envelope=envelope, sr=sr)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)

    for i, onset_time in enumerate(onset_times):
        start_time = onset_time * 1000  # pydubはミリ秒で扱うため、変換
        end_time = onset_times[i + 1] * 1000 if i + 1 < len(onset_times) else len(y) * 1000 / sr

        audio_segment = AudioSegment.from_wav(wav_filename)
        segment = audio_segment[start_time:end_time]

        # 音量チェック
        if segment.dBFS > silence_threshold:  # 指定したしきい値より音量が大きい場合のみ保存
            segment.export(f"{output_dir}/note_{i + 1}.wav", format="wav")
            print(f"note_{i + 1}.wav saved.")
        else:
            print(f"note_{i + 1}.wav not saved (silence).")

# メイン処理
def main():
    youtube_url = "https://www.youtube.com/watch?v=jAH7Y5zhyNE"  # YouTubeの動画URL
    output_path = "output"  # 出力ディレクトリ

    if not os.path.exists(output_path):
        os.makedirs(output_path)

    download_youtube_audio(youtube_url, output_path)

    m4a_filename = os.path.join(output_path, os.listdir(output_path)[0])  # 最初のファイルを取得
    wav_filename = load_m4a_as_wav(m4a_filename)

    split_output_dir = "split_notes"
    if not os.path.exists(split_output_dir):
        os.makedirs(split_output_dir)

    split_audio_by_notes(wav_filename, split_output_dir)

# 実行
if __name__ == "__main__":
    main()
