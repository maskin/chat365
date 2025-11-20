from database import Base, engine

def main():
    """
    データベースとテーブルを初期化する。
    """
    print("データベースを初期化しています...")
    
    # `database.py`で定義されたすべてのテーブルを作成
    Base.metadata.create_all(bind=engine)
    
    print("データベースの初期化が完了しました。`pai.db`ファイルが作成されました。")

if __name__ == "__main__":
    main()
