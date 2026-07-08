"""STEP1: LLM - 画像/テキスト → JSON 構造化"""

import json
import base64
from io import BytesIO
from anthropic import Anthropic

client = Anthropic()

STEP1_PROMPT = """あなたはボートレース予想システム「AEGIS V5.1」のデータ入力担当です。
渡された出走表・展示情報・気象情報から、以下のルールに従ってJSONを生成してください。

対応会場: 徳山 / 大村 / 下関 / 若松 / 蒲郡 / 唐津 / 芦屋（この7会場のみ）

出力形式の詳細は、AEGIS_入力.md を参照してください。

JSON スキーマ:
{
  "venue": "会場名",
  "race_no": 8,
  "entry_order": [1C艇番, 2C艇番, 3C艇番, 4C艇番, 5C艇番, 6C艇番],
  "wind_dir": "追い風 | 向かい風 | 横風 | 無風",
  "wind_speed": 3.0,
  "wave_cm": 2.0,
  "condition": "晴 | 曇 | 雨",
  "boats": [
    {
      "frame": 1,
      "name": "選手名",
      "grade": "A1 | A2 | B1 | B2 | 不明",
      "win_rate": 6.52,
      "nat_2": 38.46,
      "local_rate": 6.80,
      "motor_2": 42.1,
      "boat_2": 35.8,
      "exh_st": 0.15,
      "exh_time": 6.78,
      "series_st_avg": 0.158,
      "series_st_n": 3,
      "has_f_this_series": false,
      "f_val": null,
      "is_l": false,
      "exh_red_st": false,
      "is_female": false
    }
  ]
}

出力は JSON のみとしてください。
"""

def process_step1(input_data):
    """
    STEP1処理: 画像またはテキストから JSON を生成
    
    Args:
        input_data: FileStorage (画像) または dict (テキスト)
    
    Returns:
        dict: {"input_json": {...}, "confirmation": "..."} または {"error": "..."}
    """
    try:
        # 画像またはテキストから base64 またはテキストを準備
        if hasattr(input_data, 'read'):  # ファイルオブジェクト
            image_data = base64.standard_b64encode(input_data.read()).decode('utf-8')
            message_content = [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/jpeg",
                        "data": image_data
                    }
                },
                {
                    "type": "text",
                    "text": STEP1_PROMPT
                }
            ]
        else:  # テキスト入力
            text_input = input_data.get('text', '') if isinstance(input_data, dict) else str(input_data)
            message_content = [
                {
                    "type": "text",
                    "text": f"{STEP1_PROMPT}\n\n【入力データ】\n{text_input}"
                }
            ]
        
        # Claude API を呼び出し
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            messages=[
                {
                    "role": "user",
                    "content": message_content
                }
            ]
        )
        
        # レスポンスを解析
        response_text = response.content[0].text
        
        # JSON を抽出
        try:
            # JSON ブロックを探す
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start >= 0 and json_end > json_start:
                json_str = response_text[json_start:json_end]
                input_json = json.loads(json_str)
                
                return {
                    "abort": False,
                    "input_json": input_json,
                    "confirmation": response_text
                }
            else:
                raise ValueError("JSON ブロックが見つかりません")
        
        except json.JSONDecodeError as e:
            return {
                "abort": True,
                "error": f"JSON パースエラー: {str(e)}",
                "raw_response": response_text
            }
    
    except Exception as e:
        return {
            "abort": True,
            "error": f"STEP1 処理エラー: {str(e)}"
        }
