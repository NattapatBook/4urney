<template>
  <div :style="{ width: '100%', margin: '0', padding: '0' }">
    <v-row
      justify="center"
      align="center"
      class="bg-wave"
      no-gutters
      :style="{
        height: `auto`,
        minHeight: `100dvh`,
        width: `100%`,
        justifyItems: `center`,
      }"
    >
      <v-col cols="12">
        <div :style="{ marginTop: `90px`, width: `100%` }">
          <v-row class="ma-2" :style="{ paddingInline: `10px` }">
            <!-- list panel -->
            <v-col
              v-if="!hideListuserPanel"
              :cols="windowWidth > 1280 ? 3 : windowWidth > 1024 ? 4 : 12"
              class="pa-1"
              :style="{ height: `100%` }"
            >
              <v-card
                :style="{
                  height: `calc(100dvh - 110px)`,
                  marginBottom: windowWidth > 1024 ? `0px` : `15px`,
                  borderRadius: `8px`,
                }"
              >
                <ListChatbot
                  class="shake"
                  @addChatbot="addChatbotCallback"
                  @selectUser="selectUser"
                  @minimize="hideListuserPanel = !hideListuserPanel"
                  :selected-user-prop="selectedUser"
                  :user-items="userItems"
                />
              </v-card>
            </v-col>
            <!-- hide list panel -->
            <v-col
              v-else
              class="pa-1"
              :style="{
                height: `100%`,
                maxWidth: `fit-content`,
                flex: `0 0 auto`,
              }"
            >
              <v-card
                class="px-0"
                :style="{
                  height: `calc(100dvh - 110px)`,
                  marginBottom: windowWidth > 1024 ? `0px` : `15px`,
                  borderRadius: `8px`,
                }"
              >
                <ListChatbotCompact
                  class="shake"
                  @selectUser="selectUser"
                  @minimize="hideListuserPanel = !hideListuserPanel"
                  :selected-user-prop="selectedUser"
                  :user-items="userItems"
                />
              </v-card>
            </v-col>
            <!-- chatSession panel -->
            <v-col
              :cols="
                windowWidth > 1280
                  ? 3
                  : windowWidth > 1024
                  ? 4
                  : hideListuserPanel
                  ? true
                  : 12
              "
              id="chatSession"
              class="pa-1"
              :style="{
                height: `100%`,
                display:
                  !selectedUser || selectedUser.id === `-1` ? `none` : ``,
              }"
            >
              <v-card
                class="px-0"
                :style="{
                  height: `calc(100dvh - 110px)`,
                  marginBottom: windowWidth > 1024 ? `0px` : `15px`,
                  borderRadius: `8px`,
                }"
              >
                <ChatSession
                  ref="chat_session_ref"
                  :selected-user-prop="selectedUser"
                  :is-change="isSelectedDataChange"
                  :dashboard-data-prop="dashboardData"
                  @changeChatSession="changeChatSession"
                  @snackbar="snackbarAction"
                  @cancelSelected="cancelSelectedCallback"
                />
              </v-card>
            </v-col>
            <!-- chat panel -->
            <v-col
              :cols="
                windowWidth > 1024
                  ? true
                  : hideListuserPanel &&
                    !(!selectedUser || selectedUser.id === `-1`)
                  ? 12
                  : true
              "
              id="chatPanel"
              :class="fullscreen ? `pa-0` : `pa-1`"
              :style="{
                height: fullscreen ? '100dvh' : '',
                display: 'grid',
                position: fullscreen ? 'fixed' : 'relative',
                top: fullscreen ? '0' : '',
                left: fullscreen ? '0' : '',
                width: fullscreen ? '100dvw' : 'auto',
                zIndex: fullscreen ? '999' : '',
              }"
            >
              <v-card
                :class="fullscreen ? `rounded-0` : ``"
                :style="{
                  height: fullscreen ? '100dvh' : `calc(100dvh - 110px)`,
                  marginBottom: windowWidth > 1024 ? '0px' : '15px',
                  borderRadius: '8px',
                }"
              >
                <ChatPanelBot
                  ref="chat_panel_ref"
                  :selected-user-prop="selectedUser"
                  :selected-chat-prop="chatSelected"
                  :is-change="isSelectedDataChange"
                  :fullscreen="fullscreen"
                  @fullscreen="fullscreen = !fullscreen"
                  @snackbar="snackbarAction"
                />
              </v-card>
            </v-col>
          </v-row>
        </div>
      </v-col>
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
          <v-btn
            color="white"
            text
            v-bind="attrs"
            @click="snackbarAlert = false"
          >
            Close
          </v-btn>
        </template>
      </v-snackbar>
    </v-row>
  </div>
</template>

<script>
import axios from "axios";
import ChatSession from "@/components/internalChatbot/chatSession.vue";
import ListChatbot from "@/components/internalChatbot/listChatbot.vue";
import ListChatbotCompact from "@/components/internalChatbot/listChatbotCompact.vue";
import ChatPanelBot from "@/components/internalChatbot/chatPanelBot.vue";

export default {
  name: "ChatWithData",
  components: {
    ListChatbot,
    ListChatbotCompact,
    ChatSession,
    ChatPanelBot,
  },
  data() {
    return {
      windowWidth: 0,
      windowHeight: 0,
      hideListuserPanel: false,
      userItems: [],
      //selectedUser
      selectedUser: {
        id: `-1`,
        img: ``,
        name: `untitled`,
        industry: `untitled`,
        mastery: `untitled`,
        isActive: true,
      },
      isSelectedDataChange: false,
      fullscreen: false,
      //dashboard
      dashboardData: {
        dissatisfaction: 0,
        intentSummary: [],
        priority: "untitled",
        satisfaction: 0,
        totalMessage: 0,
        totalSession: 0,
        urgent: 0,
        id: "-1",
        userInformation: {
          birthday: "untitled",
          citizenId: "untitled",
          email: "untitled",
          gender: "untitled",
          name: "untitled",
          phoneNumber: "untitled",
        },
      },
      chatSelected: {
        id: `-1`,
        name: `untitled`,
        lastConversationTime: new Date(),
      },
      //snackbar
      snackbarAlert: false,
      snackbarSuccess: false,
      snackbarMsg: `untitled`,
    };
  },
  mounted() {
    // responsive
    this.$nextTick(() => {
      window.addEventListener("resize", this.onResize);
    });
    this.onResize();

    //getData
    this.getListUser();
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
    scrollTo(id) {
      const element = document.getElementById(id);
      if (element) {
        element.scrollIntoView({ behavior: "smooth" });
      }
    },
    selectUser(user, flag) {
      // Remove old chat session
      this.removeChatSessionItem();

      const oldId = this.selectedUser.id;
      this.selectedUser = user ? user : null;
      this.isSelectedDataChange = flag;

      if (user && user.id != -1 && oldId !== user.id) {
        this.$nextTick(() => {
          const chatSession = document.getElementById("chatSession");
          if (chatSession && chatSession.style.display !== "none") {
            this.scrollTo("chatSession");
          }
        });
      }
    },
    //getData
    async getListUser() {
      axios
        .get(`api/chat_center/list_bot/`)
        .then((res) => {
          this.userItems = res.data;
        })
        .catch((err) => {
          console.error(err);
        });
    },
    findById(id) {
      return this.userItems.find((item) => item.id === id);
    },
    changeChatSession(item) {
      const oldId = this.chatSelected.id;

      this.chatSelected = { ...item };

      if (
        this.chatSelected &&
        this.chatSelected.id !== `-1` &&
        oldId !== this.chatSelected.id
      ) {
        this.$nextTick(() => {
          this.scrollTo("chatPanel");
        });
      }
    },
    removeChatSessionItem() {
      this.chatSelected = {
        id: `-1`,
        name: `untitled`,
        lastConversationTime: new Date(),
      };
      this.$refs.chat_session_ref.removeChatSessionItem();
    },
    snackbarAction(item) {
      this.snackbarMsg = item.snackbarMsg;
      this.snackbarSuccess = item.snackbarSuccess;
      this.snackbarAlert = item.snackbarAlert;
    },
    cancelSelectedCallback(item) {
      this.selectUser(null, item.flag);
    },
    addChatbotCallback() {
      this.$emit("addChatbot");
    },
  },
};
</script>

<style scoped>
html,
body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow-x: hidden;
}
.bg-wave {
  box-sizing: border-box;
}

/* Add custom styles to handle vertical toolbar */
.v-col {
  transition: all 0.3s ease;
}

.v-card {
  padding: 10px;
}
</style>
