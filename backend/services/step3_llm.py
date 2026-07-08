"""STEP3: LLM - エンジン出力 → 見やすいテキスト形式"""

from anthropic import Anthropic
import json

client = Anthropic()

STEP3_SANTAN_PROMPT = """あなたはボートレース予想システム「AEGIS V5.1」の出力担当です。
以下の AEGIS エンジン計算結果を、見やすい3連単予想フォーマットに整形してください。

【出力フォーマット】
- 本命/抑え/頭違い/保険3-4着/保険5-6着の5ブロック、計10点
- 各ブロックの内容と期待度判定
- スコアランキングと環境情報
- チェック情報

エンジン計算結果を JSON として提供するので、これを見やすく整形してください。
テキスト形式で出力してください。
"""

STEP3_SANRENPUKU_PROMPT = """あなたはボートレース予想システム「AEGIS V5.1」の出力担当です。
以下の AEGIS エンジン計算結果を3連複フォーマットに変換してください。

【処理】
1. 3連単8点の各組み合わせを抽出
2. 着順を無視した3艇の組として統合
3. 同一組の確率を合算
4. 確率降順に並べ替え

出力は見やすい3連複フォーマットでお願いします。
テキスト形式で出力してください。
"""

def process_step3(engine_result, format_type='santan'):
    """
    STEP3処理: エンジン出力 → テキスト整形
    
    Args:
        engine_result: dict (AEGIS V5.1 計算結果)
        format_type: str ("santan" or "sanrenpuku")
    
    Returns:
        dict: {"formatted_output": "...", "format": "..."}
    """
    try:
        # エンジン結果を JSON 文字列に
        engine_json = json.dumps(engine_result, ensure_ascii=False, indent=2)
        
        # プロンプトを選択
        if format_type == 'sanrenpuku':
            prompt = STEP3_SANRENPUKU_PROMPT
        else:
            prompt = STEP3_SANTAN_PROMPT
        
        # Claude API を呼び出し
        response = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=3000,
            messages=[
                {
                    "role": "user",
                    "content": f"{prompt}\n\n【エンジン計算結果】\n{engine_json}"
                }
            ]
        )
        
        # 出力を取得
        formatted_output = response.content[0].text
        
        return {
            "abort": False,
            "formatted_output": formatted_output,
            "format": format_type
        }
    
    except Exception as e:
        return {
            "abort": True,
            "error": f"STEP3 処理エラー: {str(e)}"
        }
