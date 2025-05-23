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
      <!--user information & tools bar-->
      <v-card-text
        class="px-1"
        :style="{
          display: `flex`,
          justifyContent: `space-between`,
          height: `80px`,
          alignItems: `center`,
        }"
      >
        <v-container class="px-2 mx-0" :style="{ maxWidth: `100%` }">
          <v-row>
            <!--user information-->
            <v-col :style="{ display: `flex` }" cols="10" class="pa-2">
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
                    maxWidth: `calc(70%)`,
                  }"
                >
                  <span
                    :style="{
                      whiteSpace: `nowrap`,
                      overflow: `hidden`,
                      textOverflow: `ellipsis`,
                      fontWeight: `500`,
                      fontSize: `1.15rem`,
                    }"
                    >{{ selectedUser.name }}</span
                  >
                </div>
              </div>
            </v-col>
            <!--v-btn-->
            <v-col cols="2" class="pa-2">
              <div
                :style="{
                  display: `flex`,
                  alignItems: `center`,
                  justifyContent: `flex-end`,
                }"
              >
                <v-menu transition="fab-transition" class="rounded-xl">
                  <template v-slot:activator="{ props }">
                    <v-btn
                      class="no-ripple"
                      icon="mdi-dots-vertical"
                      variant="text"
                      v-bind="props"
                    ></v-btn>
                  </template>
                  <v-list class="pa-0 rounded-lg">
                    <v-list-item class="pa-0" @click="clickFullScreen()">
                      <v-card
                        class="pa-4"
                        elevation="0"
                        :style="{
                          display: `flex`,
                          alignItems: `center`,
                        }"
                      >
                        <v-icon>{{
                          fullscreen ? `mdi-fullscreen-exit` : `mdi-fullscreen`
                        }}</v-icon>
                        <span
                          >&nbsp;{{
                            fullscreen ? ` Exit Full Screen` : ` Full Screen`
                          }}</span
                        >
                      </v-card>
                    </v-list-item>
                    <v-list-item class="pa-0">
                      <v-card
                        disabled
                        class="pa-4"
                        elevation="0"
                        :style="{
                          display: `flex`,
                          alignItems: `center`,
                        }"
                      >
                        <v-icon>mdi-account-arrow-right</v-icon>
                        <span>&nbsp; Assign to</span>
                      </v-card>
                    </v-list-item>
                    <v-list-item class="pa-0">
                      <v-card
                        @click="clickChangeMessageType()"
                        class="pa-4"
                        elevation="0"
                        :style="{
                          display: `flex`,
                          alignItems: `center`,
                        }"
                      >
                        <v-icon>{{
                          messageType === `Closed Messages`
                            ? `mdi-sticker-check-outline`
                            : `mdi-sticker-remove-outline`
                        }}</v-icon>
                        <span
                          >&nbsp;{{
                            messageType === `Closed Messages`
                              ? ` Open Messages`
                              : ` Close Messages`
                          }}</span
                        >
                      </v-card>
                    </v-list-item>
                  </v-list>
                </v-menu>
              </div>
            </v-col>
          </v-row>
        </v-container>
      </v-card-text>
      <v-divider class="mx-3" />
      <!--chat panel-->
      <div :style="{ height: `calc(100% - 80px - 56px)` }">
        <Chat
          class="py-4"
          :chat-log-prop="chatLogs"
          :selected-user-props="selectedUser"
          :key="`chatPanel_chat_update_${isUpdate}`"
        />
      </div>
      <!-- text field -->
      <v-card-text
        class="pt-0"
        :class="messageType === `Closed Messages` ? `pb-0 mt-4` : ``"
        :style="
          messageType === `Closed Messages`
            ? {
                display: `flex`,
                justifyContent: `center`,
              }
            : {}
        "
      >
        <div v-if="messageType === `Closed Messages`">
          <span :style="{ color: `grey` }"
            >Please open messages to start chat with user</span
          >
        </div>
        <v-text-field
          v-else-if="messageType === `Opened Messages`"
          v-model="msgBox"
          :append-inner-icon="`mdi-send-variant`"
          :placeholder="`Write something...`"
          hint="Hmm, How did you found this!"
          density="compact"
          hide-details
          variant="outlined"
          :style="{ borderRadius: `8px` }"
          @keyup.up="clickFullScreen()"
          @keyup.enter="msgBox.trim().length > 0 ? clickSendMsg() : ``"
          @click:appendInner="msgBox.trim().length > 0 ? clickSendMsg() : ``"
        ></v-text-field>
      </v-card-text>
    </div>
    <!--snackbar-->
    <v-snackbar
      v-model="snackbarAlert"
      timeout="5000"
      :color="snackbarSuccess ? '#5EB491' : '#D6584D'"
      location="top"
      location-strategy="connected"
    >
      <span>
        <v-icon v-if="snackbarSuccess"
          >mdi-checkbox-marked-circle-outline</v-icon
        >
        <v-icon v-else>mdi-alert-circle</v-icon>
        {{ snackbarMsg }}
      </span>

      <template v-slot:action="{ attrs }">
        <v-btn color="white" text v-bind="attrs" @click="snackbarAlert = false">
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </div>
</template>

<script>
import DataError from "../tools/dataError.vue";
import Chat from "./subChatPanel/chat.vue";
import axios from "axios";
export default {
  name: "Component_ChatPanel",
  components: { DataError, Chat },
  props: {
    selectedUserProp: {
      type: Object,
      default: null,
      deep: true,
    },
    isChange: {
      type: Boolean,
      default: false,
    },
    fullscreen: {
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
        if (this.selectedUser && this.selectedUser.id !== `-1`) {
          this.getListMessage(this.selectedUser.id);
        }
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
      chatLogs: [],
      messageType: `Closed Messages`,
      //snackbar
      snackbarAlert: false,
      snackbarSuccess: false,
      snackbarMsg: "untitled",
      isUpdate: false,
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
      axios
        .post(`api/chat_center/admin_reply_post_new/`, {
          id: this.selectedUser.id,
          message: `${this.msgBox}`,
        })
        .then((res) => {
          this.msgBox = ``;
          this.chatLogs = res.data.chatLogs.reverse();
          // this.messageType = res.data.messageType;
          return this.$nextTick();
        })
        .then(() => {
          this.isUpdate = !this.isUpdate;
        })
        .catch((err) => {
          console.error(err);
          this.snackbarMsg = err;
          this.snackbarSuccess = false;
          this.snackbarAlert = true;
        });
    },
    clickFullScreen() {
      this.$emit(`fullscreen`);
    },
    getListMessage(id) {
      axios
        .get(`api/chat_center/list_message_new/${id}`)
        .then((res) => {
          // console.log(res.data);
          this.chatLogs = res.data.chatLogs;
          this.messageType = res.data.messageType;
          return this.$nextTick();
        })
        .then(() => {
          this.isUpdate = !this.isUpdate;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    clickChangeMessageType() {
      axios
        .post(`api/chat_center/change_message_type_new/`, {
          id: this.selectedUser.id,
          messageType: this.messageType,
        })
        .then((res) => {
          this.messageType = res.data.messageType;
          this.snackbarMsg = `${this.selectedUser.name}'s chat session has been successfully ${res.data.messageType}`;
          this.snackbarSuccess = true;
          this.snackbarAlert = true;
          this.$emit(`changeMessageType`);
        })
        .catch((err) => {
          console.error(err);
          this.snackbarMsg = err;
          this.snackbarSuccess = false;
          this.snackbarAlert = true;
        });
    },
    updateLastestChat() {
      this.getListMessage(this.selectedUser.id);
    },
  },
};
</script>

<style scoped>
.no-ripple .v-ripple__container {
  pointer-events: none !important;
}
</style>
