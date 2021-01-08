import hashlib
import glob
import json
import time

import determine_execute

# 任意のデバイスの生データの一斉取得。
# @parameter:
#   camera_id: カメラ番号
# @return:
#   デバイスで取得されたデータ内容をlist形式で記録したもの
def fetch_raw_data(camera_id):
        data = []
        if camera_id < 10:
                id = "0" + str(camera_id)
        else:
                id = str(camera_id)
        path = "../LiDAR_data/Sequence1a/LS_" + id + "/*.pcd"
        for i,file in enumerate(sorted(glob.glob(path))):
                file_data = open(file, "r")
                file_text ="".join(file_data)
                data.append(file_text)
        return(data)

# 多重ハッシュ化。
# @parameter:
#   before_frame_hash: 一つ前のフレームのsecond_hashハッシュ値
#   first_hash: 現フレームの一段階目のハッシュ値
# @return:
#   二重ハッシュ化を行ったハッシュ値
def doble_hash(before_frame_hash,first_hash):
        text = str(before_frame_hash) + str(first_hash)
        print(text)
        second_hash = hashlib.sha256(text.encode()).hexdigest()
        return second_hash



# json形式で出力。
# @parameter:
#   hash: ハッシュ値
#   camera_id: カメラ番号
#   first_frame_number: 初期フレーム番号
#   last_frame_number: 最終フレーム番号
def output_json(hash, camera_id, first_frame_number, last_frame_number,execute):
        file_path = "./json/" + str(camera_id) + "_" + str(first_frame_number) + "_" + str(last_frame_number) + ".json"
        data = {}
        data["hash"] = hash
        data["camera_id"] = camera_id
        data["first_frame_number"] = first_frame_number
        data["last_frame_number"] = last_frame_number
        data["execute"] = execute
        print(data)
        with open(file_path, 'w') as outfile:
                json.dump(data, outfile)
def main():
        #初期データ取得
        LS = {}
        N = 10
        importance = [0] * (N + 1)
        for i in range(1,N + 1):
                LS[i] = fetch_raw_data(i)
                importance[i] = 1 / i

        num = 1
        list = [0] * (N + 1)
        before_frame_hash = [0] * (N + 1)
        count = [0] * (N + 1)
        #シミュレーション
        while True:
                camera_id = (num % 10) + 1
                first_frame_number = (num // 10) + 1
                last_frame_number = (num // 10) + 1
                list[camera_id] = hashlib.sha256(LS[camera_id][last_frame_number].encode()).hexdigest()

                if last_frame_number > 1:
                        #書き込み判定
                        execute = 0
                        if last_frame_number % 10 == 0:
                                execute = determine_execute(camera_id,count,importance,N)
                        if execute == 0:
                                count[camera_id] += 1
                        else:
                                count[camera_id] = 0
                        #多重ハッシュ化
                        hash = doble_hash(before_frame_hash[camera_id],list[camera_id])
                        #json出力
                        output_json(hash, camera_id, first_frame_number, last_frame_number,execute)
                before_frame_hash[camera_id] = list[camera_id]
                num += 1
                if camera_id == N and last_frame_number == 1210:
                        break
                if camera_id == N:
                        time.sleep(0.1)

if __name__ == '__main__':
        main()
