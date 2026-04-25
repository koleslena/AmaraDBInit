import os
import psycopg2

from dotenv import load_dotenv

load_dotenv()

class PostgresDB:

    def get_connection(self):
        return psycopg2.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"), 
            port=os.getenv("DB_PORT")
        )
    
    def initialize_database(self, sql_file_path):
        """
        Выполняет SQL-скрипт из файла для инициализации базы данных.
        """
        conn = None
        try:
            # Подключаемся к базе, используя параметры из окружения
            conn = self.get_connection()
            
            # Открываем и читаем SQL файл
            if not os.path.exists(sql_file_path):
                print(f"❌ Файл не найден: {sql_file_path}")
                return False

            with open(sql_file_path, 'r', encoding='utf-8') as f:
                sql_script = f.read()

            # Создаем курсор и выполняем скрипт
            with conn.cursor() as cur:
                print(f"⏳ Выполнение скрипта {sql_file_path}...")
                cur.execute(sql_script)
                
            # Фиксируем изменения
            conn.commit()
            print("✅ Инициализация базы данных успешно завершена.")

            return True
        except Exception as e:
            print(f"❌ Ошибка при инициализации базы данных: {e}")
            if conn:
                conn.rollback() # Откатываем изменения в случае ошибки
            
            return False
        finally:
            if conn:
                conn.close()
