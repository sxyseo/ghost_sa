# ghost_sa
open_server for sensorsdata

# 感谢：

感谢神策公司开源了他们的SDK，让用不起神策服务端的中小微企业也可以使用大数据带来的便利。

ghost_sa（鬼策）的结构设计主要考虑方便技术资源不足的中小微企业使用，部署测试快速，并支持复杂数据字段上报（神策原版不支持），所以在长时间段，多字段扫描的场景，性能不如神策原版。需要完整的神策，请购买神策官方授权，他们的程序很给力。https://www.sensorsdata.cn/?utm_source=github&utm_campaign=ghost_sa

# 贡献列表

https://github.com/phillip2019/ 规范了程序结构，提供beacon兼容，主流程优化等

# 介绍：

ghost_sa(鬼策)可以理解为不带前端界面的神策服务端。
主要功能有

1.接收 神策SDK 上报的数据 （与神策兼容）

2.实现神策上的短链创建与解析功能 （与神策兼容）

3.移动端广告监测功能（支持追溯移动端广告来源，支持信息流和积分墙两种模式）。（大部分与神策兼容，各有所长）

4.移动端激活回调 （与神策方式不同）

5.站外阅读监测与服务端二维码返回支持（也可用于邮件打开监测）（截止更新时，神策无此功能）

6.根据用户行为，触发动作 （截止更新时，神策无此功能）

7.定时任务 （截止更新时，神策仅定时分群）

8.用户分群 (与神策方式不同)

9.召回信息发送 （截止更新时，神策无此功能）

10.支持黑名单功能，便于提高一些免费邮件如阿里的授信，也减少其他渠道的无效召回浪费 （截止更新时，神策无此功能）

11.接入控制功能，结合CDN实现反爬虫，结合后端服务实现反作弊，反羊毛等。（截止更新时，神策无此功能）

使用了flask框架，可以通过gunicorn部署。数据库建议使用TiDB，实测1天200万事件量，单次查询当天事件在10毫秒左右，查询1个月范围的数据，返回在30-60秒左右。
实际使用在TiDB最低的配置3x8c_32g的情况下，每天可以支持500万的事件量。
如果只是体验和测试功能，也可以用MySQL 5.7（含）以上的版本，不过性能很差。

支持使用Kafka。

目前经过测试，支持IOS，Android，JS，小程序，Python的SDK上报。
SDK可以在神策的项目中下载 https://github.com/sensorsdata
SDK的使用方法，可以直接查看神策官方文档 https://www.sensorsdata.cn/manual/?utm_source=github&utm_campaign=ghost_sa


# 框架说明：

/flask_main.py <--主程序，执行后即可开始接收数据

/kafka_consumer.py <--Kafka订阅程序（如果开启Kafka支持，使用此程序订阅并写入数据库）

/scheduler.py <--定时器程序，用来定时触发进行用户分群等任务

/trigger.py <--触发器订阅程序（如果配置了非独立触发器，则在写入埋点时同步触发，无需运行触发器。独立触发器不受插库性能影响，响应速度更快。而且独立增删触发器的时候，不用担心入库数据中断。）

/configs <--配置，包括查询密码，数据库密码，第三方依赖的密码都在这里配置

/component <--主要组件，运行程序所需要的主要组件都在这里

/component/messenger.py <--消息自动发送程序（发送消息列表里符合时间要求且标记为自动的消息）

/scheduler_jobs <--用户分群与自动召回的相关组件

/scheduler_jobs/scheduler_job_creator.py <--自动分群任务创建程序和自动召回模板创建程序

/geoip <--IP和ASN识别组件，下载的mmdb需要放在这里

/image <--需要返回的1像素图片所在处。当然，不嫌流量贵，也可以换成其他图片哈

/tools <--迁移工具，包括实时同步神策的数据和迁移历史数据进入鬼策

/logs <--日志，目前只会记录错误日志，按天分

/data_export <--迁移用数据，存放神策历史数据，用于导入鬼策。导入完后，可删除

/trigger_jobs <--动作触发器所触发的动作。


# 安装初始化：

安装之前需要先准备好数据库，测试功能可以用mysql5.7。

！！！正式环境建议使用tidb或其他newsql。

1.打开/geoip/geo.py 文件，根据文件里的地址，下载ipcity和ipasn文件，并放到/geoip目录下。

2.配置/configs/db.py 里的数据库连接参数。

3.打开/configs/admin.py 修改查询密码和Kafka支持（默认关闭，直接写入数据）。如果开启Kafka支持，需要配置/configs/kafka.py和运行/kafka_consumer.py来订阅数据。

4.打开/component/setup.py 在最后一行修改自己想要创建的项目名。运行setup.py程序，会完成数据表创建，鬼策服务端初始化完成。

5.运行/flask_main.py 可以开始接收数据了。


# 注意：

鬼策在基本功能上将持续依赖神策SDK，并持续维护兼容和可迁移性。

但鬼策在产品理念与路线上与神策有差异，神策倾向给运营赋能，对运营友好，鬼策倾向自动化运营取代传统运营，对技术友好。所以在一些高级功能，特别是理念不同的方面，将采取完全不同的产品路线，功能也会存在不兼容的情况，大家各取所需，尽量支持神策原版，有了神策开源，才有的鬼策。

鬼策没有兼容魔改神策SDK且不注明源于神策的各种程序的计划。吃水不忘挖井人是对开源社区基本的尊重。

目前已知问题问的比较频繁的有：

1.鬼策不支持beacon方式上报 https://github.com/white-shiro-bai/ghost_sa/issues/27 使用鬼策建议js用image方式，其他端用默认方式即可。

这个请参考神策官方文档 https://manual.sensorsdata.cn/sa/latest/tech_sdk_client_web_high-7549300.html?utm_source=github&utm_campaign=ghost_sa 的相关说明：( 神策系统 1.10 版本以后 ) 支持使用 'ajax' 和 'beacon' 方式发送数据，这两种默认都是 post 方式， beacon 方式兼容性较差。

2.不支持神策的新版本可视化全埋点功能，所以请使用较新SDK的用户，根据神策文档 https://manual.sensorsdata.cn/sa/latest/enable_visualized_autotrack-7548675.html?utm_source=github&utm_campaign=ghost_sa 关闭 可视化全埋点功能，减少报错。

# 更多文档：

wiki  https://github.com/white-shiro-bai/ghost_sa/wiki

讨论组 https://github.com/white-shiro-bai/ghost_sa/discussions

国内用户可以加我微信 Ben_Xiaobai ，加入鬼策微信群。请直奔主题，不要绕来绕去。

也可以通过视频，了解鬼策。这里有一个以鬼策为基础的视频分析课（还在佛系更新）

https://space.bilibili.com/920446/channel/detail?cid=124583&utm_source=github&utm_campaign=ghost_sa


# 2020年12月28日版本升级注意事项(to_20201015)：

1.鬼策老用户如需升级2020年12月28日及以后的版本，须文件覆盖后，运行/tools/update_base_to_20201015.py程序升级数据表。该操作不可逆，但升级后的数据表与老版本鬼策兼容。但程序与老版本鬼策不兼容，需要完整覆盖安装目录才能继续运行。建议新老版本分开两个目录放置。clone新目录->升级->运行新目录的程序即可。

2.由于TiDB v4的新特性，鬼策缩短了一些之前预留较长的字段，以提高兼容性，mysql版本也不需要额外使用安装程序，统一使用/component/setup.py安装即可。缩短后我已经在生产环境使用超过半个月，尚无不良影响。如果您的应用环境特殊，请谨慎升级TiDB到v4及以后版本，并自行修改建表程序中的字段长度。如果您的鬼策是在TiDB v3环境下安装的，那么升级到TiDB v4后，字段长度不会改变，依然有效。

# 2021年03月15日版本升级注意事项(to_20210226)：

1.2020年12月28日之前版本的鬼策老用户如需升级2021年03月15日及以后的版本，须文件覆盖后，运行/tools/update_base_to_20210226.py程序升级数据表。或2020年12月28日之后版本的鬼策老用户如需升级2021年03月15日及以后的版本，须文件覆盖后，运行/tools/update_20201015_to_20210226.py程序升级数据表。该操作不可逆，但升级后的数据表与老版本鬼策兼容。但程序与老版本鬼策不兼容，需要完整覆盖安装目录才能继续运行。建议新老版本分开两个目录放置。clone新目录->升级->运行新目录的程序即可。

2.黑名单开关可以在configs/admin.py里配置

# 2021年05月19日版本升级注意事项(to_20210406)：

1.2021年5月19日之前的版本升级到这个版本，须文件覆盖后，运行/tools/下对应的版本to_20210406的程序升级数据库。

2.接入控制的全局参数在"configs/admin.py"里配置。项目全局阈值在project_list表里配置。事件阈值在{project}_properties里配置。事件优先于项目全局优先于全局。具体可在"docs/接入控制"下找到文档，包含整个功能的介绍

3.该版本后，将不再提供跨版本的升级程序。今后再发布更新，将仅提供从该版本升级或全新安装。

4.此次更新修改了trigger功能kafka消费组的名字。如果独立订阅的，为了避免部分数据重复。所以默认订阅方式改为了latest。可在/configs/kafka.py下自行修改为需要的订阅方式。





# 近期大版本迭代规划，可能会延期：

2021年10月<-支持oCPC广告位管理，支持第三方回调及第三方监测（如秒针)，简单的效果管理，支持静默广告功能（如刷公众号，刷阅读量，刷SEO等）


------------以上可能为1.0版本除bug修复外的最后一次功能------------


2022年一季度 <- 重构2.0版本，可能延期

计划合并部分 https://github.com/phillip2019/ghost_sa 代码：

提高代码质量，降低早期因为不会写造成的潜在风险。提高beacon的兼容性，改进日志功能，优化性能。

计划改进：

时间戳精度提高到16位

ip信息可选等级，降低冗余数据量

可选内存缓存，减少update数量，提高性能

支持Hadoop，clickhouse等其他类型数据库

ghost_console（管理端）功能补齐

增加连接池，提高高并发性能

召回功能适配更多的渠道，兼容OAID和CAID。

支持项目管理和神策的crc校验功能，减少恶意攻击和恶意刷量。