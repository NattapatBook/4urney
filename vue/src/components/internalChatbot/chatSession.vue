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
      <div>
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
                <!-- <div>
                  <v-avatar>
                    <v-img
                      v-if="selectedUser.img"
                      :src="selectedUser.img"
                      aspect-ratio="1"
                    ></v-img>
                    <v-img
                      v-else
                      :src="`https://ui-avatars.com/api/?name=${selectedUser.name}`"
                      aspect-ratio="1"
                    ></v-img>
                  </v-avatar>
                </div> -->
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
        <v-card-text class="px-2 py-0">
          <v-container>
            <!-- Today Section -->
            <div v-if="groupedChats.today.length">
              <h3>Today</h3>
              <v-list>
                <v-list-item v-for="chat in groupedChats.today" :key="chat.id">
                  <v-list-item-title>{{ chat.name }}</v-list-item-title>
                  <v-list-item-subtitle>{{
                    formatDate(chat.lastConversationTime)
                  }}</v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </div>

            <!-- Yesterday Section -->
            <div v-if="groupedChats.yesterday.length">
              <h3>Yesterday</h3>
              <v-list>
                <v-list-item
                  v-for="chat in groupedChats.yesterday"
                  :key="chat.id"
                >
                  <v-list-item-title>{{ chat.name }}</v-list-item-title>
                  <v-list-item-subtitle>{{
                    formatDate(chat.lastConversationTime)
                  }}</v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </div>

            <!-- Previous 7 Days Section -->
            <div v-if="groupedChats.previous7Days.length">
              <h3>Previous 7 Days</h3>
              <v-list>
                <v-list-item
                  v-for="chat in groupedChats.previous7Days"
                  :key="chat.id"
                >
                  <v-list-item-title>{{ chat.name }}</v-list-item-title>
                  <v-list-item-subtitle>{{
                    formatDate(chat.lastConversationTime)
                  }}</v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </div>

            <!-- Older Section -->
            <div v-if="groupedChats.older.length">
              <h3>Older</h3>
              <v-list>
                <v-list-item v-for="chat in groupedChats.older" :key="chat.id">
                  <v-list-item-title>{{ chat.name }}</v-list-item-title>
                  <v-list-item-subtitle>{{
                    formatDate(chat.lastConversationTime)
                  }}</v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </div>
          </v-container>
        </v-card-text>
      </div>
    </div>
  </div>
</template>

<script>
import DataError from "../tools/dataError.vue";
export default {
  name: "Component_chatSession",
  components: { DataError },
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
          lastConversationTime: new Date("2024-12-30T20:15:00"), // Dec/30/2024 8:15 PM
        },
        {
          id: 4,
          name: `test_4`,
          lastConversationTime: new Date("2024-11-15T14:00:00"), // Nov/15/2024 2:00 PM
        },
        {
          id: 5,
          name: `test_5`,
          lastConversationTime: new Date("2024-10-05T09:30:00"), // Oct/5/2024 9:30 AM
        },
      ],
      groupedChats: {
        today: [],
        yesterday: [],
        previous7Days: [],
        older: [],
      },
    };
  },

  mounted() {
    // responsive
    this.$nextTick(() => {
      window.addEventListener("resize", this.onResize);
    });
    this.onResize();
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
  },
};
</script>

<style scoped></style>
