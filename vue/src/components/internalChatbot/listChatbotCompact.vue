<template>
  <div :style="{ width: '100%', height: `100%` }">
    <v-card-text
      class="px-1"
      :style="{
        display: `flex`,
        justifyContent: `center`,
        alignItems: `center`,
        height: `80px`,
      }"
    >
      <div>
        <v-btn
          :size="
            windowWidth > 960 && windowWidth < 1400 ? `x-small` : `default`
          "
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
      :messageSize="`0.5rem`"
      :iconSize="`2rem`"
    />
    <!-- list user -->
    <v-card-text
      class="px-0 pt-0"
      :style="{ height: `calc(100% - 80px)`, overflowY: `auto` }"
    >
      <v-card
        @click="clickSelectUser(item)"
        elevation="0"
        class="rounded-0 pa-2"
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
        <!-- <v-container> -->
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
              <!--isActive-->
              <div>
                <v-icon
                  :style="{
                    position: `absolute`,
                    top: `37px`,
                    left: `38px`,
                    fontSize: `0.8rem`,
                    color: item.isActive ? `#5EB491` : `#D6584D`,
                  }"
                  >mdi-checkbox-blank-circle
                </v-icon>
              </div>

              <div
                class="mt-1"
                :style="{
                  width: `100%`,
                  display: `flex`,
                  justifyContent: `center`,
                }"
              >
                <v-tooltip text="Tooltip" location="bottom">
                  <template v-slot:activator="{ props }">
                    <v-chip
                      v-bind="props"
                      size="x-small"
                      :style="{
                        width: `100%`,
                        display: `flex`,
                        justifyContent: `center`,
                      }"
                    >
                      <div
                        :style="{
                          whiteSpace: `nowrap`,
                          overflow: `hidden`,
                          textOverflow: `ellipsis`,
                          display: `flex`,
                          justifyContent: `center`,
                          alignItems: `center`,
                        }"
                      >
                        <span
                          :style="{
                            whiteSpace: `nowrap`,
                            overflow: `hidden`,
                            textOverflow: `ellipsis`,
                          }"
                          >{{ truncateString(item.name, 3) }}
                        </span>
                      </div>
                    </v-chip>
                  </template>
                  <div
                    class="HEHEHEHEHEHEHEHEHEEHHEHEHEHEHEHEHEHEHEEHHEHEHEHEHEHEHEHEHEEHHEHEHEHEHEHEHEHEHEEHHEHEHEHEHEHEHEHEHEEHHEHEHEHEHEHEHEHEHEEHHEHEHEHEHEHEHEHEHEEHHEHEHEHEHEHEHEHEHEEHHEHEHEHEHEHEHEHEHEEHHEHEHEHEHEHEHEHEHEEHHEHEHEHEHEHEHEHEHEEH"
                    :style="{
                      textAlignLast: `center`,
                      width: `100%`,
                    }"
                  >
                    <span>{{ truncateString(item.name, 10) }}</span>
                  </div>
                  <div
                    class="px-2 mb-2 mt-1"
                    :style="{
                      whiteSpace: `nowrap`,
                      overflow: `hidden`,
                      textOverflow: `ellipsis`,
                      borderRadius: `20px`,
                      background: `white`,
                      width: `fit-content`,
                      maxWidth: `100%`,
                    }"
                  >
                    <div
                      :style="{
                        color: item.isActive ? `#5EB491` : `#D6584D`,
                        fontSize: `0.8rem`,
                      }"
                    >
                      <span class="mx-1">
                        {{ item.isActive ? `Active` : `Inactive` }}
                      </span>
                      <v-icon :style="{ fontSize: `0.8rem` }"
                        >mdi-checkbox-blank-circle</v-icon
                      >
                    </div>
                  </div>
                </v-tooltip>
              </div>
            </div>
          </v-col>
        </v-row>
      </v-card>
    </v-card-text>
  </div>
</template>

<script>
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
    sortUserItems() {
      return this.userItems.sort((a, b) => a.name.localeCompare(b.name));
    },
    truncateString(text, maxLength) {
      if (text.length <= maxLength) {
        return text;
      }
      return text.slice(0, maxLength) + "..";
    },
  },
};
</script>

<style scoped></style>
