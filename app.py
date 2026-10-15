import numpy as np
import pandas as pd
import streamlit as st

# Thiết lập cấu hình trang
st.set_page_config(page_title="Quản lý điểm sinh viên", layout="centered")

# Tiêu đề ứng dụng
st.title("QUẢN LÝ ĐIỂM SINH VIÊN")
st.markdown("---")

# Khởi tạo dữ liệu học sinh
data = {
    "Ho_va_ten": [
        "Nguyen Thai Hoang",
        "Tran Binh",
        "Le Minh Anh",
        "Pham Quoc Dung",
        "Hoang Thu Ha",
        "Vo Thanh Nam",
        "Dang Ngoc Linh",
        "Bui Gia Bao",
        "Do Khanh Vy",
        "Nguyen Duc Minh",
    ],
    "Chuyên cần": [9, 8, 10, 6, 7, 9, 8, 5, 10, 6],
    "Giữa kỳ": [8, 7, 9, 5, 6, 8, 7, 4, 9, 5],
    "Cuối kỳ": [9, 8, 9, 4, 7, 9, 8, 5, 10, 6],
}

df = pd.DataFrame(data)

# Tính điểm tổng kết (20% Chuyên cần + 30% Giữa kỳ + 50% Cuối kỳ)
df["Tổng kết"] = (
    0.2 * df["Chuyên cần"] + 0.3 * df["Giữa kỳ"] + 0.5 * df["Cuối kỳ"]
).round(2)


# Xếp loại sinh viên
def phan_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7.0:
        return "Khá"
    elif diem >= 5.0:
        return "Trung bình"
    else:
        return "Yếu"


df["Xếp loại"] = df["Tổng kết"].apply(phan_loai)

# Đổi tên cột hiển thị cho thân thiện
df_display = df.rename(
    columns={
        "Ho_va_ten": "Họ tên",
        "Chuyên cần": "Chuyên cần",
        "Giữa kỳ": "Giữa kỳ",
        "Cuối kỳ": "Cuối kỳ",
        "Tổng kết": "Tổng kết",
        "Xếp loại": "Xếp loại",
    }
)

# 1. Hiển thị bảng điểm
st.subheader("📋 Bảng điểm chi tiết của sinh viên")
st.dataframe(df_display, use_container_width=True)

# 2. Thống kê chung của lớp
st.markdown("---")
st.subheader("📊 Thống kê chung của lớp")

diem_tb_lop = df["Tổng kết"].mean()
max_score = df["Tổng kết"].max()
min_score = df["Tổng kết"].min()

sv_max = df[df["Tổng kết"] == max_score]
sv_min = df[df["Tổng kết"] == min_score]
so_sv_dat = len(df[df["Tổng kết"] >= 5.0])

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Điểm trung bình của lớp", value=f"{diem_tb_lop:.2f}")
    ten_max = ", ".join(sv_max["Ho_va_ten"].tolist())
    st.metric(
        label="Sinh viên tổng kết cao nhất",
        value=f"{ten_max} ({max_score}đ)",
    )

with col2:
    st.metric(
        label="Số sinh viên đạt (>= 5.0)",
        value=f"{so_sv_dat} / {len(df)}",
    )
    ten_min = ", ".join(sv_min["Ho_va_ten"].tolist())
    st.metric(
        label="Sinh viên tổng kết thấp nhất",
        value=f"{ten_min} ({min_score}đ)",
    )

# 3. Danh sách xổ xuống chọn sinh viên
st.markdown("---")
st.subheader("🔍 Tra cứu thông tin sinh viên")
selected_student = st.selectbox(
    "Chọn sinh viên để xem chi tiết:", df["Ho_va_ten"].tolist()
)

student_info = df[df["Ho_va_ten"] == selected_student].iloc[0]

st.info(f"**Thông tin chi tiết cho sinh viên: {selected_student}**")
col_s1, col_s2, col_s3, col_s4, col_s5 = st.columns(5)
col_s1.metric("Chuyên cần", student_info["Chuyên cần"])
col_s2.metric("Giữa kỳ", student_info["Giữa kỳ"])
col_s3.metric("Cuối kỳ", student_info["Cuối kỳ"])
col_s4.metric("Tổng kết", student_info["Tổng kết"])
col_s5.metric("Xếp loại", student_info["Xếp loại"])

# 4. Hiển thị biểu đồ cột điểm tổng kết (Dùng st.bar_chart siêu mượt, không lỗi)
st.markdown("---")
st.subheader("📈 Biểu đồ điểm tổng kết của 10 sinh viên")

chart_data = df.set_index("Ho_va_ten")[["Tổng kết"]]
st.bar_chart(chart_data)

# 5. Thông tin người tạo ở cuối trang
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: gray; font-size: 11px;'>"
    "Người tạo: Nguyễn Hoàng Minh | MSSV: 33"
    "</div>",
    unsafe_allow_html=True,
)