# json形式で出力。
# @parameter:
#   camera_id: カメラ番号
#   count:それぞれのデバイスの書き込み待機数
# @return:
#   実行するかどうかの判定
def determine_execute(camera_id,count,importance,N):
        judge = 0
        max_index = 0
        for i in range(1,N+1):
                if judge < count[i] * (100 ** (importance[i] - 1)):
                        judge = count[i] * (100 ** (importance[i] - 1))
                        max_index = i
        if count[camera_id] > 1000:
                return 2
        elif max_index == camera_id:
                return 1
        else:
                return 0
