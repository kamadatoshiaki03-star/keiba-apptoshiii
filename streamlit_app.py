b_m and c_m: st.warning(f"💡 **ＡＢＣワイド的中実績：{d.get('abc_wide')}**")

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
