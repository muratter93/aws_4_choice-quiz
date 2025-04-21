# AWS 4択クイズアプリ（Django製）

AWS認定クラウドプラクティショナー（CLF）試験対策用の  
4択形式のクイズ学習Webアプリです。  
Djangoで開発されており、ローカル環境で手軽に動作します。

---

## このアプリでできること

- AWSに関する4択クイズの出題と解答
- 問題ごとの正誤判定とスコア表示
- Django管理画面から問題の追加・編集・削除が可能
- Bootstrapベースの軽量なUI

---

## 📸 画面イメージ

![クイズ及び正解画面](aws4.png)

---

## 使用技術

- Python 3.x
- Django 5.1.2
- SQLite3
- HTML / CSS（Bootstrap）
- Pillow（画像表示用）

---

## 🚀 セットアップ手順

1. このリポジトリをクローン：
git clone https://github.com/muratter93/aws_4_choice-quiz.git
cd aws_4_choice-quiz

仮想環境を作成・起動（Windows例）：
python -m venv venv
venv\Scripts\activate
Mac/Linux の場合： source venv/bin/activate

依存パッケージをインストール：
pip install -r requirements.txt

マイグレーションと起動：
python manage.py migrate
python manage.py runserver

ブラウザでアクセス：
http://127.0.0.1:8000/

管理画面（/admin）を使うには
python manage.py createsuperuser
→ 任意のユーザー名・メール・パスワードを入力
→ http://127.0.0.1:8000/admin/ にアクセス！


📝 ライセンス
MIT License

👤 作者
muratter93

GitHub: https://github.com/muratter93
