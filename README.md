# 爬虫应用

## 实现语言

通过Python实现

## 目的

学习`python`以及公用数据

## 实例

### 中国行政区划爬虫

#### 数据涞源

-[统计用区划和城乡划分代码](http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/)

#### 分析

##### URL规则

根URL：`http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/`

##### 具体的行政区划

- 省、直辖市获取
`tr.provincetr`
- 市、市辖区获取
`tr.citytr`
- 县、区获取
`tr.countytr`
- 城镇、市镇获取
`tr.towntr`
- 村、社区获取
`tr.villagetr`

#### 源码

[china-administrative-divisions](./china-administrative-divisions)