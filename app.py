import streamlit as st
import random

st.set_page_config(layout="wide")

if "history" not in st.session_state:
    st.session_state.history = []

st.title("ロト６ クイックピックジェネレーター")

mode = st.radio(
    "抽選方法を選択してください",
    ["完全ランダム", "連番1組＋1の位一致1組"]
)
count = st.radio(
    "生成する口数を選択してください",
    [1, 5],
    format_func=lambda x: f"{x}口",
    horizontal=True
)

if st.button("🎲 数字を生成する"):

    results = []

    for _ in range(count):

        if mode == "完全ランダム":
            numbers = random.sample(range(1, 44), 6)
            numbers.sort()

        else:
            while True:
                numbers = random.sample(range(1, 44), 6)
                numbers.sort()

                consecutive = 0

                for i in range(5):
                    if numbers[i + 1] - numbers[i] == 1:
                        consecutive += 1

                same_digit = 0

                for i in range(6):
                    for j in range(i + 1, 6):
                        if numbers[i] % 10 == numbers[j] % 10:
                            same_digit += 1

                if consecutive == 1 and same_digit == 1:
                    break

        results.append(numbers.copy())
        st.session_state.history.append(numbers.copy())

    st.success("🎉 抽選完了！")
    st.subheader("抽選結果：")

    for result in results:
        cols = st.columns(6)

        for i, number in enumerate(result):
            with cols[i]:
                st.markdown(
                    f"""
                    <div style="
                        background-color: #E95D35;
                        color: white;
                        border-radius: 50%;
                        width: 65px;
                        height: 65px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 24px;
                        font-weight: bold;
                    ">
                        {number:02d}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

st.divider()

st.subheader("📜 抽選履歴")

for i, result in enumerate(reversed(st.session_state.history), 1):

    text = "・".join(f"{n:02d}" for n in result)

    st.write(f"{len(st.session_state.history) - i + 1}回目：{text}")

if st.button("🗑️ 履歴を消去"):

    st.session_state.history = []

    st.rerun()