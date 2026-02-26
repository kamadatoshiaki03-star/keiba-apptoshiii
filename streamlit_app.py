import streamlit as st
import pandas as pd

# ページ設定
st.set_page_config(page_title="プロ競馬予想システム", layout="wide")

# --- データベース (頂いた全数値を反映) ---
data_db = {
    "Ａ": {"win":"7/17","uren5":"11/17","fuku":"15/23","abc_w":"9/17(3)","pop":[15,16,5,11,5,5,3,5,0,1,0,0,0],"idx":["8/20","13","3","4"]},
    "Ｂ": {"win":"3/6","uren5":"5/6","fuku":"4/8","abc_w":"2/6","pop":[6,2,4,2,3,1,3,1,0,0,0,0,0],"idx":["6/8","5","1","2"]},
    "Ｃ": {"win":"6/9","uren5":"6/9","fuku":"8/10","abc_w":"7/9(1)","pop":[9,6,5,3,1,1,1,1,1,1,0,0,0],"idx":["2/5","2","2","3"]},
    "ＡＢ": {"win":"9/13","uren5":"12/13","fuku":"14/17","abc_w":"10/13(1)","pop":[13,13,7,5,3,4,0,1,1,2,0,0,0],"idx":["13/14","6","2","2"]},
    "ＡＣ": {"win":"4/13","uren5":"2/5","fuku":"5/8","abc_w":"2/5","pop":[6,4,3,2,3,2,1,0,2,0,0,0,0],"idx":["12/8","0","0","2"]},
    "ＢＣ": {"win":"1/3","uren5":"2/3","fuku":"4/5","abc_w":"2/3","pop":[5,3,2,0,2,0,1,0,2,0,0,0,0],"idx":["4/5","2","2","3"]},
    "ＡＢＣ": {"win":"64/86","uren5":"56/86","fuku":"47/86","abc_w":"5476人気(98)","pop":[0]*13,"idx":["3/8","4","4","1"]},
    "ノーマーク": {"win":"10/27","uren5":"12/27","fuku":"7/27","abc_w":"3/8","pop":[6,6,4,2,1,2,2,0,3,1,0,0,0],"idx":["4/8","2","2","1"]}
}

st.title("🏇 独自ロジック・全項目入力予想システム")

# 1. タイトル
st.text_input("レース名（例：中山11R）", "中山◯レース")

# 2. パターン選択
st.subheader("🏁 パターン選択")
target = st.radio("該当するパターンを選んでください", list(data_db.keys()), horizontal=True)
d = data_db[target]

# 3. 馬番入力 (A B C)
st.subheader("🐴 軸馬入力")
c_abc = st.columns(3)
c_abc[0].text_input("Ａ馬(番)", key="a_n")
c_abc[1].text_input("Ｂ馬(番)", key="b_n")
c_abc[2].text_input("Ｃ馬(番)", key="c_n")

# 4. 独自指数
st.subheader("🎯 独自指数 (タイ含む)")
c_idx = st.columns(4)
for i in range(4):
    c_idx[i].text_input(f"{i+1}位 (的中:{d['idx'][i]})", key=f"idx_{i}")

# 5. 特殊カテゴリ
st.subheader("📋 特殊カテゴリ")
c_spec = st.columns(3)
c_spec[0].text_input("Ｐ馬", key="p_m")
c_spec[1].text_input("Ｔ馬", key="t_m")
c_spec[2].text_input("ＰＴ馬", key="pt_m")
c_up = st.columns(2)
c_up[0].text_input("昇級馬", key="up_m")
c_up[1].text_input("調教", key="tr_m")

# 6. 人気別入力 (1〜10 + 追加3)
st.subheader("📊 人気順の馬番入力")
st.write("※馬番を入れると、その人気が過去に的中した回数が分かります。")
pop_inputs = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, "追加1", "追加2", "追加3"]
col1, col2 = st.columns(2)

for idx, p in enumerate(pop_inputs):
    hits = d["pop"][idx] if idx < len(d["pop"]) else 0
    label = f"{p}番人気 (過去的中:{hits}回)" if isinstance(p, int) else f"{p} (10番人気以下)"
    target_col = col1 if idx % 2 == 0 else col2
    target_col.text_input(label, key=f"pop_{idx}")

st.divider()

# --- 結果のサマリー ---
st.header("📈 このパターンの基本的中率")
def pct(frac):
    try:
        f = frac.split('(')[0]
        if '/' not in f: return f
        n, den = map(int, f.split('/'))
        return f"{(n/den)*100:.1f}%"
    except: return "---"

res_c = st.columns(4)
res_c[0].metric("1着確率", pct(d["win"]), d["win"])
res_c[1].metric("馬連5内", pct(d["uren5"]), d["uren5"])
res_c[2].metric("複勝率", pct(d["fuku"]), d["fuku"])
res_c[3].metric("ABCワイド", pct(d["abc_w"]), d["abc_w"])
