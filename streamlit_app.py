. 期待値サマリー
st.header("📈 この条件の期待値まとめ")
col_res1, col_res2 = st.columns(2)
with col_res1:
    st.write(f"軸馬どちらか1着：**{d.get('axis_win')}**")
    st.write(f"推奨人気実績：**{d.get('rec_hit')}**")
with col_res2:
    st.write(f"ＡＢＣワイド：**{d.get('abc_wide')}**")
    st.write(f"Ａで1番人気時：**{d.get('a_fav1')}**")
