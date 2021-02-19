import os
import hashlib
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

def main():
        #カメラ一覧取得
        csv_file_list = {}
        csv_dir_list = fetch_csv_dir_list("./test-csv-data/")
        LAST_FRAME = len(fetch_csv_file_list(csv_dir_list[0]["path"])) - 1

        frame_number = 1
        camera_id = 1
        while True:
          raw_data = fetch_csv_raw_data(csv_file_list[camera_id][frame_number])
          first_hash[camera_id] = hashlib.sha256(raw_data.encode()).hexdigest()
          print(first_hash[camera_id])
          frame_number += 1
          if frame_number == LAST_FRAME:
            break
def main():
        #カメラ一覧取得
        csv_dir_list = fetch_csv_dir_list("./test-csv-data/")
        #print(csv_dir_list)
        #初期データ取得
        csv_file_list = {}
        N = len(csv_dir_list)
        N = 1
        LAST_FRAME = len(fetch_csv_file_list(csv_dir_list[0]["path"])) - 1
        first_hash = [0] * (N + 1)
        for i in range(1,N+1):
                csv_file_list[i]=fetch_csv_file_list(csv_dir_list[i-1]["path"])
        num = 0
        #テスト
        while True:
                camera_id = (num % N) + 1
                frame_number = (num // N) + 1
                raw_data = fetch_csv_raw_data(csv_file_list[camera_id][frame_number])
                #print(raw_data)
                first_hash[camera_id] = hashlib.sha256(raw_data.encode()).hexdigest()
                print(first_hash)
                print(csv_dir_list[camera_id-1]["id"])

                num +=1 


if __name__ == '__main__':
  main()
