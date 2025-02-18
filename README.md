# AUST-getElectricBill

## 项目简介

月复一月的被充电费所困扰，于是整了个获取电费的脚本来提醒自己还剩多少电，并能够自动充值，目前仅可用于淮南校区。

## 功能

- 定时获取剩余电量（默认每2小时获取一次），并在电量小于10度时通过pushplus推送消息
- 自动充值（默认关闭）

## 使用方法

1. 克隆项目到本地：
   ```bash
   git clone https://github.com/laizhangtu/AUST-getElectricBill.git
   cd AUST-getElectricBill
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 配置参数：
   在 `main.py` 的第 7 行到第 11 行填写你的 `PUSHPLUS_TOKEN`，`校区号`，`房间号`，`学号`，`密码（登录统一认证平台的密码，即 https://authserver.aust.edu.cn/authserver/login）` 。

4. 运行脚本：
   ```bash
   python main.py
   ```

## 开发计划

- 使合肥校区也能使用

## 贡献

欢迎 issue 和提交 PR。请确保在提交前先进行基础测试，并附上必要的说明。

## 许可证

此项目使用 GPL-3.0 许可证 。

