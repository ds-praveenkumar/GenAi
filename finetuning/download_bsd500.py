#/**
# * ====================================================
# * @file        download_bsd500.py
# * @author      Praveen Kumar
# * @created     2025-07-15
# * @last updated 2025-07-15
# * @version     1.0.0
# *
# *
# * @description Download BSD500
# *
# * @usage       node download_bsd500.py
# * @dependencies None
# *
# * @license     MIT
# * ====================================================
# */

import kagglehub

path = kagglehub.dataset_download("dorisdan/bsds500")

print("Path to dataset files:", path)