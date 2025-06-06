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