import os
from pydub import AudioSegment
import librosa
import numpy as np

# M4Aファイルの読み込みとWAV形式への変換
def load_m4a_as_wav(m4a_filename):
    audio = AudioSegment.from_file(m4a_filename, format='m4a')
    wav_filename = m4a_filename.replace('.m4a', '.wav')
    audio.export(wav_filename, format='wav')
    return wav_filename

# 音のピークを検出し、音ごとに分割
def split_audio_by_notes(wav_filename, output_dir, filter_ratio=1):  # フィルタリング用の比率を設定
    y, sr = librosa.load(wav_filename, sr=None)
    envelope = librosa.onset.onset_strength(y=y, sr=sr)
    onset_frames = librosa.onset.onset_detect(onset_envelope=envelope, sr=sr)
    onset_times = librosa.frames_to_time(onset_frames, sr=sr)

    # 全体の音量の平均を計算
    overall_amplitude = np.mean(np.abs(y))  # yは音声信号の波形
    print(f"Overall amplitude: {overall_amplitude:.4f}")

    for i, onset_time in enumerate(onset_times):
        start_time = onset_time * 1000  # pydubはミリ秒で扱うため、変換
        end_time = onset_times[i + 1] * 1000 if i + 1 < len(onset_times) else len(y) * 1000 / sr

        audio_segment = AudioSegment.from_wav(wav_filename)
        segment = audio_segment[start_time:end_time]

        # セグメントの振幅の平均を計算
        segment_array = np.array(segment.get_array_of_samples())
        avg_amplitude = np.mean(np.abs(segment_array)) / (2**15)  # 16ビット音声の場合
        print(f"Segment {i + 1} amplitude: {avg_amplitude:.4f}")

        # フィルタリングの条件
        if avg_amplitude > (overall_amplitude * filter_ratio):  # 全体の音量の指定した比率より大きい場合のみ保存
            segment.export(f"{output_dir}/note_{i + 1}.wav", format="wav")
            print(f"note_{i + 1}.wav saved.")
        else:
            print(f"note_{i + 1}.wav not saved (too quiet).")

# メイン処理
def main():
    m4a_filename = "output/kimi.m4a"  # 処理するM4Aファイルのパス
    output_dir = "split_notes3"  # 分割後の音を保存するディレクトリ

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    wav_filename = load_m4a_as_wav(m4a_filename)
    split_audio_by_notes(wav_filename, output_dir)

# 実行
if __name__ == "__main__":
    main()
