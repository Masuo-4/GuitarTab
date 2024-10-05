import os
from pydub import AudioSegment
import librosa

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
    m4a_filename = "output/1.m4a"  # 処理するM4Aファイルのパス
    output_dir = "split_notes"  # 分割後の音を保存するディレクトリ

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    wav_filename = load_m4a_as_wav(m4a_filename)
    split_audio_by_notes(wav_filename, output_dir)

# 実行
if __name__ == "__main__":
    main()
