from spleeter.separator import Separator
import os
import tensorflow as tf

def main():
    # インプット音源ファイルを指定
    input_file = "./output/mkc.m4a"
    # 出力ディレクトリを指定
    output_directory = "./output-python"

    # GPUメモリの成長を許可
    physical_devices = tf.config.experimental.list_physical_devices('GPU')
    if physical_devices:
        tf.config.experimental.set_memory_growth(physical_devices[0], True)

    # Spleeterの分離モードを指定
    separator = Separator("spleeter:5stems")

    # 出力先ディレクトリが存在しない場合は作成
    os.makedirs(output_directory, exist_ok=True)

    try:
        # インプットファイルと出力ディレクトリを指定して分離実行
        separator.separate_to_file(input_file, output_directory)
        print(f'音源の分離が完了しました。出力先: {output_directory}')
    except Exception as e:
        print(f'音源の分離中にエラーが発生しました: {e}')

if __name__ == '__main__':
    main()
