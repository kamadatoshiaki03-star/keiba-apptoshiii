import streamlit as st
import pandas as pd
import random

# アプリのタイトル
st.title("🏇 競馬予想・配当計算アプリ")

st.write("馬の情報やオッズを入力して、的中時の払戻金や簡易的な予想シミュレーションができます。")

# サイドバーに入力欄を作成
st.sidebar.header("馬の情報入力")
horse_name = st.sidebar.text_input("馬の名前", "ゴールドシップ")
odds = st.sidebar.number_input("単勝オッズ", min_value=1.0, value=5.0, step=0.1)
bet_amount = st.sidebar.number_input("賭け金 (円)", min_value=100, value=1000, step=100)

# 計算処理
payout = odds * bet_amount
win_prob = (1 / odds) * 100

st.divider()

# メイン画面に結果を表示
col1, col2 = st.columns(2)
with col1:
    st.metric(label="的中時の払戻金", value=f"{int(payout):,} 円")
with col2:
    st.metric(label="計算上の期待勝率", value=f"{win_prob:.1f} %")

# ボタンを押すとランダムに結果を出す「お遊び予想」機能
if st.button("AI予想シミュレーションを実行"):
    st.write(f"「{horse_name}」のレース結果をシミュレーション中...")
    
    results = ["1着", "2着", "3着", "着外"]
    # オッズに基づいてなんとなく確率を変える
    prediction = random.choices(results, weights=[win_prob, 15, 15, 70])[0]
    
    if prediction == "1着":
        st.balloons()
        st.success(f"結果：{horse_name} は見事 **{prediction}** でした！おめでとうございます！")
    else:
        st.info(f"結果：{horse_name} は **{prediction}** でした。")

st.subheader("📋 競馬メモ")
st.text_area("気になる馬やパドックの様子をメモしてください", "例：今日は馬場状態が良い。")