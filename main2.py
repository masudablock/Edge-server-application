import hashlib
import glob
import json
import time
import base64
import os
import urllib.request
import determine_execute as det
# CSVファイルのあるのディレクトリ一覧取得。
# @parameter:
#   path: csvファイルのあるパス （../test-csv-data/）
# @return:
#   CSVファイルのあるディレクトリのリスト (["../test-csv-data/aaaaaaaaaaaa","../test-csv-data/bbbbbbbbbbbb",...])
def fetch_csv_dir_list(path):
        files = os.listdir(path)
        files_dir = [{"path":path + f + "/", "id":f} for f in files if os.path.isdir(os.path.join(path, f))]
        return(files_dir)
# 各デバイスごとのCSVファイルのパス覧取得。
# @parameter:
#   path: csvファイルのディレクトリ （../test-csv-data/aaaaaaaaaa）
# @return:
#   CSVファイルのあるディレクトリのリスト (["../test-csv-data/aaaaaaaaaaaa/1.csv","../test-csv-data/aaaaaaaaaaaa/2.csv",...])
def fetch_csv_file_list(dirpath):
        files = os.listdir(dirpath)
        files_file = [dirpath + f for f in files if os.path.isfile(os.path.join(dirpath, f))]
        return(files_file)
# CSVファイルの内容を取得
# @parameter:
#   path: csvファイルのパス （../test-csv-data/aaaaaaaaaa/1.csv）
# @return:
#   CSVファイルの中身 
def fetch_csv_raw_data(filepath):
        file_data = open(filepath, "r")
        file_text =file_data.read()
        file_data.close()
        return(file_text)
# 多重ハッシュ化。
# @parameter:
#   before_frame_hash: 一つ前のフレームのsecond_hashハッシュ値
#   first_hash: 現フレームの一段階目のハッシュ値
# @return:
#   二重ハッシュ化を行ったハッシュ値
def doble_hash(before_frame_hash,first_hash):
        text = str(before_frame_hash) + str(first_hash)
        #print(text)
        second_hash = hashlib.sha256(text.encode()).hexdigest()
        return second_hash
# http形式で出力。
# @parameter:
#   raw_data: base64でエンコードした、生データ(CSVファイル)
#   camera_id: カメラ番号
#   frame_number: フレーム番号
def output_http(camera_id, frame_number,raw_data, execute):
        data = {}
        data["raw_data"] = base64.b64encode(raw_data.encode()).decode()
        data["camera_id"] = camera_id
        data["frame_number"] = frame_number
        data["execute"] = execute
        url = 'http://localhost:8000/api/set'
        headers = {'Content-Type': 'application/json',}
        req = urllib.request.Request(url, json.dumps(data).encode(), headers)
        #with urllib.request.urlopen(req) as res:
        #        body = json.load(res)
        #if execute == 1:
        #        print(camera_id)
        #        print(frame_number)
def main():
        #カメラ一覧取得
        csv_dir_list = fetch_csv_dir_list("./test-csv-data/")
        #print(csv_dir_list)
        #初期データ取得
        csv_file_list = {}
        N = len(csv_dir_list)
        LAST_FRAME = len(fetch_csv_file_list(csv_dir_list[0]["path"])) - 1
        over = 0
        importance = [0] * (N + 1)
        for i in range(1,N+1):
                csv_file_list[i]=fetch_csv_file_list(csv_dir_list[i-1]["path"])
                importance[i] = i / N
        #print(csv_file_list)
        num = 1
        count = [0] * (N + 1)
        next_frame_time = time.time() + 0.1
        #シミュレーション
        while True:
                camera_id = (num % N) + 1
                frame_number = (num // N) + 1
                #print(str(time.time()) + " camera_id:" + str(camera_id) + " frame_number:" + str(frame_number))
                raw_data = fetch_csv_raw_data(csv_file_list[camera_id][frame_number])
                if frame_number > 1:
                        #書き込み判定
                        execute = 0
                        if frame_number % N == 0 or over == 1:
                                execute = det.determine_execute(camera_id,count,importance,N)
                        if execute == 2:
                                execute = 1
                                over = 1
                        if execute == 0:
                                count[camera_id] += 1
                        else:
                                count[camera_id] = 0
                        if camera_id == N:
                                over = 0
                        #APIへ出力
                        output_http(csv_dir_list[camera_id-1]["id"], frame_number, raw_data, execute)
                num += 1
                if camera_id == N and frame_number == LAST_FRAME:
                        break
                if camera_id == N:
                        while time.time() < next_frame_time:
                                time.sleep(0.001)
                        next_frame_time = next_frame_time + 0.1

if __name__ == '__main__':
        start = time.time()
        main()
        print(str(time.time() - start) + "sec")
