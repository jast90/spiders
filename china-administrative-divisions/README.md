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

#### redis中缓存页面数

`46392` 包含：省、市、区、乡页面

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

#### 查询省、市、区、乡、村

```sql
-- 1
select p.* ,c.* ,c1.*,c2.*,c3.*
from node p
left join node c on c.parent_id=p.id
left join node c1 on c1.parent_id = c.id
left join node c2 on c2.parent_id = c1.id
left join node c3 on c3.parent_id = c2.id
where p.level=0
order by p.code,c.code;

-- 2
-- 2比1快
select * from (select * from node where level=0) p
left join node c on c.parent_id=p.id
left join node c1 on c1.parent_id = c.id
left join node c2 on c2.parent_id = c1.id
left join node c3 on c3.parent_id = c2.id
order by p.code,c.code;
```

##### 十万级数据查询优化

**从查询失败到成功，能够从几十秒到毫秒呢？**

- 未建索引时查询超过了`connect_timeout`设置的值

- 在`parent_id`、`level`上分别创建索引后查询结果如下：

```
656784 row(s) returned 53.491 sec / 28.442 sec
```


#### 省之最 TODO

##### 市最多的省

##### 区最多的省

##### 乡/镇最多的省

##### 村/社区最多的省
