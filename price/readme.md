# 农场品价格

## 参考

[ShiXi_inWuhan](https://github.com/LouisYZK/ShiXi_inWuhan)

## 安装python依赖
```
pip3 install Py3AMF
pip3 install jsonlines
```

## crontab

```shell
# 每天23点50分获取数据
50 23 * * *  /usr/local/bin/python3 /Users/zhangzhiwen/github/spiders/price/price.py
```
