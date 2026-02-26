import streamlit as st

st.set_page_config(page_title="プロ競馬分析・真の完成版", layout="wide")
st.title("🏇 独自ロジック・全自動的中実績 照合システム")

# --- あなたの「宝のデータ」を1ミリも漏らさず反映した最終データベース ---
db = {
    "ＡＢ": {
        "③": {
            "fa": "14/17", "fb": "11/17", "fc": "7/17",
            "idx": ["13/14", "6/14", "2/14", "2/14"], # 指数1位実績(13/14)
            "pop": {1: "13/17", 2: "13/17", 3: "7/17", 4: "5/17", 5: "3/17", 6: "4/17", 7: "0/17", 8: "1/17", 9: "1/17", 10: "2/17"},
            "pt_p": "21/27", "pt_t": "18/23", "pt_pt": "13/14",
            "axis_win": "9/13", # 軸馬どちらか1着
            "rec_hit": "10/17", "rec_pop": [4, 5, 6, 3], # 推奨4563実績
            "abc_wide": "10/13", # ABCワイド実績
            "a_fav1": "9-3-0-3"  # Ａで1番人気時の実績
        }
    },
    "Ａ": {
        "③": {"fa":"15/23","fb":"12/23","fc":"11/23","idx":["8/20","13/20","3/20","4/20"],"pop":{1:"15/23", 2:"16/23", 3:"5/23", 4:"11/23"},"a_fav1":"4-8-3-6","rec_hit":"---","axis_win":"7/17","abc_wide":"---"}
    }
}

# --- 1. 条件入力 ---
st.subheader("🏁 1. 条件と各馬の番号を入力")
c1, c2 = st.columns(2)
target = c1.selectbox("パターン", ["ＡＢ", "Ａ", "Ｂ", "Ｃ", "ＡＣ", "ＢＣ", "ＡＢＣ", "ノーマーク"])
lv = c2.radio("レベル", ["③", "④", "⑤"], horizontal=True)
d = db.get(target, {}).get(lv, db["ＡＢ"]["③"])

st.write("---")
# A B C馬番
ca, cb, cc = st.columns(3)
a_m = ca.text_input(f"Ａ馬(番) [実績:{d.get('fa')}]", key="a_n")
b_m = cb.text_input(f"Ｂ馬(番) [実績:{d.get('fb')}]", key="b_n")
c_m = cc.text_input(f"Ｃ馬(番) [実績:{d.get('fc')}]", key="c_n")

# 指数馬番
st.write("**独自指数ランキング (馬番)**")
ci1, ci2, ci3, ci4 = st.columns(4)
i_m = [ci1.text_input(f"1位実績: {d['idx'][0]}", key="i1"), ci2.text_input(f"2位実績: {d['idx'][1]}", key="i2"), 
       ci3.text_input(f"3位実績: {d['idx'][2]}", key="i3"), ci4.text_input(f"4位実績: {d['idx'][3]}", key="i4")]

# 特殊馬
st.write("**特殊馬 (馬番)**")
cp, ct, cpt, cup, ctr = st.columns(5)
p_m = cp.text_input(f"Ｐ [{d.get('pt_p','-')}]", key="p_m")
t_m = ct.text_input(f"Ｔ", key="t_m")
pt_m = cpt.text_input(f"ＰＴ [{d.get('pt_pt','-')}]", key="pt_m")
up_m = cup.text_input("昇級", key="up_m")
tr_m = ctr.text_input("調教", key="tr_m")

st.divider()

# 人気順
st.subheader("📊 2. 人気順に馬番を入力")
pop_m = {}
col_p1, col_p2 = st.columns(2)
for i in range(1, 11):
    target_col = col_p1 if i <= 5 else col_p2
    hits = d["pop"].get(i, "0")
    pop_m[str(i)] = target_col.text_input(f"{i}番人気 [実績:{hits}] の馬番", key=f"p{i}")

st.divider()

# --- 判定セクション（ここが今回の答えです！） ---
st.header("🎯 今回の的中期待値 判定結果")

entered_horses = set([a_m, b_m, c_m, pt_m] + i_m + [x.strip() for x in p_m.split(',') if x.strip()])
num_to_rank = {v: k for k, v in pop_m.items() if v and v.strip()}

if not any(entered_horses):
    st.write("馬番を入力すると、最強の的中根拠が自動で表示されます。")
else:
    # 軸馬1着、推奨人気、ABCワイドの全体実績を表示
    if a_m or b_m: st.warning(f"💡 **軸馬どちらか1着実績：{d.get('axis_win')}**")
    if any(num_to_rank.get(h) and int(num_to_rank[h]) in [4,5,6,3] for h in entered_horses):
        st.warning(f"💡 **推奨人気(4563)的中実績：{d.get('rec_hit')}**")
    if a_m and b_m and c_m: st.warning(f"💡 **ＡＢＣワイド的中実績：{d.get('abc_wide')}**")

    st.write("---")
    # 1頭ごとの詳細
    for h in sorted(list(entered_horses)):
        if not h: continue
        facts = []
        rank = num_to_rank.get(h)
        if h == a_m and rank == "1": facts.append(f"🔥Ａで1番人気 (実績:{d.get('a_fav1')})")
        if h == a_m and rank != "1": facts.append(f"Ａ馬 (実績:{d['fa']})")
        if h == b_m: facts.append(f"Ｂ馬 (実績:{d['fb']})")
        if rank: facts.append(f"{rank}番人気 (実績:{d['pop'].get(int(rank), '0')})")
        for idx, val in enumerate(i_m):
            if h == val: facts.append(f"独自指数{idx+1}位 (実績:{d['idx'][idx]})")
        if p_m and h in [x.strip() for x in p_m.split(',')]: facts.append(f"Ｐ馬 (実績:{d.get('pt_p','-')})")
        if pt_m and h == pt_m: facts.append(f"ＰＴ馬 (実績:{d.get('pt_pt','-')})")

        if facts: st.success(f"✅ **馬番 {h}** の根拠: " + " ／ ".join(facts))
