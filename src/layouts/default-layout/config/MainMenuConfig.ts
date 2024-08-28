import type { MenuItem } from "@/layouts/default-layout/config/types";

const MainMenuConfig: Array<MenuItem> = [
  {
    pages: [
      {
        heading: "dashboard",
        route: "/dashboard",
        keenthemesIcon: "element-11",
        bootstrapIcon: "bi-app-indicator",
      },
      // {
      //   heading: "layoutBuilder",
      //   route: "/builder",
      //   keenthemesIcon: "switch",
      //   bootstrapIcon: "bi-layers",
      // },
    ],
  },
  // 投放管理
  {
    // heading: "launchmanagement",
    route: "/launchmanagement",
    pages: [
      {
        sectionTitle: "authentication",
        keenthemesIcon: "fingerprint-scanning",
        bootstrapIcon: "bi-sticky",
        sub: [
          {
            sectionTitle: "basicFlow",
            sub: [
              {
                heading: "signIn",
                route: "/sign-in",
              },
              {
                heading: "signUp",
                route: "/sign-up",
              },
              {
                heading: "passwordReset",
                route: "/password-reset",
              },
            ],
          },
          {
            heading: "multiStepSignUp",
            route: "/multi-step-sign-up",
          },
          {
            heading: "error404",
            route: "/404",
          },
          {
            heading: "error500",
            route: "/500",
          },
        ],
      },
      {
        sectionTitle: "投放管理",
        route: "/launchmanagement",
        keenthemesIcon: "chart-line-up",
        sub: [
          {
            heading: "物品管理",
            route: "/launchmanagement/itemmanagement/ItemManagement",
          }, {
            heading: "投放管理",
            route: "/launchmanagement/launchmanagement",
          },
          {
            heading: "效果数据",
            route: "/launchmanagement/effectdata/EffectData",
          }, {
            heading: "商品展示",
            route: "/launchmanagement/goods/index",
          },
          // {
          //   heading: "RPA私信",
          //   route: "/launchmanagement/rpa/index",
          // },
          // {
          //   heading: "RPA建联",
          //   route: "/launchmanagement/rpainvitation/index",
          // }

        ]
      },


    ]
  },
  // {
  //   route: "/rpa",
  //   pages: [
  //     {
  //       sectionTitle: "authentication",
  //       keenthemesIcon: "fingerprint-scanning",
  //       bootstrapIcon: "bi-sticky",
  //       sub: [
  //         {
  //           sectionTitle: "basicFlow",
  //           sub: [
  //             {
  //               heading: "signIn",
  //               route: "/sign-in",
  //             },
  //             {
  //               heading: "signUp",
  //               route: "/sign-up",
  //             },
  //             {
  //               heading: "passwordReset",
  //               route: "/password-reset",
  //             },
  //           ],
  //         },
  //         {
  //           heading: "multiStepSignUp",
  //           route: "/multi-step-sign-up",
  //         },
  //         {
  //           heading: "error404",
  //           route: "/404",
  //         },
  //         {
  //           heading: "error500",
  //           route: "/500",
  //         },
  //       ],
  //     },
  //     {
  //       sectionTitle: "RPA管理",
  //       route: "/rpa",
  //       keenthemesIcon: "paper-clip",
  //       sub: [
  //         {
  //           heading: "RPA私信",
  //           route: "/rpa/rpa/index",
  //         },
  //         {
  //           heading: "RPA建联",
  //           route: "/rpa/rpainvitation/index",
  //         }

  //       ]
  //     },
  //   ]
  // },
  {
    route: "/productsearch",
    pages: [
      {
        sectionTitle: "authentication",
        keenthemesIcon: "fingerprint-scanning",
        bootstrapIcon: "bi-sticky",
        sub: [
          {
            sectionTitle: "basicFlow",
            sub: [
              {
                heading: "signIn",
                route: "/sign-in",
              },
              {
                heading: "signUp",
                route: "/sign-up",
              },
              {
                heading: "passwordReset",
                route: "/password-reset",
              },
            ],
          },
          {
            heading: "multiStepSignUp",
            route: "/multi-step-sign-up",
          },
          {
            heading: "error404",
            route: "/404",
          },
          {
            heading: "error500",
            route: "/500",
          },
        ],
      },
      // {
      //   sectionTitle: "商品检索",
      //   route: "/productsearch",
      //   keenthemesIcon: "purchase",
      //   sub: [
      //     {
      //       heading: "商品查询",
      //       route: "/productsearch/index",

      //     }]
      // }


    ]
  },
  {
    // heading: "usercenter",
    route: "/usercenter",
    pages: [
      {
        sectionTitle: "authentication",
        keenthemesIcon: "fingerprint-scanning",
        bootstrapIcon: "bi-sticky",
        sub: [
          {
            sectionTitle: "basicFlow",
            sub: [
              {
                heading: "signIn",
                route: "/sign-in",
              },
              {
                heading: "signUp",
                route: "/sign-up",
              },
              {
                heading: "passwordReset",
                route: "/password-reset",
              },
            ],
          },
          {
            heading: "multiStepSignUp",
            route: "/multi-step-sign-up",
          },
          {
            heading: "error404",
            route: "/404",
          },
          {
            heading: "error500",
            route: "/500",
          },
        ],
      },
      {
        sectionTitle: "用户中心",
        route: "/usercenter",
        keenthemesIcon: "profile-user",
        sub: [
          {
            heading: "用户管理",
            route: "/usercenter/usermanagement/UserManagement",
          },
          {
            heading: "店铺管理",
            route: "/usercenter/shopmanagement/ShopManagement",
          },
          // {
          //   heading: "充值管理",
          //   route: "/usercenter/rechargemanagement/RechargeManagement",
          // }
        ]
      }
    ]
  },
  // chat对话
  // {
  //   route: "/chat",
  //   pages: [
  //     {
  //       sectionTitle: "authentication",
  //       keenthemesIcon: "dots-square",
  //       bootstrapIcon: "bi-sticky",
  //       sub: [
  //         {
  //           sectionTitle: "basicFlow",
  //           sub: [
  //             {
  //               heading: "signIn",
  //               route: "/sign-in",
  //             },
  //             {
  //               heading: "signUp",
  //               route: "/sign-up",
  //             },
  //             {
  //               heading: "passwordReset",
  //               route: "/password-reset",
  //             },
  //           ],
  //         },
  //         {
  //           heading: "multiStepSignUp",
  //           route: "/multi-step-sign-up",
  //         },
  //         {
  //           heading: "error404",
  //           route: "/404",
  //         },
  //         {
  //           heading: "error500",
  //           route: "/500",
  //         },
  //       ],
  //     },
  //     {
  //       sectionTitle: "chat对话",
  //       route: "/chat",
  //       keenthemesIcon: "dots-square",
  //       sub: [
  //         {
  //           heading: "对话",
  //           route: "/chat/index",
  //         }]
  //     }


  //   ]
  // }
  // {
  //   heading: "craft",
  //   route: "/crafted",
  //   pages: [
  //     {
  //       sectionTitle: "pages",
  //       route: "/pages",
  //       keenthemesIcon: "element-plus",
  //       bootstrapIcon: "bi-archive",
  //       sub: [
  //         {
  //           sectionTitle: "profile",
  //           route: "/profile",
  //           sub: [
  //             {
  //               heading: "profileOverview",
  //               route: "/crafted/pages/profile/overview",
  //             },
  //             {
  //               heading: "projects",
  //               route: "/crafted/pages/profile/projects",
  //             },
  //             {
  //               heading: "campaigns",
  //               route: "/crafted/pages/profile/campaigns",
  //             },
  //             {
  //               heading: "documents",
  //               route: "/crafted/pages/profile/documents",
  //             },
  //             {
  //               heading: "connections",
  //               route: "/crafted/pages/profile/connections",
  //             },
  //             {
  //               heading: "activity",
  //               route: "/crafted/pages/profile/activity",
  //             },
  //           ],
  //         },
  //         {
  //           sectionTitle: "wizards",
  //           route: "/wizard",
  //           sub: [
  //             {
  //               heading: "horizontal",
  //               route: "/crafted/pages/wizards/horizontal",
  //             },
  //             {
  //               heading: "vertical",
  //               route: "/crafted/pages/wizards/vertical",
  //             },
  //           ],
  //         },
  //       ],
  //     },
  //     {
  //       sectionTitle: "account",
  //       route: "/account",
  //       keenthemesIcon: "profile-circle",
  //       bootstrapIcon: "bi-person",
  //       sub: [
  //         {
  //           heading: "accountOverview",
  //           route: "/crafted/account/overview",
  //         },
  //         {
  //           heading: "settings",
  //           route: "/crafted/account/settings",
  //         },
  //       ],
  //     },
  //     {
  //       sectionTitle: "authentication",
  //       keenthemesIcon: "fingerprint-scanning",
  //       bootstrapIcon: "bi-sticky",
  //       sub: [
  //         {
  //           sectionTitle: "basicFlow",
  //           sub: [
  //             {
  //               heading: "signIn",
  //               route: "/sign-in",
  //             },
  //             {
  //               heading: "signUp",
  //               route: "/sign-up",
  //             },
  //             {
  //               heading: "passwordReset",
  //               route: "/password-reset",
  //             },
  //           ],
  //         },
  //         {
  //           heading: "multiStepSignUp",
  //           route: "/multi-step-sign-up",
  //         },
  //         {
  //           heading: "error404",
  //           route: "/404",
  //         },
  //         {
  //           heading: "error500",
  //           route: "/500",
  //         },
  //       ],
  //     },
  //     {
  //       sectionTitle: "modals",
  //       route: "/modals",
  //       keenthemesIcon: "design",
  //       bootstrapIcon: "bi-shield-check",
  //       sub: [
  //         {
  //           sectionTitle: "general",
  //           route: "/general",
  //           sub: [
  //             {
  //               heading: "inviteFriends",
  //               route: "/crafted/modals/general/invite-friends",
  //             },
  //             {
  //               heading: "viewUsers",
  //               route: "/crafted/modals/general/view-user",
  //             },
  //             {
  //               heading: "upgradePlan",
  //               route: "/crafted/modals/general/upgrade-plan",
  //             },
  //             {
  //               heading: "shareAndEarn",
  //               route: "/crafted/modals/general/share-and-earn",
  //             },
  //           ],
  //         },
  //         {
  //           sectionTitle: "forms",
  //           route: "/forms",
  //           sub: [
  //             {
  //               heading: "newTarget",
  //               route: "/crafted/modals/forms/new-target",
  //             },
  //             {
  //               heading: "newCard",
  //               route: "/crafted/modals/forms/new-card",
  //             },
  //             {
  //               heading: "newAddress",
  //               route: "/crafted/modals/forms/new-address",
  //             },
  //             {
  //               heading: "createAPIKey",
  //               route: "/crafted/modals/forms/create-api-key",
  //             },
  //           ],
  //         },
  //         {
  //           sectionTitle: "wizards",
  //           route: "/wizards",
  //           sub: [
  //             {
  //               heading: "twoFactorAuth",
  //               route: "/crafted/modals/wizards/two-factor-auth",
  //             },
  //             {
  //               heading: "createApp",
  //               route: "/crafted/modals/wizards/create-app",
  //             },
  //             {
  //               heading: "createAccount",
  //               route: "/crafted/modals/wizards/create-account",
  //             },
  //           ],
  //         },
  //       ],
  //     },
  //     {
  //       sectionTitle: "widgets",
  //       route: "/widgets",
  //       keenthemesIcon: "element-7",
  //       bootstrapIcon: "bi-layers",
  //       sub: [
  //         {
  //           heading: "widgetsLists",
  //           route: "/crafted/widgets/lists",
  //         },
  //         {
  //           heading: "widgetsStatistics",
  //           route: "/crafted/widgets/statistics",
  //         },
  //         {
  //           heading: "widgetsCharts",
  //           route: "/crafted/widgets/charts",
  //         },
  //         {
  //           heading: "widgetsMixed",
  //           route: "/crafted/widgets/mixed",
  //         },
  //         {
  //           heading: "widgetsTables",
  //           route: "/crafted/widgets/tables",
  //         },
  //         {
  //           heading: "widgetsFeeds",
  //           route: "/crafted/widgets/feeds",
  //         },
  //       ],
  //     },
  //   ],
  // },
  // {
  //   heading: "apps",
  //   route: "/apps",
  //   pages: [
  //     {
  //       sectionTitle: "customers",
  //       route: "/customers",
  //       keenthemesIcon: "abstract-38",
  //       bootstrapIcon: "bi-printer",
  //       sub: [
  //         {
  //           heading: "gettingStarted",
  //           route: "/apps/customers/getting-started",
  //         },
  //         {
  //           heading: "customersListing",
  //           route: "/apps/customers/customers-listing",
  //         },
  //         {
  //           heading: "customerDetails",
  //           route: "/apps/customers/customer-details",
  //         },
  //       ],
  //     },
  //     {
  //       sectionTitle: "subscriptions",
  //       route: "/subscriptions",
  //       keenthemesIcon: "basket",
  //       bootstrapIcon: "bi-cart",
  //       sub: [
  //         {
  //           heading: "getStarted",
  //           route: "/apps/subscriptions/getting-started",
  //         },
  //         {
  //           heading: "subscriptionList",
  //           route: "/apps/subscriptions/subscription-list",
  //         },
  //         {
  //           heading: "addSubscription",
  //           route: "/apps/subscriptions/add-subscription",
  //         },
  //         {
  //           heading: "viewSubscription",
  //           route: "/apps/subscriptions/view-subscription",
  //         },
  //       ],
  //     },
  //     {
  //       heading: "calendarApp",
  //       route: "/apps/calendar",
  //       keenthemesIcon: "calendar-8",
  //       bootstrapIcon: "bi-calendar3-event",
  //     },
  //     {
  //       sectionTitle: "chat",
  //       route: "/chat",
  //       keenthemesIcon: "message-text-2",
  //       bootstrapIcon: "bi-chat-left",
  //       sub: [
  //         {
  //           heading: "privateChat",
  //           route: "/apps/chat/private-chat",
  //         },
  //         {
  //           heading: "groupChat",
  //           route: "/apps/chat/group-chat",
  //         },
  //         {
  //           heading: "drawerChat",
  //           route: "/apps/chat/drawer-chat",
  //         },
  //       ],
  //     },
  //   ],
  // },
];

export default MainMenuConfig;
