-- 建库 美国区
CREATE KEYSPACE kavoutdata WITH replication = {'class': 'NetworkTopologyStrategy', 'dc1': '2', 'dc2': '2'}  AND durable_writes = true;

use kavoutdata;

-- stock ratio value  股票指数信息
create table if not exists stock_ratio_from_10jqka(
	symbol               text    , -- 代码
	name                 text    , -- 名称
	date                 date    , -- 日期
	price                text    , -- 现价
	size_ratio           text    , -- 涨跌幅(%)
	rise_fall            text    , -- 涨跌
	changed_hands_ratio  text    , -- 换手(%)
	volume               text    , -- 成交量
	pe_ratio             text    , -- 市盈率(%)
	turnover             text    , -- 成交额
	week_high_52         text    , -- 52周最高
	weeks_minimum_52     text    , -- 52周最低

	PRIMARY KEY(symbol, date)
) WITH CLUSTERING ORDER BY(date DESC);


-- stock detial value  股票基本信息
create table if not exists stock_basic_from_10jqka(
	symbol               text    , -- 代码
	name                 text    , -- 名称
	rt                   text    , -- 交易时间
	total                text    , -- 总交易日数量
	start                date    , -- 上市日期
	year                 text    , -- 每年度交易日数量

	PRIMARY KEY(symbol, name)
) WITH CLUSTERING ORDER BY(name ASC);


-- stock daily trading list  每日股票交易股票号码表  取自同花顺
create table if not exists stock_daily_symbol_list_from_10jqka(
	trading_date         date    , -- 日期
	symbols              text    , -- 代码

	PRIMARY KEY(trading_date)
);

-- stock daily trading list  每日股票交易股票号码表 取自Kibot
create table if not exists stock_daily_symbol_list_from_Kibot(
	trading_date         date    , -- 日期
	symbols              text    , -- 代码

	PRIMARY KEY(trading_date)
);

-- stock daily trading list  每日股票交易股票号码表  取自quandl
create table if not exists stock_daily_symbol_list_from_quandl(
	trading_date         date    , -- 日期
	symbols              text    , -- 代码

	PRIMARY KEY(trading_date)
);

-- stock daily value  股票日级别交易信息 【不复权】
create table if not exists stock_daily_off_share_from_10jqka(
	symbol               text    , -- 代码
	name                 text    , -- 名称
	date                 date    , -- 交易日期
	open                 float   , -- 开盘价格
	high                 float   , -- 最高价格
	low                  float   , -- 最低价格
	close                float   , -- 收盘价格
	volumn               float   , -- 交易量

	PRIMARY KEY(symbol, date)
) WITH CLUSTERING ORDER BY(date DESC);

-- stock daily value  股票日级别交易信息 【前复权】
create table if not exists stock_daily_adj_share_from_10jqka(
	symbol               text    , -- 代码
	name                 text    , -- 名称
	date                 date    , -- 交易日期
	open                 float   , -- 开盘价格
	high                 float   , -- 最高价格
	low                  float   , -- 最低价格
	close                float   , -- 收盘价格
	volumn               float   , -- 交易量

	PRIMARY KEY(symbol, date)
) WITH CLUSTERING ORDER BY(date DESC);
