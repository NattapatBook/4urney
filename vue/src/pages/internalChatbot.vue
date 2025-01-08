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
                <ListUser
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
                <ListUserCompact
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
                  :selected-user-prop="selectedUser"
                  :is-change="isSelectedDataChange"
                  :dashboard-data-prop="dashboardData"
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
                <ChatPanel
                  ref="chat_panel_ref"
                  :selected-user-prop="selectedUser"
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
import ChatPanel from "@/components/listen/chatPanel.vue";
import ListUser from "@/components/listen/listUser.vue";
import ListUserCompact from "@/components/listen/listUserCompact.vue";
// import axios from "axios";
import ChatSession from "@/components/internalChatbot/chatSession.vue";

export default {
  name: "listen",
  components: {
    ListUser,
    ListUserCompact,
    ChatPanel,
    ChatSession,
    // ChatDashboard,
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
        tag: `untitled`,
        priority: `untitled`,
        lastestMsg: `untitled`,
        timestamp: new Date(),
        isUrgent: false,
        provider: `untitled`,
      },
      //
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
      const oldId = this.selectedUser.id;
      this.selectedUser = user ? user : null;
      this.isSelectedDataChange = flag;
      if (user && user.id !== `-1` && oldId !== user.id) {
        this.scrollTo("chatSession");
      }
    },
    //getData
    getListUser() {
      this.userItems = [
        {
          id: "999",
          img: "",
          name: "Test Bot 1",
          tag: "",
          priority: "",
          lastestMsg: "เทส1",
          timestamp: "2024-12-12 14:58:39+0700",
          isUrgent: false,
          provider: "line",
          agent: "Me",
          messageType: "Closed Messages",
          replyToken: "021f861c27bb4325829b9f55ed3cb1fa",
        },
      ];
    },
    findById(id) {
      return this.userItems.find((item) => item.id === id);
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
