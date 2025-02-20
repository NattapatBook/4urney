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
        display: `flex`,
      }"
    >
      <v-col cols="12" sm="12" md="10" lg="10" xl="8" xxl="8">
        <div :style="{ marginTop: `90px`, width: `100%` }">
          <v-row class="ma-2" :style="{ paddingInline: `10px` }">
            <v-col cols="12" class="pa-1" :style="{ height: `100%` }">
              <v-card
                class="rounded-xl"
                :style="{ height: `calc(100dvh - 110px)` }"
              >
                <v-card-title>
                  <p class="gradient-text" :style="{ fontWeight: 'bold' }">
                    Channel Management
                  </p>
                  <span :style="{ fontSize: '0.8rem', color: 'grey' }">
                    "Seamlessly manage your social and communication channels in
                    one place."
                  </span>
                </v-card-title>

                <v-card-text :class="windowWidth > 900 ? `` : `pa-3`">
                  <div
                    :style="{
                      textAlign: `-webkit-center`,
                    }"
                  >
                    <div
                      :style="{
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        flexDirection: 'row',
                        alignContent: 'center',
                        maxWidth: `420px`,
                      }"
                    >
                      <v-text-field
                        class="mr-3"
                        v-model="search"
                        density="compact"
                        label="Filter by account name"
                        hide-details
                        variant="outlined"
                        rounded="xl"
                        clearable
                      ></v-text-field>
                      <v-tooltip text="Tooltip" location="bottom">
                        <template v-slot:activator="{ props }">
                          <v-btn
                            @click="addChannelDialogModel = true"
                            v-bind="props"
                            icon
                            color="primary"
                          >
                            <v-icon>mdi-plus</v-icon>
                          </v-btn>
                        </template>
                        <span>Add more channel</span>
                      </v-tooltip>
                    </div>
                  </div>
                </v-card-text>
                <v-card-text
                  v-if="isLoading"
                  class="pt-0"
                  :style="{
                    height: `calc(100% - 132px)`,
                    display: `flex`,
                    justifyContent: `center`,
                  }"
                >
                  <Loading :message="`Loading Channel List...`" />
                </v-card-text>
                <v-card-text
                  v-else-if="!isLoading && isError"
                  class="pt-0"
                  :style="{
                    height: `calc(100% - 132px)`,
                    display: `flex`,
                    justifyContent: `center`,
                  }"
                >
                  <DataError :message="errMsg" />
                </v-card-text>
                <v-card-text
                  v-else-if="!isLoading && !isError"
                  class="pt-0"
                  :style="{
                    height: `calc(100% - 132px)`,
                    display: `flex`,
                    justifyContent: `center`,
                  }"
                >
                  <v-data-table-virtual
                    fixed-header
                    :style="{
                      overflowY: `auto`,
                      overflowX: `hidden`,
                      height: `calc(65vh)`,
                    }"
                    :mobile-breakpoint="901"
                    :headers="headers"
                    :items="itemTable"
                    :search="search"
                    class="custom-table"
                  >
                    <!--action-->
                    <template v-slot:item.action="prop">
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
                              :icon="
                                windowWidth > 901
                                  ? `mdi-dots-vertical`
                                  : `mdi-wrench`
                              "
                              variant="text"
                              v-bind="props"
                            ></v-btn>
                          </template>
                          <v-list class="pa-0 rounded-lg">
                            <v-list-item
                              class="pa-0"
                              @click="clickEdit(prop.item)"
                            >
                              <v-card
                                class="pa-4"
                                elevation="0"
                                :style="{
                                  display: `flex`,
                                  alignItems: `center`,
                                }"
                              >
                                <v-icon>mdi-pencil</v-icon>
                                <span>&nbsp; Edit</span>
                              </v-card>
                            </v-list-item>
                            <v-list-item
                              class="pa-0"
                              @click="clickDeactive(prop.item)"
                            >
                              <v-card
                                class="pa-4"
                                elevation="0"
                                :style="{
                                  display: `flex`,
                                  alignItems: `center`,
                                }"
                              >
                                <v-icon>
                                  {{
                                    prop.item.status ? "mdi-close" : "mdi-check"
                                  }}
                                </v-icon>
                                <span
                                  >&nbsp;{{
                                    prop.item.status ? ` Deactive` : ` Active`
                                  }}</span
                                >
                              </v-card>
                            </v-list-item>
                            <v-list-item
                              class="pa-0"
                              @click="clickDelete(prop.item)"
                            >
                              <v-card
                                class="pa-4"
                                elevation="0"
                                :style="{
                                  display: `flex`,
                                  alignItems: `center`,
                                }"
                              >
                                <v-icon>mdi-delete</v-icon>
                                <span>&nbsp; Remove</span>
                              </v-card>
                            </v-list-item>
                          </v-list>
                        </v-menu>
                        &nbsp;
                        <v-avatar
                          v-if="!(windowWidth > 900 && windowWidth < 985)"
                        >
                          <v-img
                            v-if="prop.item.img"
                            :src="prop.item.img"
                            aspect-ratio="1"
                          ></v-img>
                          <v-img
                            v-else
                            :src="`https://ui-avatars.com/api/?name=${prop.item.accountName}`"
                            aspect-ratio="1"
                          ></v-img>
                        </v-avatar>
                      </div>
                    </template>
                    <!--Account Name-->
                    <template v-slot:item.accountName="prop">
                      <div
                        :style="{
                          display: `flex`,
                          alignItems: `center`,
                          justifyContent: windowWidth > 900 ? `` : `flex-end`,
                        }"
                      >
                        <v-tooltip text="Tooltip" location="bottom">
                          <template v-slot:activator="{ props }">
                            <div
                              v-bind="props"
                              :style="{
                                whiteSpace: `nowrap`,
                                overflow: `hidden`,
                                textOverflow: `ellipsis`,
                                maxWidth:
                                  windowWidth > 900 && windowWidth < 985
                                    ? `100px`
                                    : `150px`,
                                cursor: `pointer`,
                              }"
                            >
                              <span>{{ prop.item.accountName }}</span>
                            </div>
                          </template>
                          <span>{{ prop.item.accountName }}</span>
                        </v-tooltip>
                      </div>
                    </template>
                    <!--type-->
                    <template v-slot:item.type="prop">
                      <div
                        :style="{
                          display: `flex`,
                          alignItems: `center`,
                          justifyContent: windowWidth > 900 ? `` : `flex-end`,
                        }"
                      >
                        <v-tooltip text="Tooltip" location="bottom">
                          <template v-slot:activator="{ props }">
                            <div
                              v-bind="props"
                              :style="{
                                whiteSpace: `nowrap`,
                                overflow: `hidden`,
                                textOverflow: `ellipsis`,
                                maxWidth: `115px`,
                                cursor: `pointer`,
                              }"
                            >
                              <v-avatar size="32">
                                <v-img :src="providerIcon[prop.item.type]" />
                              </v-avatar>
                              <!-- <span>{{ prop.item.type }}</span> -->
                            </div>
                          </template>
                          <span :style="{ textTransform: `capitalize` }">{{
                            prop.item.type
                          }}</span>
                        </v-tooltip>
                      </div>
                    </template>
                    <!--status-->
                    <template v-slot:item.status="prop">
                      <div
                        :style="{
                          display: `flex`,
                          alignItems: `center`,
                          justifyContent: windowWidth > 900 ? `` : `flex-end`,
                        }"
                      >
                        <div
                          :style="{
                            whiteSpace: `nowrap`,
                            overflow: `hidden`,
                            textOverflow: `ellipsis`,
                            maxWidth: `80px`,
                          }"
                        >
                          <div>
                            <v-icon
                              :style="{
                                fontSize: `0.6rem`,
                                color: prop.item.status ? '#5EB491' : '#D6584D',
                              }"
                            >
                              mdi-checkbox-blank-circle
                            </v-icon>
                            &nbsp;
                            <span>{{
                              prop.item.status ? `Active` : `Inactive`
                            }}</span>
                          </div>
                        </div>
                      </div>
                    </template>
                    <!--connected by-->
                    <template v-slot:item.connectedBy="prop">
                      <div
                        :style="{
                          display: `flex`,
                          alignItems: `center`,
                          justifyContent: windowWidth > 900 ? `` : `flex-end`,
                        }"
                      >
                        <v-tooltip text="Tooltip" location="bottom">
                          <template v-slot:activator="{ props }">
                            <div
                              v-bind="props"
                              :style="{
                                whiteSpace: `nowrap`,
                                overflow: `hidden`,
                                textOverflow: `ellipsis`,
                                maxWidth: `150px`,
                                cursor: `pointer`,
                              }"
                            >
                              <span>{{ prop.item.connectedBy }}</span>
                            </div>
                          </template>
                          <span>{{ prop.item.connectedBy }}</span>
                        </v-tooltip>
                      </div>
                    </template>
                    <!--connected on-->
                    <template v-slot:item.connectedOn="prop">
                      <div
                        :style="{
                          display: `flex`,
                          alignItems: `center`,
                          justifyContent: windowWidth > 900 ? `` : `flex-end`,
                        }"
                      >
                        <v-tooltip text="Tooltip" location="bottom">
                          <template v-slot:activator="{ props }">
                            <div
                              v-bind="props"
                              :style="{
                                whiteSpace: `nowrap`,
                                overflow: `hidden`,
                                textOverflow: `ellipsis`,
                                maxWidth: `150px`,
                                cursor: `pointer`,
                              }"
                            >
                              <span>
                                {{
                                  timeSince(
                                    new Date(`${prop.item.connectedOn}`),
                                    windowWidth > 900 && windowWidth < 985
                                      ? true
                                      : false
                                  )
                                }}
                              </span>
                            </div>
                          </template>
                          <span>{{ prop.item.connectedOn }}</span>
                        </v-tooltip>
                      </div>
                    </template>
                  </v-data-table-virtual>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </div>
      </v-col>
      <!--dialog-->
      <v-dialog v-model="dialogMenu" width="auto">
        <v-card class="rounded-lg" max-width="700">
          <v-card-title class="pt-4 pl-5">
            <span>{{ menuDialogTitle }}</span>
          </v-card-title>
          <v-card-text class="pt-0">
            <span :style="{ fontSize: `0.9rem` }">{{ menuDialogBody }}</span>
          </v-card-text>
          <v-card-text class="pb-3" :style="{ alignSelf: `end` }">
            <v-btn
              @click="dialogMenu = false"
              variant="text"
              :style="{ textTransform: `capitalize`, color: `black` }"
            >
              Cancel
            </v-btn>
            <v-btn
              @click="dialogMenu = false"
              variant="tonal"
              class="ml-4"
              :style="{
                textTransform: `capitalize`,
                backgroundColor: `rgb(251 56 57)`,
                color: `white`,
              }"
            >
              {{ menuDialogBtn }}
            </v-btn>
          </v-card-text>
        </v-card>
      </v-dialog>
      <addChannelDialog
        v-model="addChannelDialogModel"
        @callbackAddedChannel="addedChannel"
      />
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
import line_icon from "@/assets/img/provider/line_icon.png";
import messenger_icon from "@/assets/img/provider/messenger_icon.png";
import instagram_icon from "@/assets/img/provider/instagram_icon.png";
import tiktok_icon from "@/assets/img/provider/tiktok_icon.png";
import addChannelDialog from "@/components/channelManage/addChannelDialog.vue";
import axios from "axios";
import Loading from "@/components/tools/loading.vue";
import DataError from "@/components/tools/dataError.vue";
export default {
  name: "channelManage",
  components: { addChannelDialog, Loading, DataError },
  data() {
    return {
      windowWidth: 0,
      windowHeight: 0,
      search: ``,
      //tools
      providerIcon: {
        line: line_icon,
        messenger: messenger_icon,
        instagram: instagram_icon,
        tiktok: tiktok_icon,
      },
      headers: [
        {
          align: "end",
          key: "action",
          sortable: false,
          title: "",
        },
        { key: "accountName", title: "Account Name" },
        { key: "type", title: "Type" },
        { key: "status", title: "Status" },
        { key: "connectedBy", title: "By" },
        { key: "connectedOn", title: "Connected On" },
      ],
      itemTable: [
        // {
        //   id: `-1`,
        //   img: ``,
        //   accountName: `4Plus Consulting_mockup`,
        //   type: `messenger`,
        //   status: false,
        //   connectedBy: `developer_test`,
        //   connectedOn: new Date("2024-04-03 17:00:04+07:00"),
        // },
        // {
        //   id: `-2`,
        //   img: ``,
        //   accountName: `4Plus LineOA_mockup`,
        //   type: `line`,
        //   status: true,
        //   connectedBy: `developer_test`,
        //   connectedOn: new Date("2024-04-03 17:00:04+07:00"),
        // },
      ],
      //MENU DIALOG
      dialogMenu: false,
      menuDialogTitle: ``,
      menuDialogBody: ``,
      menuDialogBtn: ``,
      //addDialog
      addChannelDialogModel: false,
      //snackbar
      snackbarAlert: false,
      snackbarSuccess: false,
      snackbarMsg: "untitled",
      //loading
      isLoading: false,
      isError: false,
      errMsg: `untitled`,
    };
  },
  mounted() {
    // responsive
    this.$nextTick(() => {
      window.addEventListener("resize", this.onResize);
    });
    this.onResize();

    this.getList();
  },
  beforeDestroy() {
    window.removeEventListener("resize", this.onResize);
  },
  methods: {
    // resposive
    onResize() {
      this.windowWidth = window.innerWidth;
      this.windowHeight = window.innerHeight;
    },
    async getList() {
      this.isLoading = true;
      axios
        .get(`api/chat_center/list_channel_management/`)
        .then((res) => {
          this.itemTable = res.data;
          this.isLoading = false;
        })
        .catch((err) => {
          console.error(err);
          this.errMsg = err;
          this.isError = true;
          this.isLoading = false;
        });
    },
    //TOOLS
    timeSince(date, short) {
      const seconds = Math.floor((new Date() - date) / 1000);

      let interval = seconds / 31536000;
      if (interval > 1) {
        return Math.floor(interval) + (short ? " yr" : " years ago");
      }

      interval = seconds / 2592000;
      if (interval > 1) {
        return Math.floor(interval) + (short ? " mo" : " months ago");
      }

      interval = seconds / 86400;
      if (interval > 1) {
        return Math.floor(interval) + (short ? " d" : " days ago");
      }

      interval = seconds / 3600;
      if (interval > 1) {
        return Math.floor(interval) + (short ? " hr" : " hours ago");
      }

      interval = seconds / 60;
      if (interval > 1) {
        return Math.floor(interval) + (short ? " min" : " minutes ago");
      }

      return short ? "sec" : "seconds ago";
    },
    //Click
    clickEdit(item) {
      console.log(`edit`, item);
    },
    clickDeactive(item) {
      console.log(`deactive`, item);
      this.menuDialogTitle = `Are you sure to deactivate this channel?`;
      this.menuDialogBody = `If you deactivate the channel, the platform will stop collecting conversation from it.`;
      this.menuDialogBtn = `Yes, deactive`;
      this.dialogMenu = true;
    },
    clickDelete(item) {
      this.menuDialogTitle = `Are you sure to delete this channel?`;
      this.menuDialogBody = `If you delete the channel, It will be permanently deleted from the platform.`;
      this.menuDialogBtn = `Yes, delete`;
      this.dialogMenu = true;
    },
    addedChannel(item) {
      this.snackbarSuccess = item.isSuccess;
      this.snackbarMsg = item.msg;
      this.snackbarAlert = true;
      //reload list here
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

.custom-table td {
  display: flex;
  align-items: center;
  justify-content: flex-start;
}
</style>
