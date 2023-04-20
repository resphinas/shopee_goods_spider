

Here's a more polished version of your README file:

# Web Scraping Tool Deployment Guide

## Introduction

This guide provides instructions for deploying a web scraping tool that focuses on Python 3.7-3.8. The tool requires several dependencies, including `fake_useragent`, `httpx`, `redis`, `requests`, `threadpool`, and `tqdm`.

## Environment Setup

1. Activate the Virtual Environment

In the root directory, activate the virtual environment by running the following command in the terminal:

```sh
.\venv\Scripts\activate
```

2. Install Required Dependencies

Install the required dependencies by running the following command in the terminal:

```sh
pip install -r requirements
```

## Deployment Steps

Follow these steps to deploy the web scraping tool:

1. Configure the Config File

Specify the `host` and `checkpoint` parameters in the `config` file. 

2. Enable IP Support (Optional)

Start the `change_ip_windows_timely.py` script to enable IP support. If you don't need IP support, you can modify the `config` file.

3. Run the Tool

Run the following command in the terminal to initiate the tool:

```sh
python main_get_products_by_cat.py --host sg
```

Use the optional `--check_point` parameter to resume progress from a previous run.

Note: Steps A and B are not required unless updating the categories.

### Updating Categories

If you need to update the categories, execute the following steps:

A. Get the Categories

- Run `1.get_third(facet)_category.py` to collect all original category information.
- Run `2.create_tree_last.py` to parse the information based on custom JSON logic.

B. Manually Modify the Category Information

- Modify the network request URLs in the code by navigating to the Shopee website's homepage and a single category page.
- Manually put the generated `spider_categories.json` file into the `category_info` folder in the root directory.

## Directory Structure

```
E:.
├─catagories
│  ├─category_info        # All site-specific category-related information; do not modify or start this
│  ├─check_point          # Progress checkpoint storage
│  ├─data
│  │  ├─products          # Store keyword-related product information for store-level
│  │  │  ├─polymerization_products # The following are information storage for each platform
│  ├─external_api         # Monitoring API interface
│  ├─tools                # Tool package
│  ├─main_get_products_by_cat.py # Main file
│  ├─1.get_third(facet)_category.py # Get original category information
│  ├─2.create_tree_last.py # Parse according to original classification information
│  ├─3.ac_cert_d.txt      # Cookie; update when this parameter is invalid
│  ├─change_ip_windows_timely.py # Automatic update
│  ├─get_backups.py       # Get the category task provided by the backend
│  ├─selenium_capture    # Docking file for Super English CAPTCHA
│  ├─...
│  └─...
└─venv                    # Virtual environment files
   └─Lib                  # Virtual environment dependencies
      └─site-packages
``` 

## Version History

### V1.0.0

- Implemented normal collection across all platforms.
- Note: Captcha processing is required, but can be ignored when collecting small amounts of data. Taiwanese station IP proxies are complex.
