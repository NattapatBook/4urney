<template>
  <div :style="{ width: '100%', height: `100%` }">
    <DataError
      v-if="!chatLogProp || chatLogProp.length < 1"
      :style="{ height: `100%` }"
      :iconSize="`3rem`"
      :message="`No conversations yet.`"
      :sub-message="`They’ll appear here once started.`"
      :icon="`mdi-message-off`"
    />
    <v-card-text
      id="chatContainer"
      :style="{ height: `100%`, overflowY: `auto` }"
    >
      <div
        v-for="(item, idx) in chatLogProp"
        :key="`listen_chat_msg_${idx}_${item.by}`"
      >
        <!--customer-->
        <div
          v-if="item.by === `customer`"
          :style="{
            display: `flex`,
            justifyContent: `flex-start`,
            flexDirection: `column`,
            alignItems: `flex-start`,
          }"
        >
          <div
            :style="{
              display: `flex`,
              alignItems: `center`,
              whiteSpace: `nowrap`,
              overflow: `hidden`,
              textOverflow: `ellipsis`,
              maxWidth: `75%`,
            }"
          >
            <div class="mr-2 mb-1">
              <v-avatar
                :style="{ width: `20px`, height: `20px`, aspectRatio: 1 }"
              >
                <v-img
                  v-if="selectedUserProps.img"
                  :src="selectedUserProps.img"
                  aspect-ratio="1"
                ></v-img>
                <v-img
                  v-else
                  :src="`https://ui-avatars.com/api/?name=${checkTextTooLong(
                    selectedUserProps.name,
                    15
                  )}`"
                  aspect-ratio="1"
                ></v-img>
              </v-avatar>
            </div>
            <span
              :style="{
                whiteSpace: `nowrap`,
                overflow: `hidden`,
                textOverflow: `ellipsis`,
              }"
              >{{ checkTextTooLong(selectedUserProps.name, 15) }}</span
            >
          </div>
          <v-tooltip location="bottom" text="Tooltip">
            <template v-slot:activator="{ props }">
              <div
                :style="{
                  background: `rgba(254,56,147,1)`,
                  color: `white`,
                  maxWidth: `75%`,
                  borderRadius: `20px`,
                  borderTopLeftRadius: `0px`,
                }"
                class="pa-2"
                v-bind="props"
              >
                <p :style="{ textAlign: `start` }">
                  {{ item.msg }}
                </p>
              </div>
              <p
                :style="{
                  fontSize: `0.72rem`,
                  color: `grey`,
                }"
                class="mb-2 ml-1"
              >
                {{ timeSince(item.timestamp) }}
              </p>
            </template>
            {{ new Date(item.timestamp) }}
          </v-tooltip>
        </div>
        <!--admin-->
        <div
          v-else-if="item.by === `admin`"
          :style="{
            display: `flex`,
            justifyContent: `flex-end`,
            flexDirection: `column`,
            alignItems: `flex-end`,
          }"
        >
          <div>
            <span>Admin</span>
          </div>
          <v-tooltip location="bottom" text="Tooltip">
            <template v-slot:activator="{ props }">
              <div
                :style="{
                  background: `rgb(201,195,195)`,
                  color: `black`,
                  maxWidth: `75%`,
                  borderRadius: `20px`,
                  borderTopRightRadius: `0px`,
                }"
                class="pa-2"
                v-bind="props"
              >
                <p :style="{ textAlign: `start` }">
                  {{ item.msg }}
                </p>
              </div>
              <p
                :style="{
                  fontSize: `0.72rem`,
                  color: `grey`,
                }"
                class="mb-2 mr-1"
              >
                {{ timeSince(item.timestamp) }}
              </p>
            </template>
            {{ new Date(item.timestamp) }}
          </v-tooltip>
        </div>
        <!--bot-->
        <div
          v-else-if="item.by === `bot`"
          :style="{
            display: `flex`,
            justifyContent: `flex-end`,
            flexDirection: `column`,
            alignItems: `flex-end`,
          }"
        >
          <div>
            <span>Chatbot</span>
          </div>
          <v-tooltip location="bottom" text="Tooltip">
            <template v-slot:activator="{ props }">
              <div
                :style="{
                  border: `solid 1px rgba(94, 180, 145, 1)`,
                  color: `black`,
                  maxWidth: `75%`,
                  borderRadius: `20px`,
                  borderTopRightRadius: `0px`,
                }"
                class="pa-2"
                v-bind="props"
              >
                <p :style="{ textAlign: `start` }">
                  {{ item.msg }}
                </p>
              </div>
              <p
                :style="{
                  fontSize: `0.72rem`,
                  color: `grey`,
                }"
                class="mb-2 mr-1"
              >
                {{ timeSince(item.timestamp) }}
              </p>
            </template>
            <span
              :style="{
                color: `rgba(94, 180, 145, 1)`,
              }"
              >* This message has sent by chatbot</span
            ><br />
            {{ new Date(item.timestamp) }}
          </v-tooltip>
        </div>
      </div>
    </v-card-text>
  </div>
</template>

<script>
import DataError from "@/components/tools/dataError.vue";

export default {
  name: "Component_SubChatPanel_Chat",
  components: { DataError },
  props: {
    selectedUserProps: {
      type: Object,
      default: {
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
    },
    chatLogProp: {
      type: Object,
      default: null,
    },
    isChange: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      windowWidth: 0,
      windowHeight: 0,
    };
  },
  mounted() {
    // responsive
    this.$nextTick(() => {
      window.addEventListener("resize", this.onResize);
      this.scrollToBottom();
    });
    this.onResize();
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.onResize);
  },
  watch: {
    chatLogProp: {
      handler() {
        this.scrollToBottom(true);
      },
      deep: true,
    },
  },
  methods: {
    // Resizes the window and updates window dimensions
    onResize() {
      this.windowWidth = window.innerWidth;
      this.windowHeight = window.innerHeight;
    },
    //tools
    checkTextTooLong(text, cutVal) {
      if (text.length > cutVal) {
        return `${text.slice(0, cutVal)}...`;
      } else {
        return text;
      }
    },
    timeSince(dateString, short = false) {
      const date = new Date(dateString);
      const now = new Date();
      const differenceInSeconds = Math.floor(Math.abs((now - date) / 1000));

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
    scrollToBottom(alwaysScroll = false) {
      const chatContainer = document.getElementById("chatContainer");
      if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
      }
    },
  },
};
</script>

<style scoped></style>
