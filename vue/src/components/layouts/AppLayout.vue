<template>
  <v-app :style="{ width: `100%` }">
    <v-app-bar
      :elevation="2"
      rounded
      :style="{
        top: `15px`,
        zIndex: `904`,
        transform: `translateY(0px)`,
        position: `absolute`,
        left:
          windowWidth > 960 ? `${windowWidth / 4}px` : `${windowWidth / 24}px`,
        width: dialog ? `0px` : windowWidth > 960 ? `50vw` : `90vw`,
        borderRadius: `100px`,
      }"
    >
      <div class="text-center pa-4">
        <v-dialog
          close-on-content-click="true"
          v-model="dialog"
          :transition="
            windowWidth > 960
              ? `dialog-left-transition`
              : `dialog-top-transition`
          "
          :style="{
            width: windowWidth > 960 ? `25.5vw !important` : `100%`,
            right: `initial`,
          }"
          :min-width="`400px`"
          fullscreen
        >
          <template v-slot:activator="{ props: activatorProps }">
            <v-btn icon="mdi-menu" v-bind="activatorProps"></v-btn>
          </template>

          <v-card :style="{ overflowY: `hidden` }">
            <v-toolbar
              :style="{
                background: `linear-gradient(
                  270deg,
                  rgba(242, 195, 235, 1) 10%,
                  rgba(229, 216, 245, 1) 40%,
                  rgba(217, 212, 252, 1) 70%,
                  rgba(201, 234, 247, 1) 100%
                )`,
              }"
            >
              <v-toolbar-title class="mx-0" :style="{ width: `100dvw` }">
                <div
                  :style="{
                    display: `flex`,
                    justifyContent: `space-between`,
                  }"
                >
                  <div
                    class="pl-4"
                    :style="{
                      display: `flex`,
                      alignItems: `center`,
                    }"
                  >
                    <v-avatar>
                      <img
                        :style="{ height: `50px` }"
                        src="@/assets/img/4urneyLogo.png"
                      />
                    </v-avatar>

                    &nbsp;
                    <span
                      v-if="windowWidth >= 360"
                      :style="{
                        fontSize: `1.7rem`,
                        color: `black`,
                      }"
                      >4urney</span
                    >
                  </div>
                  <div class="pr-4">
                    <v-btn icon="mdi-close" @click="dialog = false"></v-btn>
                  </div>
                </div>
              </v-toolbar-title>
            </v-toolbar>

            <v-list
              class="mt-4"
              lines="two"
              subheader
              :style="{ overflowX: `hidden` }"
            >
              <div class="px-4">
                <v-avatar
                  :style="{
                    height: '48px !important',
                    minWidth: '48px !important',
                    width: '48px !important',
                    aspectRatio: '1',
                  }"
                >
                  <v-img
                    aspect-ratio="1"
                    :src="`https://ui-avatars.com/api/?name=${user.name}`"
                  ></v-img>
                </v-avatar>
              </div>
              <v-list-item
                class="py-0"
                :style="{
                  whiteSpace: `nowrap`,
                  overflow: `hidden`,
                  textOverflow: `ellipsis`,
                }"
                :subtitle="`${user.role}`"
              >
                <span class="gradient-text">{{ user.name }}</span>
              </v-list-item>
              <v-list-item class="pt-0">
                <div class="pt-0">
                  <v-btn
                    @click="clickLogout()"
                    :style="{
                      color: `white`,
                      background: `rgb(254,56,147)`,
                      background: `linear-gradient(45deg, rgba(254,56,147,1) 0%, rgba(55,61,133,1) 59%)`,
                    }"
                  >
                    <span>logout</span>&nbsp;
                    <v-icon>mdi-logout</v-icon>
                  </v-btn>
                </div>
              </v-list-item>

              <v-divider></v-divider>

              <v-list-subheader>Menu</v-list-subheader>

              <v-list-item
                class="hover-gradient"
                v-for="item in items"
                :key="`appLayout_${item.name}`"
                link
                @click="clickChangeMenu(item.name)"
              >
                <div>
                  <v-icon>{{ item.icon }}</v-icon>
                  &nbsp;
                  <span :style="{ textTransform: `capitalize` }">{{
                    item.name
                  }}</span>
                </div>
              </v-list-item>
            </v-list>
            <v-spacer />
            <v-divider></v-divider>

            <v-list-subheader>
              <v-card-text>
                <span
                  v-if="windowWidth >= 360"
                  class="gradient-text"
                  :style="{ fontSize: `0.8rem` }"
                  >4urney</span
                >
                <p class="gradient-text">Version 1.0.1 Beta (Demo Edition)</p>
                <p class="gradient-text">All copyrights reserved</p>
              </v-card-text>
            </v-list-subheader>
          </v-card>
        </v-dialog>
      </div>
      <v-app-bar-title class="ma-0">
        <div
          :style="{
            display: `flex`,
            alignItems: `center`,
            justifyContent: windowWidth > 960 ? `space-between` : `center`,
          }"
        >
          <div
            :style="{
              display: `flex`,
              alignItems: `center`,
            }"
          >
            <v-avatar>
              <img
                :style="{ height: `50px` }"
                src="@/assets/img/4urneyLogo.png"
              />
            </v-avatar>
            &nbsp;
            <span v-if="windowWidth >= 360" :style="{ fontSize: `1.7rem` }"
              >4urney</span
            >
          </div>
        </div>
      </v-app-bar-title>
      <div
        :style="{
          display: `flex`,
          alignItems: `center`,
        }"
      >
        <div v-if="windowWidth > 960">
          <div
            :style="{
              whiteSpace: `nowrap`,
              overflow: `hidden`,
              textOverflow: `ellipsis`,
              maxWidth: `15vw`,
            }"
          >
            <p
              :style="{
                fontSize: `1rem`,
                fontWeight: `bold`,
              }"
            >
              Login as
            </p>
            <v-tooltip text="Tooltip" location="bottom">
              <template v-slot:activator="{ props }">
                <span
                  class="gradient-text"
                  :style="{ cursor: `pointer` }"
                  v-bind="props"
                  >{{ user.name }}</span
                >
              </template>
              {{ user.name }}
            </v-tooltip>
          </div>
        </div>
        <div class="pa-4">
          <v-menu transition="scale-transition">
            <template v-slot:activator="{ props }">
              <v-avatar
                v-bind="props"
                :style="{
                  height: '48px !important',
                  minWidth: '48px !important',
                  width: '48px !important',
                  aspectRatio: '1',
                  cursor: `pointer`,
                }"
              >
                <v-img
                  aspect-ratio="1"
                  :src="`https://ui-avatars.com/api/?name=${user.name}`"
                ></v-img>
              </v-avatar>
            </template>
            <v-card
              class="rounded-lg"
              :style="{ width: windowWidth > 960 ? `30vw` : `70vw` }"
            >
              <!--profile-->
              <v-card-text>
                <v-container>
                  <v-row>
                    <v-col
                      class="pb-0"
                      :style="{
                        display: `flex`,
                        alignItems: `center`,
                        justifyContent: `center`,
                      }"
                      cols="12"
                    >
                      <span :style="{ fontWeight: `bold` }">Profile</span>
                    </v-col>
                    <v-col
                      class="pb-0"
                      :style="{
                        display: `flex`,
                        alignItems: `center`,
                        justifyContent: `center`,
                      }"
                      cols="12"
                    >
                      <v-avatar
                        v-bind="props"
                        :style="{
                          height: '75px !important',
                          minWidth: '75px !important',
                          width: '75px !important',
                          aspectRatio: '1',
                          cursor: `pointer`,
                        }"
                      >
                        <v-img
                          aspect-ratio="1"
                          :src="`https://ui-avatars.com/api/?name=${user.name}`"
                        ></v-img>
                      </v-avatar>
                    </v-col>
                    <v-col
                      :style="{
                        display: `flex`,
                        alignItems: `center`,
                        justifyContent: `center`,
                      }"
                      cols="12"
                    >
                      <span class="gradient-text">{{ user.name }}</span>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>
              <v-divider :style="{ color: `black` }" class="mx-10" />
              <!--notification-->
              <v-card-text>
                <v-row>
                  <v-col
                    class="pt-0"
                    :style="{
                      display: `flex`,
                      alignItems: `center`,
                      justifyContent: `center`,
                    }"
                    cols="12"
                  >
                    <span :style="{ fontWeight: `bold` }">Notification</span>
                  </v-col>
                  <v-col class="pt-0">
                    <v-card
                      elevation="0"
                      :style="{ height: `50vh`, overflowY: `auto` }"
                    >
                      <v-card-text
                        class="pa-1"
                        v-for="(noti, idx) in notification"
                        :key="`noti_${idx}_${noti.titleMsg}`"
                        :style="{ borderBottom: `solid 1px lightgrey` }"
                      >
                        <div>
                          <span :style="{ color: `black` }">{{
                            noti.titleMsg
                          }}</span>
                        </div>
                        <div
                          :style="{
                            whiteSpace: `nowrap`,
                            overflow: `hidden`,
                            textOverflow: `ellipsis`,
                          }"
                        >
                          <span
                            :style="{
                              whiteSpace: `nowrap`,
                              overflow: `hidden`,
                              textOverflow: `ellipsis`,
                              color: `grey`,
                            }"
                            >{{ noti.bodyMsg }}
                          </span>
                        </div>
                      </v-card-text>
                    </v-card>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-menu>
        </div>
      </div>
    </v-app-bar>
    <main>
      <slot />
    </main>
  </v-app>
</template>

<script>
import axios from "axios";
export default {
  props: {
    user: {
      type: Object,
      default: () => {
        return {
          email: `untitled`,
          name: `untitled`,
          role: `untitled`,
        };
      },
    },
  },
  data() {
    return {
      // responsive
      windowWidth: 0,
      items: [
        { name: "home", icon: `mdi-home` },
        { name: "listen", icon: `mdi-message` },
        { name: "channel manage", icon: `mdi-account-file` },
        { name: "user manage", icon: `mdi-account` },
        { name: "Dashboard", icon: `mdi-view-dashboard` },
        { name: "Feature 5", icon: `mdi-numeric-5-box` },
      ],
      dialog: false,
      notification: [
        {
          id: 1,
          img: ``,
          titleMsg: `Title Message 1`,
          bodyMsg: `Body Message 1 Body Message 1 Body Message 1 Body Message 1 Body Message 1 Body Message 1`,
        },
        {
          id: `2`,
          img: ``,
          titleMsg: `Title Message 2`,
          bodyMsg: `Body Message 2 Body Message 2 Body Message 2 Body Message 2 Body Message 2 Body Message 2`,
        },
        {
          id: `3`,
          img: ``,
          titleMsg: `Title Message 3`,
          bodyMsg: `Body Message 3 Body Message 3 Body Message 3`,
        },
        {
          id: `4`,
          img: ``,
          titleMsg: `Title Message 4`,
          bodyMsg: `Body Message 4 Body Message 4 Body Message 4`,
        },
      ],
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
    // resposive
    onResize() {
      this.windowWidth = window.innerWidth;
    },
    clickChangeMenu(menu) {
      this.$emit(`navigate`, menu);
    },
    clickLogout() {
      axios
        .get(`api/chat_center/logout/`)
        .then((res) => {
          console.log(res.data);
          this.$emit("navigate", "landing");
        })
        .catch((err) => {
          console.error(err);
        });
    },
  },
};
</script>
<style scoped>
.hover-gradient {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.hover-gradient:hover {
  transform: scale(1.01);
  z-index: 999;
  color: rgb(55, 61, 133);
}
</style>
