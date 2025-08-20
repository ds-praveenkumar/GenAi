#===============================================================================
#  File Name    : browser_use.py
#  Project Name : Project Name
#  Description  : 
#    Description of this file

#  Author       : Praveen Kumar
#  Created On   : 2025-08-20
#  Last Updated : 2025-08-20
#  Version      : v1.0.0

#  Language     : Python
#  File name    : browser_use.py
#  Dependencies : 
#    - Dependency 1
#    - Dependency 2

#  Inputs       : Expected inputs
#  Outputs      : Expected outputs
#  Usage        : 
#    Example usage

#  Notes        : 
#    - Notes or TODOs
#===============================================================================

from playwright.sync_api import sync_playwright, Page, expect
import re
import time
from dotenv import load_dotenv
load_dotenv(".env")
import os
ph = os.getenv("PHONE")

def rail_wire_login(page: Page):
    page.goto("https://jh.railwire.co.in/Websitebsscntl")

    box = page.get_by_role("textbox")
    box.fill(ph)
    page.get_by_role("button", name="submit").click()
    otp = input("Enter OTP: ")
    enter_otp = page.get_by_role("textbox", name="otp")
    enter_otp.fill(otp)
    page.get_by_role("button", name="ok").click()
    page.get_by_role("button", name="submit").click()
    page.get_by_text("my receipts").click()
    download_file(page)
    
def download_file(page: Page):
    page.locator("text=/^RWJH/").first.click()
    with page.expect_download() as download_info:
    # Perform the action that initiates download
        page.get_by_role("link", name="Download PDF").click()
    download = download_info.value
    download.save_as("bill.pdf")
    print("Download completed")
    # page.pause()

    
if __name__ == "__main__":
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        rail_wire_login(page)
        context.close()
        browser.close()