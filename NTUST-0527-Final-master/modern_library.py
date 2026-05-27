import json
import os
from typing import Dict, List, Optional

class LibraryManager:
    """圖書館管理系統 - 負責書籍資料的操作"""
    
    def __init__(self, data_file: str = "books.json"):
        self.data_file = data_file
        self.books: Dict[str, Dict] = {}  # 使用 ISBN 作為 key 實現 O(1) 查詢
        self._load_books()
    
    def _load_books(self) -> None:
        """從 JSON 檔案載入書籍資料"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, "r", encoding="utf-8") as file:
                    books_list = json.load(file)
                    # 轉換為字典以實現快速查詢
                    for book in books_list:
                        self.books[book["isbn"]] = book
        except json.JSONDecodeError:
            print(f"警告：{self.data_file} 格式錯誤，已清空")
        except Exception as e:
            print(f"警告：載入檔案失敗 - {e}")
    
    def _save_books(self) -> None:
        """將書籍資料保存到 JSON 檔案"""
        try:
            books_list = list(self.books.values())
            with open(self.data_file, "w", encoding="utf-8") as file:
                json.dump(books_list, file, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"錯誤：保存檔案失敗 - {e}")
    
    def add_book(self, title: str, isbn: str, status: str) -> bool:
        """新增書籍"""
        # 資料驗證
        if not self._validate_input(title, isbn, status):
            return False
        
        if self._book_exists(isbn):
            print("ISBN Exist")
            return False
        
        self.books[isbn] = {
            "title": title,
            "isbn": isbn,
            "status": status
        }
        self._save_books()
        print("Success")
        return True
    
    def borrow_book(self, isbn: str) -> bool:
        """借書"""
        if not self._book_exists(isbn):
            print("Book Not Found")
            return False
        
        self.books[isbn]["status"] = "borrowed"
        self._save_books()
        print("Updated")
        return True
    
    def return_book(self, isbn: str) -> bool:
        """還書"""
        if not self._book_exists(isbn):
            print("Book Not Found")
            return False
        
        self.books[isbn]["status"] = "available"
        self._save_books()
        print("Updated")
        return True
    
    def show_all_books(self) -> None:
        """顯示所有書籍"""
        if not self.books:
            print("書籍清單為空")
            return
        
        for book in self.books.values():
            print(f"書名: {book['title']}, ISBN: {book['isbn']}, 狀態: {book['status']}")
    
    def get_statistics(self) -> Dict[str, int]:
        """取得書籍分類統計"""
        total = len(self.books)
        available = sum(1 for book in self.books.values() if book["status"] == "available")
        borrowed = sum(1 for book in self.books.values() if book["status"] == "borrowed")
        
        return {
            "total": total,
            "available": available,
            "borrowed": borrowed
        }
    
    def _book_exists(self, isbn: str) -> bool:
        """檢查書籍是否存在 (O(1) 查詢)"""
        return isbn in self.books
    
    def _validate_input(self, title: str, isbn: str, status: str) -> bool:
        """驗證輸入資料"""
        if not title or not title.strip():
            print("Format Error")
            return False
        
        if not isbn or not isbn.strip():
            print("Format Error")
            return False
        
        valid_statuses = ["available", "borrowed"]
        if status not in valid_statuses:
            print("Format Error")
            return False
        
        return True


class LibraryUI:
    """圖書館系統的使用者介面"""
    
    def __init__(self, library: LibraryManager):
        self.library = library
        self.commands = {
            "add": self._handle_add,
            "show": self._handle_show,
            "borrow": self._handle_borrow,
            "return": self._handle_return,
            "exit": self._handle_exit,
        }
    
    def run(self) -> None:
        """執行互動式命令迴圈"""
        print("=== 圖書管理系統 v1.0 (Modern) ===")
        print("命令：add <書名>/<ISBN>/<狀態> | show | borrow <ISBN> | return <ISBN> | exit")
        
        while True:
            try:
                user_input = input("> ").strip()
                
                if not user_input:
                    continue
                
                command = user_input.split()[0]
                
                if command in self.commands:
                    if command == "exit":
                        self.commands[command]()
                        break
                    else:
                        self.commands[command](user_input)
                else:
                    print("Unknown Command")
            
            except KeyboardInterrupt:
                print("\n程式已中斷，資料已自動保存")
                break
            except Exception as e:
                print(f"錯誤：{e}")
    
    def _handle_add(self, user_input: str) -> None:
        """處理 add 命令"""
        if not user_input.startswith("add "):
            print("Format Error")
            return
        
        parts = user_input[4:].split("/")
        
        if len(parts) != 3:
            print("Format Error")
            return
        
        title, isbn, status = parts[0].strip(), parts[1].strip(), parts[2].strip()
        self.library.add_book(title, isbn, status)
    
    def _handle_show(self, user_input: str = None) -> None:
        """處理 show 命令"""
        self.library.show_all_books()
    
    def _handle_borrow(self, user_input: str) -> None:
        """處理 borrow 命令"""
        if not user_input.startswith("borrow "):
            print("Format Error")
            return
        
        isbn = user_input[7:].strip()
        self.library.borrow_book(isbn)
    
    def _handle_return(self, user_input: str) -> None:
        """處理 return 命令"""
        if not user_input.startswith("return "):
            print("Format Error")
            return
        
        isbn = user_input[7:].strip()
        self.library.return_book(isbn)
    
    def _handle_exit(self) -> None:
        """處理 exit 命令"""
        stats = self.library.get_statistics()
        print("\n" + "="*40)
        print("         📊 系統統計摘要")
        print("="*40)
        print(f"  📚 總書籍數:      {stats['total']:>3} 本")
        print(f"  ✅ 可用書籍:      {stats['available']:>3} 本")
        print(f"  📖 已借出書籍:    {stats['borrowed']:>3} 本")
        if stats['total'] > 0:
            available_rate = (stats['available'] / stats['total']) * 100
            print(f"  📈 可用率:        {available_rate:>6.1f}%")
        print("="*40)
        print("\n👋 感謝使用圖書館管理系統，再見！\n")


def main():
    """主程式入口"""
    library = LibraryManager("books.json")
    ui = LibraryUI(library)
    ui.run()


if __name__ == "__main__":
    main()
