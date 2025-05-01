import pandas as pd


def get_sheet_all_values(sheet):
    # Google Sheetsからデータを取得し、処理したpandas DataFrameを返す関数
    data = pd.DataFrame(sheet.get_all_values())
    data.columns = list(data.iloc[0])
    data = data.drop(0, axis=0)
    data = data.reset_index(drop=True)
    return data


def symbols_escape(text):
    # 特殊記号をすべてエスケープする関数
    escaped_text = ""
    for char in text:
        if char in ["*", "_", "`", "~", "|", ">"]:
            escaped_text += "\\"
        escaped_text += char
    return escaped_text


# 内戦用
guild_ws = ""
mgr_role = ""

# ジュエリー用
admins_mention = []

result_ws = ""
room_ws = ""
member_ws = ""
club_ws = ""
input_member_ws = ""
input_club_ws = ""

room_data = ""
member_data = ""
club_data = ""

remind_role = ""

remind_ch = ""
result_ch = ""
repeat_result_ch = ""
register_ch = ""

small_build_message = "★部屋建て\n\
以下のレギュレーションで部屋建てをお願いします。\n\
【レース】￤天皇賞･春\n\
【人数】￤9人\n\
【時間】￤24時間後\n\
【季節/天気・バ場状態】￤春/晴･良\n\
【やる気設定】￤絶好調\n"

build_message = (
    small_build_message
    + "\n\
    部屋建て後、本テキストチャンネルにてレースID及び役職を添え、参加対象者をメンションの上でテキストを入力・送信してください。\n\
    【例】\n\
    @対戦相手1 @対戦相手2\n\
    先鋒戦\n\
    ルームID: 12345678\n\
    参加対象者に対象レースへご参加いただき、揃い次第出走可とします。\n\
    \n\
    ★結果報告\n\
    レース結果を確認後、《レースに勝利した方》は本テキストチャンネルにてbotを用いて結果入力をしていただくようにお願いします。\n\
    botで入力した内容は結果入力チャンネルでのみ公開され、本テキストチャンネルの表示は周りの方には見えません。\n\
    また、レース参加者は念のためにスクリーンショット等により結果を保存してください。"
)
