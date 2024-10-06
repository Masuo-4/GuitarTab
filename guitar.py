# import libraries
import scipy.io.wavfile as wav  # .wavファイルを扱うためのライブラリ
from sklearn.svm import SVC     # SVC（クラス分類をする手法）を使うためのライブラリ
import numpy                    # ndarray（多次元配列）などを扱うためのライブラリ
import librosa                  # 音声信号処理をするためのライブラリ
import os                       # osに依存する機能を利用するためのライブラリ

# ルートディレクトリ
ROOT_PATH = 'data/'

# ギターの種類（データのディレクトリ名になっている）
strings=['1', '2', '3', '4', '5', '6']

sound_training=[]    # 学習用のFCCの値を格納する配列
guitar_training=[] # 学習用のラベルを格納する配列

import librosa

def getMfcc(filename):
    y, sr = librosa.load(filename, sr=None)  # sr=Noneで元のサンプリングレートを使用
    n_fft = min(2048, len(y))  # FFTサイズの設定
    n_mels = 128  # メルフィルタバンクの数を128に設定
    fmax = sr / 2  # ナイキスト周波数（最大周波数）に設定
    
    # MFCCを計算
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13, n_fft=n_fft, n_mels=n_mels, fmax=fmax)
    return mfcc

# 各ディレクトリごとにデータをロードし、MFCCを求めていく
for guitar in strings:
    # どのギターのデータを読み込んでいるかを表示
    print('data of %s...' % guitar)
    # ギターの種類でディレクトリを作成しているため<ルートパス+ギター名>で読み込める。
    path = os.path.join(ROOT_PATH + guitar)  
    print('path = %s' % path)  
    # パス、ディレクトリ名、ファイル名に分けることができる便利なメソッド
    for pathname, dirnames, filenames in os.walk(path): 
        for filename in filenames:
            # macの場合は勝手に.DS_Storeやらを作るので、念の為.wavファイルしか読み込まないようにします。
            if filename.endswith('.wav'):
                mfcc=getMfcc(os.path.join(pathname, filename))
                sound_training.append(mfcc.T)    # sound_trainingにmfccの値を追加
                label=numpy.full((mfcc.shape[1] ,), 
                strings.index(guitar), dtype=int)   # labelをstringsのindexで全て初期化# numpy.int→intに変更
                guitar_training.append(label)  # guitar_trainingにラベルを追加

sound_training=numpy.concatenate(sound_training)  # ndarrayを結合
guitar_training=numpy.concatenate(guitar_training)

# カーネル係数を1e-4で学習
clf = SVC(C=1, gamma=1e-4)      # SVCはクラス分類をするためのメソッド
clf.fit(sound_training, guitar_training)    # MFCCの値とラベルを組み合わせて学習
print('Learning Done')

counts = []     # predictionの中で各値（予測される話者のインデックス）が何回出ているかのカウント
file_list = []  # file名を格納する配列

# 各ギターのテストデータが入っている~testというディレクトリごとにMFCCを求めていく
for guitar in strings:
    path = os.path.join(ROOT_PATH + '%stest' % guitar)
    print(path)
    for pathname, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if filename.endswith('.wav'):
                mfcc = getMfcc(os.path.join(pathname, filename))
                prediction = clf.predict(mfcc.T)    # MFCCの値から予測した結果を代入
                # predictionの中で各値（予測される話者のインデックス）が何回出ているかをカウントして追加
                counts.append(numpy.bincount(prediction))   
                file_list.append(filename)  # 実際のファイル名を追加
print(file_list)

total = 0   # データの総数
correct = 0 # 正解の数

# 推測されるギターの名前がファイル名の頭と一致したらCorrect
for filename, count in zip(file_list, counts):
    total += 1
    result = strings[numpy.argmax(count-count.mean(axis=0))]  
    if  filename.startswith(result):
        correct += 1
print('correct: ' + str(correct) + '/' + str(total))
print('score : ' + str(correct / total))