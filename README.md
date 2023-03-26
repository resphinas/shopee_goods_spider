DEMO
===========================

###########环境依赖
python 3.7-3.8
fake_useragent==0.1.11
httpx==0.23.0
redis==4.3.4
requests==2.28.1
threadpool==1.3.2
tqdm==4.64.1

###########部署步骤

0. 首先执行虚拟环境 在根目录 直接运行 .\venv\Scripts\activate 启动虚拟环境

1. pip install -r requirements //安装运行依赖


3. 具体文件运行步骤

## ab 两个步骤暂时不需要再运行(除非需要更新分类),直接运行下面c步骤即可

[//]: # (a. 1.get_third(facet)_category.py  //采集所有原始分类信息)

         b. 2.create_tree_last.py //根据自定义json逻辑 解析
		a步骤在根目录生成all_categories.txt
		b步骤在all_categories.txt的基础上生成spider_categories.json 
		暂时没有写这方面自动化的逻辑 时间不够测试 所以目前如果确实需要更新分类，需要动的步骤如下
		进入虾皮某站点主页 获取a步骤中的网络请求url 并且进行更改
		进入虾皮单个分类 获取a步骤中的第二个网络请求url 并且进行更改
		手动将 生成的spider_categories.json 放入根目录下的category_info中
		
	   c.此步骤为核心步骤
			1.进行config文件配置 超参数无错方案目前支持 host 和 checkpoint  ，详情请查看超参数帮助信息
			1.2 请启动change_ip_windows_timely.py 进行ip支持 如不用 则修改config.py中的配置即可
			2. 为避免进度条失效 在终端运行 python  main_get_products_by_cat.py --host sg(根据需要自行更改) --check_point(可选参数，选择则进行进度读取)
			

###########目录结构描述

E:.
├─catagories
│ ├─category_info // 全站点分类相关信息 无必要不改动 不启动
│ ├─check_point // 进度存储点
│ ├─data // 采集文件存放
│ │ ├─products // 店铺层面的关键词相关商品信息
│ │ │ ├─polymerization_products 下面是各平台的信息存储 
│ ├─external_api // 监控api接口
│ ├─tools //工具包
│ ├main_get_products_by_cat.py //运行主文件
│ ├1.get_third(facet)_category.py //获取原始分类信息
│ ├2.create_tree_last.py //根据原始分类信息进行解析
│ ├3.ac_cert_d.txt //cookie 此参数失效时进行更新
│ ├change_ip_windows_timely.py //自动更新
│ ├get_backups.py //获取后端提供的分类任务
│ ├selenium_capture //对接超级英的验证码打码文件
│ ├ ..
│ ├ ...
│ └ ....
└─venv //虚拟环境文件
├─Lib //虚拟环境依赖
│ └─site-packages


###########V1.0.0 版本内容更新
实现全平台正常采集 
缺陷：
	验证码需要处理，少量采集时可以忽略
	台湾站的ip代理比较复杂
	
	
	
Title: Deployment Steps for Web Scraping Tool

Introduction:
The following is a guide for deploying a web scraping tool, with a focus on Python 3.7-3.8. The tool requires several dependencies, including fake_useragent, httpx, redis, requests, threadpool, and tqdm.

Step 1: Activate the Virtual Environment
In the root directory, activate the virtual environment by running ".\venv\Scripts\activate" in the terminal.

Step 2: Install Required Dependencies
Install the required dependencies by running "pip install -r requirements" in the terminal.

Step 3: Run the Tool
To run the tool, execute the following steps:

Configure the config file, specifying host and checkpoint parameters.
Start the change_ip_windows_timely.py script to enable IP support, or modify the config file if not using IP support.
Run "python main_get_products_by_cat.py --host sg" in the terminal to initiate the tool. Use the optional "--check_point" parameter to resume progress from a previous run.
Note: Steps A and B are not required unless updating the categories.

Step A: Get the Categories
To update the categories, execute the following steps:

Run "1.get_third(facet)_category.py" to collect all original category information.
Run "2.create_tree_last.py" to parse the information based on custom JSON logic.
Manually modify the spider_categories.json file as needed based on network request URLs obtained from the Shopee site.
Step B: Directory Structure
The directory structure for the tool is as follows:
E:.
├─catagories
│ ├─category_info
│ ├─check_point
│ ├─data
│ │ ├─products
│ │ │ ├─polymerization_products
│ ├─external_api
│ ├─tools
│ ├main_get_products_by_cat.py
│ ├1.get_third(facet)_category.py
│ ├2.create_tree_last.py
│ ├3.ac_cert_d.txt
│ ├change_ip_windows_timely.py
│ ├get_backups.py
│ ├selenium_capture
│ ├ ..
│ ├ ...
│ └ ....
└─venv
├─Lib
│ └─site-packages

Version 1.0.0 updates:

Achieved successful scraping for all platforms.
Known issue: requires captcha processing, which can be ignored for small scraping jobs. IP proxy for Taiwan site is complex.
