# TOC Project 2020

[![Maintainability](https://api.codeclimate.com/v1/badges/dc7fa47fcd809b99d087/maintainability)](https://codeclimate.com/github/NCKU-CCS/TOC-Project-2020/maintainability)

[![Known Vulnerabilities](https://snyk.io/test/github/NCKU-CCS/TOC-Project-2020/badge.svg)](https://snyk.io/test/github/NCKU-CCS/TOC-Project-2020)


Template Code for TOC Project 2020

A Line bot based on a finite state machine

More details in the [Slides](https://hackmd.io/@TTW/ToC-2019-Project#) and [FAQ](https://hackmd.io/s/B1Xw7E8kN)

## Setup

### Prerequisite
* Python 3.6
* Pipenv
* Facebook Page and App
* HTTPS Server

#### Install Dependency
```sh
pip3 install pipenv

pipenv --three

pipenv install

pipenv shell
```

* pygraphviz (For visualizing Finite State Machine)
    * [Setup pygraphviz on Ubuntu](http://www.jianshu.com/p/a3da7ecc5303)
	* [Note: macOS Install error](https://github.com/pygraphviz/pygraphviz/issues/100)


#### Secret Data
You should generate a `.env` file to set Environment Variables refer to our `.env.sample`.
`LINE_CHANNEL_SECRET` and `LINE_CHANNEL_ACCESS_TOKEN` **MUST** be set to proper values.
Otherwise, you might not be able to run your code.

#### Run Locally
You can either setup https server or using `ngrok` as a proxy.

#### a. Ngrok installation
* [ macOS, Windows, Linux](https://ngrok.com/download)

or you can use Homebrew (MAC)
```sh
brew cask install ngrok
```

**`ngrok` would be used in the following instruction**

```sh
ngrok http 8000
```

After that, `ngrok` would generate a https URL.

#### Run the sever

```sh
python3 app.py
```

#### b. Servo

Or You can use [servo](http://serveo.net/) to expose local servers to the internet.


## Finite State Machine
![fsm](./img/fsm.png)

## Usage
The initial state is set to `user`.

Every time `user` state is triggered to `advance` to another state, it will `go_back` to `user` state after the bot replies corresponding message.

* user
	* Input: "考古"
		* state: exam
		* Reply: "年級選擇"
		* Reply: 三個按鈕 1. 大一 2. 大二 3. 大三

			* Input: 選擇按鈕"大一"
				* state: first
		  		* Reply: "學期選擇"
		  		* Reply: 兩個按鈕 1. 大一上 2. 大一下

					* Input: 選擇按鈕"大一上"
						* state: first_1
		  				* Reply: "科目選擇"
		  				* Reply: 三個按鈕 1. 程設(一) 2. 普物(一) 3. 計概

							* Input: 選擇任一科目按鈕
		  						* Reply: 直接跳轉到該科目之Google雲端
						  
					* Input: 選擇按鈕"大一下"
						* state: first_2
		  				* Reply: "科目選擇"
		  				* Reply: 四個按鈕 1. 程設(二) 2. 普物(二) 3. 線代 4. 數導
						
							* Input: 選擇任一科目按鈕
		  						* Reply: 直接跳轉到該科目之Google雲端

			* Input: 選擇按鈕"大二"
				* state: second
	  			* Reply: "學期選擇"
	  			* Reply: 兩個按鈕 1. 大二上 2. 大二下

					* Input: 選擇按鈕"大二上"
						* state: second_1
		  				* Reply: "科目選擇"
		  				* Reply: 四個按鈕 1. 資結 2. 數導 3. 工數 4. 機統

							* Input: 選擇任一科目按鈕
								* Reply: 直接跳轉到該科目之Google雲端
					  
					* Input: 選擇按鈕"大二下"
						* state: second_2
						* Reply: "科目選擇"
						* Reply: 四個按鈕 1. 計組 2. 離散 3. 演算法 4. JAVA
							
							* Input: 選擇任一科目按鈕
								* Reply: 直接跳轉到該科目之Google雲端

			* Input: 選擇按鈕"大三"
				* state: third
	  			* Reply: "學期選擇"
	  			* Reply: 一個按鈕 1. 大三上

					* Input: 選擇按鈕"大三上"
						* state: third_1
						* Reply: "科目選擇"
						* Reply: 四個按鈕 1. 程設(一) 2. 計理 3. 微算機 4. 無線

							* Input: 選擇任一科目按鈕
								* Reply: 直接跳轉到該科目之Google雲端
				
						  
	* Input: "音樂"
		* state: music
		* Reply: 三個選擇介面 1. 讀書 2. 抒情 3. 嗨歌

			* Input: 選擇任一風格音樂
		  		* Reply: 直接跳轉到該類型之youtube搜尋網址

## Deploy
Setting to deploy webhooks on Heroku.

### Heroku CLI installation

* [macOS, Windows](https://devcenter.heroku.com/articles/heroku-cli)

or you can use Homebrew (MAC)
```sh
brew tap heroku/brew && brew install heroku
```

or you can use Snap (Ubuntu 16+)
```sh
sudo snap install --classic heroku
```

### Connect to Heroku

1. Register Heroku: https://signup.heroku.com

2. Create Heroku project from website

3. CLI Login

	`heroku login`

### Upload project to Heroku

1. Add local project to Heroku project

	heroku git:remote -a {HEROKU_APP_NAME}

2. Upload project

	```
	git add .
	git commit -m "Add code"
	git push -f heroku master
	```

3. Set Environment - Line Messaging API Secret Keys

	```
	heroku config:set LINE_CHANNEL_SECRET=your_line_channel_secret
	heroku config:set LINE_CHANNEL_ACCESS_TOKEN=your_line_channel_access_token
	```

4. Your Project is now running on Heroku!

	url: `{HEROKU_APP_NAME}.herokuapp.com/callback`

	debug command: `heroku logs --tail --app {HEROKU_APP_NAME}`

5. If fail with `pygraphviz` install errors

	run commands below can solve the problems
	```
	heroku buildpacks:set heroku/python
	heroku buildpacks:add --index 1 heroku-community/apt
	```

	refference: https://hackmd.io/@ccw/B1Xw7E8kN?type=view#Q2-如何在-Heroku-使用-pygraphviz

## Reference
[Pipenv](https://medium.com/@chihsuan/pipenv-更簡單-更快速的-python-套件管理工具-135a47e504f4) ❤️ [@chihsuan](https://github.com/chihsuan)

[TOC-Project-2019](https://github.com/winonecheng/TOC-Project-2019) ❤️ [@winonecheng](https://github.com/winonecheng)

Flask Architecture ❤️ [@Sirius207](https://github.com/Sirius207)

[Line line-bot-sdk-python](https://github.com/line/line-bot-sdk-python/tree/master/examples/flask-echo)
