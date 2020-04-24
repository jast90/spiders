# 中国行政区划爬虫

## 数据涞源

- [统计用区划和城乡划分代码](http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/)

## 分析

### URL规则

- 根URL：`http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/2019/`

### 具体的行政区划

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

### 数据统计

#### 省、市、区、乡/镇、村/社区个数

|省|市|区|乡/镇|村/社区|
|---|---|---|---|---|
|31|342|2991|43027|656781|

```sql
SELECT 
    CASE
        WHEN level = 0 THEN '省'
        WHEN level = 1 THEN '市'
        WHEN level = 2 THEN '区'
        WHEN level = 3 THEN '乡/镇'
        WHEN level = 4 THEN '村/社区'
    END as name,
    COUNT(level)
FROM
    node
GROUP BY level
```

#### 省之最 TODO

##### 市最多的省

##### 区最多的省

##### 乡/镇最多的省

##### 村/社区最多的省
