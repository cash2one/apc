# 基于OpenNebula的IaaS解决方案


## 需求分析

![需求分析](images/requirement.png?raw=true)


## 功能模块

* 普通用户
    * OAuth认证，初次登录的用户自动添加到系统
    * Email、SSH key修改
* 管理员
    * 基础设施
        * IDC
        * Cluster
        * CPU/Memory方案
        * 网段
        * 操作系统
    * 用户管理
        * 角色变更
* 宿主机
    * 查看
        * CPU、内存、磁盘（filesystem）
        * 下属虚拟机
    * 维护（ceph）
* 虚拟机
    * 基本功能
        * 申请
        * 列表、查询
        * 开机、关机、重启
        * 重建、删除
    * 访问
        * SSH key，修改即生效
        * VNC
    * 快照（ceph）
        * 磁盘快照
        * 恢复（关机）
    * 配置变更
        * CPU和内存的Resize（关机）
        * 网卡热插拔
        * 磁盘热插拔
        * datablock disk resize
    * 其他
        * 热迁移（ceph）
        * 监控
        * 操作日志
* 主面板
    * 宿主机、虚拟机数目
    * 使用率
    * 营收等
* 收费机制
    * 每分钟的job按照主机配置从Owner账户扣费
