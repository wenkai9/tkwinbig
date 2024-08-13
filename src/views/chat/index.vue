<template>
  <el-card>
    <div>
      <el-button type="primary" @click="handleSend">立即收信</el-button>
    </div>
    <div
      class="card w-100"
      id="kt_drawer_chat_messenger"
      style="margin-top: 1rem"
    >
      <div class="card-header pe-5" id="kt_drawer_chat_messenger_header">
        <div class="card-title">
          <!-- <div class="d-flex justify-content-center flex-column me-3">
          <a
            href="#"
            class="fs-4 fw-bold text-gray-900 text-hover-primary me-1 mb-2 lh-1"
            >Brian Cox</a
          >

          <div class="mb-0 lh-1">
            <span
              class="badge badge-success badge-circle w-10px h-10px me-1"
            ></span>
            <span class="fs-7 fw-semibold text-gray-500">Active</span>
          </div>
        </div> -->
        </div>

        <div class="card-toolbar">
          <div class="me-2">
            <button
              class="btn btn-sm btn-icon btn-active-icon-primary"
              data-kt-menu-trigger="click"
              data-kt-menu-placement="bottom-end"
              data-kt-menu-flip="top-end"
            >
              <i class="bi bi-three-dots fs-3"></i>
            </button>
            <Dropdown4></Dropdown4>
          </div>

          <div
            class="btn btn-sm btn-icon btn-active-icon-primary"
            id="kt_drawer_chat_close"
          >
            <KTIcon icon-name="cross" icon-class="fs-2x" />
          </div>
        </div>
      </div>

      <div class="card-body" id="kt_drawer_chat_messenger_body">
        <div
          class="scroll-y me-n5 pe-5"
          ref="messagesRef"
          data-kt-element="messages"
          data-kt-scroll="true"
          data-kt-scroll-activate="true"
          data-kt-scroll-height="auto"
          data-kt-scroll-dependencies="#kt_drawer_chat_messenger_header, #kt_drawer_chat_messenger_footer"
          data-kt-scroll-wrappers="#kt_drawer_chat_messenger_body"
          data-kt-scroll-offset="0px"
        >
          <template v-for="(item, index) in messages" :key="index">
            <!-- <MessageIn
            ref="messagesInRef"
            v-if="item.type === 'in'"
            :name="item.name"
            :image="item.image"
            :time="item.time"
            :text="item.text"
          ></MessageIn> -->
            <!-- {{ item }} -->
            <MessageIn
              ref="messagesInRef"
              v-if="item.role === 'creator'"
              :name="item.name"
              :image="item.image"
              :time="item.dateTime"
              :text="item.content"
            ></MessageIn>
            <MessageOut
              ref="messagesOutRef"
              v-if="item.role === 'me'"
              :name="item.name"
              :image="item.image"
              :time="item.dateTime"
              :text="item.content"
            ></MessageOut>
          </template>
        </div>
      </div>

      <div class="card-footer pt-4" id="kt_drawer_chat_messenger_footer">
        <input
          class="form-control form-control-flush mb-3"
          data-kt-element="input"
          placeholder="请输入想要发送的信息"
          v-model="newMessageText"
          @keydown.enter="addNewMessage"
        />

        <div class="d-flex flex-stack">
          <div class="d-flex align-items-center me-2">
            <button
              class="btn btn-sm btn-icon btn-active-light-primary me-1"
              type="button"
              data-bs-toggle="tooltip"
              title="Coming soon"
            >
              <!-- <i class="bi bi-paperclip fs-3"></i> -->
            </button>
            <button
              class="btn btn-sm btn-icon btn-active-light-primary me-1"
              type="button"
              data-bs-toggle="tooltip"
              title="Coming soon"
            >
              <!-- <i class="bi bi-upload fs-3"></i> -->
            </button>
          </div>

          <button
            @click="addNewMessage"
            class="btn btn-primary"
            type="button"
            data-kt-element="send"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  </el-card>
</template>

<script lang="ts">
import { getAssetPath } from "@/core/helpers/assets";
import { defineComponent, ref } from "vue";
import MessageIn from "@/components/messenger-parts/MessageIn.vue";
import MessageOut from "@/components/messenger-parts/MessageOut.vue";
import Dropdown4 from "@/components/dropdown/Dropdown4.vue";

import { ApiGetChat, ApiChat } from "@/api/chat";

interface KTMessage {
  role?: string;
  userName?: string;
  image: string;
  dateTime?: string;
  content?: string;
}

export default defineComponent({
  name: "upgrade-to-pro",
  components: {
    MessageIn,
    MessageOut,
    Dropdown4,
  },
  setup() {
    const messagesRef = ref<null | HTMLElement>(null);
    const messagesInRef = ref<null | HTMLElement>(null);
    const messagesOutRef = ref<null | HTMLElement>(null);

    const messages = ref<Array<KTMessage>>([
      // {
      //   role: "creator",
      //   userName: "Brian Cox",
      //   image: getAssetPath("media/avatars/300-25.jpg"),
      //   dateTime: "May 21 5:12 AM",
      //   content: "Cussinmomma83@gmail.com",
      // },
      // {
      //   role: "me",
      //   image: getAssetPath("media/avatars/300-1.jpg"),
      //   dateTime: "2 Hours",
      //   content:
      //     "Hey there, we’re just writing to let you know that you’ve been subscribed to a repository on GitHub.",
      // },
      // {
      //   role: "creator",
      //   userName: "Brian Cox",
      //   image: getAssetPath("media/avatars/300-25.jpg"),
      //   dateTime: "May 21 5:12 AM",
      //   content: "Cussinmomma83@gmail.com",
      // },
      // {
      //   role: "me",
      //   image: getAssetPath("media/avatars/300-1.jpg"),
      //   dateTime: "2 Hours",
      //   content:
      //     "Hey there, we’re just writing to let you know that you’ve been subscribed to a repository on GitHub.",
      // },
    ]);

    const newMessageText = ref("");

    const addNewMessage = () => {
      if (!newMessageText.value) {
        return;
      }
      messages.value.push({
        role: "me",
        name: window.localStorage.getItem("userName"),
        image: getAssetPath("media/avatars/300-1.jpg"),
        dateTime: "Just now",
        content: newMessageText.value,
      });

      let data = {
        task_id: "2024zxcv",
        // content: "test",
        content: newMessageText.value,
        creator: "Maxim",
        shop_id: "Vexloria",
        brand: "Vexloria",
        product_info: "Vexloria",
        product_link:
          "https://shop.tiktok.com/view/product/1729401957854974731?region=US&locale=en",
        reward: "-20% Sales Commission",
        requirement: "-A 30 - 60 seconds video showing our product",
        limits: "200 dollars",
      };
      ApiChat(data).then((res) => {
        console.log(res, "对话=========");
        setTimeout(() => {
          if (messagesRef.value) {
            messagesRef.value.scrollTop = messagesRef.value.scrollHeight;
          }
        }, 1);
        newMessageText.value = "";
        setTimeout(() => {
          messages.value.push({
            role: "creator",
            name: res.creator,
            image: getAssetPath("media/avatars/300-25.jpg"),
            dateTime: res.sendtime,
            content: res.data,
          });

          setTimeout(() => {
            if (messagesRef.value) {
              messagesRef.value.scrollTop = messagesRef.value.scrollHeight;
            }
          }, 1);
        }, 2000);
      });
      // setTimeout(() => {
      //   if (messagesRef.value) {
      //     messagesRef.value.scrollTop = messagesRef.value.scrollHeight;
      //   }
      // }, 1);

      // newMessageText.value = "";
      // setTimeout(() => {
      //   messages.value.push({
      //     role: "creator",
      //     name: "Ja Morant",
      //     image: getAssetPath("media/avatars/300-25.jpg"),
      //     dateTime: "Just now",
      //     content: "这是达人回复的信息",
      //   });

      //   setTimeout(() => {
      //     if (messagesRef.value) {
      //       messagesRef.value.scrollTop = messagesRef.value.scrollHeight;
      //     }
      //   }, 1);
      // }, 2000);
    };
    const handleSend = () => {
      ApiGetChat("6657f80fde3ec24b04071568").then((res) => {
        console.log(res, "对话");
      });
    };
    return {
      messages,
      messagesRef,
      newMessageText,
      addNewMessage,
      messagesInRef,
      messagesOutRef,
      getAssetPath,
      handleSend,
    };
  },
});
</script>
