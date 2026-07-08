# AEGIS V5.1 データ入力プロンプト（STEP1）

## 概要

ユーザーが提供した画像またはテキストから、ボートレース出走表・展示情報・気象情報を抽出し、
JSON 形式に構造化するステップです。

## 対応会場

- 徳山
- 大村
- 下関
- 若松
- 蒲郡
- 唐津
- 芦屋

## 出力形式

```json
{
  "venue": "会場名",
  "race_no": 8,
  "entry_order": [1, 2, 3, 4, 5, 6],
  "wind_dir": "逃げ風 | 向かい風 | 横風 | 無風",
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
```

## フィールド定義

| フィールド | 説明 | 型 | 必須 |
|-----------|------|-----|------|
| venue | 会場名（7会場のいずれか） | string | ✅ |
| race_no | レース番号（1～12） | int | ✅ |
| entry_order | 各枠番の艇番（1C, 2C, ..., 6C） | array | ✅ |
| wind_dir | 風向 | string | ✅ |
| wind_speed | 風速（m/s） | float | ✅ |
| wave_cm | 波高（cm） | float | ✅ |
| condition | 天候 | string | ✅ |
| boats | 6艇の詳細情報 | array | ✅ |
| frame | 枠番（1～6） | int | ✅ |
| name | 選手名 | string | ✅ |
| grade | 級別（A1, A2, B1, B2, 不明） | string | ✅ |
| win_rate | 全国勝率 | float | ✅ |
| nat_2 | 全国2連率（%） | float | ✅ |
| local_rate | 当地勝率 | float | ✅ |
| motor_2 | モーター2連率（%） | float | ✅ |
| boat_2 | ボート2連率（%） | float | ✅ |
| exh_st | 展示ST | float | ✅ |
| exh_time | 展示タイム | float | ✅ |
| series_st_avg | 今節ST平均 | float | ✅ |
| series_st_n | 今節レース数 | int | ✅ |
| has_f_this_series | 今節F有無 | bool | ✅ |
| f_val | F値（ある場合） | float/null | - |
| is_l | L艇フラグ | bool | ✅ |
| exh_red_st | 展示赤ST | bool | ✅ |
| is_female | 女子艇フラグ | bool | ✅ |
