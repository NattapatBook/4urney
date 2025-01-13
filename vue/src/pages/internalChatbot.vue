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
                />
              </v-card>
            </v-col>
          </v-row>
        </div>
      </v-col>
    </v-row>
  </div>
</template>

<script>
// import axios from "axios";
import ChatSession from "@/components/internalChatbot/chatSession.vue";
import ListChatbot from "@/components/internalChatbot/listChatbot.vue";
import ListChatbotCompact from "@/components/internalChatbot/listChatbotCompact.vue";
import ChatPanelBot from "@/components/internalChatbot/chatPanelBot.vue";
// import chatPanelChatBot from "@/components/listen/chatPanelChatBot.vue";

export default {
  name: "listen",
  components: {
    ListChatbot,
    ListChatbotCompact,
    ChatSession,
    ChatPanelBot,
    // chatPanelChatBot,
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
        // tag: `untitled`,
        // priority: `untitled`,
        // lastestMsg: `untitled`,
        // isUrgent: false,
        // provider: `untitled`,
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
      socket: null,
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
    getListUser() {
      this.userItems = [
        {
          id: `999`,
          img: ``,
          name: `Test Bot_1`,
          industry: `Industry1`,
          mastery: `Mastery1`,
          isActive: true,
          // priority: `untitled`,
          // lastestMsg: `untitled`,
          // isUrgent: false,
          // provider: `untitled`,
        },
        {
          id: `888`,
          img: ``,
          name: `Test Bot`,
          industry: `Industry`,
          mastery: `Mastery`,
          isActive: false,
          // priority: `untitled`,
          // lastestMsg: `untitled`,
          // isUrgent: false,
          // provider: `untitled`,
        },
        {
          id: `777`,
          img: ``,
          name: `Bamm Bot`,
          industry: `Developer`,
          mastery: `Frontend Master`,
          isActive: true,
          // priority: `untitled`,
          // lastestMsg: `untitled`,
          // isUrgent: false,
          // provider: `untitled`,
        },
        {
          id: `666`,
          img: ``,
          name: `LONG NAMEEEEEEEEEEEEEEEEEEEEeeLONG NAMEEEEEEEEEEEEEEEEEEEEeeLONG NAMEEEEEEEEEEEEEEEEEEEEee`,
          industry: `LONG NAMEEEEEEEEEEEEEEEEEEEEee`,
          mastery: `LONG NAMEEEEEEEEEEEEEEEEEEEEee`,
          isActive: false,
          // priority: `untitled`,
          // lastestMsg: `untitled`,
          // isUrgent: false,
          // provider: `untitled`,
        },
      ];
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
