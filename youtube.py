import os
import subprocess

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
        print(f"An error occurred: {e}")

# メイン処理
if __name__ == "__main__":
    youtube_url = "https://www.youtube.com/watch?v=1H1Eyk6iAIg"  # YouTubeの動画URL
    output_path = "output"  # 出力ディレクトリ

    # 出力ディレクトリが存在しない場合は作成
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    download_youtube_audio(youtube_url, output_path)
