import pytest
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import NoSuchElementException

@pytest.fixture
def driver():
    # Khởi tạo trình duyệt Edge
    driver = webdriver.Edge()
    driver.maximize_window()
    yield driver
    # Đóng trình duyệt sau khi hoàn thành
    driver.quit()

def test_valid_date_filter(driver):
    # Mở trang đăng nhập
    driver.get("http://watchplace.great-site.net/admin-login.php")
    time.sleep(1)
    # Nhập thông tin đăng nhập
    driver.find_element(By.NAME, "username").send_keys("admin@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("123123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)
    # Điều hướng đến trang cần kiểm tra
    driver.find_element(By.XPATH, "/html/body/div[1]/div/ul/li[2]/a").click()
    # Nhập khoảng thời gian cần lọc
    driver.find_element(By.NAME, "date-from").send_keys("01-01-2023")
    driver.find_element(By.NAME, "date-to").send_keys("01-01-2024")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(2)

    # Lấy dữ liệu từ biểu đồ
    chart_data = driver.execute_script("""
        var chart = Chart.getChart('myChart');
        return chart ? chart.data.datasets[0].data : null;
    """)
    print("Dữ liệu biểu đồ:", chart_data)
    # Điều hướng đến trang khác
    driver.find_element(By.XPATH, "/html/body/div[1]/div/ul/li[5]/a").click()
    # Nhập lại khoảng thời gian cần lọc
    driver.find_element(By.NAME, "date-from").send_keys("01-01-2023")
    driver.find_element(By.NAME, "date-to").send_keys("01-01-2024")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    # Lấy giá từ bảng
    price = driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/table/tbody/tr[1]/td[7]").text.replace(',', '')
    # Kiểm tra dữ liệu biểu đồ và giá có khớp nhau không
    assert chart_data[0] == price
    
    time.sleep(2)

def test_valid_date_no_data_filter(driver):
    # Mở trang đăng nhập
    driver.get("http://watchplace.great-site.net/admin-login.php")
    time.sleep(1)
    # Nhập thông tin đăng nhập
    driver.find_element(By.NAME, "username").send_keys("admin@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("123123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)
    # Điều hướng đến trang cần kiểm tra
    driver.find_element(By.XPATH, "/html/body/div[1]/div/ul/li[2]/a").click()
    # Nhập khoảng thời gian không có dữ liệu
    driver.find_element(By.NAME, "date-from").send_keys("01-01-2025")
    driver.find_element(By.NAME, "date-to").send_keys("01-01-2026")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(2)

    # Lấy dữ liệu từ biểu đồ
    chart_data = driver.execute_script("""
        var chart = Chart.getChart('myChart');
        return chart ? chart.data.datasets[0].data : null;
    """)
    print("Dữ liệu biểu đồ:", chart_data)
    # Kiểm tra dữ liệu biểu đồ có rỗng không
    assert chart_data == []
    time.sleep(2)

def test_dateFrom_greater_than_dateTo(driver):
    # Mở trang đăng nhập
    driver.get("http://watchplace.great-site.net/admin-login.php")
    time.sleep(1)
    # Nhập thông tin đăng nhập
    driver.find_element(By.NAME, "username").send_keys("admin@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("123123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)
    # Điều hướng đến trang cần kiểm tra
    driver.find_element(By.XPATH, "/html/body/div[1]/div/ul/li[2]/a").click()
    # Nhập khoảng thời gian không hợp lệ
    driver.find_element(By.NAME, "date-from").send_keys("01-01-2024")
    driver.find_element(By.NAME, "date-to").send_keys("01-01-2023")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(2)
    # Kiểm tra xem có thông báo lỗi không
    error_container = driver.find_element(By.CLASS_NAME, "modal-sale-container-content-unit__err")
    assert error_container is not None

def test_filter_without_date(driver):
    # Mở trang đăng nhập
    driver.get("http://watchplace.great-site.net/admin-login.php")    
    time.sleep(1)
    # Nhập thông tin đăng nhập
    driver.find_element(By.NAME, "username").send_keys("admin@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("123123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)
    # Điều hướng đến trang cần kiểm tra
    driver.find_element(By.XPATH, "/html/body/div[1]/div/ul/li[2]/a").click()
    # Không nhập ngày và nhấn lọc
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(2)
    # Kiểm tra xem có thông báo lỗi không
    error_container = driver.find_element(By.CLASS_NAME, "modal-sale-container-content-unit__err")
    assert error_container is not None

def test_filter_without_dateTo(driver):
    # Mở trang đăng nhập
    driver.get("http://watchplace.great-site.net/admin-login.php")    
    time.sleep(1)
    # Nhập thông tin đăng nhập
    driver.find_element(By.NAME, "username").send_keys("admin@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("123123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)
    # Điều hướng đến trang cần kiểm tra
    driver.find_element(By.XPATH, "/html/body/div[1]/div/ul/li[2]/a").click()
    # Chỉ nhập ngày bắt đầu và nhấn lọc
    driver.find_element(By.NAME, "date-from").send_keys("01-01-2023")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(2)
    # Kiểm tra xem có thông báo lỗi không
    error_container = driver.find_element(By.CLASS_NAME, "modal-sale-container-content-unit__err")
    assert error_container is not None

def test_filter_without_dateFrom(driver):
    # Mở trang đăng nhập
    driver.get("http://watchplace.great-site.net/admin-login.php")    
    time.sleep(1)
    # Nhập thông tin đăng nhập
    driver.find_element(By.NAME, "username").send_keys("admin@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("123123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)
    # Điều hướng đến trang cần kiểm tra
    driver.find_element(By.XPATH, "/html/body/div[1]/div/ul/li[2]/a").click()
    # Chỉ nhập ngày kết thúc và nhấn lọc
    driver.find_element(By.NAME, "date-to").send_keys("01-01-2024")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(2)
    # Kiểm tra xem có thông báo lỗi không
    error_container = driver.find_element(By.CLASS_NAME, "modal-sale-container-content-unit__err")
    assert error_container is not None

def test_month_button(driver):
    # Mở trang đăng nhập
    driver.get("http://watchplace.great-site.net/admin-login.php")
    time.sleep(1)
    # Nhập thông tin đăng nhập
    driver.find_element(By.NAME, "username").send_keys("admin@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("123123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)
    # Điều hướng đến trang cần kiểm tra
    driver.find_element(By.XPATH, "/html/body/div[1]/div/ul/li[2]/a").click()
    # Nhấn nút lọc theo tháng
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[1]/div/button[2]").click()
    time.sleep(2)
    # Lấy dữ liệu từ biểu đồ
    chart_data = driver.execute_script("""
        var chart = Chart.getChart('myChart');
        return chart ? chart.data.datasets[0].data : null;
    """)
    chart_labels = driver.execute_script("""
        var chart = Chart.getChart('myChart');
        return chart ? chart.data.labels : null;
    """)
    # Nhãn bạn muốn tìm
    target_label = "03/2023"

    # Tìm chỉ số của nhãn
    try:
        index = chart_labels.index(target_label)
        # Lấy dữ liệu tương ứng
        target_data = chart_data[index]
        print(f"Dữ liệu cho nhãn {target_label}: {target_data}")
    except ValueError:
        print(f"Nhãn {target_label} không tồn tại trong biểu đồ.")
    print("Dữ liệu biểu đồ:", chart_data)
    print("Dữ liệu biểu đồ:", chart_labels)
    # Điều hướng đến trang khác
    driver.find_element(By.XPATH, "/html/body/div[1]/div/ul/li[5]/a").click()
    # Nhập khoảng thời gian cần lọc
    driver.find_element(By.NAME, "date-from").send_keys("03-01-2023")
    driver.find_element(By.NAME, "date-to").send_keys("03-31-2023")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(2)
    # Tính tổng giá từ bảng
    rows = driver.find_elements(By.XPATH, "/html/body/div[2]/div[2]/table/tbody/tr")
    
    total_price = 0
    for row in rows:
        try:
            # Tìm <td> chứa giá (giả sử là <td> thứ 10 trong mỗi hàng)
            price_td = row.find_element(By.XPATH, "./td[10]")
            # Loại bỏ dấu phẩy và chuyển đổi văn bản thành số nguyên
            price = int(price_td.text.replace(',', ''))
            # Cộng giá vào tổng
            total_price += price
        except NoSuchElementException:
            print("Không tìm thấy <td> giá trong hàng này.")
        except ValueError:
            print("Không thể chuyển đổi giá thành số nguyên.")

    print("Tổng giá:", total_price)
    time.sleep(2)
    # Kiểm tra tổng giá có khớp với dữ liệu biểu đồ không
    assert total_price == int(target_data)

def test_year_button(driver):
    # Mở trang đăng nhập
    driver.get("http://watchplace.great-site.net/admin-login.php")
    time.sleep(1)
    # Nhập thông tin đăng nhập
    driver.find_element(By.NAME, "username").send_keys("admin@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("123123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)
    # Điều hướng đến trang cần kiểm tra
    driver.find_element(By.XPATH, "/html/body/div[1]/div/ul/li[2]/a").click()
    # Nhấn nút lọc theo năm
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/div[1]/div/button[3]").click()
    time.sleep(2)
    # Lấy dữ liệu từ biểu đồ
    chart_data = driver.execute_script("""
        var chart = Chart.getChart('myChart');
        return chart ? chart.data.datasets[0].data : null;
    """)
    chart_labels = driver.execute_script("""
        var chart = Chart.getChart('myChart');
        return chart ? chart.data.labels : null;
    """)
    # Nhãn bạn muốn tìm
    target_label = "2023"

    # Tìm chỉ số của nhãn
    try:
        index = chart_labels.index(target_label)
        # Lấy dữ liệu tương ứng
        target_data = chart_data[index]
        print(f"Dữ liệu cho nhãn {target_label}: {target_data}")
    except ValueError:
        print(f"Nhãn {target_label} không tồn tại trong biểu đồ.")
    print("Dữ liệu biểu đồ:", chart_data)
    print("Dữ liệu biểu đồ:", chart_labels)
    # Điều hướng đến trang khác
    driver.find_element(By.XPATH, "/html/body/div[1]/div/ul/li[5]/a").click()
    # Nhập khoảng thời gian cần lọc
    driver.find_element(By.NAME, "date-from").send_keys("01-01-2023")
    driver.find_element(By.NAME, "date-to").send_keys("12-31-2023")
    driver.find_element(By.XPATH, "//button[@type='submit']").click()
    time.sleep(2)
    # Tính tổng giá từ bảng
    rows = driver.find_elements(By.XPATH, "/html/body/div[2]/div[2]/table/tbody/tr")
    
    total_price = 0
    for row in rows:
        try:
            # Tìm <td> chứa giá (giả sử là <td> thứ 10 trong mỗi hàng)
            price_td = row.find_element(By.XPATH, "./td[10]")
            # Loại bỏ dấu phẩy và chuyển đổi văn bản thành số nguyên
            price = int(price_td.text.replace(',', ''))
            # Cộng giá vào tổng
            total_price += price
        except NoSuchElementException:
            print("Không tìm thấy <td> giá trong hàng này.")
        except ValueError:
            print("Không thể chuyển đổi giá thành số nguyên.")

    print("Tổng giá:", total_price)
    time.sleep(2)
    # Kiểm tra tổng giá có khớp với dữ liệu biểu đồ không
    assert total_price == int(target_data)