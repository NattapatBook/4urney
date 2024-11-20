<template>
  <v-app>
    <!-- layout -->
    <div
      :style="{
        boxShadow:
          scrollPosition > 60
            ? `1px 2px ${
                scrollPosition - 60 > 20 ? 20 : scrollPosition - 60
              }px 0px black !important`
            : ``,
      }"
      class="landing-layout py-3"
    >
      <div
        class="div-app-bar"
        :style="{ fontWeight: `bold`, cursor: `pointer` }"
        @click="scrollTo('landingPage')"
      >
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
      <!-- <v-btn
        v-if="windowWidth > 880"
        variant="text"
        @click="scrollTo('solution')"
        >Solution</v-btn
      > -->
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
          <!-- <v-list-item class="pa-0">
            <v-card class="pa-4" @click="scrollTo('solution')" elevation="0">
              <span>Solution</span>
            </v-card>
          </v-list-item> -->
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
                      justifyContent: `center`,
                    }"
                  >
                    <div :style="{ maxWidth: `880px`, width: `100%` }">
                      <v-img
                        :style="{
                          aspectRatio: `30/9 !important`,
                        }"
                        :src="'/img/landing/showChat.png'"
                      ></v-img>
                    </div>

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
                    :style="{ height: `calc(100% - 165px)`, overflowX: `auto` }"
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
                          <v-tooltip location="bottom">
                            <template v-slot:activator="{ props }">
                              <v-chip
                                v-bind="props"
                                class="mb-2 pr-4"
                                :style="{
                                  maxWidth: `100%`,
                                }"
                              >
                                <div
                                  :style="{
                                    display: `grid`,
                                  }"
                                >
                                  <span class="ellipsis-text">
                                    {{ item.emoji }}{{ item.head }}</span
                                  >
                                </div>
                              </v-chip>
                            </template>
                            <span>{{ item.head }}</span>
                          </v-tooltip>
                          <p class="ml-2">{{ item.body }}</p>
                        </v-col>
                      </v-row>
                    </v-container>
                  </v-card-text>
                </v-card>
              </v-carousel-item>
              <!-- login&trial both in > 880 -->
              <v-carousel-item v-if="windowWidth > 880">
                <v-card
                  :style="{
                    height: `100%`,
                    display: `flex`,
                    justifyContent: `space-between`,
                  }"
                >
                  <!-- login -->
                  <v-card
                    elevation="0"
                    class="pa-4 rounded-xl card-landing-top"
                    :style="{ height: `100%`, width: `50%` }"
                  >
                    <v-card-title>
                      <p :style="{ fontSize: `2em`, fontWeight: `bold` }">
                        Login 🔑
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
                        justifyContent: `flex-start`,
                      }"
                    >
                      <p
                        class="mb-10 mt-5"
                        :style="{ color: `grey`, textAlign: `center` }"
                      >
                        Log In to Begin Experience AI Power
                      </p>
                      <v-btn
                        class="get-login-page-btn rounded-lg"
                        color="primary"
                        elevation="10"
                        :style="{ width: `15em` }"
                      >
                        Login
                      </v-btn>

                      <p
                        class="mt-10"
                        :style="{ color: `grey`, textAlign: `center` }"
                      >
                        <span
                          >Powered by
                          <span
                            :style="{
                              color: `#757575`,
                              fontWeight: `bold`,
                            }"
                            >AWS Cognito</span
                          >
                        </span>
                      </p>
                    </v-card-text>
                  </v-card>
                  <v-divider
                    class="border-opacity-50 my-15"
                    color="grey"
                    vertical
                  />
                  <!-- trial -->
                  <v-card
                    elevation="0"
                    class="pa-4 rounded-xl card-landing-top"
                    :style="{ height: `100%`, width: `50%` }"
                  >
                    <v-card-title>
                      <p :style="{ fontSize: `2em`, fontWeight: `bold` }">
                        Trial 🔥
                      </p>
                      <p :style="{ fontSize: `0.8em` }">
                        "Start Your Free Trial Today!"
                      </p>
                      <p :style="{ fontSize: `0.8em` }">
                        &nbsp;Unlock the
                        <span
                          class="gradient-text"
                          :style="{ fontWeight: `bold` }"
                          >Power of AI</span
                        >.
                      </p>
                      <p :style="{ fontSize: `0.8em` }">
                        &nbsp;Discover the new possibilities!
                      </p>
                    </v-card-title>
                    <v-card-text
                      class="pb-0"
                      :style="{
                        height: `calc(100% - 165px)`,
                        overflowX: `auto`,
                        display: `flex`,
                        alignItems: `center`,
                        flexDirection: `column`,
                        justifyContent: `flex-start`,
                      }"
                    >
                      <p
                        class="mb-10 mt-5"
                        :style="{ color: `grey`, textAlign: `center` }"
                      >
                        {{
                          !alreadyGetTrial
                            ? `"Start your free trial here."`
                            : `"We'll contact you shortly."`
                        }}
                      </p>
                      <v-btn
                        :disabled="alreadyGetTrial"
                        class="get-trial-btn rounded-lg"
                        color="primary"
                        @click="trialDialog = true"
                        elevation="10"
                        :style="{ width: `15em` }"
                      >
                        {{
                          !alreadyGetTrial
                            ? `Get Trial for Free`
                            : `Request Submitted!`
                        }}
                      </v-btn>
                      <p
                        class="mt-10"
                        :style="{ color: `grey`, textAlign: `center` }"
                      >
                        <span v-if="!alreadyGetTrial"
                          >"No charge, no commitment <br />
                          just a quick follow-up to get you started."</span
                        >
                        <span v-else
                          >In a hurry? Call us now at
                          <span
                            :style="{
                              color: `#757575`,
                              fontWeight: `bold`,
                            }"
                            >+66 2 640 1151</span
                          >
                          for quick assistance.</span
                        >
                      </p>
                    </v-card-text>
                  </v-card>
                </v-card>
              </v-carousel-item>
              <!-- trial <= 880 -->
              <v-carousel-item v-if="windowWidth <= 880">
                <v-card
                  elevation="0"
                  class="pa-4 rounded-xl card-landing-top"
                  :style="{ height: `100%` }"
                >
                  <v-card-title>
                    <p :style="{ fontSize: `2em`, fontWeight: `bold` }">
                      Trial 🔥
                    </p>
                    <p :style="{ fontSize: `0.8em` }">
                      "Start Your Free Trial Today!"
                    </p>
                    <p :style="{ fontSize: `0.8em` }">
                      &nbsp;Unlock the
                      <span
                        class="gradient-text"
                        :style="{ fontWeight: `bold` }"
                        >Power of AI</span
                      >.
                    </p>
                    <p :style="{ fontSize: `0.8em` }">
                      &nbsp;Discover the new possibilities!
                    </p>
                  </v-card-title>
                  <v-card-text
                    class="pb-0"
                    :style="{
                      height: `calc(100% - 165px)`,
                      overflowX: `auto`,
                      display: `flex`,
                      alignItems: `center`,
                      flexDirection: `column`,
                      justifyContent: `flex-start`,
                    }"
                  >
                    <p
                      class="mb-10 mt-5"
                      :style="{ color: `grey`, textAlign: `center` }"
                    >
                      {{
                        !alreadyGetTrial
                          ? `"Start your free trial here."`
                          : `"We'll contact you shortly."`
                      }}
                    </p>
                    <v-btn
                      :disabled="alreadyGetTrial"
                      class="get-trial-btn rounded-lg"
                      color="primary"
                      @click="trialDialog = true"
                      elevation="10"
                      :style="{ width: `15em` }"
                    >
                      {{
                        !alreadyGetTrial
                          ? `Get Trial for Free`
                          : `Request Submitted!`
                      }}
                    </v-btn>
                    <p
                      class="mt-10"
                      :style="{ color: `grey`, textAlign: `center` }"
                    >
                      <span v-if="!alreadyGetTrial"
                        >"No charge, no commitment <br />
                        just a quick follow-up to get you started."</span
                      >
                      <span v-else
                        >In a hurry? Call us now at
                        <span
                          :style="{
                            color: `#757575`,
                            fontWeight: `bold`,
                          }"
                          >+66 2 640 1151</span
                        >
                        for quick assistance.</span
                      >
                    </p>
                  </v-card-text>
                </v-card>
              </v-carousel-item>
              <!-- login <= 880 -->
              <!-- <v-carousel-item v-if="windowWidth <= 880">
                <v-card
                  elevation="0"
                  class="pa-4 rounded-xl card-landing-top"
                  :style="{ height: `100%` }"
                >
                  <v-card-title>
                    <p :style="{ fontSize: `2em`, fontWeight: `bold` }">
                      Login 🔑
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
                      justifyContent: `flex-start`,
                    }"
                  >
                    <p
                      class="mb-10 mt-5"
                      :style="{ color: `grey`, textAlign: `center` }"
                    >
                      Log In to Begin Experience AI Power
                    </p>
                    <v-btn
                      class="get-login-page-btn rounded-lg"
                      color="primary"
                      elevation="10"
                      :style="{ width: `15em` }"
                    >
                      Login
                    </v-btn>

                    <p
                      class="mt-10"
                      :style="{ color: `grey`, textAlign: `center` }"
                    >
                      <span
                        >Powered by
                        <span
                          :style="{
                            color: `#757575`,
                            fontWeight: `bold`,
                          }"
                          >AWS Cognito</span
                        >
                        for unmatched reliability and protection.</span
                      >
                    </p>
                  </v-card-text>
                </v-card>
              </v-carousel-item> -->
            </v-carousel>
          </v-col>
        </v-row>

        <!-- Trusted Customers Section -->
        <v-row
          id="trustedCustomers"
          class="pb-5"
          :style="{ paddingTop: `60px` }"
        >
          <v-col cols="12">
            <v-card
              class="elevation-0"
              :style="{
                display: `flex`,
                flexDirection: `column`,
                alignItems: `center`,
              }"
            >
              <v-card-title class="d-flex justify-center py-6">
                <h2
                  class="text-center font-weight-bold"
                  :style="{ color: `#34495e` }"
                >
                  Our Trusted Customers
                </h2>
              </v-card-title>

              <v-card-text class="text-center px-8">
                <p :style="{ color: `#7f8c8d` }">
                  Join a growing list of satisfied customers who trust us for
                  our exceptional services.
                </p>
              </v-card-text>
              <v-card-text :style="{ maxWidth: `800px` }">
                <v-container>
                  <v-row>
                    <v-col
                      cols="3"
                      class="pa-8"
                      v-for="(item, idx) in customers"
                      :key="`landing_trusted_customer_${idx}`"
                    >
                      <v-tooltip location="bottom">
                        <template v-slot:activator="{ props }">
                          <v-avatar
                            v-bind="props"
                            :style="{
                              height: `100%`,
                              width: `100%`,
                              maxHeight: `150px`,
                              maxWidth: `150px`,
                              aspectRatio: `1`,
                            }"
                          >
                            <v-img :src="item.img"></v-img>
                          </v-avatar>
                        </template>
                        <span>{{ item.name }}</span>
                      </v-tooltip>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <v-divider class="mx-15" />

        <!-- Features Section -->
        <v-row id="features" class="pb-5" :style="{ paddingTop: `60px` }">
          <v-col cols="12">
            <v-card elevation="0">
              <v-card-title class="d-flex justify-center py-6">
                <h2
                  class="text-center font-weight-bold"
                  :style="{ color: `#34495e` }"
                >
                  Feature
                </h2>
              </v-card-title>

              <v-card-text class="text-center px-8">
                <p :style="{ color: `#7f8c8d` }">
                  Discover cutting-edge tools and solutions designed to
                  streamline your workflow, enhance creativity, and drive
                  business success.
                </p>
              </v-card-text>
              <v-card-text>
                <v-container>
                  <v-row
                    :style="{
                      display: `flex`,
                      justifyContent: `center`,
                    }"
                  >
                    <v-col
                      class="pa-10 rounded-xl"
                      :style="{ maxWidth: `805px`, backgroundColor: `#f5f5f5` }"
                    >
                      <div
                        v-for="(category, categoryIndex) in menu"
                        :key="categoryIndex"
                      >
                        <div
                          v-for="(feature, featureIndex) in category"
                          :key="featureIndex"
                          class="mb-2"
                          :disabled="feature.disabled"
                          :style="{
                            display: `flex`,
                            alignItems: `center`,
                            justifyContent:
                              featureIndex % 3 === 0
                                ? `flex-start`
                                : `flex-end`,
                          }"
                        >
                          <v-tooltip location="bottom">
                            <template v-slot:activator="{ props }">
                              <div
                                v-bind="props"
                                :style="{
                                  display: `flex`,
                                  alignItems: `start`,
                                  cursor: `pointer`,
                                  transition: `transform 0.2s ease-in-out`,
                                  filter:
                                    featureHover.trim().length < 1
                                      ? ``
                                      : feature.name === featureHover
                                      ? ``
                                      : `blur(3px)`,
                                  maxWidth: `100%`,
                                }"
                                class="hover-scale"
                                @mouseover="featureHover = feature.name"
                                @mouseleave="featureHover = ``"
                              >
                                <v-chip
                                  v-if="featureIndex % 3 === 0"
                                  :prepend-icon="feature.icon"
                                  class="mr-2 chip_feature_landing_icon"
                                >
                                </v-chip>
                                <v-card
                                  class="py-2 px-4 rounded-xl"
                                  elevation="0"
                                  :style="{
                                    backgroundColor:
                                      featureIndex % 3 === 0
                                        ? `#8eff8e`
                                        : `rgb(219 219 219)`,
                                  }"
                                >
                                  <div>
                                    {{ feature.name }}
                                  </div>
                                </v-card>
                                <v-chip
                                  v-if="featureIndex % 3 !== 0"
                                  :prepend-icon="feature.icon"
                                  class="ml-2 chip_feature_landing_icon"
                                >
                                </v-chip>
                              </div>
                            </template>
                            <div>
                              <p
                                :style="{
                                  fontSize: `0.95rem`,
                                  fontWeight: `bold`,
                                }"
                              >
                                {{ feature.name }}
                              </p>
                              <span
                                class="break-word"
                                :style="{
                                  fontSize: `0.8rem`,
                                }"
                                >{{ feature.description }}</span
                              >
                            </div>
                          </v-tooltip>
                        </div>
                      </div>
                      <div
                        class="mt-10"
                        :style="{
                          filter:
                            featureHover.trim().length >= 1 ? `blur(3px)` : ``,
                        }"
                      >
                        <v-text-field
                          v-model="featureText"
                          hide-details
                          density="compact"
                          variant="outlined"
                          :append-inner-icon="`mdi-send-variant`"
                          :placeholder="`Write something...`"
                          @keyup.enter="clickInteresting()"
                          @click:appendInner="clickInteresting()"
                        ></v-text-field>
                      </div>
                    </v-col>
                  </v-row>
                </v-container>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <v-divider class="mx-15" />

        <!-- Pricing Section -->
        <v-row id="pricing" class="py-5" :style="{ paddingTop: `60px` }">
          <v-col cols="12">
            <v-card elevation="0" class="rounded-lg">
              <v-card-title class="d-flex justify-center">
                <h2
                  class="text-center font-weight-bold"
                  :style="{ color: `#34495e` }"
                >
                  Flexible Pricing Plans
                </h2>
              </v-card-title>

              <v-card-text class="text-center">
                <p :style="{ color: `#7f8c8d`, fontSize: `1rem` }">
                  Choose the plan that fits your needs. Our pricing is
                  transparent and flexible based on the features you require.
                </p>
              </v-card-text>

              <v-card-text>
                <v-container>
                  <!-- Plan Selector -->
                  <v-row class="justify-center">
                    <!-- Basic Plan -->
                    <v-col cols="12" sm="4" class="mb-4">
                      <v-card
                        class="pa-4 rounded-lg"
                        :style="{ backgroundColor: `#dbe9f1`, height: `100%` }"
                      >
                        <v-card-title class="justify-center">
                          <h3
                            class="font-weight-bold"
                            :style="{ color: `#34495e` }"
                          >
                            Basic Plan
                          </h3>
                        </v-card-title>
                        <v-card-subtitle
                          class="text-center"
                          :style="{ color: `#7f8c8d` }"
                        >
                          Simple plan for individuals.
                        </v-card-subtitle>
                        <v-divider
                          class="my-3"
                          :style="{ backgroundColor: `#b2bec3` }"
                        ></v-divider>

                        <div class="text-center">
                          <h4
                            class="font-weight-bold"
                            :style="{ color: `#2980b9` }"
                          >
                            From $19/month
                          </h4>
                          <p class="mt-2" :style="{ color: `#7f8c8d` }">
                            Basic features for small teams.
                          </p>
                        </div>
                      </v-card>
                    </v-col>

                    <!-- Standard Plan -->
                    <v-col cols="12" sm="4" class="mb-4">
                      <v-card
                        class="pa-4 rounded-lg"
                        :style="{ backgroundColor: `#a9cce3`, height: `100%` }"
                      >
                        <v-card-title class="justify-center">
                          <h3
                            class="font-weight-bold"
                            :style="{ color: `#2c3e50` }"
                          >
                            Standard Plan
                          </h3>
                        </v-card-title>
                        <v-card-subtitle
                          class="text-center"
                          :style="{ color: `#2c3e50` }"
                        >
                          Popular plan for teams.
                        </v-card-subtitle>
                        <v-divider
                          class="my-3"
                          :style="{ backgroundColor: `#b2bec3` }"
                        ></v-divider>

                        <div class="text-center">
                          <h4
                            class="font-weight-bold"
                            :style="{ color: `#2980b9` }"
                          >
                            From $49/month
                          </h4>
                          <p class="mt-2" :style="{ color: `#7f8c8d` }">
                            Ideal for growing teams.
                          </p>
                        </div>
                      </v-card>
                    </v-col>

                    <!-- Advanced Plan -->
                    <v-col cols="12" sm="4" class="mb-4">
                      <v-card
                        class="pa-4 rounded-lg"
                        :style="{ backgroundColor: `#a8e6cf`, height: `100%` }"
                      >
                        <v-card-title class="justify-center">
                          <h3
                            class="font-weight-bold"
                            :style="{ color: `#34495e` }"
                          >
                            Advanced Plan
                          </h3>
                        </v-card-title>
                        <v-card-subtitle
                          class="text-center"
                          :style="{ color: `#2c3e50` }"
                        >
                          For advanced needs.
                        </v-card-subtitle>
                        <v-divider
                          class="my-3"
                          :style="{ backgroundColor: `#b2bec3` }"
                        ></v-divider>

                        <div class="text-center">
                          <h4
                            class="font-weight-bold"
                            :style="{ color: `#27ae60` }"
                          >
                            From $79/month
                          </h4>
                          <p class="mt-2" :style="{ color: `#7f8c8d` }">
                            Advanced features for larger teams.
                          </p>
                        </div>
                      </v-card>
                    </v-col>

                    <!-- Custom Plan -->
                    <v-col cols="12" sm="4" class="mb-4">
                      <v-card
                        class="pa-4 rounded-lg"
                        :style="{
                          background:
                            'linear-gradient(90deg, rgba(242, 195, 235, 1) 9%, rgba(217, 212, 252, 1) 77%)',
                          height: `100%`,
                        }"
                      >
                        <v-card-title class="justify-center">
                          <h3
                            class="font-weight-bold"
                            :style="{ color: `#8e44ad` }"
                          >
                            Custom Plan
                          </h3>
                        </v-card-title>
                        <v-card-subtitle
                          class="text-center"
                          :style="{ color: `#2f3640` }"
                        >
                          Pay for what you need.
                        </v-card-subtitle>
                        <v-divider
                          class="my-3"
                          :style="{ backgroundColor: `#e0a9c7` }"
                        ></v-divider>

                        <div class="text-center">
                          <h4
                            class="font-weight-bold"
                            :style="{ color: `#8e44ad` }"
                          >
                            From $4.99/month
                          </h4>
                          <p class="mt-2" :style="{ color: `#7f8c8d` }">
                            Start with one feature, expand as needed.
                          </p>
                        </div>
                      </v-card>
                    </v-col>

                    <!-- Premium Plan -->
                    <v-col cols="12" sm="4" class="mb-4">
                      <v-card
                        class="pa-4 rounded-lg"
                        :style="{ backgroundColor: `#e74c3c`, height: `100%` }"
                      >
                        <v-card-title class="justify-center">
                          <h3
                            class="font-weight-bold"
                            :style="{ color: `#fff` }"
                          >
                            Premium Plan
                          </h3>
                        </v-card-title>
                        <v-card-subtitle
                          class="text-center"
                          :style="{ color: `#fff` }"
                        >
                          For large-scale operations.
                        </v-card-subtitle>
                        <v-divider
                          class="my-3"
                          :style="{ backgroundColor: `#b2bec3` }"
                        ></v-divider>

                        <div class="text-center">
                          <h4
                            class="font-weight-bold"
                            :style="{ color: `#fff` }"
                          >
                            From $199/month
                          </h4>
                          <p class="mt-2" :style="{ color: `#fff` }">
                            All features and premium support.
                          </p>
                        </div>
                      </v-card>
                    </v-col>
                  </v-row>
                  <v-row>
                    <v-col
                      cols="12"
                      :style="{ display: `flex`, justifyContent: `center` }"
                    >
                      <v-btn
                        :style="{
                          backgroundColor: `#f3f3f3`,
                        }"
                        variant="outlined"
                        rounded
                        class="compare-btn"
                        @click="onComparePlans"
                      >
                        Compare Plans
                        <v-icon>mdi-chevron-double-down</v-icon>
                      </v-btn>
                    </v-col>
                  </v-row>
                </v-container>
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
      </v-container>
    </v-main>

    <!-- Footer Section -->
    <v-footer
      app
      :style="{
        backgroundColor: `rgba(244, 244, 249, ${
          scrollPosition - 60 >= 1 ? `1` : `0`
        })`,
      }"
    >
      <v-col class="text-center">
        <p>
          &copy; 2024 4Plus Consulting Co. Ltd
          <span v-if="windowWidth > 615">
            | Contact us:
            <span :style="{ fontWeight: `bold` }">+66 2 640 1151</span>
            (Thailand)
          </span>
        </p>
      </v-col>
    </v-footer>
    <!-- trial dialog -->
    <v-dialog v-model="trialDialog" max-width="600px">
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
                (v) => /.+@.+\..+/.test(v) || 'Email must be valid',
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
              :rules="[(v) => !!v || 'Company Name is required']"
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
          <v-btn text @click="trialDialog = false">Cancel</v-btn>
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
    <!-- interesting dialog -->
    <v-dialog v-model="interestingDialog" max-width="600px">
      <v-card class="pa-6 rounded-xl shake">
        <v-card-title
          class="headline"
          :style="{
            display: `flex`,
            justifyContent: `space-between`,
            alignItems: `center`,
          }"
        >
          <span
            ><span :style="{ fontWeight: `bold`, fontSize: `1.5rem` }"
              >Interested?
            </span></span
          >
          <v-btn
            icon="mdi-close"
            variant="fab"
            @click="interestingDialog = false"
          ></v-btn>
        </v-card-title>
        <v-card-text class="pb-0 pt-1">
          <p>
            "It looks like you're interested in our app! You can request a free
            trial right now."
          </p>
        </v-card-text>
        <v-card-action>
          <!-- <v-btn text @click="interestingDialog = false">Cancel</v-btn> -->
          <div
            class="pa-10"
            :style="{ display: `flex`, justifyContent: `center` }"
          >
            <v-btn
              @click="clickInterestingRequest()"
              class="get-trial-btn"
              :style="{
                backgroundColor: `#00c853`,
                color: `white`,
                minWidth: `100px`,
              }"
              >Request Trial</v-btn
            >
          </div>
        </v-card-action>
        <v-card-text class="pt-0">
          <p :style="{ fontSize: `0.75rem`, color: `grey` }">
            "If you need immediate assistance, feel free to contact us at
            <span :style="{ fontWeight: `bold` }">+66 2 640 1151</span>
          </p>
        </v-card-text>
      </v-card>
    </v-dialog>
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
      featureText: ``,
      trialDialog: false,
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
              "Streamline customer communication by effortlessly connecting across multiple online channels, creating a unified hub for all your interactions",
          },
        ],
        Data_Insight: [
          {
            icon: "mdi-database",
            name: "Data Warehouse Explorer",
            description:
              "Unlock the potential of your enterprise's data by exploring vast datasets, revealing hidden insights to drive smarter business decisions.",
          },
          {
            icon: "mdi-robot",
            name: "Product Knowledge Hub",
            description:
              "Access a wealth of expert-level product knowledge instantly through an AI-driven chatbot, providing your team with valuable insights for every query.",
          },
        ],
        Design_Partner: [
          {
            icon: "mdi-facebook",
            name: "Facebook Ads with AI",
            description:
              "Harness the power of AI to create highly engaging, data-driven Facebook ad campaigns that resonate with your audience and drive measurable results.",
          },
          {
            icon: "mdi-google",
            name: "Google Ads with AI",
            description:
              "Optimize your Google Ads strategy by leveraging AI to generate compelling ad content, target the right audience, and maximize your ROI.",
          },
          {
            icon: "mdi-lightbulb",
            name: "AI-Powered Product Design",
            description:
              "Collaborate with AI to push the boundaries of creativity and innovation, helping you design your next groundbreaking product with ease.",
          },
        ],
        Support_Function: [
          {
            icon: "mdi-account-group",
            name: "Human Resource",
            description:
              "Streamline HR processes by quickly accessing relevant dashboards to handle employee inquiries and manage HR needs efficiently.",
          },
        ],
        Dashboard_Solutions: [
          {
            icon: "mdi-view-dashboard",
            name: "Smart Dashboard Finder",
            description:
              "Easily discover and access the dashboards that matter most to your team, enabling you to focus on key metrics and decisions without wasting time.",
          },
          {
            icon: "mdi-chart-areaspline",
            name: "AI-Enhanced Automated Dashboards",
            description:
              "Leverage the power of Copilot to automatically create dynamic Power BI dashboards that update in real-time, ensuring you have the latest insights at your fingertips.",
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
      customers: [
        {
          name: `4Plus Consulting`,
          img: `https://media.licdn.com/dms/image/v2/C560BAQGB4JBkIt74mA/company-logo_200_200/company-logo_200_200/0/1630646658833?e=2147483647&v=beta&t=APD0So5Q75j5MqOQeYxGtVYwSJHzBTb6J4qLG3iZ6Cg`,
        },
        {
          name: `4Plus Consulting`,
          img: `https://media.licdn.com/dms/image/v2/C560BAQGB4JBkIt74mA/company-logo_200_200/company-logo_200_200/0/1630646658833?e=2147483647&v=beta&t=APD0So5Q75j5MqOQeYxGtVYwSJHzBTb6J4qLG3iZ6Cg`,
        },
        {
          name: `4Plus Consulting`,
          img: `https://media.licdn.com/dms/image/v2/C560BAQGB4JBkIt74mA/company-logo_200_200/company-logo_200_200/0/1630646658833?e=2147483647&v=beta&t=APD0So5Q75j5MqOQeYxGtVYwSJHzBTb6J4qLG3iZ6Cg`,
        },
        {
          name: `4Plus Consulting`,
          img: `https://media.licdn.com/dms/image/v2/C560BAQGB4JBkIt74mA/company-logo_200_200/company-logo_200_200/0/1630646658833?e=2147483647&v=beta&t=APD0So5Q75j5MqOQeYxGtVYwSJHzBTb6J4qLG3iZ6Cg`,
        },
        {
          name: `4Plus Consulting`,
          img: `https://media.licdn.com/dms/image/v2/C560BAQGB4JBkIt74mA/company-logo_200_200/company-logo_200_200/0/1630646658833?e=2147483647&v=beta&t=APD0So5Q75j5MqOQeYxGtVYwSJHzBTb6J4qLG3iZ6Cg`,
        },
        {
          name: `4Plus Consulting`,
          img: `https://media.licdn.com/dms/image/v2/C560BAQGB4JBkIt74mA/company-logo_200_200/company-logo_200_200/0/1630646658833?e=2147483647&v=beta&t=APD0So5Q75j5MqOQeYxGtVYwSJHzBTb6J4qLG3iZ6Cg`,
        },
        {
          name: `4Plus Consulting`,
          img: `https://media.licdn.com/dms/image/v2/C560BAQGB4JBkIt74mA/company-logo_200_200/company-logo_200_200/0/1630646658833?e=2147483647&v=beta&t=APD0So5Q75j5MqOQeYxGtVYwSJHzBTb6J4qLG3iZ6Cg`,
        },
        {
          name: `4Plus Consulting`,
          img: `https://media.licdn.com/dms/image/v2/C560BAQGB4JBkIt74mA/company-logo_200_200/company-logo_200_200/0/1630646658833?e=2147483647&v=beta&t=APD0So5Q75j5MqOQeYxGtVYwSJHzBTb6J4qLG3iZ6Cg`,
        },
      ],
      snackbarAlert: false,
      snackbarSuccess: false,
      snackbarMsg: "untitled",
      alreadyGetTrial: false,
      featureHover: ``,
      interestingDialog: false,
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
    clickInteresting() {
      this.featureText = ``;
      this.interestingDialog = true;
    },
    clickInterestingRequest() {
      this.interestingDialog = false;
      this.trialDialog = true;
    },
    clickSubmitRequestTrial() {
      this.form.name = ``;
      this.form.company = ``;
      this.form.email = ``;
      this.form.message = ``;

      this.trialDialog = false;
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

.get-login-page-btn {
  background: linear-gradient(45deg, #00c853, #00bfae);
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

.get-login-page-btn:hover {
  background: linear-gradient(45deg, #00bfae, #00c853);
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.2);
  transform: scale(1.05);
}

.get-login-page-btn:active {
  transform: scale(0.98);
}

.get-login-page-btn:focus {
  outline: none;
}
.chip_feature_landing_icon {
  aspect-ratio: 1 / 1;
  display: flex;
  align-items: center;
}

.hover-scale:hover {
  transform: scale(1.2);
}

span.break-word {
  display: inline-block;
  max-width: 300px;
  word-wrap: break-word;
}

span.break-word-chip {
  display: inline-block;
  max-width: 100%;
  word-wrap: break-word;
}

@keyframes shake {
  0%,
  100% {
    transform: translateX(0);
  }
  20%,
  60% {
    transform: translateX(-10px);
  }
  40%,
  80% {
    transform: translateX(10px);
  }
}

.shake {
  animation: shake 0.5s ease;
}

.compare-btn {
  text-transform: none;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.compare-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}
.ellipsis-text {
  display: inline-block;
  max-width: 100%;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
