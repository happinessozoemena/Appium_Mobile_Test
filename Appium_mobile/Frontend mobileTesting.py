from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from appium.options.android import UiAutomator2Options
import time

def main(product_elements=None):
    # Define capabilities using UiAutomator2Options
    options = UiAutomator2Options()
    options.device_name = "Android Emulator"
    options.platform_name = "Android"
    options.platform_version = "12"
    options.app_package = "com.saucelabs.mydemoapp.rn"
    options.app = "C:/Users/USER/Downloads/Android-MyDemoAppRN.1.3.0.build-244.apk"
    options.app_activity = "com.saucelabs.mydemoapp.rn.MainActivity"
    options.automation_name = "UiAutomator2"
    options.no_reset = True

    driver = webdriver.Remote(command_executor="http://127.0.0.1:4723/wd/hub", options=options)
    wait = WebDriverWait(driver, 20)

    try:
        print("Opening menu...")
        menu_button = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="open menu"]')))
        menu_button.click()

        print("Clicking login...")
        login_button = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="menu item log in"]')))
        login_button.click()

        # NEGATIVE TEST 1
        print("Performing negative test 1...")
        username = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@content-desc="Username input field"]')))
        username.send_keys("happy")
        password = driver.find_element(AppiumBy.XPATH, '//android.widget.EditText[@content-desc="Password input field"]')
        password.send_keys("wrongP")
        login = driver.find_element(AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="Login button"]')
        login.click()
        time.sleep(2)

        # NEGATIVE TEST 2
        print("Performing negative test 2...")
        username = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@content-desc="Username input field"]')))
        username.clear()
        login.click()
        time.sleep(2)

        # LOGIN WITH VALID USERNAME AND PASSWORD
        print("Logging in with valid credentials...")
        username = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.EditText[@content-desc="Username input field"]')))
        username.send_keys("bob@example.com")
        password = driver.find_element(AppiumBy.XPATH,'//android.widget.EditText[@content-desc="Password input field"]')
        password.clear()
        password.send_keys("10203040")
        login.click()

        # Assert you are on the Product Page
        print("Asserting product page...")
        product = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.TextView[@text="Products"]')))
        assert product.text == "Products", "Failed to login to the product page"
        print("This is the Product page")

        # Sort page by "Price - Ascending"
        print("Sorting by price ascending...")
        sort_page = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="sort button"]')))
        sort_page.click()
        priceAscending = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.TextView[@text="Price - Ascending"]')))
        priceAscending.click()
        time.sleep(2)  # Give time for sorting to complete

        # Give a 5-star review to the first product
        if product_elements:
            first_product_name = product_elements[0].text
            print(f"Giving a 5-star review to {first_product_name}...")
            product_elements[0].click()
            review_button = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="Write a Review button"]')))
            review_button.click()
            stars = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="star rating 5"]')))
            stars.click()
            submit_review = driver.find_element(AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="Submit Review button"]')
            submit_review.click()
            print("Review submitted successfully.")

        # List of products to add to cart
        products_to_add = [
            'Sauce Labs Onesie',
            'Sauce Labs Bike Light',
            'Sauce Labs Bolt T-Shirt',
            'Test.allTheThings() T-Shirt',
            'Sauce Labs Backpack',
            'Sauce Labs Fleece Jacket'
        ]

        for product_name in products_to_add:
            print(f"Adding {product_name} to cart...")
            product_element = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, f'//android.widget.TextView[@content-desc="store item text" and @text="{product_name}"]')))
            product_element.click()
            add_to_cart_button = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="Add To Cart button"]')))
            add_to_cart_button.click()
            driver.back()

        # Click on My Cart Icon
        print("Clicking on My Cart icon...")
        cartIcon = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="cart badge"]/android.widget.ImageView')))
        cartIcon.click()

        # Assert that the items you added to cart are displayed correctly on the "My Cart" page
        print("Asserting My Cart page...")
        my_cart_page = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.TextView[@text="My Cart"]')))
        assert my_cart_page.text == "My Cart", "My Cart page is incomplete"
        print("My Cart page display correctly")

        # Remove any 2 items from the cart
        print("Removing 2 items from cart...")
        remove_buttons = driver.find_elements(AppiumBy.XPATH, '//android.widget.TextView[@text="Remove Item"]')
        for i in range(min(2, len(remove_buttons))):  # Ensure there are at least 2 items to remove
            remove_buttons[i].click()

            # Assert the number of items remaining in your cart
            print("Asserting number of items in cart...")
            remaining_items = driver.find_elements(AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="cart item"]')
            print(f"Number of items in cart: {len(remaining_items)}")

        # Click on the "Proceed to checkout" button
        print("Proceeding to checkout...")
        checkout = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="Proceed To Checkout button"]')))
        checkout.click()

        # Input your shipping details on the Checkout page
        print("Entering shipping details...")
        shipping_details = {
            'Full Name* input field': 'Happiness Ozoemena',
            'Address Line 1* input field': 'Mpape Juction',
            'Address Line 2 input field': 'Maitama 2',
            'City* input field': 'Fct',
            'State/Region input field': 'Abuja',
            'Zip Code* input field': '10009',
            'Country* input field': 'Nigeria'
        }
        for field, value in shipping_details.items():
            input_field = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, f'//android.widget.EditText[@content-desc="{field}"]')))
            input_field.send_keys(value)

            print(f"{field} entered successfully.")

        # Proceed to the payment page
        print("Proceeding to the payment page...")
        payment_button = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.TextView[@text="To Payment"]')))
        payment_button.click()

        # Assert that you are on the payment page
        print("Asserting payment page...")
        payment_page_title = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.TextView[@text="Enter a payment method"]')))
        assert payment_page_title.text == "Enter a payment method", "Not on the payment page"
        print("I am on the payment page")

        # Input your payment information
        print("Entering payment information...")
        payment_info = {
            'Full Name* input field': 'Jane Smith',
            'Card Number* input field': '4111111111111111',
            'Expiration Date* input field': '12/25',
            'Security Code* input field': '123'
        }
        for field, value in payment_info.items():
            input_field = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, f'//android.widget.EditText[@content-desc="{field}"]')))
            input_field.send_keys(value)

            print(f"{field} entered successfully.")

        # Click on the "Place order" button
        print("Placing order...")
        place_order_button = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.view.ViewGroup[@content-desc="Place Order button"]')))
        place_order_button.click()

        # Assert order completion
        print("Asserting order completion...")
        order_confirmation = wait.until(EC.presence_of_element_located((AppiumBy.XPATH, '//android.widget.TextView[@text="Thank you for your order"]')))
        assert order_confirmation.text == "Thank you for your order", "Order not completed successfully"
        print("Thank you for your order")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        driver.save_screenshot('error_screenshot.png')  # Save a screenshot on failure
    finally:
        driver.quit()

if __name__ == "__main__":
    main()