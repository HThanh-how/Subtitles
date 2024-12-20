import os
import subprocess
from datetime import datetime
import schedule
import time

def is_large_file(file_path, max_size_mb=1):
    """Kiểm tra xem file có lớn hơn giới hạn không."""
    max_size_bytes = max_size_mb * 1024 * 1024  # Convert MB to bytes
    return os.path.getsize(file_path) > max_size_bytes

def auto_git_commit():
    """Tự động commit và push code lên GitHub."""
    try:
        # Kiểm tra trạng thái git
        status = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if 'nothing to commit' in status.stdout:
            print("Không có thay đổi để commit")
            return False

        # Lấy danh sách file thay đổi
        changed_files = subprocess.run(['git', 'diff', '--name-only'], 
                                     capture_output=True, text=True).stdout.splitlines()
        
        # Kiểm tra và bỏ qua các file lớn
        for file in changed_files:
            if os.path.exists(file) and is_large_file(file):
                print(f"Bỏ qua file lớn: {file}")
                subprocess.run(['git', 'reset', file])

        # Lấy thời gian hiện tại
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Add các file còn lại
        subprocess.run(['git', 'add', '.'])
        
        # Kiểm tra xem còn gì để commit không
        status = subprocess.run(['git', 'status'], capture_output=True, text=True)
        if 'nothing to commit' in status.stdout:
            print("Không có file nào dưới 1MB để commit")
            return False
        
        # Commit và push
        commit_message = f"Auto commit at {current_time}"
        subprocess.run(['git', 'commit', '-m', commit_message])
        subprocess.run(['git', 'push'])
        
        print(f"Đã commit và push thành công lúc: {current_time}")
        return True
        
    except Exception as e:
        print(f"Lỗi khi commit code: {e}")
        return False

def main():
    # Lên lịch commit vào 23:59 mỗi ngày
    schedule.every().day.at("23:59").do(auto_git_commit)
    
    print("Đã bắt đầu lên lịch tự động commit...")
    print("Script sẽ tự động commit mỗi ngày lúc 23:59")
    print("Nhấn Ctrl+C để dừng")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Kiểm tra mỗi phút
    except KeyboardInterrupt:
        print("\nĐã dừng tự động commit")

if __name__ == "__main__":
    main() 