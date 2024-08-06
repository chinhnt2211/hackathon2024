# Các bước thực hiện
- Xác định các chức năng cần thiết kế
- Xác định các bước thực hiện
- Xác định các đối tượng tham gia 
- Vẽ diagram

# Xác định các chức năng cần thiết kế
Chức năng: Migrate database psql on-prem của khách hàng về psql database service

# Xác định các bước thực hiện
- Khi khách hàng nhấn vào tab Migration, gọi APIGetDetailMigrate để xem status migrate
  - Nếu Status là processing, hiển thị giao diện đang processing 
  - Nếu Status là Yes, hiển thị thông tin khách hàng đã migrate 
  - Nếu Status là No, hiển thị form cho khách hàng migrate 
    - Người dùng nhập các thông tin của database on-prem vào form 
    - Người dùng nhấn nút test connection
    - Form thông tin gửi request đến APITestConnection, APITestConnection sẽ check kết nối, và kiểm tra xem database service hiện tại có dữ liệu hay không
      - Nếu check thành công, gửi lại thông báo cho khách hàng, enable button 'Migrate'
      - Nếu check thất bại, gửi lại thông báo cho khách hàng 
    - Sau khi khách hàng check thành công, khách hàng nhấn vào 'Migrate', gửi request migrate đến APICallAWX
    - APICallAwx gửi request tạo workflow và AWX, sửa trường status migrate thành processing
      - AWX trả ra workflow id nếu thành công, APICallAwx lưu workflow_id, thông tin trong form vào trong 1 db để phục vụ việc kiểm tra trạng thái 
      - Nếu thất bại, trả về cho frontend, frontend hiển thị thông báo lỗi cho người dùng
    - Backend crontab chạy 1 phút 1 lần, kiểm tra xem workflow_id của các cluster_id có status migrate là processing xem nó chạy xong chưa, nếu chạy xong rồi thì cập nhật vào DB 
    - Frontend gọi APIGetDetailMigrate để xem status migrate thành công hay chưa, nếu thành công rồi, thông báo cho khách hàng 
# Xác định các đối tượng tham gia
- User: Người dùng dịch vụ
- Frontend: Nơi người dùng thao tác
- APITestConnection: API check kết nối và kiểm tra db engine hiện tại có trống dữ liệu hay không
- APICallAWX: API được gọi khi khách hàng nhấn migration, gọi vào awx để thực hiện
- DB: Lưu cluster id, trạng thái migrate, workflow_id, host, port, user, pass (Nếu đang process)
- Backend crontab: Chạy 1 phút 1 lần kiểm tra workflow_id xem chạy xong chưa, nếu xong rồi thì cập nhật vào db
- APIGetDetailMigrate: API truy vấn status migration của cluster_id

<!-- 
# Vẽ diagram
... -->
