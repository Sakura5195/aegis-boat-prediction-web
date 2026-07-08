"""STEP2: AEGIS V5.1 エンジン実行"""

import json
import subprocess
import sys
import os

engine_path = os.path.join(os.path.dirname(__file__), '..', 'engine', 'aegis_engine_v51.py')

def run_engine(input_data):
    """
    AEGIS V5.1 エンジンを実行
    
    Args:
        input_data: dict (JSON 構造化データ)
    
    Returns:
        dict: エンジン計算結果
    """
    try:
        # JSON を準備
        input_json = json.dumps(input_data, ensure_ascii=False)
        
        # エンジンを subprocess で実行
        result = subprocess.run(
            [sys.executable, engine_path],
            input=input_json,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        # 出力を解析
        if result.returncode != 0:
            return {
                "abort": True,
                "error": f"エンジン実行エラー: {result.stderr}"
            }
        
        # JSON として解析
        output = json.loads(result.stdout)
        return output
    
    except subprocess.TimeoutExpired:
        return {
            "abort": True,
            "error": "エンジン実行がタイムアウトしました（30秒以上かかりました）"
        }
    
    except json.JSONDecodeError as e:
        return {
            "abort": True,
            "error": f"エンジン出力の JSON パースエラー: {str(e)}",
            "raw_output": result.stdout if 'result' in locals() else "N/A"
        }
    
    except Exception as e:
        return {
            "abort": True,
            "error": f"STEP2 処理エラー: {str(e)}"
        }
