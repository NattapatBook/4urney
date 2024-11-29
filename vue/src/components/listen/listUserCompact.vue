<template>
  <div :style="{ width: '100%', height: `100%` }">
    <v-card-text
      :style="{
        display: `flex`,
        justifyContent: `space-between`,
        height: `80px`,
      }"
    >
      <div>
        <v-btn
          @click="minimizeComponents()"
          variant="tonal"
          icon=" mdi-chevron-right"
        />
      </div>
    </v-card-text>
    <v-divider class="mx-3" />
    <DataError
      :style="{ height: `calc(100% - 80px)` }"
      v-if="userItems.length < 1"
      :message="`No Data`"
    />
    <!-- list user -->
    <v-card-text
      class="pt-0 px-0"
      :style="{ height: `calc(100% - 80px)`, overflowY: `auto` }"
    >
      <v-card
        @click="clickSelectUser(item)"
        elevation="0"
        class="rounded-0"
        v-for="(item, idx) in sortUserItems()"
        :key="`listen_userItems_${item}_${idx}`"
        :style="{
          height: `auto`,
          cursor: `pointer`,
          backgroundColor:
            selectedUser && selectedUser.id === item.id
              ? `rgb(255 168 199)`
              : `white`,
        }"
      >
        <v-container>
          <v-row>
            <v-col
              cols="12"
              :style="{
                height: `100%`,
                display: `flex`,
                alignItems: `center`,
                justifyContent: `center`,
                flexDirection: `column`,
              }"
            >
              <div>
                <!--user avatar-->
                <div>
                  <v-avatar>
                    <v-img
                      v-if="item.img"
                      :src="item.img"
                      aspect-ratio="1"
                    ></v-img>
                    <v-img
                      v-else
                      :src="`https://ui-avatars.com/api/?name=${item.name}`"
                      aspect-ratio="1"
                    ></v-img>
                  </v-avatar>
                </div>
                <!--provider icon-->
                <div>
                  <v-img
                    :style="{
                      width: `15px`,
                      position: `absolute`,
                      top: `40px`,
                      left: `45px`,
                    }"
                    :src="providerIcon[item.provider]"
                    aspect-ratio="1"
                  ></v-img>
                </div>
                <!--chat-alert-icon-->
                <div v-if="selectedUser && selectedUser.id !== item.id">
                  <v-icon
                    :style="{
                      width: `15px`,
                      position: `absolute`,
                      top: `10px`,
                      right: `11px`,
                      // color: `rgb(254, 56, 147)`,
                      color:
                        item.priority === `high`
                          ? `#D6584D`
                          : item.priority === `medium`
                          ? `#ffa600`
                          : item.priority === `low`
                          ? `#5EB491`
                          : ``,
                    }"
                  >
                    <!-- mdi-chat-alert -->
                    mdi-alert-circle
                  </v-icon>
                </div>
                <!--priority-->
                <!-- <div
              v-if="item.priority"
              :style="{
                position: `absolute`,
                top: `7px`,
                left: `7px`,
              }"
            >
              <v-chip
                class="pa-1"
                size="small"
                :style="{
                  //   paddingInline: `8px`,
                  borderRadius: `50px`,
                  backgroundColor:
                    item.priority === `high`
                      ? `#D6584D`
                      : item.priority === `medium`
                        ? `#ffa600`
                        : item.priority === `low`
                          ? `#5EB491`
                          : ``,
                }"
              >
                <span
                  :style="{
                    textTransform: `uppercase`,
                    fontSize: `0.8rem`,
                    width: `18px`,
                    height: `15px`,
                    textAlign: `center`,
                    color: `white`,
                  }"
                  >{{ item.priority[0] }}</span
                >
              </v-chip>
            </div> -->
                <!--timestamp-->
                <div
                  class="mt-1"
                  :style="{
                    width: `100%`,
                    display: `flex`,
                    justifyContent: `center`,
                  }"
                >
                  <v-chip
                    size="x-small"
                    :style="{
                      width: `100%`,
                      display: `flex`,
                      justifyContent: `center`,
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
                            display: `flex`,
                            justifyContent: `center`,
                            alignItems: `center`,
                          }"
                        >
                          <!-- <v-icon :style="{ fontSize: `0.8rem` }"
                      >mdi-clock</v-icon
                    >&nbsp; -->
                          <span
                            :style="{
                              whiteSpace: `nowrap`,
                              overflow: `hidden`,
                              textOverflow: `ellipsis`,
                            }"
                            >{{ timeSince(item.timestamp, true) }}
                          </span>
                        </div>
                      </template>
                      <span>{{ new Date(item.timestamp) }} </span>
                    </v-tooltip>
                  </v-chip>
                </div>
              </div>
            </v-col>
          </v-row>
        </v-container>
      </v-card>
    </v-card-text>
  </div>
</template>

<script>
import line_icon from "@/assets/img/provider/line_icon.png";
import messenger_icon from "@/assets/img/provider/messenger_icon.png";
import instagram_icon from "@/assets/img/provider/instagram_icon.png";
import tiktok_icon from "@/assets/img/provider/tiktok_icon.png";
import DataError from "../tools/dataError.vue";
export default {
  name: "Component_ListUser_Compact",
  components: { DataError },
  props: {
    selectedUserProp: {
      type: Object,
      default: null,
    },
    userItems: {
      type: Object,
      default: () => {
        return [];
      },
    },
  },
  data() {
    return {
      windowWidth: 0,
      windowHeight: 0,
      //list user
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
      isSelectedDataChange: false,
      //tools
      providerIcon: {
        line: line_icon,
        messenger: messenger_icon,
        instagram: instagram_icon,
        tiktok: tiktok_icon,
      },
    };
  },
  mounted() {
    // responsive
    this.$nextTick(() => {
      window.addEventListener("resize", this.onResize);
    });
    this.onResize();

    //set selectedUset
    if (this.selectedUserProp) {
      this.clickSelectUser(this.selectedUserProp);
    }
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
    minimizeComponents() {
      this.$emit(`minimize`);
    },
    //userSelected
    clickSelectUser(item) {
      if (this.selectedUser.id !== item.id) {
        this.selectedUser = JSON.parse(JSON.stringify(item));
        this.isSelectedDataChange = !this.isSelectedDataChange;
      } else {
        this.selectedUser = JSON.parse(
          JSON.stringify({
            id: `-1`,
            img: ``,
            name: `untitled`,
            tag: `untitled`,
            priority: `untitled`,
            lastestMsg: `untitled`,
            timestamp: new Date(),
            isUrgent: false,
            provider: `untitled`,
          })
        );
        this.isSelectedDataChange = !this.isSelectedDataChange;
      }
      this.$emit("selectUser", this.selectedUser, this.isSelectedDataChange);
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
    sortUserItems() {
      return this.userItems.sort(
        (a, b) => new Date(b.timestamp) - new Date(a.timestamp)
      );
    },
  },
};
</script>

<style scoped></style>
