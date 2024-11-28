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
    <div v-else>
      <!--user information & tools bar-->
      <v-card-text
        :style="{
          display: `flex`,
          justifyContent: `space-between`,
          height: `80px`,
          alignItems: `center`,
        }"
      >
        <v-container class="px-2">
          <v-row>
            <!--user information-->
            <v-col cols="6" class="pa-2">
              <div :style="{ display: `flex`, alignItems: `center` }">
                <!--user-->
                <div>
                  <v-avatar>
                    <v-img
                      v-if="selectedUser.img"
                      :src="selectedUser.img"
                      aspect-ratio="1"
                    ></v-img>
                    <v-img
                      v-else
                      :src="`https://ui-avatars.com/api/?name=${checkTextTooLong(
                        selectedUser.name,
                        15
                      )}`"
                      aspect-ratio="1"
                    ></v-img>
                  </v-avatar>
                </div>
                <div
                  class="ml-2"
                  :style="{
                    display: `flex`,
                    flexDirection: `column`,
                    maxWidth: `calc(100% - 50px)`,
                  }"
                >
                  <span
                    :style="{
                      whiteSpace: `nowrap`,
                      overflow: `hidden`,
                      textOverflow: `ellipsis`,
                    }"
                    >{{ checkTextTooLong(selectedUser.name, 15) }}</span
                  >
                </div>
              </div>
            </v-col>
            <!--v-btn-->
            <v-col cols="6" class="pa-2">
              <div
                :style="{
                  display: `flex`,
                  alignItems: `center`,
                  justifyContent: `flex-end`,
                }"
              >
                <v-tooltip text="Tooltip" location="bottom">
                  <template v-slot:activator="{ props }">
                    <v-btn
                      v-bind="props"
                      :size="
                        windowWidth > 960 && windowWidth < 1400
                          ? `x-small`
                          : `default`
                      "
                      text
                      icon="mdi-fullscreen"
                      rounded="pill"
                    >
                    </v-btn>
                  </template>
                  <span>Full Screen</span>
                </v-tooltip>
                <v-tooltip text="Tooltip" location="bottom">
                  <template v-slot:activator="{ props }">
                    <v-btn
                      class="mx-2"
                      v-bind="props"
                      :size="
                        windowWidth > 960 && windowWidth < 1400
                          ? `x-small`
                          : `default`
                      "
                      text
                      icon="mdi-account-arrow-right"
                      rounded="pill"
                    >
                    </v-btn>
                  </template>
                  <span>Assign To</span>
                </v-tooltip>
                <v-tooltip text="Tooltip" location="bottom">
                  <template v-slot:activator="{ props }">
                    <v-btn
                      v-bind="props"
                      :size="
                        windowWidth > 960 && windowWidth < 1400
                          ? `x-small`
                          : `default`
                      "
                      text
                      :icon="
                        selectedUser.messageType === `Closed Messages`
                          ? `mdi-sticker-check-outline`
                          : `mdi-sticker-remove-outline`
                      "
                      rounded="pill"
                    >
                    </v-btn>
                  </template>
                  <span>
                    {{
                      selectedUser.messageType === `Closed Messages`
                        ? `Open Messages`
                        : `Close Messages`
                    }}</span
                  >
                </v-tooltip>
              </div>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
      <v-divider class="mx-3" />
      <!--chat panel-->
      <v-card-text></v-card-text>
      <!-- text field -->
      <v-card-text
        :class="
          selectedUser.messageType === `Closed Messages` ? `pb-0 mt-4` : ``
        "
        :style="
          selectedUser.messageType === `Closed Messages`
            ? {
                display: `flex`,
                justifyContent: `center`,
              }
            : {}
        "
      >
        <div v-if="selectedUser.messageType === `Closed Messages`">
          <span :style="{ color: `grey` }"
            >Please open messages to start chat with user</span
          >
        </div>
        <v-text-field
          v-else-if="selectedUser.messageType === `Opened Messages`"
          v-model="msgBox"
          :append-inner-icon="`mdi-send-variant`"
          :placeholder="`Write something...`"
          density="compact"
          hide-details
          variant="outlined"
          :style="{ borderRadius: `8px` }"
          @click="scrollToBottom"
          @keyup.enter="msgBox.trim().length > 0 ? clickSendMsg() : ``"
          @click:appendInner="msgBox.trim().length > 0 ? clickSendMsg() : ``"
        ></v-text-field>
      </v-card-text>
    </div>
  </div>
</template>

<script>
import DataError from "../tools/dataError.vue";
export default {
  name: "Component_ChatPanel",
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
    userItems: {
      type: Object,
      default: () => {
        return [];
      },
    },
  },
  watch: {
    isChange(newValue, oldValue) {
      if (newValue !== oldValue) {
        this.selectedUser = JSON.parse(JSON.stringify(this.selectedUserProp));
        // console.log(this.selectedUserProp);
        // console.log(this.isChange);
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
        tag: `untitled`,
        priority: `untitled`,
        lastestMsg: `untitled`,
        timestamp: new Date(),
        isUrgent: false,
        provider: `untitled`,
      },
      msgBox: ``,
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
    //Tools
    checkTextTooLong(text, cutVal) {
      if (text.length > cutVal) {
        return `${text.slice(0, cutVal)}...`;
      } else {
        return text;
      }
    },
    clickSendMsg() {
      alert(this.msgBox);
      this.msgBox = ``;
    },
  },
};
</script>

<style scoped></style>
