import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from datetime import datetime, timedelta
from scipy import stats
import matplotlib

sns.set(font_scale=2)


# Google Fontsの読み込み
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');
    body {
        font-family: 'Roboto', sans-serif;
    }
    </style>
""", unsafe_allow_html=True)

password = st.text_input("パスワード", type="password")
 
if password == st.secrets["password"]:
    st.success("アクセスが許可されました。")
else:
    st.error("アクセスが拒否されました。")

###サイドバー###

# サイドバーでの日付選択
st.sidebar.subheader("施策詳細")

# サイドバーでの評価指標入力
evaluation_metrix = st.sidebar.text_area("評価指標（CVRになる指標を想定しています。）", placeholder="入力できます", height=5)

# 2つのカラムを作成
col1, col2 = st.sidebar.columns(2)

# 1つ目のカラムに開始日を配置
with col1:
    start_date = st.date_input("テスト開始日", value=datetime.today() - timedelta(days=7))

# 2つ目のカラムに終了日を配置
with col2:
    end_date = st.date_input("テスト終了日", value=datetime.today())

# サイドバーでの評価指標入力
url_link = st.sidebar.text_area("関連URL（必要であれば）", placeholder="URLを記載してください", height=5)

st.sidebar.markdown("-----------------")  # ここで横線を追加

st.sidebar.subheader('取得データを入力して下さい。')
col3, col4 = st.sidebar.columns(2)
with col3:
    visitors_a = st.number_input('Aの訪問者数', value=1000)
with col4:
    conversion_a = st.number_input('AのCV数', value=50)
cvr_a = conversion_a / visitors_a
st.sidebar.markdown(f'AのCVR :  **{"{:.1%}".format(cvr_a)}**')

col5, col6 = st.sidebar.columns(2)
with col5:
    visitors_b = st.number_input('Bの訪問者数', value=1000)
with col6:
    conversion_b = st.number_input('BのCV数', value=50)
cvr_b = conversion_b / visitors_b
st.sidebar.markdown(f'BのCVR :  **{"{:.1%}".format(cvr_b)}**')



###メインコンテンツ###

##タイトル##
st.header('A/Bテストツール')

#タイトルメッセージ
st.markdown('A/Bテスト結果の訪問者数とCV数を入力することで、一般的なA/BテストおよびベイジアンA/Bテストによる信頼性を判定できます。また、そのままpdf化して結果報告に使うことも可能です。')

## 施策内容 ##
st.markdown("<h4>■施策について</h4>", unsafe_allow_html=True)
policy_content = st.text_area("〇施策内容", placeholder="入力できます", height=5)

st.write("〇評価指標")
st.markdown(f'<span style="font-weight: bold;"><u>{evaluation_metrix}</u></span>', unsafe_allow_html=True)


##テスト日数##
st.write("〇テスト期間")
if end_date >= start_date:
    days_difference = (end_date - start_date).days
    st.markdown(f'<span style="font-weight: bold;"><u>{start_date} ➡ {end_date}（{days_difference} days）</u></span>', unsafe_allow_html=True)
else:
    st.markdown('<span style="font-weight: bold;"><u>終了日は開始日より後の日付を選択してください。</u></span>', unsafe_allow_html=True)

st.write("〇施策関連URL（必要であれば）")
st.markdown(f'<span style="font-weight: bold;"><u>{url_link}</u></span>', unsafe_allow_html=True)


st.markdown("-----------------")  # ここで横線を追加


##通常ABテストセクション##
st.markdown("<h4>■通常のA/Bテスト（統計的仮説検定）</h4>", unsafe_allow_html=True)
st.markdown("通常のA/Bテストの結果です。カイ二乗検定を使用しています。（両側検定）")


# テーブルのスタイルを調整
st.markdown(rf'''
    <style>
    table {{
        width: 100%;
        border-collapse: collapse;
        table-layout: fixed;
    }}
    th, td {{
        padding: 10px;
        text-align: center;
        border: 1px solid black;
        font-size: 18px;
    }}
    th:nth-child(1), td:nth-child(1) {{
        width: 19%;
    }}
    th:nth-child(2), td:nth-child(2),
    th:nth-child(3), td:nth-child(3),
    th:nth-child(4), td:nth-child(4) {{
        width: 19%;
    }}
    th:nth-child(5){{
        width: 19%;
        font-size:15px
    }}

    td:nth-child(5) {{
        width: 24%;
    }}
    </style>

    <table>
      <tr>
        <th>対象</th><th>訪問者数</th><th>CV数</th><th>CVR</th><th>CVR改善率（B/A）</th>
      </tr>
      <tr>
        <td>A</td><td>{visitors_a}</td><td>{conversion_a}</td><td>{"{:.1%}".format(cvr_a)}</td><td rowspan="2" colspan="1">{"{:.1%}".format(cvr_b / cvr_a)}</td>
      </tr>
      <tr>
        <td>B</td><td>{visitors_b}</td><td>{conversion_b}</td><td>{"{:.1%}".format(cvr_b)}</td>
      </tr>
    </table>
    ''', unsafe_allow_html=True)


st.markdown("<h5>◇結果</h5>", unsafe_allow_html=True)

#t検定（今回は未使用）
a = np.zeros(visitors_a)
a[:conversion_a] = 1
b = np.zeros(visitors_b)  # 修正：変数名をvisitors_bに変更
b[:conversion_b] = 1      # 修正：変数名をconversion_bに変更
res = stats.ttest_ind(a, b, equal_var=False)


##カイ二乗セクション##
#カイ2乗検定用のデータ
non_conversion_a = visitors_a - conversion_a
non_conversion_b = visitors_b - conversion_b

# 観測データ
observed = np.array([[conversion_a, non_conversion_a],
                     [conversion_b, non_conversion_b]])
# カイ二乗適合度検定
chi2, p_value, dof, expected = stats.chi2_contingency(observed, correction=False)


# p値によって出力を変更
if p_value <= 0.05:
    st.markdown(f'''
    <p style="text-align: center; font-size: 24px; color:#0F7AD3; font-weight: bold;">95%の信頼度で有意差あり (P値={p_value:.2f})</p>
    ''', unsafe_allow_html=True)
elif p_value <= 0.1:
    st.markdown(f'''
    <p style="text-align: center; font-size: 24px; color: #27B1FF; font-weight: bold;">90%の信頼度で有意差あり (P値={p_value:.2f})</p>
    ''', unsafe_allow_html=True)
else:
    st.markdown(f'''
    <p style="text-align: center; font-size: 24px; font-weight: bold;">有意差なし (P値={p_value:.2f})</p>
    ''', unsafe_allow_html=True)


st.markdown("-----------------")  # ここで横線を追加

## ベイジアンA/Bテストセクション##
st.markdown("<h4>■ベイジアンA/Bテスト</h4>", unsafe_allow_html=True)
st.markdown("ベイジアンA/Bテストを用いて、AとBの各コンバージョン率（CVR）に対する事後分布を算出し、どちらの施策がより効果的かを評価しています。")
st.markdown("ここでは各施策のCVRは数学的にベータ分布に従うと仮定しているため、得られた事後分布に基づき、乱数を生成（サンプリング）しました。このサンプリングした乱数同士で比較を行い、BのCVRがAを上回る確率を計算しています。")

# 事前分布のパラメータのα、βを指定
alpha_prior = 1
beta_prior = 1
# 事後分布の算出
posterior_A = stats.beta(alpha_prior + conversion_a, beta_prior + visitors_a - conversion_a)
posterior_B = stats.beta(alpha_prior + conversion_b, beta_prior + visitors_b - conversion_b)
# サンプリング数
samples = 20000
samples_posterior_A = posterior_A.rvs(samples)
samples_posterior_B = posterior_B.rvs(samples)
# A<Bとなる確率算出
prob = (samples_posterior_A < samples_posterior_B).mean()

# グラフ設定
fig = plt.figure(figsize=(20,10))
ax = fig.add_subplot(111)
sns.histplot(samples_posterior_A, ax=ax, kde=True, label='AのCVR')
sns.histplot(samples_posterior_B, ax=ax, kde=True, label='BのCVR')
ax.set_ylabel('密', fontsize='x-large')  
ax.set_xlabel('CVR', fontsize='x-large')
ax.set_title('CVRの分布', fontsize='x-large')  
ax.legend(loc='upper right', fontsize='x-large')
fig.tight_layout()

# 可視化
st.markdown("<h5>◇CVRの事後分布（A vs B）</h5>", unsafe_allow_html=True)

st.pyplot(fig)

# probの値に基づいて色を決定
if prob <= 0.3:
    color = "red"
    font_size = "28px"
elif 0.3 < prob <= 0.7:
    color = None
    font_size = "28px"
elif 0.7 < prob <= 0.85:
    color = "#27B1FF"  # 薄い青
    font_size = "28px"
else:
    color = "#0F7AD3"  # 濃い青
    font_size = "28px"

st.markdown(fr'''
  <p style="text-align: center; font-size: 20px;">Aの方がCVRが高い確率は <span style="color: {color}; font-size: {font_size}; font-weight: bold;">{"{:.1%}".format(prob)}</span></p>
  ''', unsafe_allow_html=True)
