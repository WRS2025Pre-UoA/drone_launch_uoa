# drone_launch_uoa
## 内容
 - drone用PCで以下のノードを立ち上げる
    - drone_operation/operator_gui_node：ドローン用GUI、各検出ノードへ画像を分配
    - misora2_dt_client/client.py dt_client_node：デジタルツインへ送信
    - misora2_pressure/pressure_node：圧力メータを読み取る
    - misora2_qr/qr_node：QRコードの読み取り
    - misora2_cracks/cracks_node：テストピース(クラック)の検査
 - ミッションごとにファイルを分けている bringupP[<font color="red">ミッション番号1~4,6</font>].launch.py
## 実行コード
~~~bash!
git clone git@github.com:WRS2025Pre-UoA/drone_launch_uoa.git
cd [ワークスペース]
colcon build
source install/setup.bash
ros2 launch drone_launch_uoa bringupP<1~4,6>.launch.py
~~~