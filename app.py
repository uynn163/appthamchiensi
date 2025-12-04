import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Cấu hình trang
st.set_page_config(
    page_title="Đăng kí thăm chiến sĩ đại đội 3",
    page_icon="🇻🇳",
    layout="centered"
)

# Hàm thiết lập ảnh nền
def set_background_image(image_path=None, image_url=None, opacity=0.1):
    """
    Thiết lập ảnh nền cho ứng dụng Streamlit
    
    Parameters:
    - image_path: Đường dẫn đến file ảnh trong thư mục dự án (ví dụ: "background.jpg")
    - image_url: URL của ảnh nền
    - opacity: Độ trong suốt của ảnh nền (0.0 - 1.0), mặc định 0.1
    """
    if image_path or image_url:
        # Sử dụng file ảnh từ thư mục dự án
        if image_path and os.path.exists(image_path):
            with open(image_path, "rb") as f:
                import base64
                img_data = base64.b64encode(f.read()).decode()
            bg_image = f"data:image/png;base64,{img_data}"
        # Hoặc sử dụng URL
        elif image_url:
            bg_image = image_url
        else:
            return
        
        # CSS để thiết lập ảnh nền
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url({bg_image});
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            .stApp::before {{
                content: "";
                position: absolute;
                top: 0;
                left: 0;
                right: 0;
                bottom: 0;
                background-color: rgba(0, 0, 0, 0.4);
                z-index: -1;
            }}
            .main .block-container {{
                background-color: rgba(0, 0, 0, 0.6);
                padding: 2rem;
                border-radius: 10px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
            }}
            h1, h2, h3, h4, h5, h6 {{
                color: white !important;
            }}
            p, label, .stMarkdown {{
                color: white !important;
            }}
            .stTextInput label, .stSelectbox label, .stNumberInput label, 
            .stDateInput label, .stTimeInput label {{
                color: white !important;
            }}
            .stTextInput input, .stSelectbox select, .stNumberInput input,
            .stDateInput input, .stTimeInput input {{
                color: black !important;
                background-color: rgba(255, 255, 255, 0.9) !important;
            }}
            .stSelectbox select option {{
                color: black !important;
            }}
            .stAlert, .stSuccess, .stError, .stWarning, .stInfo {{
                color: white !important;
            }}
            .stDataFrame {{
                color: white !important;
            }}
            div[data-testid="stMetricValue"], div[data-testid="stMetricLabel"] {{
                color: white !important;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

# Thiết lập ảnh nền - sử dụng file "love.jpg"
background_image = "love.jpg"
if os.path.exists(background_image):
    set_background_image(image_path=background_image, opacity=0.15)

# Khởi tạo session state cho admin
if 'is_admin' not in st.session_state:
    st.session_state.is_admin = False

# Sidebar cho máy chủ/admin
with st.sidebar:
    st.header("🔐 Chế độ máy chủ")
    
    # Kiểm tra nếu đã đăng nhập admin
    if st.session_state.is_admin:
        st.success("✅ Đã đăng nhập với tư cách máy chủ")
        if st.button("🚪 Đăng xuất", use_container_width=True):
            st.session_state.is_admin = False
            st.rerun()
    else:
        with st.form("admin_login_form"):
            admin_password = st.text_input("Mật khẩu máy chủ", type="password", help="Mật khẩu mặc định: admin123")
            login_button = st.form_submit_button("🔑 Đăng nhập", use_container_width=True)
            
            if login_button:
                # Kiểm tra mật khẩu (có thể thay đổi)
                if admin_password == "admin123":  # Mật khẩu mặc định, có thể thay đổi
                    st.session_state.is_admin = True
                    st.rerun()
                elif admin_password == "":
                    st.warning("⚠️ Vui lòng nhập mật khẩu!")
                else:
                    st.error("❌ Mật khẩu không đúng!")

# Tiêu đề ứng dụng
st.title("Đăng kí thăm chiến sĩ đại đội 3")
st.markdown("---")

# File lưu trữ dữ liệu
DATA_FILE = "dang_ky_tham.csv"

# Khởi tạo file CSV nếu chưa tồn tại
def init_data_file():
    if not os.path.exists(DATA_FILE):
        df = pd.DataFrame(columns=[
            "Họ và tên",
            "Họ và tên chiến sĩ",
            "Mối quan hệ",
            "Số lượng khách",
            "Đơn vị",
            "Thời gian",
            "Ngày đăng ký"
        ])
        df.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')

# Đọc dữ liệu từ CSV
def load_data():
    if os.path.exists(DATA_FILE):
        return pd.read_csv(DATA_FILE, encoding='utf-8-sig')
    return pd.DataFrame(columns=[
        "Họ và tên",
        "Họ và tên chiến sĩ",
        "Mối quan hệ",
        "Số lượng khách",
        "Đơn vị",
        "Thời gian",
        "Ngày đăng ký"
    ])

# Lưu dữ liệu vào CSV
def save_data(df):
    df.to_csv(DATA_FILE, index=False, encoding='utf-8-sig')

# Khởi tạo file dữ liệu
init_data_file()

# Form đăng ký
with st.form("form_dang_ky", clear_on_submit=True):
    st.subheader("📝 Điền thông tin đăng ký")
    
    ho_ten = st.text_input("Họ và tên *", placeholder="Nhập họ và tên của bạn")
    ten_chien_si = st.text_input("Họ và tên chiến sĩ *", placeholder="Nhập họ và tên chiến sĩ cần thăm")
    moi_quan_he = st.text_input("Mối quan hệ với chiến sĩ *", placeholder="Nhập mối quan hệ (ví dụ: Bố, Mẹ, Anh, Chị...)")
    so_luong_khach = st.number_input("Số lượng khách *", min_value=1, max_value=50, value=1, step=1)
    don_vi = st.selectbox("Đơn vị *", ["Trung đội 7", "Trung đội 8", "Trung đội 9"])
    
    # Chọn thời gian
    col1, col2 = st.columns(2)
    with col1:
        ngay = st.date_input("Ngày thăm *", min_value=datetime.now().date())
    with col2:
        gio = st.time_input("Giờ thăm *", value=datetime.now().time())
    
    thoi_gian = f"{ngay.strftime('%d/%m/%Y')} - {gio.strftime('%H:%M')}"
    
    submitted = st.form_submit_button("📌 Đăng ký", use_container_width=True)
    
    if submitted:
        # Kiểm tra dữ liệu đầu vào
        if not ho_ten or not ten_chien_si or not moi_quan_he or not so_luong_khach or not don_vi:
            st.error("⚠️ Vui lòng điền đầy đủ thông tin bắt buộc (*)")
        else:
            # Đọc dữ liệu hiện có
            df = load_data()
            
            # Thêm dữ liệu mới
            new_row = {
                "Họ và tên": ho_ten,
                "Họ và tên chiến sĩ": ten_chien_si,
                "Mối quan hệ": moi_quan_he,
                "Số lượng khách": int(so_luong_khach),
                "Đơn vị": don_vi,
                "Thời gian": thoi_gian,
                "Ngày đăng ký": datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }
            
            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            
            # Lưu dữ liệu
            save_data(df)
            
            st.success("✅ Đăng ký thành công!")
            st.balloons()

# Hiển thị danh sách đăng ký (chỉ dành cho máy chủ)
if st.session_state.is_admin:
    st.markdown("---")
    st.subheader("📋 Danh sách đăng ký")

    df = load_data()

    if not df.empty:
        # Hiển thị bảng dữ liệu
        st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Nút xóa tất cả (chỉ hiển thị khi có dữ liệu)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("🗑️ Xóa tất cả", use_container_width=True):
                if os.path.exists(DATA_FILE):
                    os.remove(DATA_FILE)
                st.success("✅ Đã xóa tất cả dữ liệu!")
                st.rerun()
        
        # Thống kê
        st.markdown("---")
        st.subheader("📊 Thống kê")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Tổng số đăng ký", len(df))
        with col2:
            st.metric("Số chiến sĩ", df["Họ và tên chiến sĩ"].nunique())
        with col3:
            st.metric("Số đơn vị", df["Đơn vị"].nunique())
        with col4:
            tong_khach = df["Số lượng khách"].sum() if "Số lượng khách" in df.columns else 0
            st.metric("Tổng số khách", int(tong_khach))
    else:
        st.info("📭 Chưa có đăng ký nào.")

