import pytest
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoAlertPresentException

@pytest.fixture
def driver():
    # Khởi tạo trình duyệt Edge
    driver = webdriver.Edge()
    driver.maximize_window()
    yield driver
    # Đóng trình duyệt sau khi hoàn thành
    driver.quit()

def test_add_valid_voucher(driver):
    # Điều hướng đến trang đăng nhập quản trị
    driver.get("http://watchplace.great-site.net/admin-login.php")
    time.sleep(1)
    # Nhập thông tin đăng nhập và gửi
    driver.find_element(By.NAME, "username").send_keys("admin@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("123123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)
    # Điều hướng đến phần mã giảm giá
    driver.find_element(By.XPATH, "/html/body/div[1]/div/ul/li[7]/a").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/button").click()
    time.sleep(2)
    # Điền thông tin chi tiết mã giảm giá
    driver.find_element(By.NAME, "voucher-name").send_keys("12/12")
    driver.find_element(By.NAME, "voucher-unit").click()
    driver.find_element(By.NAME, "voucher-unit").send_keys("%")
    driver.find_element(By.NAME, "voucher-discount").send_keys("20")
    driver.find_element(By.NAME, "voucher-dateFrom").send_keys("01-01-2023")
    driver.find_element(By.NAME, "voucher-dateTo").send_keys("01-01-2024")
    # Gửi biểu mẫu mã giảm giá
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    # Xử lý thông báo đầu tiên nếu có
    try:
        alert = driver.switch_to.alert
        alert.accept()
    except NoAlertPresentException:
        pass
    time.sleep(2)
    # Xử lý thông báo thứ hai và kiểm tra nội dung của nó
    alert = driver.switch_to.alert
    alert_text = alert.text
    expected_text = r"Thêm mã giảm giá mới có mã .* thành công!"
    assert re.match(expected_text, alert_text), f"Thông báo không đúng! Nhận được: {alert_text}"
    time.sleep(2)

def test_add_voucher_without_data(driver):
    # Điều hướng đến trang đăng nhập quản trị
    driver.get("http://watchplace.great-site.net/admin-login.php")
    time.sleep(1)
    # Nhập thông tin đăng nhập và gửi
    driver.find_element(By.NAME, "username").send_keys("admin@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("123123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)
    # Điều hướng đến phần mã giảm giá
    driver.find_element(By.XPATH, "/html/body/div[1]/div/ul/li[7]/a").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/button").click()
    time.sleep(2)
    # Gửi biểu mẫu mã giảm giá mà không điền dữ liệu
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    # Kiểm tra xem có thông báo lỗi không
    error_container = driver.find_element(By.CLASS_NAME, "modal-voucher-container-content-unit__err")
    assert error_container is not None
    time.sleep(2)

def test_add_exist_name_voucher(driver):
    # Điều hướng đến trang đăng nhập quản trị
    driver.get("http://watchplace.great-site.net/admin-login.php")
    time.sleep(1)
    # Nhập thông tin đăng nhập và gửi
    driver.find_element(By.NAME, "username").send_keys("admin@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("123123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)
    # Điều hướng đến phần mã giảm giá
    driver.find_element(By.XPATH, "/html/body/div[1]/div/ul/li[7]/a").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/button").click()
    time.sleep(2)
    # Điền thông tin chi tiết mã giảm giá
    driver.find_element(By.NAME, "voucher-name").send_keys("12/12")
    driver.find_element(By.NAME, "voucher-unit").click()
    driver.find_element(By.NAME, "voucher-unit").send_keys("%")
    driver.find_element(By.NAME, "voucher-discount").send_keys("20")
    driver.find_element(By.NAME, "voucher-dateFrom").send_keys("01-01-2023")
    driver.find_element(By.NAME, "voucher-dateTo").send_keys("01-01-2024")
    # Gửi biểu mẫu mã giảm giá
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    # Xử lý thông báo đầu tiên nếu có
    try:
        alert = driver.switch_to.alert
        alert.accept()
    except NoAlertPresentException:
        pass
    time.sleep(2)
    # Xử lý thông báo thứ hai và kiểm tra nội dung của nó
    alert = driver.switch_to.alert
    alert_text = alert.text
    expected_text = r"Thêm mã giảm giá mới có mã .* thành công!"
    assert re.match(expected_text, alert_text), f"Thông báo không đúng! Nhận được: {alert_text}"
    time.sleep(2)
def test_add_over_limit_name_voucher(driver):
    driver.get("http://watchplace.great-site.net/admin-login.php")
    time.sleep(1)
    driver.find_element(By.NAME, "username").send_keys("admin@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("123123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/div[1]/div/ul/li[7]/a").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/button").click()
    time.sleep(2)
    driver.find_element(By.NAME, "voucher-name").send_keys("hehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehehe")
    driver.find_element(By.NAME, "voucher-unit").click()
    driver.find_element(By.NAME, "voucher-unit").send_keys("%")
    driver.find_element(By.NAME, "voucher-discount").send_keys("20")
    driver.find_element(By.NAME, "voucher-dateFrom").send_keys("01-01-2023")
    driver.find_element(By.NAME, "voucher-dateTo").send_keys("01-01-2024")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    # Kiểm tra xem có thông báo lỗi không
    error_container = driver.find_element(By.CLASS_NAME, "modal-voucher-container-content-unit__err")
    assert error_container is not None
    time.sleep(2)
def test_add_negative_percentage_value_voucher(driver):
    driver.get("http://watchplace.great-site.net/admin-login.php")
    time.sleep(1)
    driver.find_element(By.NAME, "username").send_keys("admin@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("123123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/div[1]/div/ul/li[7]/a").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/button").click()
    time.sleep(2)
    driver.find_element(By.NAME, "voucher-name").send_keys("negative value")
    driver.find_element(By.NAME, "voucher-unit").click()
    driver.find_element(By.NAME, "voucher-unit").send_keys("%")
    driver.find_element(By.NAME, "voucher-discount").send_keys("-20")
    driver.find_element(By.NAME, "voucher-dateFrom").send_keys("01-01-2023")
    driver.find_element(By.NAME, "voucher-dateTo").send_keys("01-01-2024")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    # Kiểm tra xem có thông báo lỗi không
    error_container = driver.find_element(By.CLASS_NAME, "modal-voucher-container-content-unit__err")
    assert error_container is not None
    time.sleep(2)
def test_add_decimal_percentage_value_voucher(driver):
    driver.get("http://watchplace.great-site.net/admin-login.php")
    time.sleep(1)
    driver.find_element(By.NAME, "username").send_keys("admin@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("123123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/div[1]/div/ul/li[7]/a").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/button").click()
    time.sleep(2)
    driver.find_element(By.NAME, "voucher-name").send_keys("decimal value")
    driver.find_element(By.NAME, "voucher-unit").click()
    driver.find_element(By.NAME, "voucher-unit").send_keys("%")
    driver.find_element(By.NAME, "voucher-discount").send_keys("30.5")
    driver.find_element(By.NAME, "voucher-dateFrom").send_keys("01-01-2023")
    driver.find_element(By.NAME, "voucher-dateTo").send_keys("01-01-2024")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    # Xử lý thông báo đầu tiên nếu có
    try:
        alert = driver.switch_to.alert
        alert.accept()
    except NoAlertPresentException:
        pass
    time.sleep(2)
    # Lấy thông báo lỗi từ validationMessage
    validation_message = driver.find_element(By.NAME, "voucher-discount").get_attribute("validationMessage")

    assert "Please enter a valid value. The two nearest valid values are" in validation_message
    time.sleep(2)
def test_add_VND_negative_value_voucher(driver):
    driver.get("http://watchplace.great-site.net/admin-login.php")
    time.sleep(1)
    driver.find_element(By.NAME, "username").send_keys("admin@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("123123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/div[1]/div/ul/li[7]/a").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/button").click()
    time.sleep(2)
    driver.find_element(By.NAME, "voucher-name").send_keys("negative value")
    driver.find_element(By.NAME, "voucher-unit").click()
    driver.find_element(By.NAME, "voucher-unit").send_keys("V")
    driver.find_element(By.NAME, "voucher-discount").send_keys("-20000")
    driver.find_element(By.NAME, "voucher-dateFrom").send_keys("01-01-2023")
    driver.find_element(By.NAME, "voucher-dateTo").send_keys("01-01-2024")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    # Kiểm tra xem có thông báo lỗi không
    error_container = driver.find_element(By.CLASS_NAME, "modal-voucher-container-content-unit__err")
    assert error_container is not None
    time.sleep(2)
def test_add_VND_decimal_value_voucher(driver):
    driver.get("http://watchplace.great-site.net/admin-login.php")
    time.sleep(1)
    driver.find_element(By.NAME, "username").send_keys("admin@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("123123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/div[1]/div/ul/li[7]/a").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/button").click()
    time.sleep(2)
    driver.find_element(By.NAME, "voucher-name").send_keys("decimal value")
    driver.find_element(By.NAME, "voucher-unit").click()
    driver.find_element(By.NAME, "voucher-unit").send_keys("V")
    driver.find_element(By.NAME, "voucher-discount").send_keys("30.5")
    driver.find_element(By.NAME, "voucher-dateFrom").send_keys("01-01-2023")
    driver.find_element(By.NAME, "voucher-dateTo").send_keys("01-01-2024")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    # Xử lý thông báo đầu tiên nếu có
    try:
        alert = driver.switch_to.alert
        alert.accept()
    except NoAlertPresentException:
        pass
    time.sleep(2)
    # Lấy thông báo lỗi từ validationMessage
    validation_message = driver.find_element(By.NAME, "voucher-discount").get_attribute("validationMessage")

    assert "Please enter a valid value. The two nearest valid values are" in validation_message
    time.sleep(2)
def test_add_dateFrom_greater_dateTo_voucher(driver):
    driver.get("http://watchplace.great-site.net/admin-login.php")
    time.sleep(1)
    driver.find_element(By.NAME, "username").send_keys("admin@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("123123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/div[1]/div/ul/li[7]/a").click()
    driver.find_element(By.XPATH, "/html/body/div[2]/div[2]/div[1]/button").click()
    time.sleep(2)
    driver.find_element(By.NAME, "voucher-name").send_keys("dateFrom greater dateTo")
    driver.find_element(By.NAME, "voucher-unit").click()
    driver.find_element(By.NAME, "voucher-unit").send_keys("%")
    driver.find_element(By.NAME, "voucher-discount").send_keys("20")
    driver.find_element(By.NAME, "voucher-dateFrom").send_keys("01-01-2024")
    driver.find_element(By.NAME, "voucher-dateTo").send_keys("01-01-2023")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(2)
    # Kiểm tra xem có thông báo lỗi không
    error_container = driver.find_element(By.CLASS_NAME, "modal-voucher-container-content-unit__err")
    assert error_container is not None
    time.sleep(2)
def test_change_all_data_voucher(driver):
    driver.get("http://watchplace.great-site.net/admin-login.php")
    time.sleep(1)
    driver.find_element(By.NAME, "username").send_keys("admin@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("123123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/div[1]/div/ul/li[7]/a").click()
    driver.find_element(By.XPATH, "//tbody/tr[1]/td[@onclick]").click()
    time.sleep(2)
    driver.find_element(By.NAME, "voucher-name").clear()
    driver.find_element(By.NAME, "voucher-name").send_keys("change all data")
    driver.find_element(By.NAME, "voucher-unit").click()
    driver.find_element(By.NAME, "voucher-unit").send_keys("V")
    driver.find_element(By.NAME, "voucher-discount").clear()
    driver.find_element(By.NAME, "voucher-discount").send_keys("50")
    driver.find_element(By.NAME, "voucher-dateFrom").clear()
    driver.find_element(By.NAME, "voucher-dateFrom").send_keys("01-01-2023")
    driver.find_element(By.NAME, "voucher-dateTo").clear()
    driver.find_element(By.NAME, "voucher-dateTo").send_keys("01-01-2024")
    driver.find_element(By.XPATH,"//button[@value='edit']").click()
    time.sleep(2)
    try:
        alert = driver.switch_to.alert
        alert.accept()
    except NoAlertPresentException:
        pass
    time.sleep(2)
    # Xử lý thông báo thứ hai và kiểm tra nội dung của nó
    alert = driver.switch_to.alert
    alert_text = alert.text
    expected_text = r"Sửa mã giảm giá có mã .* thành công!"
    assert re.match(expected_text, alert_text), f"Thông báo không đúng! Nhận được: {alert_text}"
    time.sleep(2)
def test_clear_all_data_voucher(driver):
    driver.get("http://watchplace.great-site.net/admin-login.php")
    time.sleep(1)
    driver.find_element(By.NAME, "username").send_keys("admin@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("123123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/div[1]/div/ul/li[7]/a").click()
    driver.find_element(By.XPATH, "//tbody/tr[1]/td[@onclick]").click()
    time.sleep(2)
    driver.find_element(By.NAME, "voucher-name").clear()
    driver.find_element(By.NAME, "voucher-unit").click()
    driver.find_element(By.NAME, "voucher-unit").send_keys("V")
    driver.find_element(By.NAME, "voucher-discount").clear()
    driver.find_element(By.NAME, "voucher-dateFrom").clear()
    driver.find_element(By.NAME, "voucher-dateTo").clear()
    driver.find_element(By.XPATH,"//button[@value='edit']").click()
    time.sleep(2)
    error_container = driver.find_element(By.CLASS_NAME, "modal-voucher-container-content-unit__err")
    assert error_container is not None
    time.sleep(2)
def test_search_valid_voucher(driver):
    driver.get("http://watchplace.great-site.net/admin-login.php")
    time.sleep(1)
    driver.find_element(By.NAME, "username").send_keys("admin@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("123123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/div[1]/div/ul/li[7]/a").click()
    driver.find_element(By.NAME, "voucher-search").send_keys("valentine")
    driver.find_element(By.NAME, "voucher-search").send_keys(Keys.ENTER)
    time.sleep(2)
    assert driver.find_element(By.XPATH, "//td[translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz')='valentine']") is not None
def test_search_invalid_voucher(driver):
    driver.get("http://watchplace.great-site.net/admin-login.php")
    time.sleep(1)
    driver.find_element(By.NAME, "username").send_keys("admin@gmail.com")
    driver.find_element(By.NAME, "password").send_keys("123123")
    driver.find_element(By.NAME, "submit").click()
    time.sleep(1)
    driver.find_element(By.XPATH, "/html/body/div[1]/div/ul/li[7]/a").click()
    driver.find_element(By.NAME, "voucher-search").send_keys("@!invalid")
    driver.find_element(By.NAME, "voucher-search").send_keys(Keys.ENTER)
    time.sleep(2)
    assert driver.find_element(By.XPATH, "//td[text()='Không có mã giảm giá nào để hiển thị!']") is not None