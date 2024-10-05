import os
import subprocess
from pydub import AudioSegment
import librosa

# YouTubeから音声をダウンロード
def download_youtube_audio(youtube_url, output_path):
    try:
        # yt-dlpコマンドを生成
        command = [
            "yt-dlp",
            "-x",                   # 音声のみを抽出
            "--audio-format", "m4a", # 音声フォーマットをm4aに指定
            "-o", f"{output_path}/%(title)s.%(ext)s", # 出力パスの指定
            youtube_url             # YouTubeのURL
        ]

        # コマンドを実行
        subprocess.run(command, check=True)
        print(f"Downloaded audio to {output_path}")

    except Exception as e:
        print(f"An error occurred while downloading: {e}")

# M4Aファイルの読み込みとWAV形式への変換
def load_m4a_as_wav(m4a_filename):
    # M4AファイルをAudioSegmentとして読み込む
    audio = AudioSegment.from_file(m4a_filename, format='m4a')
    
    # 一時的にwavファイルとして保存
    wav_filename = m4a_filename.replace('.m4a', '.wav')
    audio.export(wav_filename, format='wav')
    return wav_filename

# 音のピークを検出し、音ごとに分割
def split_audio_by_notes(wav_filename, output_dir):
    # librosaで音声を読み込む
    y, sr = librosa.load(wav_filename, sr=None)

    # 音声のエンベロープを計算（大まかに音の強弱を捉える）
    envelope = librosa.onset.onset_strength(y=y, sr=sr)
    
    # 音の区切りとなるフレーム（音が鳴り始めるタイミング）を検出
    onset_frames = librosa.onset.onset_detect(onset_envelope=envelope, sr=sr)

    # フレームを秒に変換
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)

    # 分割点を取得し、1つずつ保存
    for i, onset_time in enumerate(onset_times):
        start_time = onset_time * 1000  # pydubはミリ秒で扱うため、変換
        if i + 1 < len(onset_times):
            end_time = onset_times[i + 1] * 1000  # 次の音の開始点
        else:
            end_time = len(y) * 1000 / sr  # 最後の音はファイルの最後まで

        # pydubでオーディオファイルを分割
        audio_segment = AudioSegment.from_wav(wav_filename)
        segment = audio_segment[start_time:end_time]

        # 分割した音を保存
        segment.export(f"{output_dir}/note_{i + 1}.wav", format="wav")
        print(f"note_{i + 1}.wav saved.")

# メイン処理
def main():
    youtube_url = "https://www.youtube.com/watch?v=jAH7Y5zhyNE"  # YouTubeの動画URL
    output_path = "output"  # 出力ディレクトリ

    # 出力ディレクトリが存在しない場合は作成
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # YouTubeから音声をダウンロード
    download_youtube_audio(youtube_url, output_path)

    # ダウンロードしたM4Aファイルのパスを取得
    m4a_filename = os.path.join(output_path, os.listdir(output_path)[0])  # 最初のファイルを取得

    # M4AファイルをWAV形式に変換
    wav_filename = load_m4a_as_wav(m4a_filename)

    # 分割後の音を保存するディレクトリ
    split_output_dir = "split_notes"
    if not os.path.exists(split_output_dir):
        os.makedirs(split_output_dir)

    # 音を分割して保存
    split_audio_by_notes(wav_filename, split_output_dir)

# 実行
if __name__ == "__main__":
    main()
