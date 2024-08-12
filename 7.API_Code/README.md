# DOC API
Đây là nơi list ra các thông tin cần thiết để viết API

## Chức năng API

- APICallAWX: API được gọi khi khách hàng nhấn migration, gọi vào awx để thực hiện
- APIGetDetailMigrate: API truy vấn status migration của cluster_id, gọi vào DB status(Được dựng) và trả ra các thông tin được ghi trong list API yêu cầu 
- APITestConnection: API check kết nối đến db on-prem

## Thông tin DB status 
host: 103.160.75.63
port: 15432
user: admin
pass: Pk32qrNW6LqD
database: DBdefault

# Run
```commandline
cd 7.API_Code
```
```commandline
python3 -m venv venv
```
```commandline
source venv/bin/activate
```
```commandline
pip install -r requirement.txt
```
```commandline
fastapi dev main.py
```
