# Các bước thực hiện
- Tạo thử 1 con postgres on-prem
- Tạo dữ liệu ở trong con on-prem
- Thử migrate về database của FCI

# Tạo thử psql
- Tạo bằng image ubuntu 20.04, cài đặt theo đường dẫn sau: https://www.atlantic.net/dedicated-server-hosting/how-to-install-and-configure-postgres-14-on-ubuntu/

# Tạo dữ liệu

Truy cập vào psql và tạo dữ liệu

```sql
CREATE DATABASE school_db;
\c school_db

CREATE TABLE student (
  id SERIAL PRIMARY KEY,
  name VARCHAR(100),
  age INTEGER,
  grade VARCHAR(10)
);

INSERT INTO student (name, age, grade) VALUES
('Alice', 14, '9th'),
('Bob', 15, '10th'),
('Charlie', 13, '8th'),
('David', 14, '9th'),
('Eve', 15, '10th'),
('Frank', 13, '8th'),
('Grace', 14, '9th'),
('Hannah', 15, '10th'),
('Ivy', 13, '8th'),
('Jack', 14, '9th');
```

# Thử migrate về

- Tạo 1 con psql 14 trên portal thành công
- Vào user `root`, tạo file `~/.pgpass` có nội dung như sau:
```
103.160.75.63:5432:*:admin:DBMTC@Fci999
```
Với các thông tin ở trên là thông tin của db nguồn

Sau đó sửa phân quyền của .pgpass thành 600
```
sudo chmod 0600 ~/.pgpass
```
- Dump dữ liệu ra file sql bằng câu lệnh:
```
pg_dumpall -h 103.160.75.63 -U admin >/tmp/test.sql
```

- Phục hồi dữ liệu bằng câu lệnh:
```
sudo -iu postgres
psql -f /tmp/test.sql
```
Thì ta đã có thể migrate thành công