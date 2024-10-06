# import libraries
import scipy.io.wavfile as wav  # .wavファイルを扱うためのライブラリ
from sklearn.svm import SVC     # SVC（クラス分類をする手法）を使うためのライブラリ
import numpy                    # ndarray（多次元配列）などを扱うためのライブラリ
import librosa                  # 音声信号処理をするためのライブラリ
import os                       # osに依存する機能を利用するためのライブラリ

# ルートディレクトリ
ROOT_PATH = 'data/'

# ギターの種類（データのディレクトリ名になっている）
strings = ['1', '2', '3', '4', '5', '6']

sound_training = []    # 学習用のMFCCの値を格納する配列
guitar_training = []   # 学習用のラベルを格納する配列

def getMfcc(filename):
    y, sr = librosa.load(filename, sr=44100)  # サンプリングレートを44100 Hzに固定
    n_fft = min(2048, len(y))  # FFTサイズの設定
    n_mels = 128  # メルフィルタバンクの数を128に設定
    fmax = sr / 2  # ナイキスト周波数（最大周波数）に設定
    
    # MFCCを計算
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, n_fft=2048, n_mels=n_mels, fmax=fmax)
    return mfcc

# 各ディレクトリごとにデータをロードし、MFCCを求めていく
for guitar in strings:
    print('data of %s...' % guitar)
    path = os.path.join(ROOT_PATH + guitar)  
    print('path = %s' % path)  
    for pathname, dirnames, filenames in os.walk(path): 
        for filename in filenames:
            if filename.endswith('.wav'):
                mfcc = getMfcc(os.path.join(pathname, filename))
                sound_training.append(mfcc.T)    # sound_trainingにmfccの値を追加
                label = numpy.full((mfcc.shape[1],), strings.index(guitar), dtype=int)
                guitar_training.append(label)  # guitar_trainingにラベルを追加

sound_training = numpy.concatenate(sound_training)  # ndarrayを結合
guitar_training = numpy.concatenate(guitar_training)

# カーネル係数を1e-4で学習
clf = SVC(C=1, gamma=1e-4)      # SVCはクラス分類をするためのメソッド
clf.fit(sound_training, guitar_training)    # MFCCの値とラベルを組み合わせて学習
print('Learning Done')

counts = []     # 各ファイルの予測結果のカウントを保持
file_list = []  # ファイル名を保持するリスト
actual_labels = []  # 実際のラベルを保持するリスト

# 各ギターのテストデータを処理
for guitar in strings:
    path = os.path.join(ROOT_PATH + '%stest' % guitar)
    print(path)
    for pathname, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith('.wav'):
                mfcc = getMfcc(os.path.join(pathname, filename))
                prediction = clf.predict(mfcc.T)    # MFCCの値から予測した結果を代入
                counts.append(numpy.bincount(prediction))  # 予測の結果をカウントして追加
                file_list.append(filename)  # ファイル名をリストに追加
                actual_labels.append(guitar)  # 正解のラベルを追加

# 予測の詳細を表示
total = 0   # データの総数
correct = 0 # 正解の数

print("\nPrediction results:\n")
for filename, count, actual_label in zip(file_list, counts, actual_labels):
    total += 1
    predicted_guitar = strings[numpy.argmax(count)]  # 最も多く予測されたギターの種類
    result = "Correct" if predicted_guitar == actual_label else "Incorrect"
    
    # 各ファイルの予測結果を表示 (予測と実際の値も表示)
    print(f"File: {filename}, Predicted: {predicted_guitar}, Actual: {actual_label}, {result}")
    
    if result == "Correct":
        correct += 1

# 正解率を表示
print(f'\nCorrect: {correct}/{total}')
print(f'Score: {correct / total:.2f}')
