from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from time import sleep
import time
import pytest
import random
import string

def open_site(url):
    driver = webdriver.Chrome(service=Service(), options=webdriver.ChromeOptions())
    driver.maximize_window()
    driver.get(url)
    return driver

def close_browser(driver):
    driver.close()

def test_automationexercise_smoke():
    driver = open_site('https://automationexercise.com/')
    sleep(2)
    assert "automation" in driver.title.lower() or "exercise" in driver.title.lower(), "Title check failed"
    print('Home page title verified.')
    close_browser(driver)

# Helper: Generate random email
def generate_random_email():
    return "testuser_" + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6)) + "@example.com"

    email = generate_random_email()
    print(f"[INFO] Using unique email: {email}")
    driver.find_element(By.NAME, "email").send_keys(email)

def test_register_new_user():
    driver = open_site("https://automationexercise.com")
    sleep(3)
    print("[INFO] Navigating to Signup / Login page...")
    email = generate_random_email()
    # ✅ Close overlay if present
    try:
        driver.find_element(By.XPATH, "//p[@class='fc-button-label' and contains(text(), 'Consent')]").click()
        print("[INFO] Clicked 'Consent' popup button.")
        sleep(1)
    except:
        print("[INFO] No 'Consent' popup found.")
    driver.find_element(By.XPATH, "//a[contains(text(), 'Signup')]").click()
    sleep(3)

    # Step 2: Fill name and email
    driver.find_element(By.NAME, "name").send_keys("John Doe")
    driver.find_element(By.CSS_SELECTOR, "input[data-qa='signup-email']").send_keys(email)
    driver.find_element(By.CSS_SELECTOR, "button[data-qa='signup-button']").click()
    sleep(5)

    # Check if redirected to the registration form
    if "Email Address already exist!" in driver.page_source:
        print("[ERROR] Email already exists. Cannot proceed.")
        print("[DEBUG] Used email:", email)
        close_browser(driver)
        return

    if "Enter Account Information" not in driver.page_source:
        print("[ERROR] Registration form did not load.")
        print("[DEBUG] Current URL:", driver.current_url)
        print("[DEBUG] Page snapshot:\n", driver.page_source[:1000])
        close_browser(driver)
        return

    print("[INFO] Filling out registration form...")

    driver.find_element(By.ID, "id_gender1").click()
    driver.find_element(By.ID, "password").send_keys("Test@1234")
    driver.find_element(By.ID, "days").send_keys("10")
    driver.find_element(By.ID, "months").send_keys("May")
    driver.find_element(By.ID, "years").send_keys("1995")
    driver.find_element(By.ID, "optin").click()
    driver.find_element(By.ID, "first_name").send_keys("Test")
    driver.find_element(By.ID, "last_name").send_keys("User")
    driver.find_element(By.ID, "address1").send_keys("123 Test Street")
    driver.find_element(By.ID, "state").send_keys("TestState")
    driver.find_element(By.ID, "city").send_keys("TestCity")
    driver.find_element(By.ID, "zipcode").send_keys("12345")
    driver.find_element(By.ID, "mobile_number").send_keys("1234567890")
    driver.find_element(By.XPATH, "//button[@data-qa='create-account']").click()
    sleep(3)
    confirmation = driver.find_element(By.TAG_NAME, "h2").text
    assert "ACCOUNT CREATED!" in confirmation.upper(), "Account creation failed"
    print("[SUCCESS] New user registered successfully.")
    driver.find_element(By.LINK_TEXT, "Continue").click()
    sleep(3)
    close_browser(driver)

def test_signup_with_existing_email():
    driver = open_site("https://automationexercise.com")
    sleep(2)
    try:
        driver.find_element(By.XPATH, "//p[@class='fc-button-label' and contains(text(), 'Consent')]").click()
        print("[INFO] Clicked 'Consent' popup button.")
        sleep(1)
    except:
        print("[INFO] No 'Consent' popup found.")
    driver.find_element(By.XPATH, "//a[contains(text(), 'Signup')]").click()
    sleep(2)
    # Step 2: Fill name and email
    driver.find_element(By.NAME, "name").send_keys("John Doe")
    driver.find_element(By.CSS_SELECTOR, "input[data-qa='signup-email']").send_keys("test@example.com")
    driver.find_element(By.XPATH, "//button[@data-qa='signup-button']").click()
    sleep(2)
# Step 3: Verify if an error message appears for existing email
    try:
        error_message = driver.find_element(By.XPATH, "//p[text()='Email Address already exist!']")
        assert error_message.is_displayed(), "Email already in use error is not displayed."
        print('Error message for existing email displayed successfully.')
    except Exception as e:
        print(f"Error: {e}")
    close_browser(driver)

def test_login_with_valid_credentials():
    driver = open_site("https://automationexercise.com")
    sleep(2)
    try:
        driver.find_element(By.XPATH, "//p[@class='fc-button-label' and contains(text(), 'Consent')]").click()
        print("[INFO] Clicked 'Consent' popup button.")
        sleep(1)
    except:
        print("[INFO] No 'Consent' popup found.")

    driver.find_element(By.XPATH, "//a[@href='/login']").click()
    sleep(2)
    driver.find_element(By.NAME, "email").send_keys("test123456@example.com")
    driver.find_element(By.NAME, "password").send_keys("Aventura25")
    driver.find_element(By.XPATH, "//button[@data-qa='login-button']").click()
    sleep(4)
    try:
        logout_button = driver.find_element(By.XPATH, "//a[@href='/logout']")
        assert logout_button.is_displayed(), "Logout button is not visible after login."
        print("Logout button is visible after successful login.")
    except Exception as e:
        print(f"Error: {e}")

    close_browser(driver)

def test_login_with_invalid_credentials():
    driver = open_site("https://automationexercise.com")
    sleep(2)
    try:
        driver.find_element(By.XPATH, "//p[@class='fc-button-label' and contains(text(), 'Consent')]").click()
        print("[INFO] Clicked 'Consent' popup button.")
        sleep(1)
    except:
        print("[INFO] No 'Consent' popup found.")
    # Step 1: Go to Signup/Login
    driver.find_element(By.XPATH, "//a[text()=' Signup / Login']").click()
    print("Clicked on Signup/Login.")
    sleep(2)
    assert "Login" in driver.page_source
    print("Signup/Login page loaded correctly.")

    email_input = driver.find_element(By.XPATH, "//input[@data-qa='login-email']").send_keys("invalid@example.com")
    password_input = driver.find_element(By.XPATH, "//input[@data-qa='login-password']").send_keys("wrongpassword")
    print("Entered invalid email and password.")

    login_button = driver.find_element(By.XPATH, "//button[@data-qa='login-button']")
    login_button.click()
    print("Clicked Login button.")
    sleep(2)

    error_message = driver.find_element(By.XPATH, "//p[text()='Your email or password is incorrect!']")
    assert error_message.is_displayed()
    print("Error message is shown: 'Your email or password is incorrect!'")

    print("Test Passed: Login with invalid credentials was correctly rejected.")
    driver.quit()

def test_add_product_to_cart_from_list():
    driver = open_site("https://automationexercise.com")
    wait = WebDriverWait(driver, 10)

    try:
        # Consent popup (ako postoji)
        try:
            consent_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//p[@class='fc-button-label' and contains(text(), 'Consent')]")))
            consent_btn.click()
            print("[INFO] Clicked 'Consent' popup button.")
        except:
            print("[INFO] No 'Consent' popup found.")

        # Step 1: Otvori "Products" stranicu
        products_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()=' Products']")))
        products_link.click()

        # Step 2: Provera da je učitana stranica
        wait.until(EC.presence_of_element_located((By.XPATH, "//h2[text()='All Products']")))

        # Step 3: Hover na prvi proizvod
        product = wait.until(EC.presence_of_element_located((By.XPATH, "(//div[@class='productinfo text-center'])[1]/..")))
        ActionChains(driver).move_to_element(product).perform()

        # Step 4: Klik na "Add to cart" preko JavaScript-a
        add_to_cart = wait.until(EC.visibility_of_element_located((By.XPATH, "(//a[@data-product-id='1'])[1]")))
        ActionChains(driver).move_to_element(add_to_cart).perform()
        driver.execute_script("arguments[0].click();", add_to_cart)

        # Step 5: Provera popup poruke
        popup_title = wait.until(EC.visibility_of_element_located((By.XPATH, "//h4[text()='Added!']")))
        assert popup_title.is_displayed()

        success_msg = wait.until(EC.visibility_of_element_located((By.XPATH, "//p[contains(text(), 'Your product has been added to cart')]")))
        assert success_msg.is_displayed()

        # Step 6: Klik na "View Cart"
        view_cart = wait.until(EC.element_to_be_clickable((By.XPATH, "//u[text()='View Cart']")))
        view_cart.click()

        # Step 7: Provera da je proizvod u korpi
        cart_item = wait.until(EC.visibility_of_element_located((By.XPATH, "//td[@class='cart_description']/h4/a")))
        assert cart_item.is_displayed()
        print("Test Passed: Product was successfully added to cart and displayed in cart.")

    finally:
        close_browser(driver)

def test_view_cart_and_verify_items():
    driver = open_site("https://automationexercise.com")
    wait = WebDriverWait(driver, 10)
    try:
        # Consent popup (ako postoji)
        try:
            consent_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//p[@class='fc-button-label' and contains(text(), 'Consent')]")))
            consent_btn.click()
            print("[INFO] Clicked 'Consent' popup button.")
        except:
            print("[INFO] No 'Consent' popup found.")

        # Step 1: Otvori "Products" stranicu
        products_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()=' Products']")))
        products_link.click()

        # Step 2: Provera da je učitana stranica
        wait.until(EC.presence_of_element_located((By.XPATH, "//h2[text()='All Products']")))

        # Step 3: Hover na prvi proizvod
        product = wait.until(
            EC.presence_of_element_located((By.XPATH, "(//div[@class='productinfo text-center'])[1]/..")))
        ActionChains(driver).move_to_element(product).perform()

        # Step 4: Klik na "Add to cart" preko JavaScript-a
        add_to_cart = wait.until(EC.visibility_of_element_located((By.XPATH, "(//a[@data-product-id='1'])[1]")))
        ActionChains(driver).move_to_element(add_to_cart).perform()
        driver.execute_script("arguments[0].click();", add_to_cart)

        # Step 5: Provera popup poruke
        popup_title = wait.until(EC.visibility_of_element_located((By.XPATH, "//h4[text()='Added!']")))
        assert popup_title.is_displayed()

        success_msg = wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//p[contains(text(), 'Your product has been added to cart')]")))
        assert success_msg.is_displayed()

        # Step 6: Klik na "View Cart"
        view_cart = wait.until(EC.element_to_be_clickable((By.XPATH, "//u[text()='View Cart']")))
        view_cart.click()

        # Step 7: Provera da je stranica korpe učitana
        wait.until(EC.presence_of_element_located((By.XPATH, "//section[@id='cart_items']")))
        assert "Shopping Cart" in driver.page_source

        # Step 8: Provera naziva proizvoda
        product_name = driver.find_element(By.XPATH, "//td[@class='cart_description']/h4/a").text.strip()
        assert product_name != "", "Product name is empty."
        print(f"Product name in cart: {product_name}")

        # Step 9: Provera cene proizvoda
        product_price = driver.find_element(By.XPATH, "//td[@class='cart_price']/p").text.strip().replace("Rs. ", "").replace(",", "")
        assert product_price.isdigit(), f"Invalid price value: {product_price}"
        print(f"Product price in cart: {product_price}")

        # Step 10: Provera količine proizvoda
        product_quantity = driver.find_element(By.XPATH, "//td[@class='cart_quantity']/button").text.strip()
        assert product_quantity.isdigit(), f"Invalid quantity: {product_quantity}"
        print(f"Product quantity in cart: {product_quantity}")

        # Step 11: Provera ukupne cene (price * quantity)
        expected_total = str(int(product_price) * int(product_quantity))
        cart_total = driver.find_element(By.XPATH, "//td[@class='cart_total']/p").text.strip().replace("Rs. ", "").replace(",", "")
        assert expected_total == cart_total, f"Total mismatch: expected {expected_total}, got {cart_total}"
        print(f"Total price in cart is correct: {cart_total}")

        print("Product details verified successfully in the cart.")

    finally:
        driver.quit()

def test_add_and_remove_product_from_cart():
    driver = open_site("https://automationexercise.com")
    wait = WebDriverWait(driver, 15)

    try:
        # Step 0: Handle consent popup if present
        try:
            consent_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, "//p[@class='fc-button-label' and contains(text(), 'Consent')]"))
            )
            consent_btn.click()
            print("[INFO] Clicked 'Consent' popup button.")
        except:
            print("[INFO] No 'Consent' popup found.")

        # Step 1: Open Products page
        products_link = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()=' Products']")))
        products_link.click()

        # Step 2: Wait for All Products page
        wait.until(EC.presence_of_element_located((By.XPATH, "//h2[text()='All Products']")))

        # Step 3: Hover over first product
        product = wait.until(EC.presence_of_element_located((By.XPATH, "(//div[@class='productinfo text-center'])[1]/..")))
        ActionChains(driver).move_to_element(product).perform()

        # Step 4: Click "Add to cart"
        add_to_cart = wait.until(EC.element_to_be_clickable((By.XPATH, "(//a[@data-product-id='1'])[1]")))
        driver.execute_script("arguments[0].click();", add_to_cart)

        # Step 5: Confirm popup
        wait.until(EC.visibility_of_element_located((By.XPATH, "//h4[text()='Added!']")))
        wait.until(EC.visibility_of_element_located((By.XPATH, "//p[contains(text(), 'Your product has been added to cart')]")))

        # Step 6: Click "View Cart"
        view_cart = wait.until(EC.element_to_be_clickable((By.XPATH, "//u[text()='View Cart']")))
        view_cart.click()

        # Step 7: Wait for cart and verify product
        wait.until(EC.presence_of_element_located((By.ID, "cart_items")))
        product_name = driver.find_element(By.XPATH, "//td[@class='cart_description']/h4/a").text.strip()
        assert product_name != ""
        print(f"[INFO] Product in cart: {product_name}")

        # Step 8: Click delete (X) button
        delete_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//a[@class='cart_quantity_delete' and @data-product-id='1']"))
        )
        delete_button.click()
        print("[INFO] Clicked delete (X) button.")

        # Step 9: Wait for "Cart is empty!" text anywhere in page source (fallback)
        try:
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//p[@class='text-center' and contains(., 'Cart is empty!')]")
                )
            )
            print("[SUCCESS] Product successfully removed. Cart is empty.")
        except TimeoutException:
            print("[WARNING] Specific empty cart element not found by XPath, trying fallback check in page source.")
            if wait.until(lambda d: "Cart is empty!" in d.page_source):
                print("[SUCCESS - fallback] Found 'Cart is empty!' text in page source.")
            else:
                print("[ERROR] 'Cart is empty!' text NOT found anywhere on page after deletion.")
                driver.save_screenshot("cart_empty_not_found.png")
                raise TimeoutException("Cart empty message not found.")

    except TimeoutException as e:
        print("[ERROR] Timeout waiting for element:", e)
        driver.save_screenshot("error_screenshot.png")
        raise
    finally:
        driver.quit()

def close_ads_iframe(driver):
    """Closes popup ad if it exists inside an iframe."""
    try:
        sleep(2)
        iframe = driver.find_element(By.TAG_NAME, "iframe")
        driver.switch_to.frame(iframe)
        close_btn = driver.find_element(By.XPATH, "//div[contains(@id,'dismiss') or contains(@id,'close')]")
        close_btn.click()
        driver.switch_to.default_content()
        print("[INFO] Popup ad closed.")
    except Exception:
        driver.switch_to.default_content()
        print("[INFO] No popup iframe detected.")

def test_search_for_product():
    driver = open_site("https://automationexercise.com")
    wait = WebDriverWait(driver, 10)

    try:
        sleep(2)
        close_ads_iframe(driver)

        # Go to Products
        product_link = driver.find_element(By.XPATH, "//a[@href='/products']")
        driver.execute_script("arguments[0].scrollIntoView(true);", product_link)
        sleep(1)
        product_link.click()

        # Search
        sleep(2)
        driver.find_element(By.ID, "search_product").send_keys("Polo T-Shirts")
        driver.find_element(By.ID, "submit_search").click()

        # Wait for results
        sleep(2)
        assert "Searched Products" in driver.page_source

        results = driver.find_elements(By.XPATH, "//div[@class='productinfo text-center']/p")
        assert results, "No products found."
        assert any("polo" in r.text.lower() or "t-shirt" in r.text.lower() for r in results)

        print("[SUCCESS] Relevant search results for 'Polo T-Shirts' were displayed.")

    except Exception as e:
        driver.save_screenshot("search_test_error.png")
        print("[ERROR] Test failed. Screenshot saved.")
        raise e

    finally:
        driver.quit()















def test_place_order_as_registered_user():
    driver = open_site("https://automationexercise.com")
    wait = WebDriverWait(driver, 10)

    try:
        # Step 1: Login
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()=' Signup / Login']"))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@data-qa='login-email']"))).send_keys("test123456@example.com")
        driver.find_element(By.XPATH, "//input[@data-qa='login-password']").send_keys("Aventura25")
        driver.find_element(By.XPATH, "//button[@data-qa='login-button']").click()
        wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'Logged in as')]")))

        # Step 2: Add product to cart
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()=' Products']"))).click()
        product_card = wait.until(EC.presence_of_element_located((By.XPATH, "(//div[@class='productinfo text-center'])[1]/..")))
        ActionChains(driver).move_to_element(product_card).perform()
        add_button = wait.until(EC.element_to_be_clickable((By.XPATH, "(//a[@data-product-id])[1]")))
        add_button.click()

        # View cart
        wait.until(EC.element_to_be_clickable((By.XPATH, "//u[text()='View Cart']"))).click()

        # Step 3: Proceed to Checkout
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Proceed To Checkout']"))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[text()='Address Details']")))

        # Step 4: Enter comment and place order
        driver.find_element(By.XPATH, "//textarea[@name='message']").send_keys("Please deliver quickly.")
        driver.find_element(By.XPATH, "//a[text()='Place Order']").click()

        # Fill payment details
        wait.until(EC.visibility_of_element_located((By.NAME, "name_on_card"))).send_keys("Test User")
        driver.find_element(By.NAME, "card_number").send_keys("4111111111111111")
        driver.find_element(By.NAME, "cvc").send_keys("123")
        driver.find_element(By.NAME, "expiry_month").send_keys("12")
        driver.find_element(By.NAME, "expiry_year").send_keys("2026")
        driver.find_element(By.ID, "submit").click()

        # Step 5: Confirm order success
        wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Your order has been placed successfully!')]")))
        print("[SUCCESS] Order placed successfully by registered user.")

    except Exception as e:
        driver.save_screenshot("place_order_error.png")
        print("[ERROR] Test failed. Screenshot saved as 'place_order_error.png'.")
        raise e

    finally:
        driver.quit()
def test_place_order_as_registered_user():
    driver = open_site("https://automationexercise.com")
    wait = WebDriverWait(driver, 15)

    try:
        # Step 1: Login
        driver.find_element(By.XPATH, "//a[text()=' Signup / Login']").click()
        wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@data-qa='login-email']"))).send_keys("test123456@example.com")
        driver.find_element(By.XPATH, "//input[@data-qa='login-password']").send_keys("Aventura25")
        driver.find_element(By.XPATH, "//button[@data-qa='login-button']").click()
        wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(),'Logged in as')]")))
        print("[INFO] Logged in successfully.")

        # Step 2: Navigate to Products and Add to Cart
        driver.find_element(By.XPATH, "//a[text()=' Products']").click()
        wait.until(EC.presence_of_element_located((By.XPATH, "(//div[@class='productinfo text-center'])[1]")))

        product = driver.find_element(By.XPATH, "(//div[@class='productinfo text-center'])[1]/..")
        ActionChains(driver).move_to_element(product).perform()
        sleep(1)

        add_button = driver.find_element(By.XPATH, "(//a[@data-product-id])[1]")
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", add_button)
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//a[@data-product-id])[1]")))
        driver.execute_script("arguments[0].click();", add_button)
        print("[INFO] Product added to cart.")

        # View cart
        wait.until(EC.element_to_be_clickable((By.XPATH, "//u[text()='View Cart']"))).click()
        wait.until(EC.visibility_of_element_located((By.XPATH, "//a[text()='Proceed To Checkout']")))
        print("[INFO] Viewing cart and proceeding to checkout.")

        # Step 3: Proceed to Checkout
        driver.find_element(By.XPATH, "//a[text()='Proceed To Checkout']").click()
        wait.until(EC.visibility_of_element_located((By.XPATH, "//textarea[@name='message']")))

        # Step 4: Enter comment and place order
        driver.find_element(By.XPATH, "//textarea[@name='message']").send_keys("Please deliver quickly.")
        driver.find_element(By.XPATH, "//a[text()='Place Order']").click()

        # Step 5: Enter payment details
        wait.until(EC.visibility_of_element_located((By.NAME, "name_on_card"))).send_keys("Test User")
        driver.find_element(By.NAME, "card_number").send_keys("4111111111111111")
        driver.find_element(By.NAME, "cvc").send_keys("123")
        driver.find_element(By.NAME, "expiry_month").send_keys("12")
        driver.find_element(By.NAME, "expiry_year").send_keys("2026")
        driver.find_element(By.ID, "submit").click()

        # Step 6: Wait for order confirmation (flexible XPath)
        wait.until(EC.visibility_of_element_located(
            (By.XPATH, "//*[contains(text(),'Congratulations! Your order has been confirmed!') or contains(text(),'Order Placed!')]")
        ))
        print("[SUCCESS] Order placed successfully by registered user.")
        # Optional: Click Continue to complete flow
        continue_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-qa='continue-button']")))
        continue_button.click()

        # Immediately quit driver after clicking continue, no extra wait
        driver.quit()
        print("[INFO] Browser closed immediately after test.")

    except Exception as e:
        print(driver.page_source)  # Debug: see actual page content on failure
        driver.save_screenshot("order_failure.png")
        print("[ERROR] Test failed. Screenshot saved as 'order_failure.png'.")
        raise e
    finally:
        driver.quit()

def test_verify_contact_us_form_submission():
    driver = open_site("https://automationexercise.com")
    sleep(2)

    try:
        # Step 1: Go to “Contact Us” page
        driver.find_element(By.XPATH, "//a[text()=' Contact us']").click()
        sleep(2)

        assert "Get In Touch" in driver.page_source

        # Step 2: Fill required fields
        driver.find_element(By.NAME, "name").send_keys("Test User")
        driver.find_element(By.NAME, "email").send_keys("test123456@example.com")
        driver.find_element(By.NAME, "subject").send_keys("Test Subject")
        driver.find_element(By.ID, "message").send_keys("This is a test message.")

        # Optional file upload
        # driver.find_element(By.NAME, "upload_file").send_keys("/path/to/file.txt")

        # Step 3: Click "Submit" and handle alert
        driver.find_element(By.NAME, "submit").click()
        sleep(2)  # wait for alert to appear
        alert = driver.switch_to.alert
        alert.accept()
        sleep(2)

        # Step 4: Confirm success message
        assert "Success! Your details have been submitted successfully." in driver.page_source

        print("Test Passed: Contact form submitted and success message displayed.")

    except Exception as e:
        driver.save_screenshot("contact_form_error.png")
        print("[ERROR] Test failed. Screenshot saved as 'contact_form_error.png'.")
        raise e

    finally:
        driver.quit()


def test_scroll_to_top_button():
    driver = open_site("https://automationexercise.com")
    sleep(2)

    # Step 1: Scroll down the home page smoothly
    driver.execute_script("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});")
    sleep(3)  # Wait for smooth scroll to finish

    # Step 2: Click the “Scroll to Top” button
    driver.find_element(By.ID, "scrollUp").click()
    sleep(2)

    # Step 3: Verify no errors / glitches (check if button is still functional and not hidden/broken)
    assert driver.find_element(By.ID, "scrollUp").is_displayed()

    # Step 4: Confirm top of page is visible
    header_visible = driver.find_element(By.XPATH, "//div[@class='logo pull-left']/a/img").is_displayed()
    scroll_position = driver.execute_script("return window.pageYOffset;")

    assert header_visible
    assert scroll_position <= 100  # Accepting small offset due to animation

    print("Test Passed: 'Scroll to Top' button worked smoothly and returned view to top without UI issues.")
    driver.quit()


def test_scroll_to_top_button():
    driver = open_site("https://automationexercise.com")
    sleep(2)

    try:
        # Scroll down the page
        driver.execute_script("window.scrollTo({top: document.body.scrollHeight, behavior: 'smooth'});")
        sleep(3)

        # Click "Scroll to Top" button via JavaScript (to avoid ad iframe issues)
        scroll_btn = driver.find_element(By.ID, "scrollUp")
        driver.execute_script("arguments[0].click();", scroll_btn)
        sleep(2)

        # Verify it's back at the top
        header_visible = driver.find_element(By.XPATH, "//div[@class='logo pull-left']/a/img").is_displayed()
        scroll_position = driver.execute_script("return window.pageYOffset;")

        assert header_visible
        assert scroll_position <= 100  # Allow some animation tolerance

        print("Test Passed: 'Scroll to Top' button worked without ad-related issues.")

    except Exception as e:
        driver.save_screenshot("scroll_to_top_error.png")
        print("[ERROR] Test failed. Screenshot saved as 'scroll_to_top_error.png'.")
        raise e

    finally:
        driver.quit()

def test_logout_functionality():
    driver = open_site("https://automationexercise.com")
    sleep(2)

    # Step 1: Login
    driver.find_element(By.XPATH, "//a[text()=' Signup / Login']").click()
    sleep(2)
    driver.find_element(By.XPATH, "//input[@data-qa='login-email']").send_keys("test123456@example.com")  # Replace with valid email
    driver.find_element(By.XPATH, "//input[@data-qa='login-password']").send_keys("Aventura25")         # Replace with valid password
    driver.find_element(By.XPATH, "//button[@data-qa='login-button']").click()
    sleep(2)
    assert "Logged in as" in driver.page_source

    # Step 2: Click Logout button
    driver.find_element(By.XPATH, "//a[text()=' Logout']").click()
    sleep(2)

    # Step 3: Verify redirection to login page
    assert "login" in driver.current_url.lower()
    assert driver.find_element(By.XPATH, "//h2[text()='Login to your account']").is_displayed()

    # Step 4: Confirm user is logged out (no user-specific header)
    assert "Logged in as" not in driver.page_source

    print("Test Passed: User successfully logged out and redirected to login page.")
    driver.quit()

def test_sidebar_category_and_brand_navigation():
    driver = open_site("https://automationexercise.com")
    sleep(2)

    try:
        # Step 1: Click on a category from sidebar
        driver.find_element(By.XPATH, "//a[@href='#Women']").click()
        sleep(1)
        driver.find_element(By.XPATH, "//a[normalize-space(text())='Dress']").click()
        sleep(2)
        assert "women - dress products" in driver.page_source.lower()

        # Step 2: Verify products are shown
        products = driver.find_elements(By.XPATH, "//div[@class='productinfo text-center']/p")
        assert products
        assert all(p.is_displayed() for p in products)

        # Step 3: Click on a brand from sidebar
        polo_brand = driver.find_element(By.XPATH, "//a[text()='Polo']")
        driver.execute_script("arguments[0].scrollIntoView();", polo_brand)
        polo_brand.click()
        sleep(2)
        assert "brand - polo products" in driver.page_source.lower()

        # Step 4: Verify brand-filtered products
        brand_products = driver.find_elements(By.XPATH, "//div[@class='productinfo text-center']/p")
        assert brand_products
        assert all(p.is_displayed() for p in brand_products)

        print("Test Passed: Sidebar category and brand filters work correctly.")

    except Exception as e:
        driver.save_screenshot("sidebar_filter_error.png")
        print("[ERROR] Test failed. Screenshot saved as 'sidebar_filter_error.png'.")
        raise e

    finally:
        driver.quit()

def test_newsletter_subscription():
    driver = open_site("https://automationexercise.com")
    sleep(2)

    try:
        # Step 1: Scroll to the newsletter subscription input box
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(2)

        # Yes, 'susbscribe_email' is the actual ID on the site (typo preserved)
        assert driver.find_element(By.ID, "susbscribe_email").is_displayed()

        # Step 2: Enter valid email
        driver.find_element(By.ID, "susbscribe_email").send_keys("testnewsletter@example.com")

        # Step 3: Click the Subscribe button
        driver.find_element(By.ID, "subscribe").click()
        sleep(2)

        # Step 4: Check confirmation message (case-insensitive)
        assert "successfully subscribed" in driver.page_source.lower()

        print("Test Passed: Newsletter subscription completed and confirmation message displayed.")

    except Exception as e:
        driver.save_screenshot("newsletter_error.png")
        print("[ERROR] Test failed. Screenshot saved as 'newsletter_error.png'.")
        raise e

    finally:
        driver.quit()

