import os
from pydub import AudioSegment
import re

def concatenate_wav_files(input_dir, output_filename):
    # 空のオーディオセグメントを作成
    combined_audio = AudioSegment.empty()

    # 指定されたディレクトリ内のすべてのWAVファイルを読み込む
    wav_files = [f for f in os.listdir(input_dir) if f.endswith('.wav')]
    
    # 数字を抽出してソート
    wav_files.sort(key=lambda x: int(re.search(r'\d+', x).group()))

    for filename in wav_files:
        file_path = os.path.join(input_dir, filename)
        audio_segment = AudioSegment.from_wav(file_path)
        combined_audio += audio_segment  # オーディオセグメントを追加

    # 結合したオーディオを保存
    combined_audio.export(output_filename, format='wav')
    print(f"Combined audio saved as {output_filename}")

# メイン処理
def main():
    input_dir = "split_notes3"  # 入力ディレクトリ
    output_filename = "combined_audio.wav"  # 出力ファイル名

    concatenate_wav_files(input_dir, output_filename)

# 実行
if __name__ == "__main__":
    main()
