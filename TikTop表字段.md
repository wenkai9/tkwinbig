

## 	tk_anchor_rawdata(主播数据)



| 参数名            | 类型          | 描述                                     |
| ----------------- | ------------- | ---------------------------------------- |
| id                | int(10)       | 作为主键 记录id                          |
| unique_id         | varchar(1024) | 主播的id                                 |
| aweme_id          | vachar(64)    | 视频的id                                 |
| keyword           | varchar(1024) | 主播的关键词或标签                       |
| product_id        | varchar(64)   | 产品的id                                 |
| title             | varchar(4096) | 条目的标题或名称                         |
| market_price      | int(11)       | 产品的价格                               |
| in_shop           | bool          | 产品是否可用(1表示是，0表示否)           |
| ad_lable_position | varchar(32)   | 广告标签的位置                           |
| mix_product_type  | varchar(32)   | 混合产品的类型                           |
| seller_id         | varchar(64)   | 卖家id                                   |
| componet_key      | varchar(64)   | 组件id                                   |
| product_cnt       | int(11)       | 产品数量                                 |
| is_ec_video       | bool          | 视频是否是电子商务视频(1表示是，0表示否) |

## tk_author_rawdata(作者数据)



| 参数名                    | 类型    | 描述                                           |
| ------------------------- | ------- | ---------------------------------------------- |
| **id**                    | int     | 作者数据的唯一标识符，通常用于数据库的主键     |
| **aweme_count**           | int     | 作者发布的视频数量                             |
| **download_setting**      | int     | 下载设置，可能表示作者对视频下载的偏好设置     |
| **favoriting_count**      | int     | 被收藏的次数，即作者的视频被其他用户收藏的次数 |
| **follower_count**        | int     | 粉丝数，即关注该作者的用户数量                 |
| **following_count**       | int     | 关注数，即该作者关注的其他用户数量             |
| **friends_status**        | int     | 好友状态，可能表示作者和其他用户之间的关系状态 |
| **google_account**        | varchar | 绑定的 Google 账号                             |
| **has_email**             | bool    | 是否有邮箱                                     |
| **is_ad_fake**            | bool    | 是否是假广告                                   |
| **nickname**              | varchar | TikTok昵称                                     |
| **original_music_count**  | int     | 原创音乐数量                                   |
| **relative_users**        | varchar | 相关用户                                       |
| **total_favorited**       | int     | 视频被收藏的总次数                             |
| **twitter_id**            | varchar | 绑定的Twitter 用户 ID                          |
| **twitter_name**          | varchar | 绑定的Twitter 用户名                           |
| **uid**                   | varchar | 作者TikTop的uid                                |
| **unique_id**             | varchar | 唯一id                                         |
| **user_mode**             | int     | 用户模式                                       |
| **user_rate**             | int     | 用户评级                                       |
| **user_tags**             | varchar | 用户标签                                       |
| **verification_type**     | int     | 认证类型                                       |
| **with_commerce_entry**   | bool    | 是否有商业入口                                 |
| **with_shop_entry**       | bool    | 是否有商店入口                                 |
| **youtube_channel_id**    | varchar | YouTube 频道 ID                                |
| **youtube_channel_title** | varchar | YouTube 频道名称                               |
| **youtube_expire_time**   | int     | YouTube 频道过期时间                           |
| **ins_id**                | varchar | Instagram 用户 ID                              |
| **author_user_id**        | varchar | 作者 ID                                        |

## tk_video_rawdata(视频数据)

| 参数名                      | 类型    | 描述             |
| --------------------------- | ------- | ---------------- |
| **id**                      | int     | 视频id           |
| **unique_id**               | varchar | 视频标识id       |
| **aweme_id**                | varchar | 视频唯一id       |
| **aweme_type**              | int     | 视频类型         |
| **bodydance_score**         | int     | 舞蹈得分         |
| **adv_promotable**          | bool    | 是否可以推广     |
| **bc_label_test_text**      | varcahr | 标签测试文本     |
| **auction_ad_invited**      | bool    | 是否邀请竞拍广告 |
| **branded_content_type**    | int     | 品牌内容类型     |
| **content_type**            | varchar | 内容类型         |
| **create_time**             | int     | 创建时间         |
| **video_desc**              | varchar | 视频描述         |
| **creation_used_functions** | varchar | 创建使用的功能   |
| **distribute_type**         | int     | 分发类型         |
| **group_id**                | vachar  | 分组 ID          |
| **has_danmaku**             | bool    | 是否有弹幕       |
| **has_promote_entry**       | int     | 是否有推广入口   |
| **has_vs_entry**            | bool    | 是否有 VS 入口   |
| **material_index**          | varchar | 素材索引         |
| **track_info**              | text    | 轨迹信息         |
| **type**                    | int     | 类型             |
| **is_ads**                  | bool    | 是否广告         |
| **is_hash_tag**             | bool    | 是否是哈希标签   |
| **label_top_text**          | varchar | 顶部标签文本     |
| **music_title_style**       | int     | 音乐标题样式     |
| **products_info**           | varchar | 产品信息         |
| **promote_toast**           | varchar | 推广提示         |
| **collect_count**           | int     | 收藏数           |
| **comment_count**           | int     | 评论数           |
| **digg_count**              | int     | 点赞数           |
| **download_count**          | int     | 下载数           |
| **forward_count**           | int     | 转发数           |
| **lose_comment_count**      | int     | 失去评论数       |
| **lose_count**              | int     | 失去数           |
| **play_count**              | intint  | 播放数           |
| **repost_count**            | int     | 转发数           |
| **share_count**             | int     | 分享数           |
| **whatsapp_share_count**    | int     | WhatsApp 分享数  |
| **support_danmaku**         | bool    | 是否支持弹幕     |
| **hashtag_id**              | varchar | 哈希标签 ID      |
| **hashtag_name**            | varchar | 哈希标签名称     |
| **duration**                | int     | 视频时长         |
| **has_watermark**           | bool    | 是否有水印       |
| **video_labels**            | varchar | 视频标签         |
| **region**                  | varchar | 地区             |
| **allow_download**          | bool    | 是否允许下载     |
| **allow_duet**              | bool    | 是否允许二重唱   |
| **allow_stitch**            | bool    | 是否允许缝合     |
| **allow_react**             | bool    | 是否允许回应     |
| **is_commerce_music**       | bool    | 是否商业音乐     |
| **title**                   | varchar | 标题             |
| **author**                  | varchar | 作者             |
| **user_count**              | int     | 用户数           |
| **album**                   | varchar | 专辑             |
| **handle**                  | varchar | 处理             |
| **cha_name**                | varchar | CHA 名称         |
| **cid**                     | varchar | Cid              |
| **share_info**              | varchar | 分享信息         |
| **video_text**              | varchar | 视频文本         |

