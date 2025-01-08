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
        multiple
        label="Enter chatbot name to search"
        variant="outlined"
        hide-details
        :density="`comfortable`"
        rounded="lg"
        :style="{ width: `5vw` }"
      >
      </v-text-field>
      <div
        :style="{
          display: `flex`,
          alignItems: `center`,
        }"
      >
        <v-btn
          :size="
            windowWidth > 960 && windowWidth < 1400 ? `x-small` : `default`
          "
          class="ml-2"
          variant="tonal"
          icon=" mdi-plus"
        />
      </div>
      <div
        :style="{
          display: `flex`,
          alignItems: `center`,
        }"
      >
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
        :key="`internalChatbot_chatbotItems_${item}_${idx}`"
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
                <!--industry-->
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
                    >&nbsp;{{ item.industry }}
                  </span>
                </div>
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
                <!--isActive-->
                <div
                  class="px-2"
                  :style="{
                    whiteSpace: `nowrap`,
                    overflow: `hidden`,
                    textOverflow: `ellipsis`,
                    border:
                      selectedUser && selectedUser.id === item.id
                        ? `solid 1px white`
                        : `solid 1px ${item.isActive ? `#5EB491` : `#D6584D`}`,
                    borderRadius: `20px`,
                    background: `white`,
                    width: `fit-content`,
                    maxWidth: `100%`,
                  }"
                >
                  <div
                    :style="{ color: item.isActive ? `#5EB491` : `#D6584D` }"
                  >
                    <span class="mx-1">
                      {{ item.isActive ? `Active` : `Inactive` }}
                    </span>
                    <v-icon :style="{ fontSize: `0.8rem` }"
                      >mdi-checkbox-blank-circle</v-icon
                    >
                  </div>
                </div>
              </div>
              <div
                :style="{
                  display: `flex`,
                  justifyContent: `flex-end`,
                }"
              >
                <span
                  :style="{
                    whiteSpace: `nowrap`,
                    overflow: `hidden`,
                    textOverflow: `ellipsis`,
                    maxWidth: `80%`,
                  }"
                  >{{ item.mastery }}
                </span>
              </div>
            </v-col>
          </v-row>
        </v-container>
      </v-card>
    </v-card-text>
  </div>
</template>

<script>
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

    filterUserItems() {
      const userItems = this.userItems;
      const filter = {
        searchMessage: this.searchMessage,
      };

      // Pre-process filter criteria
      const searchMessage = filter.searchMessage.trim().toLowerCase(); // Normalize search query

      // Filter items
      const filteredItems = userItems.filter((item) => {
        return (
          searchMessage === "" ||
          item.name.toLowerCase().includes(searchMessage) // Filter by name
        );
      });

      // Sort filtered items by name
      return filteredItems.sort((a, b) => a.name.localeCompare(b.name));
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
            industry: `untitled`,
            mastery: `untitled`,
            isActive: true,
            // tag: `untitled`,
            // priority: `untitled`,
            // lastestMsg: `untitled`,
            // isUrgent: false,
            // provider: `untitled`,
          })
        );
        this.isSelectedDataChange = !this.isSelectedDataChange;
      }
      this.$emit("selectUser", this.selectedUser, this.isSelectedDataChange);
    },
  },
};
</script>

<style scoped></style>
