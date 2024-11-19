<template>
  <v-app>
    <div
      :style="{
        boxShadow:
          scrollPosition > 60
            ? `2px 2px 20px 6px #000000${scrollPosition - 60} !important`
            : ``,
      }"
      class="landing-layout py-3"
    >
      <div class="div-app-bar" :style="{ fontWeight: `bold` }">
        <v-avatar class="mr-2">
          <v-img :src="'/img/4urneyLogo.png'"></v-img>
        </v-avatar>
        <p :style="{ fontSize: `1.2rem` }">4urney</p>
      </div>
      <v-spacer></v-spacer>
      <v-btn
        v-if="windowWidth > 880"
        variant="text"
        @click="scrollTo('features')"
        >Features</v-btn
      >
      <v-btn
        v-if="windowWidth > 880"
        variant="text"
        @click="scrollTo('solution')"
        >Solution</v-btn
      >
      <v-btn
        v-if="windowWidth > 880"
        variant="text"
        @click="scrollTo('trustedCustomers')"
        >Our Trusted Customers</v-btn
      >

      <v-dialog
        v-if="windowWidth > 880"
        max-width="500"
        transition="dialog-bottom-transition"
      >
        <template v-slot:activator="{ props: activatorProps }">
          <v-btn v-bind="activatorProps" variant="text">Contact Us</v-btn>
        </template>

        <template v-slot:default="{ isActive }">
          <v-card
            class="rounded-xl pa-4"
            :style="{ backgroundColor: `#f1f1f1` }"
          >
            <v-card-title class="card-title-contact-dialog">
              <span>Contact Us</span>
              <v-btn
                variant="plain"
                text
                icon="mdi-close"
                @click="isActive.value = false"
              ></v-btn>
            </v-card-title>
            <v-card-text>
              <div
                class="mb-5"
                :style="{ display: `flex`, justifyContent: `center` }"
              >
                <v-avatar :style="{ width: `150px`, height: `150px` }">
                  <v-img
                    src="https://itupdate.com.au/IBMPartnerSolutionsHub/images/Partner-logo-circle-4plus.png"
                  />
                </v-avatar>
              </div>
              <p :style="{ fontWeight: `bold` }">
                4Plus Group Company Limited.
              </p>
              <p>18th Floor K.S.L.Tower</p>
              <p>503 Sri-Ayutthaya Road, Ratchathewi</p>
              <p>Bangkok 10400, Thailand</p>
              <p>
                Emall.
                <span :style="{ fontWeight: `bold` }">4urney@4plus.co.th</span>
              </p>
              <p>
                Tel. <span :style="{ fontWeight: `bold` }">+662 640 1151</span>
              </p>
            </v-card-text>
          </v-card>
        </template>
      </v-dialog>
      <v-menu transition="fab-transition">
        <template v-slot:activator="{ props }">
          <v-btn
            v-if="windowWidth <= 880"
            class="mr-2"
            icon="mdi-dots-vertical"
            variant="text"
            v-bind="props"
          ></v-btn>
        </template>

        <v-list class="pa-0">
          <v-list-item class="pa-0">
            <v-card class="pa-4" @click="scrollTo('features')" elevation="0">
              <span>Features</span>
            </v-card>
          </v-list-item>
          <v-list-item class="pa-0">
            <v-card class="pa-4" @click="scrollTo('solution')" elevation="0">
              <span>Solution</span>
            </v-card>
          </v-list-item>
          <v-list-item class="pa-0">
            <v-card
              class="pa-4"
              @click="scrollTo('trustedCustomers')"
              elevation="0"
            >
              <span>Our Trusted Customers</span>
            </v-card>
          </v-list-item>

          <v-list-item class="pa-0">
            <v-dialog max-width="500" transition="dialog-bottom-transition">
              <template v-slot:activator="{ props: activatorProps }">
                <v-card
                  v-bind="activatorProps"
                  class="pa-4"
                  @click="scrollTo('trustedCustomers')"
                  elevation="0"
                >
                  <span>Contact Us</span>
                </v-card>
              </template>

              <template v-slot:default="{ isActive }">
                <v-card
                  elevation="0"
                  class="rounded-xl pa-4"
                  :style="{ backgroundColor: `#f1f1f1` }"
                >
                  <v-card-title class="card-title-contact-dialog">
                    <span>Contact Us</span>
                    <v-btn
                      variant="plain"
                      text
                      icon="mdi-close"
                      @click="isActive.value = false"
                    ></v-btn>
                  </v-card-title>
                  <v-card-text>
                    <div
                      class="mb-5"
                      :style="{ display: `flex`, justifyContent: `center` }"
                    >
                      <v-avatar :style="{ width: `150px`, height: `150px` }">
                        <v-img
                          src="https://itupdate.com.au/IBMPartnerSolutionsHub/images/Partner-logo-circle-4plus.png"
                        />
                      </v-avatar>
                    </div>
                    <p :style="{ fontWeight: `bold` }">
                      4Plus Group Company Limited.
                    </p>
                    <p>18th Floor K.S.L.Tower</p>
                    <p>503 Sri-Ayutthaya Road, Ratchathewi</p>
                    <p>Bangkok 10400, Thailand</p>
                    <p>
                      Emall.
                      <span :style="{ fontWeight: `bold` }"
                        >4urney@4plus.co.th</span
                      >
                    </p>
                    <p>
                      Tel.
                      <span :style="{ fontWeight: `bold` }">+662 640 1151</span>
                    </p>
                  </v-card-text>
                </v-card>
              </template>
            </v-dialog>
          </v-list-item>
        </v-list>
      </v-menu>
      <v-btn
        class="get-login-btn rounded-lg px-5 py-2"
        color="primary"
        @click="$emit('navigate', 'home')"
        >Login</v-btn
      >
    </div>

    <v-main>
      <v-container fluid class="px-0">
        <!-- Landing Page Section -->
        <v-row
          justify="center"
          align="center"
          class="landing-page"
          id="landingPage"
        >
          <v-col cols="9" sm="9" md="8" lg="8" xl="6" xxl="6">
            <v-carousel
              class="rounded-xl"
              hide-delimiters
              hide-delimiter-background
              show-arrows="hover"
            >
              <!-- BOOST -->
              <v-carousel-item>
                <v-card class="pa-4 rounded-xl card-landing-top">
                  <v-card-title>
                    <p :style="{ fontSize: `2em`, fontWeight: `bold` }">
                      BOOST 🚀
                    </p>
                    <p :style="{ fontSize: `0.8em` }">Your Customer Service</p>
                    <p :style="{ fontSize: `0.8em` }">
                      with
                      <span
                        class="gradient-text"
                        :style="{ fontWeight: `bold` }"
                        >AI-Powered</span
                      >
                    </p>
                  </v-card-title>
                  <v-card-text class="pb-0">
                    <p :style="{ fontSize: `1rem`, color: `grey` }">
                      "Seamlessly integrate with LINE OA, Facebook, and more.
                      Manage chats effortlessly with automated responses and
                      personalized support to resolve customer issues quickly."
                    </p>
                  </v-card-text>
                  <v-card-text
                    :style="{
                      display: `flex`,
                    }"
                  >
                    <v-img
                      :style="{ aspectRatio: `30/9 !important` }"
                      :src="'/img/landing/showChat.png'"
                    ></v-img>
                    <!-- <div
                      class="mb-2"
                      v-for="(item, idx) in showChat"
                      :key="`landing_show_chat_${idx}`"
                      :style="{
                        display: `flex`,
                        justifyContent:
                          item.type === `customer` ? `flex-start` : `flex-end`,
                      }"
                    >
                      <v-avatar
                        v-if="item.type === `customer`"
                        size="small"
                        class="mr-2"
                      >
                        <v-img
                          :src="`https://ui-avatars.com/api/?name=${item.type}`"
                          aspect-ratio="1"
                        ></v-img>
                      </v-avatar>
                      <v-chip
                        :style="{
                          backgroundColor:
                            item.type === `admin`
                              ? `#8eff8e`
                              : item.type === `ai`
                              ? `rgba(242, 195, 235, 1)`
                              : ``,
                          color:
                            item.type === `ai` ? `rgba(254, 56, 147, 1)` : ``,
                        }"
                      >
                        {{ item.msg }}
                      </v-chip>
                      <v-avatar
                        v-if="item.type !== `customer`"
                        size="small"
                        class="ml-2"
                      >
                        <v-img
                          :src="`https://ui-avatars.com/api/?name=${item.type}`"
                          aspect-ratio="1"
                        ></v-img>
                      </v-avatar>
                    </div> -->
                  </v-card-text>
                </v-card>
              </v-carousel-item>
              <!-- CORE -->
              <v-carousel-item>
                <v-card class="pa-4 rounded-xl card-landing-top">
                  <v-card-title>
                    <p :style="{ fontSize: `2em`, fontWeight: `bold` }">
                      CORE 🌟
                    </p>
                  </v-card-title>
                  <v-card-text
                    class="pb-0"
                    :style="{ height: `calc(100% - 64px)`, overflowX: `auto` }"
                  >
                    <v-container>
                      <v-row>
                        <v-col
                          cols="12"
                          sm="12"
                          md="12"
                          lg="6"
                          xl="6"
                          xxl="6"
                          v-for="(item, idx) in core"
                          :key="`core_item_key=${idx}`"
                        >
                          <v-chip class="mb-2 pr-4"
                            >{{ item.emoji }} {{ item.head }}</v-chip
                          >

                          <p class="ml-2">{{ item.body }}</p>
                        </v-col>
                      </v-row>
                    </v-container>
                  </v-card-text>
                </v-card>
              </v-carousel-item>
              <!-- START -->
              <v-carousel-item>
                <v-card class="pa-4 rounded-xl card-landing-top">
                  <v-card-title>
                    <p :style="{ fontSize: `2em`, fontWeight: `bold` }">
                      Trial 🔥
                    </p>
                    <p :style="{ fontSize: `0.8em` }">"Start Your Journey"</p>
                    <p :style="{ fontSize: `0.8em` }">
                      &nbsp;Smarter, faster, easier service.
                    </p>
                    <p :style="{ fontSize: `0.8em` }">
                      &nbsp;with the
                      <span
                        class="gradient-text"
                        :style="{ fontWeight: `bold` }"
                        >Power of AI</span
                      >.
                    </p>
                  </v-card-title>
                  <v-card-text
                    class="pb-0"
                    :style="{
                      height: `calc(100% - 64px)`,
                      overflowX: `auto`,
                      display: `flex`,
                      alignItems: `center`,
                      flexDirection: `column`,
                      justifyContent: `center`,
                    }"
                  >
                    <p
                      class="mb-10"
                      :style="{ color: `grey`, textAlign: `center` }"
                    >
                      {{
                        !alreadyGetTrial
                          ? `"Start your free trial and unlock AI-powered support!"`
                          : `"Request submitted! We'll contact you shortly."`
                      }}
                    </p>
                    <v-btn
                      :disabled="alreadyGetTrial"
                      class="get-trial-btn rounded-lg"
                      color="primary"
                      @click="dialog = true"
                      elevation="10"
                    >
                      {{
                        !alreadyGetTrial
                          ? ` Get Trial for Free`
                          : `Request Submitted`
                      }}
                    </v-btn>

                    <v-dialog v-model="dialog" max-width="600px">
                      <v-card class="pa-6 rounded-xl">
                        <v-card-title class="headline"
                          >Request Your Free Trial 🔑
                        </v-card-title>
                        <v-card-text class="pb-0">
                          <v-form>
                            <v-text-field
                              hint="*Required"
                              persistent-hint
                              class="mb-3"
                              rounded="xl"
                              variant="outlined"
                              label="Name"
                              :rules="[(v) => !!v || 'Name is required']"
                              v-model="form.name"
                              required
                            ></v-text-field>
                            <v-text-field
                              hint="*Required"
                              persistent-hint
                              class="mb-3"
                              rounded="xl"
                              variant="outlined"
                              label="Email"
                              :rules="[
                                (v) => !!v || 'Email is required',
                                (v) =>
                                  /.+@.+\..+/.test(v) || 'Email must be valid',
                              ]"
                              v-model="form.email"
                              required
                              type="email"
                            ></v-text-field>
                            <v-text-field
                              hint="*Required"
                              persistent-hint
                              class="mb-3"
                              rounded="xl"
                              variant="outlined"
                              label="Company Name"
                              :rules="[
                                (v) => !!v || 'Company Name is required',
                              ]"
                              v-model="form.company"
                              required
                            ></v-text-field>
                            <v-textarea
                              class="mb-3"
                              rounded="xl"
                              variant="outlined"
                              label="Message"
                              v-model="form.message"
                              required
                            ></v-textarea>
                          </v-form>
                        </v-card-text>
                        <v-card-actions>
                          <v-btn text @click="dialog = false">Cancel</v-btn>
                          <v-btn
                            :disabled="validateForm()"
                            @click="clickSubmitRequestTrial()"
                            :style="{
                              backgroundColor: `#00c853`,
                              color: `white`,
                              minWidth: `100px`,
                            }"
                            >Submit</v-btn
                          >
                        </v-card-actions>
                      </v-card>
                    </v-dialog>
                    <p
                      class="mt-10"
                      :style="{ color: `grey`, textAlign: `center` }"
                    >
                      <span v-if="!alreadyGetTrial"
                        >"No charge, no commitment – just a quick follow-up to
                        get you started."</span
                      >
                      <span v-else
                        >In a hurry? Call us now at
                        <span :style="{ color: `darkgrey`, fontWeight: `bold` }"
                          >+66 2 640 1151</span
                        >
                        for quick assistance.</span
                      >
                    </p>
                  </v-card-text>
                </v-card>
              </v-carousel-item>
            </v-carousel>
          </v-col>
        </v-row>

        <!-- Features Section -->
        <v-row id="features" class="pb-5" :style="{ paddingTop: `60px` }">
          <v-col cols="12">
            <v-card>
              <v-card-title>
                <h2>Our Features</h2>
              </v-card-title>
              <v-card-text>
                <p>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla
                  ut tristique urna. Integer bibendum auctor purus.
                </p>
                <v-list>
                  <v-list-item-group
                    v-for="(category, categoryIndex) in menu"
                    :key="categoryIndex"
                  >
                    <v-list-item
                      v-for="(feature, featureIndex) in category"
                      :key="featureIndex"
                      :disabled="feature.disabled"
                    >
                      <v-list-item-icon>
                        <v-icon>{{ feature.icon }}</v-icon>
                      </v-list-item-icon>
                      <v-list-item-content>
                        <v-list-item-title>{{
                          feature.name
                        }}</v-list-item-title>
                        <v-list-item-subtitle>{{
                          feature.description
                        }}</v-list-item-subtitle>
                      </v-list-item-content>
                      <v-list-item-action>
                        <v-btn color="primary">Learn More</v-btn>
                      </v-list-item-action>
                    </v-list-item>
                  </v-list-item-group>
                </v-list>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Solution Section -->
        <v-row id="solution" class="py-5">
          <v-col cols="12">
            <v-card>
              <v-card-title>
                <h2>Solution</h2>
              </v-card-title>
              <v-card-text>
                <p>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla
                  ut tristique urna. Integer bibendum auctor purus.
                </p>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <!-- Trusted Customers Section -->
        <v-row id="trustedCustomers" class="py-5">
          <v-col cols="12">
            <v-card>
              <v-card-title>
                <h2>Our Trusted Customers</h2>
              </v-card-title>
              <v-card-text>
                <p>
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla
                  ut tristique urna. Integer bibendum auctor purus.
                </p>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>

    <!-- Footer Section -->
    <v-footer app>
      <v-col class="text-center">
        <p>
          &copy; 2024 4Plus Consulting Co. Ltd
          <span v-if="windowWidth > 615">
            | Contact us:
            <span :style="{ fontWeight: `bold` }">+66 2 640 1151</span>
          </span>
        </p>
      </v-col>
    </v-footer>

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
        <v-btn color="white" text v-bind="attrs" @click="snackbarAlert = false">
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </v-app>
</template>

<script>
export default {
  data() {
    return {
      dialog: false,
      form: {
        name: "",
        email: "",
        company: "",
        message: "",
      },
      showChat: [
        { type: `customer`, msg: `Hi, I need some help.` },
        { type: `admin`, msg: `Sorry, I’m swamped. Can you wait a bit?` },
        { type: `ai`, msg: `I got this! What’s your issue? 😊` },
        { type: `customer`, msg: `Oh, cool! How do I use this product?` },
        {
          type: `ai`,
          msg: `Easy! Here’s the guide: [link].`,
        },
      ],
      windowWidth: 0,
      windowHeight: 0,
      scrollPosition: 0,
      menu: {
        Communication: [
          {
            icon: "mdi-chat-outline",
            name: "Unified Online Channel Chat",
            description:
              "Seamlessly connect with customers from multiple channels in one place.",
          },
        ],
        Data_Insight: [
          {
            icon: "mdi-database",
            name: "Data Warehouse Explorer",
            description:
              "Dive deep into enterprise data to uncover key insights and serve users effectively.",
          },
          {
            icon: "mdi-robot",
            name: "Product Knowledge Hub",
            description:
              "Get expert product information directly from an intelligent chatbot.",
          },
        ],
        Design_Partner: [
          {
            icon: "mdi-facebook",
            name: "Facebook Ads with AI",
            description:
              "Leverage AI to craft engaging and optimized Facebook ad campaigns.",
          },
          {
            icon: "mdi-google",
            name: "Google Ads with AI",
            description:
              "Enhance your Google Ads strategy using AI-driven content creation.",
          },
          {
            icon: "mdi-lightbulb",
            name: "AI-Powered Product Design",
            description:
              "Collaborate with AI to innovate and design your next big product.",
          },
        ],
        Dashboard_Solutions: [
          {
            icon: "mdi-view-dashboard",
            name: "Smart Dashboard Finder",
            description:
              "Quickly locate relevant dashboards to address inquiries and needs.",
          },
          {
            icon: "mdi-chart-areaspline",
            name: "AI-Enhanced Automated Dashboards",
            description:
              "Utilize Copilot to create dynamic Power BI dashboards effortlessly.",
          },
        ],
        Support_Function: [
          {
            icon: "mdi-account-group",
            name: "Human Resource",
            description:
              "Quickly locate relevant dashboards to address inquiries and needs.",
          },
        ],
      },
      core: [
        {
          head: ` Intelligent Chat Analysis`,
          body: `Understand customer questions and needs with precision.`,
          emoji: `💡`,
        },
        {
          head: ` Instant Responses`,
          body: `24/7 automated replies to keep your customers engaged.`,
          emoji: `⚡`,
        },
        {
          head: `Unified Chat Management`,
          body: `Centralize all chats from LINE OA, Facebook, and other platforms in one dashboard.`,
          emoji: `📋`,
        },
        {
          head: `Complete Control`,
          body: `Users can step in anytime to respond and manage conversations.`,
          emoji: `🎛️`,
        },
        {
          head: `Professional Problem Solving`,
          body: `Ensure customer satisfaction with quick and effective issue resolution.`,
          emoji: `🛠️`,
        },
        {
          head: `Insightful Analytics Dashboard`,
          body: `Access a dashboard that analyzes customer needs and tracks responder (admin) performance to enhance service efficiency.`,
          emoji: `📊`,
        },
      ],
      snackbarAlert: false,
      snackbarSuccess: false,
      snackbarMsg: "untitled",
      alreadyGetTrial: false,
    };
  },
  mounted() {
    window.addEventListener("scroll", this.trackScroll);
    // responsive
    this.$nextTick(() => {
      window.addEventListener("resize", this.onResize);
    });
    this.onResize();
  },
  beforeDestroy() {
    window.removeEventListener("scroll", this.trackScroll);
    window.removeEventListener("resize", this.onResize);
  },
  methods: {
    // resposive
    onResize() {
      this.windowWidth = window.innerWidth;
      this.windowHeight = window.innerHeight;
    },
    trackScroll() {
      this.scrollPosition = window.scrollY;
    },
    scrollTo(id) {
      const element = document.getElementById(id);
      if (element) {
        element.scrollIntoView({ behavior: "smooth" });
      }
    },
    validateForm() {
      if (!this.form.name || this.form.name.trim() === "") {
        return true;
      }

      const emailPattern = /.+@.+\..+/;
      if (!this.form.email || this.form.email.trim() === "") {
        return true;
      } else if (!emailPattern.test(this.form.email)) {
        return true;
      }

      if (!this.form.company || this.form.company.trim() === "") {
        return true;
      }

      return false;
    },
    //click
    clickSubmitRequestTrial() {
      this.form.name = ``;
      this.form.company = ``;
      this.form.email = ``;
      this.form.message = ``;

      this.dialog = false;
      this.alreadyGetTrial = true;
      this.snackbarMsg = `Success! We'll contact you as soon as possible.`;
      this.snackbarSuccess = true;
      this.snackbarAlert = true;
    },
  },
};
</script>

<style scoped>
.card-title-contact-dialog {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.card-landing-top {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.div-app-bar {
  font-weight: bold;
  display: flex;
  justify-content: flex-start;
  align-items: center;
}
.landing-page {
  height: 100vh;
  background: rgb(242, 195, 235);
  background: linear-gradient(
    180deg,
    rgba(242, 195, 235, 1) 9%,
    rgba(217, 212, 252, 1) 77%
  );
  background: linear-gradient(
    270deg,
    rgba(242, 195, 235, 1) 10%,
    rgba(229, 216, 245, 1) 40%,
    rgba(217, 212, 252, 1) 70%,
    rgba(201, 234, 247, 1) 100%
  );

  background-size: 400% 400%;
  animation: bgAnimation 12s ease infinite;
}

.bg-wave {
  display: inline-block;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    270deg,
    rgba(242, 195, 235, 1) 10%,
    rgba(229, 216, 245, 1) 40%,
    rgba(217, 212, 252, 1) 70%,
    rgba(201, 234, 247, 1) 100%
  );

  background-size: 400% 400%;
  animation: bgAnimation 12s ease infinite;
  color: #ffffff;
  font-size: 1.5rem;
  text-align: center;
  padding: 10px;
  border-radius: 8px;
  position: absolute;
}

@keyframes bgAnimation {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

.landing-layout {
  width: 100%;
  position: fixed;
  display: flex;
  flex-direction: row;
  align-items: center;
  z-index: 99;
  background: linear-gradient(
    270deg,
    rgba(242, 195, 235, 1) 10%,
    rgba(229, 216, 245, 1) 40%,
    rgba(242, 195, 235, 1) 50%,
    rgba(217, 212, 252, 1) 70%,
    rgba(201, 234, 247, 1) 100%
  );

  background-size: 400% 400%;
  animation: bgAnimation 12s ease infinite;
}

.v-footer {
  background-color: #f4f4f9;
}

.hidden {
  display: none;
}
.get-trial-btn {
  background: linear-gradient(45deg, #c87100, #a9ac16);
  color: white;
  font-weight: bold;
  font-size: 18px;
  border-radius: 50px;
  padding: 12px 40px;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  height: 35%;
}

.get-trial-btn:hover {
  background: linear-gradient(45deg, #ffa42c, #d5d80b);
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.2);
  transform: scale(1.05);
}

.get-trial-btn:active {
  transform: scale(0.98);
}

.get-trial-btn:focus {
  outline: none;
}

.get-login-btn {
  display: flex;
  background: linear-gradient(45deg, #00c853, #00bfae);
  color: white;
  font-weight: bold;
  font-size: 18px;
  border-radius: 50px;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  height: 100%;
}

.get-login-btn:hover {
  background: linear-gradient(45deg, #00bfae, #00c853);
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.2);
  transform: scale(1.05);
}

.get-login-btn:active {
  transform: scale(0.98);
}

.get-login-btn:focus {
  outline: none;
}
</style>
