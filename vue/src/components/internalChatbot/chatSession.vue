<template>
  <div :style="{ width: '100%', height: `100%` }">
    <div
      v-if="!selectedUserProp || selectedUserProp.id === `-1`"
      :style="{
        height: `100%`,
        display: `flex`,
        justifyContent: `center`,
      }"
    >
      <DataError
        :iconSize="`3rem`"
        :iconColor="`#5EB491`"
        :message="`No Chat Selected`"
        :sub-message="`Please select a chat from the list to view and respond.`"
        :icon="`mdi-message-alert`"
      />
    </div>
    <div
      v-else
      :style="{
        height: `100%`,
      }"
    >
      <!--customer profile-->
      <div :style="{ height: `100%` }">
        <v-card-text
          class="px-1 py-0"
          :style="{
            display: `flex`,
            justifyContent: `space-between`,
            alignItems: `center`,
          }"
        >
          <v-container class="px-2 mx-0" :style="{ maxWidth: `100%` }">
            <v-row>
              <!--Customer Profile-->
              <v-col
                :style="{
                  display: `flex`,
                  alignItems: `center`,
                  justifyContent: `space-between`,
                  height: `72px`,
                }"
                cols="12"
              >
                <div>
                  <span
                    :style="{
                      whiteSpace: `nowrap`,
                      overflow: `hidden`,
                      textOverflow: `ellipsis`,
                      fontWeight: `500`,
                      fontSize: `1.15rem`,
                    }"
                    >Chat Session</span
                  >
                </div>
                <div>
                  <v-tooltip text="Tooltip" location="bottom">
                    <template v-slot:activator="{ props }">
                      <v-btn
                        @click="clickNewChat()"
                        v-bind="props"
                        text
                        :icon="`mdi-chat-plus`"
                        rounded="pill"
                        :size="
                          windowWidth > 960 && windowWidth < 1400
                            ? `x-small`
                            : `default`
                        "
                      />
                    </template>
                    <span>New Chat</span>
                  </v-tooltip>
                </div>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-divider class="mx-3" />
        <v-card-text
          class="px-2 py-0"
          :style="{
            overflowY: `auto`,
            height: `calc(100% - 80px)`,
          }"
        >
          <v-container class="px-0">
            <div
              v-for="(chats, key) in groupedChats"
              :key="`session_chat_${key}`"
            >
              <div v-if="chats.length">
                <!-- Section Header -->
                <v-chip class="my-2">
                  <h3 class="mb-0" :style="{ textTransform: `capitalize` }">
                    {{ key === `previous7Days` ? `Previous 7 Days` : key }}
                  </h3>
                </v-chip>

                <!-- Chat List -->
                <v-list-item
                  class="rounded-xl"
                  v-for="chat in chats"
                  :key="`chatSession_${key}_${chat.id}`"
                  :class="chatSelected.id === chat.id ? `` : `hover-gradient`"
                  link
                  @click="clickSelectChatSession(chat)"
                  :style="
                    chatSelected.id === chat.id
                      ? {
                          backgroundColor: `rgb(255, 168, 199)`,
                          color: `white`,
                        }
                      : {}
                  "
                >
                  <v-row align="center">
                    <!-- Empty Column for Alignment (Optional) -->
                    <v-col class="px-0"></v-col>

                    <!-- Chat Details -->
                    <v-col class="px-0" cols="8">
                      <v-list-item-title>{{ chat.name }}</v-list-item-title>
                      <v-list-item-subtitle>
                        {{ formatDate(chat.lastConversationTime) }}
                      </v-list-item-subtitle>
                    </v-col>

                    <!-- Action Menu -->
                    <v-col class="px-0">
                      <v-menu transition="fab-transition" class="rounded-xl">
                        <template v-slot:activator="{ props }">
                          <v-btn
                            class="no-ripple"
                            icon="mdi-dots-vertical"
                            variant="text"
                            v-bind="props"
                          ></v-btn>
                        </template>

                        <!-- Action List -->
                        <v-list class="pa-0 rounded-lg">
                          <!-- Rename Action -->
                          <v-list-item class="pa-0" @click="clickRename(chat)">
                            <v-card
                              class="pa-4 d-flex align-center"
                              elevation="0"
                            >
                              <v-icon>mdi-pencil</v-icon>
                              <span class="ms-2">Rename</span>
                            </v-card>
                          </v-list-item>

                          <!-- Delete Action -->
                          <v-list-item class="pa-0" @click="clickDelete(chat)">
                            <v-card
                              class="pa-4 d-flex align-center"
                              elevation="0"
                            >
                              <v-icon>mdi-delete</v-icon>
                              <span class="ms-2">Delete</span>
                            </v-card>
                          </v-list-item>
                        </v-list>
                      </v-menu>
                    </v-col>
                  </v-row>
                </v-list-item>
              </div>
            </div>
          </v-container>
        </v-card-text>
      </div>
    </div>
    <ChatSessionDialog
      v-model="dialog"
      :mode="dialogMode"
      :item="dialogItem"
      @apply="applyFromDialog"
    />
  </div>
</template>

<script>
import DataError from "../tools/dataError.vue";
import ChatSessionDialog from "./chatSessionDialog.vue";
export default {
  name: "Component_chatSession",
  components: { DataError, ChatSessionDialog },
  props: {
    selectedUserProp: {
      type: Object,
      default: null,
    },
    isChange: {
      type: Boolean,
      default: false,
    },
  },
  watch: {
    isChange(newValue, oldValue) {
      if (newValue !== oldValue) {
        this.selectedUser = JSON.parse(JSON.stringify(this.selectedUserProp));
      }
    },
  },
  data() {
    return {
      windowWidth: 0,
      windowHeight: 0,
      selectedUser: {
        id: `-1`,
        img: ``,
        name: `untitled`,
        industry: `untitled`,
        mastery: `untitled`,
        isActive: true,
        // tag: `untitled`,
        // priority: `untitled`,
        // lastestMsg: `untitled`,
        // isUrgent: false,
        // provider: `untitled`,
      },
      chatSelected: {
        id: `-1`,
        name: `untitled`,
        lastConversationTime: new Date(),
      },
      chatSessionItem: [
        {
          id: 1,
          name: `test_1`,
          lastConversationTime: new Date("2025-01-07T10:30:00"), // Jan/7/2025 10:30 AM
        },
        {
          id: 2,
          name: `test_2`,
          lastConversationTime: new Date("2025-01-07T15:45:00"), // Jan/7/2025 3:45 PM
        },
        {
          id: 3,
          name: `test_3`,
          lastConversationTime: new Date("2025-01-06T20:15:00"), // Jan/6/2025 8:15 PM
        },
        {
          id: 4,
          name: `test_4`,
          lastConversationTime: new Date("2025-01-01T14:00:00"), // Jan/1/2025 2:00 PM
        },
        {
          id: 5,
          name: `test_5`,
          lastConversationTime: new Date("2025-01-02T09:30:00"), // Jan/2/2025 9:30 AM
        },
        {
          id: 6,
          name: `test_6`,
          lastConversationTime: new Date("2024-10-05T09:30:00"), // Oct/5/2024 9:30 AM
        },
        {
          id: 7,
          name: `test_7`,
          lastConversationTime: new Date("2024-10-05T09:30:00"), // Oct/5/2024 9:30 AM
        },
      ],
      groupedChats: {
        today: [],
        yesterday: [],
        previous7Days: [],
        older: [],
      },
      dialog: false,
      dialogMode: `untitled`,
      dialogItem: {
        id: `-1`,
        name: `untitled`,
        lastConversationTime: new Date(),
      },
    };
  },

  mounted() {
    // responsive
    this.$nextTick(() => {
      window.addEventListener("resize", this.onResize);
    });
    this.onResize();

    this.groupChats();
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.onResize);
  },
  methods: {
    // Resizes the window and updates window dimensions
    onResize() {
      this.windowWidth = window.innerWidth;
      this.windowHeight = window.innerHeight;
    },
    //tools
    timeSince(dateString, short = false) {
      // Convert the input date string to a Date object
      const date = new Date(dateString);
      // Get the current time
      const now = new Date();

      // Convert both dates to milliseconds since epoch
      const utcDate = date.getTime();
      const utcNow = now.getTime();

      // Calculate the time difference in seconds
      const differenceInSeconds = Math.floor(
        Math.abs((utcNow - utcDate) / 1000)
      );

      let interval = differenceInSeconds / 31536000; // seconds in a year
      if (interval >= 1) {
        return Math.floor(interval) + `${short ? ` yr.` : ` years ago`}`;
      }

      interval = differenceInSeconds / 2592000; // seconds in a month
      if (interval >= 1) {
        return Math.floor(interval) + `${short ? ` mo.` : ` months ago`}`;
      }

      interval = differenceInSeconds / 86400; // seconds in a day
      if (interval >= 1) {
        return Math.floor(interval) + `${short ? ` d.` : ` days ago`}`;
      }

      interval = differenceInSeconds / 3600; // seconds in an hour
      if (interval >= 1) {
        return Math.floor(interval) + `${short ? ` h.` : ` hours ago`}`;
      }

      interval = differenceInSeconds / 60; // seconds in a minute
      if (interval >= 1) {
        return Math.floor(interval) + `${short ? ` m.` : ` minute ago`}`;
      }

      return short ? `now` : "just now";
    },
    numberKMB(num) {
      if (num < 1000) {
        return num;
      }
      const si = [
        { v: 1e3, s: "K" },
        { v: 1e6, s: "M" },
        { v: 1e9, s: "B" },
        { v: 1e12, s: "T" },
        { v: 1e15, s: "P" },
        { v: 1e18, s: "E" },
      ];
      let i;
      for (i = si.length - 1; i > 0; i--) {
        if (num >= si[i].v) {
          break;
        }
      }
      return (
        (num / si[i].v).toFixed(2).replace(/\.0+$|(\.[0-9]*[1-9])0+$/, "$1") +
        si[i].s
      );
    },
    groupChats() {
      const today = new Date();
      const startOfToday = new Date(
        today.getFullYear(),
        today.getMonth(),
        today.getDate()
      );
      const startOfYesterday = new Date(startOfToday);
      startOfYesterday.setDate(startOfYesterday.getDate() - 1);
      const startOf7DaysAgo = new Date(startOfToday);
      startOf7DaysAgo.setDate(startOf7DaysAgo.getDate() - 7);

      this.groupedChats.today = this.chatSessionItem.filter(
        (chat) => chat.lastConversationTime >= startOfToday
      );
      this.groupedChats.yesterday = this.chatSessionItem.filter(
        (chat) =>
          chat.lastConversationTime >= startOfYesterday &&
          chat.lastConversationTime < startOfToday
      );
      this.groupedChats.previous7Days = this.chatSessionItem.filter(
        (chat) =>
          chat.lastConversationTime >= startOf7DaysAgo &&
          chat.lastConversationTime < startOfYesterday
      );
      this.groupedChats.older = this.chatSessionItem.filter(
        (chat) => chat.lastConversationTime < startOf7DaysAgo
      );
    },
    formatDate(date) {
      return new Intl.DateTimeFormat("en-US", {
        dateStyle: "medium",
        timeStyle: "short",
      }).format(date);
    },
    clickRename(item) {
      this.dialogMode = `rename`;
      this.dialogItem = { ...item };
      this.dialog = true;
    },
    clickDelete(item) {
      this.dialogMode = `delete`;
      this.dialogItem = { ...item };
      this.dialog = true;
    },
    clickNewChat() {
      this.dialogMode = `newChat`;
      this.dialog = true;
    },
    applyFromDialog(item) {
      console.log(item);
    },
    clickSelectChatSession(item) {
      if (this.chatSelected.id === item.id) {
        this.chatSelected = {
          id: `-1`,
          name: `untitled`,
          lastConversationTime: new Date(),
        };
      } else {
        this.chatSelected = { ...item };
      }
      this.$emit(`changeChatSession`, this.chatSelected);
    },
    removeChatSessionItem() {
      this.chatSelected = {
        id: `-1`,
        name: `untitled`,
        lastConversationTime: new Date(),
      };
    },
  },
};
</script>

<style scoped>
.hover-gradient {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.hover-gradient:hover {
  transform: scale(1.01);
  z-index: 999;
  color: rgb(255, 168, 199);
}
</style>
