#!/usr/bin/env python3
"""AEGIS Web Application - Main Flask App"""

import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

from config import config
from services.step1_llm import process_step1
from services.step2_engine import run_engine
from services.step3_llm import process_step3

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config[os.getenv('FLASK_ENV', 'development')])

# Enable CORS
CORS(app)

# Routes
@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'version': 'V5.1',
        'engine': 'AEGIS'
    }), 200

@app.route('/api/predict/step1', methods=['POST'])
def step1_input():
    """
    STEP1: 画像/テキスト → JSON 構造化
    """
    try:
        # ファイルまたは JSON を受け取る
        if 'image' in request.files:
            image = request.files['image']
            result = process_step1(image)
        elif request.is_json:
            data = request.get_json()
            # テキスト入力の場合
            result = process_step1(data)
        else:
            return jsonify({'error': 'Image or JSON data required'}), 400
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict/step2', methods=['POST'])
def step2_calculate():
    """
    STEP2: AEGIS エンジン実行
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'JSON data required'}), 400
        
        # エンジン実行
        result = run_engine(data)
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict/step3', methods=['POST'])
def step3_output():
    """
    STEP3: 出力整形
    """
    try:
        data = request.get_json()
        
        if not data or 'engine_result' not in data:
            return jsonify({'error': 'engine_result required'}), 400
        
        # 出力形式を指定（santan or sanrenpuku）
        format_type = data.get('format', 'santan')  # santan or sanrenpuku
        
        result = process_step3(data['engine_result'], format_type)
        
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/predict/full', methods=['POST'])
def predict_full():
    """
    フルパイプライン実行: STEP1 → STEP2 → STEP3
    """
    try:
        # 入力を受け取る
        if 'image' in request.files:
            image = request.files['image']
            step1_result = process_step1(image)
        elif request.is_json:
            data = request.get_json()
            step1_result = process_step1(data)
        else:
            return jsonify({'error': 'Image or JSON data required'}), 400
        
        # STEP1 で abort が発生した場合
        if step1_result.get('abort'):
            return jsonify(step1_result), 400
        
        # STEP2 実行
        step2_result = run_engine(step1_result['input_json'])
        
        # STEP2 で abort が発生した場合
        if step2_result.get('abort'):
            return jsonify(step2_result), 400
        
        # STEP3 実行
        format_type = request.get_json().get('format', 'santan') if request.is_json else 'santan'
        step3_result = process_step3(step2_result, format_type)
        
        # 全結果を返す
        return jsonify({
            'step1': step1_result,
            'step2': step2_result,
            'step3': step3_result
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])
