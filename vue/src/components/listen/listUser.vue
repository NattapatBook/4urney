<template>
  <div :style="{ width: '100%', height: `100%` }">
    <v-card-text
      class="px-1"
      :style="{
        display: `flex`,
        justifyContent: `space-between`,
        height: `80px`,
      }"
    >
      <v-text-field
        v-model="searchMessage"
        clearable
        @click:clear="searchText = ''"
        multiple
        label="Enter name to search"
        variant="outlined"
        hide-details
        :density="`comfortable`"
        rounded="lg"
        :style="{ width: `5vw` }"
      >
      </v-text-field>
      <div
        class="ml-2"
        :style="{
          display: `flex`,
          alignItems: `center`,
        }"
      >
        <!--filter-->
        <v-menu
          v-if="windowWidth >= 360"
          v-model="filterMenu"
          :close-on-content-click="false"
          transition="scale-transition"
          location="bottom"
        >
          <template v-slot:activator="{ props: menu }">
            <v-btn
              :size="
                windowWidth > 960 && windowWidth < 1400 ? `x-small` : `default`
              "
              v-bind="menu"
              variant="tonal"
              icon="mdi-filter"
              :style="{
                backgroundColor: isFilterInUse() ? `#ffa8c7` : ``,
              }"
            >
            </v-btn>
          </template>
          <v-container>
            <v-row>
              <!-- filter -->
              <v-col class="px-1" :style="{ height: `100%`, width: `50%` }">
                <v-card
                  elevation="0"
                  :style="{
                    height: `100%`,
                    width: `100%`,
                    borderRadius: `8px`,
                    border: `solid 1px lightgrey`,
                  }"
                >
                  <v-card-title
                    :style="{
                      display: `flex`,
                      alignItems: `center`,
                    }"
                  >
                    <span :style="{ fontWeight: `bold` }">Message</span>
                    <v-spacer />
                    <v-btn
                      @click="filterMenu = false"
                      variant="text"
                      icon="mdi-close"
                    ></v-btn>
                  </v-card-title>
                  <div
                    :style="{
                      overflowY: `auto`,
                      overflowX: `hidden`,
                    }"
                  >
                    <!-- channelsSelected -->
                    <v-card-text class="pt-2 pb-0">
                      <v-autocomplete
                        v-model="channelsModel"
                        clearable
                        multiple
                        label="Channels"
                        variant="outlined"
                        hide-details
                        rounded="lg"
                        item-title="name"
                        item-value="name"
                        chips
                        density="comfortable"
                        :color="`#ff5d97`"
                        :items="channelsItem"
                        :style="{
                          textTransform: `capitalize`,
                        }"
                        @update:model-value="getData"
                      >
                        <template v-slot:chip="{ props, item }">
                          <v-chip
                            variant="text"
                            v-bind="props"
                            :prepend-avatar="item.raw.icon"
                            :text="``"
                          ></v-chip>
                        </template>
                        <template v-slot:item="{ props, item }">
                          <v-list-item
                            v-bind="props"
                            :prepend-avatar="item.raw.icon"
                          ></v-list-item>
                        </template>
                      </v-autocomplete>
                    </v-card-text>
                    <!-- messageTypeSelected -->
                    <v-card-text class="pb-0" :style="{ width: `100%` }">
                      <v-btn
                        v-for="(item, idx) in messageTypeSelectedItem"
                        :key="`messageTypeSelected_${item}_${idx}`"
                        :disabled="messageType === item"
                        block
                        class="rounded-pill mb-2"
                        elevation="0"
                        :style="{
                          backgroundColor:
                            messageType === item ? `#ff5d97` : `white`,
                          color: messageType === item ? `white` : `black`,
                          display: `block`,
                          // alignItems: `center`,
                          // justifyContent: `center`,
                          height: `25px`,
                          cursor: `pointer`,
                          whiteSpace: `nowrap`,
                          overflow: `hidden`,
                          textOverflow: `ellipsis`,
                          width: `100%`,
                        }"
                        @click="clickSelectMessageType(item)"
                      >
                        <span
                          :style="{
                            fontSize: `0.8rem`,
                            whiteSpace: `nowrap`,
                            overflow: `hidden`,
                            textOverflow: `ellipsis`,
                          }"
                          >{{ item }}</span
                        >
                      </v-btn>
                    </v-card-text>
                    <v-divider class="mx-10" />
                    <!-- messagePriority -->
                    <v-card-text class="pb-0">
                      <p class="mb-2" :style="{ fontWeight: `bold` }">
                        Priority
                      </p>
                      <div :style="{ display: `flex` }">
                        <v-btn
                          v-for="(item, idx) in messagePriorityItems"
                          :key="`messagePriority${item}_${idx}`"
                          class="rounded-pill mb-2 mx-1"
                          elevation="0"
                          :style="{
                            backgroundColor: messagePriority.includes(item)
                              ? item === `high`
                                ? `#D6584D`
                                : item === `medium`
                                ? `#ffa600`
                                : item === `low`
                                ? `#5EB491`
                                : `#ff5d97`
                              : `white`,
                            color: messagePriority.includes(item)
                              ? `white`
                              : `black`,
                            display: `block`,
                            // alignItems: `center`,
                            // justifyContent: `center`,
                            height: `25px`,
                            width: `30%`,
                            cursor: `pointer`,
                          }"
                          @click="clickMessagePriorityChange(item)"
                        >
                          <span :style="{ fontSize: `0.8rem` }">{{
                            item
                          }}</span>
                        </v-btn>
                      </div>
                    </v-card-text>
                    <!-- Tag -->
                    <v-card-text class="pb-0">
                      <p class="mb-2" :style="{ fontWeight: `bold` }">Tag</p>
                      <v-autocomplete
                        v-model="tagModel"
                        clearable
                        multiple
                        label="Tag"
                        variant="outlined"
                        hide-details
                        rounded="lg"
                        closable-chips
                        density="comfortable"
                        chips
                        :items="tagItems"
                        :color="`#ff5d97`"
                        @update:model-value="getData"
                      >
                        <template v-slot:chip="{ props, item }">
                          <v-chip
                            v-bind="props"
                            :text="item.raw"
                            :style="{
                              backgroundColor: `#ff5d97`,
                              color: `white`,
                            }"
                          ></v-chip>
                        </template>
                      </v-autocomplete>
                    </v-card-text>
                    <v-divider class="mx-10" />
                    <!-- Agents -->
                    <v-card-text class="pb-2">
                      <p class="mb-2" :style="{ fontWeight: `bold` }">Agents</p>
                      <v-autocomplete
                        v-model="agentsSelected"
                        clearable
                        multiple
                        label="Agents"
                        variant="outlined"
                        hide-details
                        rounded="lg"
                        chips
                        density="comfortable"
                        closable-chips=""
                        :items="agentsItems"
                        :color="`#ff5d97`"
                        @update:model-value="getData"
                      >
                        <template v-slot:chip="{ props, item }">
                          <v-chip
                            v-bind="props"
                            :text="item.raw"
                            :style="{
                              backgroundColor: `#ff5d97`,
                              color: `white`,
                            }"
                          ></v-chip>
                        </template>
                      </v-autocomplete>
                    </v-card-text>
                    <!-- set default -->
                    <v-card-text
                      :style="{
                        display: `flex`,
                        justifyContent: `center`,
                        alignItems: `center`,
                      }"
                    >
                      <v-btn
                        rounded
                        size="small"
                        @click="clickClearFilter()"
                        :disabled="!isFilterInUse()"
                        variant="outlined"
                        >set default</v-btn
                      >
                    </v-card-text>
                  </div>
                </v-card>
              </v-col>
            </v-row>
          </v-container>
        </v-menu>
        <v-btn
          :size="
            windowWidth > 960 && windowWidth < 1400 ? `x-small` : `default`
          "
          class="ml-2"
          @click="minimizeComponents()"
          variant="tonal"
          icon=" mdi-chevron-left"
        />
      </div>
    </v-card-text>
    <v-divider class="mx-3" />
    <DataError
      :style="{ height: `calc(100% - 80px)` }"
      v-if="userItems.length < 1 || filterUserItems().length < 1"
      :message="`No Data`"
    />
    <!-- list user -->
    <v-card-text
      v-else
      class="pt-0 px-0"
      :style="{ height: `calc(100% - 80px)`, overflowY: `auto` }"
    >
      <v-card
        elevation="0"
        class="rounded-xl"
        @click="clickSelectUser(item)"
        v-for="(item, idx) in filterUserItems()"
        :key="`listen_userItems_${item}_${idx}`"
        :style="{
          height: `70px`,
          cursor: `pointer`,
          backgroundColor:
            selectedUser && selectedUser.id === item.id
              ? `rgb(255 168 199)`
              : `white`,
          // border: `solid 0.05rem lightgrey`,
        }"
      >
        <v-container>
          <v-row>
            <v-col class="pr-0" cols="6" :style="{ display: `flex` }">
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
                    top: `44px`,
                    left: `45px`,
                  }"
                  :src="providerIcon[item.provider]"
                  aspect-ratio="1"
                ></v-img>
              </div>
              <!--chat-alert-icon-->
              <div
                :key="`listUser_alert_${item.id}_${item.timestamp}`"
                v-if="
                  selectedUser &&
                  selectedUser.id !== item.id &&
                  checkLatest(item.id, item.timestamp)
                "
              >
                <v-icon
                  class="pa-0"
                  :style="{
                    width: `15px`,
                    position: `absolute`,
                    top: `13px`,
                    left: `43px`,
                    color: `rgb(254, 56, 147)`,
                    //color:
                    // item.priority === `high`
                    // ? `#D6584D`
                    // : item.priority === `medium`
                    // ? `#ffa600`
                    // : item.priority === `low`
                    // ? `#5EB491`
                    // : ``,
                  }"
                >
                  <!-- mdi-chat-alert -->
                  mdi-alert-circle
                </v-icon>
              </div>
              <div
                class="ml-2"
                :style="{
                  display: `flex`,
                  flexDirection: `column`,
                  maxWidth: `calc(100% - 50px)`,
                }"
              >
                <div
                  :style="{
                    display: `flex`,
                    justifyContent: `flex-start`,
                  }"
                >
                  <span
                    :style="{
                      whiteSpace: `nowrap`,
                      overflow: `hidden`,
                      textOverflow: `ellipsis`,
                    }"
                    >&nbsp;{{ item.name }}
                  </span>
                </div>
                <v-tooltip text="Tooltip" location="bottom">
                  <template v-slot:activator="{ props }">
                    <div
                      v-bind="props"
                      class="px-2"
                      :style="{
                        whiteSpace: `nowrap`,
                        overflow: `hidden`,
                        textOverflow: `ellipsis`,
                        backgroundColor:
                          selectedUser && selectedUser.id === item.id
                            ? `white`
                            : `lightgrey`,
                        borderRadius: `20px`,
                        width: `fit-content`,
                        maxWidth: `100%`,
                      }"
                    >
                      <span>{{ item.lastestMsg }} </span>
                    </div>
                  </template>
                  {{ item.lastestMsg }}
                </v-tooltip>
              </div>
            </v-col>
            <v-col
              class="pl-0"
              cols="6"
              :style="{
                display: `flex`,
                flexDirection: `column`,
                justifyContent: `flex-end`,
              }"
            >
              <div
                :style="{
                  justifyContent: `flex-end`,
                  display: `flex`,
                  alignItems: `center`,
                }"
              >
                <!--tags-->
                <div
                  v-if="item.tag"
                  :style="{
                    justifyContent: `flex-end`,
                    display: `flex`,
                    alignItems: `center`,
                  }"
                >
                  <v-icon :style="{ fontSize: `0.8rem` }">mdi-tag</v-icon>&nbsp;
                  <span>{{ item.tag }}</span>
                </div>
                &nbsp;
                <div
                  v-if="item.messageType"
                  :style="{
                    justifyContent: `flex-end`,
                    display: `flex`,
                    alignItems: `center`,
                  }"
                >
                  <v-chip
                    size="x-small"
                    :color="
                      item.messageType === `Closed Messages`
                        ? ``
                        : item.messageType === `Opened Messages`
                        ? `#2196f3`
                        : `red`
                    "
                  >
                    <span>{{
                      item.messageType === `Closed Messages`
                        ? `Closed`
                        : item.messageType === `Opened Messages`
                        ? `Open`
                        : `???`
                    }}</span>
                  </v-chip>
                </div>
              </div>
              <v-tooltip text="Tooltip" location="bottom">
                <template v-slot:activator="{ props }">
                  <div
                    v-bind="props"
                    :style="{
                      whiteSpace: `nowrap`,
                      overflow: `hidden`,
                      textOverflow: `ellipsis`,
                      display: `flex`,
                      justifyContent: `flex-end`,
                      alignItems: `center`,
                    }"
                  >
                    <v-icon :style="{ fontSize: `0.8rem` }">mdi-clock</v-icon
                    >&nbsp;
                    <span
                      :style="{
                        whiteSpace: `nowrap`,
                        overflow: `hidden`,
                        textOverflow: `ellipsis`,
                      }"
                      >{{ timeSince(item.timestamp) }}
                    </span>
                  </div>
                </template>
                <span>{{ new Date(item.timestamp) }}</span>
              </v-tooltip>
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
  name: "Component_ListUser",
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
      //head
      searchMessage: ``,
      //filter
      filterMenu: false,
      //filter - channel
      channelsModel: [],
      channelsItem: [
        { name: `Line`, icon: line_icon },
        { name: `Messenger`, icon: messenger_icon },
        { name: `Instagram`, icon: instagram_icon },
        { name: `Tiktok`, icon: tiktok_icon },
      ],
      //filter - messageTypeSelected
      messageTypeSelectedItem: [
        `All Messages`,
        `Opened Messages`,
        `Closed Messages`,
      ],
      messageType: `All Messages`,
      //filter - messagePriority
      messagePriorityItems: [`high`, `medium`, `low`],
      messagePriority: [],
      //filter - tag
      tagModel: [],
      tagItems: [`VVIP`, `VIP`],
      //filter - agents
      searchAgent: ``,
      agentsItems: [
        `Me`,
        `Agent1`,
        `Agent2`,
        `Agent3`,
        `Agent4`,
        `Agent5`,
        `Agent6`,
        `Agent7`,
        `Agent8`,
      ],
      agentsSelected: [],
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
    //filter
    clickClearFilter() {
      this.channelsModel = [];
      this.messageType = `All Messages`;
      this.messagePriority = [];
      this.tagModel = [];
      this.agentsSelected = [];
      this.searchMessage = ``;
    },
    isFilterInUse() {
      const filter = {
        provider: this.channelsModel,
        messageType: this.messageType,
        priority: this.messagePriority,
        tag: this.tagModel,
        agent: this.agentsSelected,
        searchMessage: this.searchMessage,
      };
      return Object.values(filter).some((criteria) => {
        if (Array.isArray(criteria)) {
          return criteria.length > 0;
        } else {
          return criteria !== "" && criteria.toLowerCase() !== "all messages";
        }
      });
    },
    filterUserItems() {
      const userItems = this.userItems;
      const filter = {
        provider: this.channelsModel,
        messageType: this.messageType,
        priority: this.messagePriority,
        tag: this.tagModel,
        agent: this.agentsSelected,
        searchMessage: this.searchMessage,
      };

      // Pre-process filter criteria
      const providerSet = new Set(filter.provider.map((p) => p.toLowerCase()));
      const messageType = filter.messageType.toLowerCase(); // Lowercase for case insensitivity
      const prioritySet = new Set(filter.priority);
      const tagSet = new Set(filter.tag);
      const agentSet = new Set(filter.agent);
      const searchMessage = filter.searchMessage.trim().toLowerCase(); // Normalize search query

      // Filter items
      const filteredItems = userItems.filter((item) => {
        return (
          (providerSet.size === 0 ||
            providerSet.has(item.provider.toLowerCase())) &&
          (messageType === "all messages" ||
            messageType === "" ||
            item.messageType.toLowerCase() === messageType) &&
          (prioritySet.size === 0 || prioritySet.has(item.priority)) &&
          (tagSet.size === 0 || tagSet.has(item.tag)) &&
          (agentSet.size === 0 || agentSet.has(item.agent)) &&
          (searchMessage === "" ||
            item.name.toLowerCase().includes(searchMessage)) // Filter by name
        );
      });

      // Sort filtered items by timestamp
      return filteredItems.sort(
        (a, b) => new Date(b.timestamp) - new Date(a.timestamp)
      );
    },
    clickSelectMessageType(item) {
      this.messageType = item;
    },
    clickMessagePriorityChange(item) {
      if (this.messagePriority.includes(item)) {
        this.messagePriority = this.messagePriority.filter((priority) => {
          if (priority !== item) {
            return item;
          }
        });
      } else {
        this.messagePriority.push(item);
      }
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
    checkLatest(id, time) {
      const storedData = JSON.parse(localStorage.getItem("chatData")) || [];

      const item = storedData.find((entry) => entry.id === id);
      if (item) {
        return new Date(item.timestamp) < new Date(time);
      }
      return false;
    },
  },
};
</script>

<style scoped></style>
